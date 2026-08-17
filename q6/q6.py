from pathlib import Path
import pandas as pd
import numpy as np
import math

csv_folder_path = Path('../arquivos/')
files_list = ["products.csv", "product_variants.csv", "orders.csv", "order_items.csv"]

# Loop para ler cada arquivo e criar as variáveis globais
for file_name in files_list:
    # Junta o caminho da pasta com o nome do arquivo
    full_path = csv_folder_path / file_name

    # Extrai o nome sem o '.csv' (ex: 'products')
    var_name = f"df_{Path(file_name).stem}"

    # Cria a variável global independente com o DataFrame
    globals()[var_name] = pd.read_csv(full_path)



## Mergear df_orders com o df_order_items no df1

df1 = pd.merge(
    df_orders, 
    df_order_items, 
    left_on='id',       
    right_on='order_id', 
    how='left',         
    suffixes=('_orders', '_order_items')
)
df1 = df1.drop(columns='order_id')


## Mergear df1 com o df_product_variants no df2

df2 = pd.merge(
    df1, 
    df_product_variants, 
    left_on='product_variant_id',       
    right_on='id', 
    how='left',         
    suffixes=('', '_product_variant')
)

## Mergear df2 com o df_products no df3

df3 = pd.merge(
    df2, 
    df_products, 
    left_on='product_id',       
    right_on='id', 
    how='left',         
    suffixes=('', '_product')
)

df3.rename(columns={
    'id_orders': 'order_id',
    'id_order_items': 'order_items_id',
    'id_product': 'product_id',
    'placed_at' : 'placed_at_orders',
    'created_at' : 'created_at_orders',
    'updated_at' : 'updated_at_orders'
    }, inplace=True)

## Filtrar o df3 para pegar apenas o produto desejado

df_bussola = df3[df3['name'] == 'Bússola de Bordo 702']
df_bussola.head()


## Filtrar o df_bussola para pegar apenas as linhas com status 'confirmed' para garatir que estamo falando de vendas que foram completamente efetivadas

df_bussola = df_bussola [df_bussola ['status'].isin(['confirmed'])]

## Preparando as previsões usando média móvel dos ultimos três meses como base

# 1. Preparação e Agrupamento dos Dados (Seu código original)
df_bussola['placed_at_orders'] = pd.to_datetime(df_bussola['placed_at_orders'])
df_bussola['year_month'] = df_bussola['placed_at_orders'].dt.to_period('M')

monthly_sales = df_bussola.groupby('year_month')['quantity'].sum().reset_index()
monthly_sales = monthly_sales.set_index('year_month').sort_index()

new_index = pd.period_range(start=monthly_sales.index.min(), end='2026-03', freq='M')
monthly_sales = monthly_sales.reindex(new_index, fill_value=0)

# Criamos a coluna de previsões inicializada com NaN
monthly_sales['baseline_predictions'] = np.nan

# Definimos o período que queremos prever
final_months = pd.period_range(start='2026-01', end='2026-03', freq='M')

# 2. Iteramos mês a mês no período de teste
for month in final_months:
    # Identificamos os 3 meses imediatamente anteriores
    last_three_months = pd.period_range(end=month - 1, periods=3, freq='M')

    last_three_months_values = []
    for m in last_three_months:
        # Se o mês anterior já estiver no período de previsão (2026), pegamos a PREVISÃO dele
        if m in final_months:
            value = monthly_sales.loc[m, 'baseline_predictions']
        # Se for um mês de 2025 ou anterior, pegamos o valor REAL (quantity)
        else:
            value = monthly_sales.loc[m, 'quantity']

        last_three_months_values.append(value)

    # Calcula a média dos 3 meses (recursiva) e salva na linha do mês atual
    monthly_sales.loc[month, 'baseline_predictions'] = math.ceil(np.mean(last_three_months_values))

# 3. Filtrando os meses de teste de 2026 para avaliação
df_final_months = monthly_sales.loc[final_months].copy()

# 4. Cálculo do MAE (Mean Absolute Error) Mês a Mês e Global
df_final_months['absolute_error'] = (df_final_months['quantity'] - df_final_months['baseline_predictions']).abs()
mae_global = df_final_months['absolute_error'].mean()

# Exibindo os Resultados detalhados mês a mês
print("-- PREVISÃO E COMPARAÇÃO MÊS A MÊS (1º TRIMESTRE 2026) do item 'Bússola de Bordo 702' --")
print("--- Obs: utilizando apenas as orders com o status 'confirmed' como base ---")
for mes in df_final_months.index:
    real = df_final_months.loc[mes, 'quantity']
    previsto = df_final_months.loc[mes, 'baseline_predictions']
    erro = df_final_months.loc[mes, 'absolute_error']

    # Identificando os meses usados para o cálculo da previsão atual
    meses_treino = [str(mes - i) for i in range(3, 0, -1)]

    print(f"\nMes Previsto: {mes}")
    print(f"  -> Baseado nos meses de treino: {', '.join(meses_treino)}")
    print(f"  -> Valor Real: {real:,.0f} unidades")
    print(f"  -> Previsão Baseline: {previsto:,.0f} unidades")
    print(f"  -> Erro Absoluto do Mês: {erro:,.0f} unidades")

print("\n" + "="*63)
print(f" MAE GLOBAL DO PERÍODO (Média dos erros absolutos): {mae_global:,.0f} unidades")
print("="*63)
