import os
import pandas as pd
from sqlalchemy import create_engine

# Configurações do banco de dados
USER = "lighthouse"
PASSWORD = "lighthouse1"
HOST = "localhost"
PORT = "5430"
DATABASE = "LH_Nautical"
csv_folder_path = "../arquivos/"

# Cria a conexão com o PostgreSQL
db_url = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(db_url)

print("-- Iniciando o carregamento dos arquivos no banco de dados. --\n\n")
# Lista todos os arquivos da pasta e filtra apenas os que terminam com .csv
for file_name in os.listdir(csv_folder_path):
    if file_name.endswith(".csv"):
        # Monta o caminho completo do arquivo
        file_path = os.path.join(csv_folder_path, file_name)
        
        # Pega o nome do arquivo sem a extensão .csv para usar como nome da tabela
        table_name = os.path.splitext(file_name)[0]
        
        try:
            # Lê o arquivo CSV
            df = pd.read_csv(file_path)
            
            # Insere os dados na tabela existente (append)
            df.to_sql(table_name, con=engine, if_exists="append", index=False)
            print(f"{file_name} carregado a tabela '{table_name}' com sucesso.")
        except Exception as e:
            print(f"Erro ao carregar {file_name}: {e}")
print("\n\n-- Todos os arquivos foram carregados com sucesso no banco de dados. --")