from pathlib import Path
import pandas as pd

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

# 1. Preparação e Agrupamento dos Dados
# Convertendo a coluna de data para o formato datetime
df_bussola['placed_at_orders'] = pd.to_datetime(df_bussola['placed_at_orders'])

# Criando a coluna de ano-mês para agrupamento
df_bussola['year_month'] = df_bussola['placed_at_orders'].dt.to_period('M')

# Agrupando o faturamento total por mês (utilizando total para valor vendido)
monthly_sales = df_bussola.groupby('year_month')['total'].sum().reset_index()
monthly_sales = monthly_sales.set_index('year_month').sort_index()

# Garantindo que todos os meses do intervalo existam no índice (evita meses faltando)
new_index = pd.period_range(start=monthly_sales.index.min(), end='2026-03', freq='M')
monthly_sales = monthly_sales.reindex(new_index, fill_value=0)

# 2. Construção da Previsão Mês a Mês (Média Móvel dos últimos 3 meses)
# O shift(1) garante o uso estrito apenas dos 3 meses anteriores ao mês que está sendo previsto
monthly_sales['baseline_predictions'] = monthly_sales['total'].shift(1).rolling(window=3).mean()

# 3. Filtrando os meses de teste de 2026
final_months = pd.period_range(start='2026-01', end='2026-03', freq='M')
df_final_months = monthly_sales.loc[final_months].copy()

# 4. Cálculo do MAE (Mean Absolute Error) Mês a Mês e Global
df_final_months['absolute_error'] = (df_final_months['total'] - df_final_months['baseline_predictions']).abs()
mae_global = df_final_months['absolute_error'].mean()

# Exibindo os Resultados detalhados mês a mês
print("-- PREVISÃO E COMPARAÇÃO MÊS A MÊS (1º TRIMESTRE 2026) do item 'Bússola de Bordo 702' --")
print("--- Obs: utilizando apenas as orders com o status 'confirmed' como base ---")
for mes in df_final_months.index:
    real = df_final_months.loc[mes, 'total']
    previsto = df_final_months.loc[mes, 'baseline_predictions']
    erro = df_final_months.loc[mes, 'absolute_error']

    # Identificando os meses usados para o cálculo da previsão atual
    meses_treino = [str(mes - i) for i in range(3, 0, -1)]

    print(f"\nMes Previsto: {mes}")
    print(f"  -> Baseado nos meses de treino: {', '.join(meses_treino)}")
    print(f"  -> Valor Real: R$ {real:,.2f}")
    print(f"  -> Previsão Baseline: R$ {previsto:,.2f}")
    print(f"  -> Erro Absoluto do Mês: R$ {erro:,.2f}")

print("\n" + "="*65)
print(f" MAE GLOBAL DO PERÍODO (Média dos erros absolutos): R$ {mae_global:,.2f}")
print("="*65)
