# Como ativar o venv
- Abra o terminal na pasta raiz do projeto
- No terminal execute o comando:
  ```shell
  source venv/bin/activate
  ```

# Como utilizar o docker para testar o db
- Primeiro crie o schema.sql executanto o arquivo q2.1.py presente na pasta q2
- Abra o terminal na pasta raiz do projeto
- No terminal execute o comando para subir o banco:
  ```shell
  docker compose up db -d
  ```

# Questões

- ## 1
  - [ ] 1.1
  - [ ] 1.2
  - [ ] 1.3
____

- ## 2
  - [x] 2.1
    - [x] ler csv
    - [x] gerar tabela apartir do nome do arquivo e dos headers
    - [x] gerar schema.sql
    - [x] adicionar as primary keys a coluna com o nome de "id"
    - [x] corrigir os tipos de algumas colunas no script que gera o schema.sql para poder fazer a questão 3.1
  - [x] 2.2 - arquivo schema.sql
____

- ## 3
  - [x] 3.1
    - [x] criar script python para carregar todos os dados de cada tabela no banco
  - [x] 3.2
    - [x] Qual o total de linhas somadas das seguintes tabelas: customers, orders, order_items e payments?
		> [!TIP]
		> Resposta: 251864
____

- ## 4
  - [ ] 4.1
  - [ ] 4.2
____

- ## 5
  - [ ] 5.1
  - [ ] 5.2
____

- ## 6
  - [ ] 6.1
  - [ ] 6.2
  - [ ] 5.3
____

- ## 7
  - [ ] 7.1
  - [ ] 7.2
  - [ ] 7.3
____