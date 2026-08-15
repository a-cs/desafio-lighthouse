import os
import csv
import sys
from datetime import datetime

csv_folder_path = "../arquivos/"
sql_folder_path = "../q2/"
sql_file_name = "schema.sql"

def infer_data_type(value):
    #infere o tipo de dado de uma string.
    value = value.strip().lower()
    if not value or value.lower() in ("null", "none", "na", "n/a"):
        return None # checka se é nulo

    timestamp_formats = [
        "%Y-%m-%d %H:%M:%S",        # 2026-08-13 22:45:00
        "%Y-%m-%dT%H:%M:%S",        # 2026-08-13T22:45:00 (ISO)
        "%Y-%m-%d %H:%M:%S.%f",     # 2026-08-13 22:45:00.123
        "%d/%m/%Y %H:%M:%S",        # 13/08/2026 22:45:00
        "%d/%m/%Y %H:%M",           # 13/08/2026 22:45
    ]
    for fmt in timestamp_formats:
        try:
            datetime.strptime(value, fmt)
            return "TIMESTAMP" # checka se é timestamp
        except ValueError:
            pass
    
    date_formats = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"]
    for fmt in date_formats:
        try:
            datetime.strptime(value, fmt)
            return "DATE" # checka se é data
        except ValueError:
            pass
    try:
        int_value = int(value)
        return "INTEGER" # checka se é int
    except ValueError:
        pass

    if value.lower() in ("true", "false"):
        return "BOOLEAN" # checka se é bool

    try:
        float(value)
        return "FLOAT" # checka se é float
    except ValueError:
        pass

    # Padrão é Texto
    return "TEXT" # se não for nenhum, retorn text

def generate_sql_from_csvs_in_a_folder_infering_col_type(csv_folder_path, sample_rows=1000):
    #checkar se o caminho da pasta espificada existe existe
    sql_schema = ""
    if not os.path.isdir(csv_folder_path):
        print(f"Error: A pasta '{csv_folder_path}' não existe. Corrija o caminho da pasta.")
        return

    #ranking dos tipos das colunas do sql
    type_priority = {
        "BOOLEAN": 1, 
        "INTEGER": 2, 
        "FLOAT": 3, 
        "DATE": 4, 
        "TIMESTAMP": 5, 
        "TEXT": 6
    }
    
    #iterarar na lista de arquivos presentes na pasta 
    for file_name in os.listdir(csv_folder_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(csv_folder_path, file_name)

            # gerar tabelas a partir do nome dos arquivos
            table_name = os.path.splitext(file_name)[0]

            try:
                with open(file_path, mode="r", encoding="utf-8") as file:
                    reader = csv.reader(file)
                    if(os.path.getsize(file_path) == 0): # chekar se o csv está vazio
                        raise Exception(f"Arquivo vazio.\n")
                    
                    headers = next(reader)  # ler o a linha de Header
                    col_types = {col_name: None for col_name in headers if col_name} # criar dicionario com o nome e o tipo da coluna
                    
                    for row_idx, row in enumerate(reader):
                        if row_idx >= sample_rows:
                            break
                        for index, value in enumerate(row):
                            if index >= len(headers):
                                break
                            
                            col_name = headers[index]
                            if not col_name:
                                continue

                            current_type = infer_data_type(value)
                            
                            # atualizar o valor do tipo da coluna caso tenha um ranking maior
                            if current_type is not None:
                                existing_type = col_types[col_name]
                                if not existing_type:
                                    col_types[col_name] = current_type
                                else:
                                    if type_priority[current_type] > type_priority[existing_type]:
                                        col_types[col_name] = current_type

                # atualizar o tipo da coluna caso ela esteja vazia
                for col_name in col_types:
                        if col_types[col_name] is None:
                            col_types[col_name] = "TEXT"

                # criar a tabela com as colunas
                columns = [f"    {col_name} {col_types[col_name]}" for col_name in headers if col_name]
                if columns:
                    sql_schema += f"CREATE TABLE {table_name} (\n"
                    sql_schema += ",\n".join(columns)
                    sql_schema += "\n);\n"


            except Exception as e:
                print(f"Erro ao ler o arquivo '{file_name}': {e}\n")
                sys.exit(1)
                

    #criar pasta caso ela não exita
    os.makedirs(sql_folder_path, exist_ok=True)
    
    #gravar os dados no arquivo .sql  
    with open(os.path.join(sql_folder_path, sql_file_name), "w", encoding="utf-8") as file:
        file.write(sql_schema)
    print(f"Arquivo '{sql_file_name}' gerado com sucesso\nno caminho '{os.path.join(sql_folder_path, sql_file_name)}'\n")

#gerar o sql de acordo com o csv e ler a qtd de sample_rows para determinar o tipo
generate_sql_from_csvs_in_a_folder_infering_col_type(csv_folder_path, sample_rows=100)