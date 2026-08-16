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
  - [x] 1.1
    - [x] Código SQL calculando:
		- Quantidade total de linhas
		- Intervalo de datas analisado (data mínima e máxima)
		- Valor mínimo
		- Valor máximo
		- Valor médio
  - [x] 1.2
    - [x] Qual é o valor médio registrado na coluna "total"?
		> [!TIP]
		> Resposta: 28704,992077227675

  - [x] 1.3
    - [x] Possíveis outliers em "total"
    	> [!TIP]
		> Resposta: Sobre outliers na coluna “total”, existem possíveis outliers na parte superior do Q3(Terceiro Quartil) + 1,5 * IQR (Intervalo Interquartil) acima do valor 82597,85. Chegando a um total de 452 valores de possíveis outliers de um total de 48998 linhas, que significam 0,92% do total.
    - [x] Qualidade dos dados (valores nulos ou inconsistentes)
  		> [!TIP]
		> Sobre a qualidade dos dados da tabela orders, na coluna  “salesperson_id”, existem 24131 ocorrências de um total de  48998 linhas, dando uma porcentagem de 49,25% valores nulos. Esse valor nos faz perceber que a qualidade da tabela está baixa e precisaria de tratamento desses valores
    - [x] e se você considera que a tabela orders está pronta para análises ou se exigiria tratamento prévio ou relacionamento com demais tabelas?
		> [!TIP]
		> Sobre se a tabela "orders” está pronta para análises, podemos perceber que não, pois ainda precisaremos tratar os valores nulos que correspondem a 49,25% dos valores da coluna “salesperson_id”. Caso quisesse aprofundar ainda mais a análise da tabela orders, seria bom juntar com as informações das tabelas “customers” e “locations”,  para ter mais informações para usar de filtro.

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

# Fix code text 1.3
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