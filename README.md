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
		> Sobre outliers na coluna “total”, existem possíveis outliers na parte superior do Q3(Terceiro Quartil) + 1,5 * IQR (Intervalo Interquartil) acima do valor 82597,85. Chegando a um total de 452 valores de possíveis outliers de um total de 48998 linhas, que significam 0,92% do total.
    - [x] Qualidade dos dados (valores nulos ou inconsistentes)
  		> [!TIP]
		> Sobre a qualidade dos dados da tabela orders, na coluna  “salesperson_id”, existem 24131 ocorrências de um total de  48998 linhas, dando uma porcentagem de 49,25% valores nulos. Esse valor nos faz perceber que existem valores nulos, mas ao aprofundar a análise, percebemos que todos o valores nulos na “salesperson_id” acontecem quando “channel” tem o valor igual a "ecommerce", e por conta disso a falta provavelmente se deve a não terem cadastrado um valor padrão para o “salesperson_id”, quando a venda acontece pelo canal "ecommerce" e o usuário não informa o vendedor
    - [x] e se você considera que a tabela orders está pronta para análises ou se exigiria tratamento prévio ou relacionamento com demais tabelas?
		> [!TIP]
		> Sobre se a tabela "orders” está pronta para análises ou se precisa de algum tratamento, podemos perceber que depende. No caso de ser uma análise financeira do faturamento, os outlier presentes na coluna “total”, precisam estar presentes para não mascarar os valores reais de faturamento. Caso fosse para uma análise de previsão de estoque mensal ou faturamento médio dia-a-dia o ideal seria remover os outliers, para conseguir ter previsões mais corretas.
		
		> [!TIP]
		> Sobre se a tabela "orders” precisa de relacionamento com demais tabelas, caso quisesse aprofundar ainda mais a análise da tabela “orders”, seria bom juntar com as informações por exemplo das tabelas “customers” e “locations”,  para ter mais informações para usar de filtro.


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
  - [x] 4.1
    - [x] Código SQL calculando:
		- [x]  O Ticket Médio e a Diversidade de categorias por cliente.
		- [x]  A identificação e filtro dos 10 clientes "Fiéis" (maior Ticket Médio entre aqueles com diversidade >= 13 categorias).
  - [x] 4.2
    - [x] Como você chegou nas categorias mais vendidas? (mapeamento da cadeia de chaves)
        - >[!TIP]
			> - A categoria mais vendida para o top 10 clientes é a category_id 8, com uma quantidade total de itens de 492, o código sql para encontrar essa informação consta no arquivo na pasta “./q4/q4.2.sql” no material completo. 
			> - Para conseguir chegar nesse valor, utilizei a consulta da questão 4.1 como uma tabela temporária, para aí conseguir conectar o customer_id da tabela top 10 com o customer_id da tabela orders.
			> - Conectei a tabela orders usando a coluna id, com a tabela order_items usando a coluna order_id.
			> - Conectei a tabela order_items usando a coluna product_variant_id, com a tabela product_variants usando a coluna id.
			> - Conectei a tabela product_variants usando a coluna product_id, com a tabela products usando a coluna id.
			> - Com todas as tabela conectadas, selecionei a coluna category_id presente na tabela produtos e soma da quantity presente na tabela order_items.
			> - Agrupei pelo category_id presente na tabela produtos.
			> - Ordenei de forma Descendente pela quantidade de itens naquela categoria.
			> - E por último limitei a apenas o primeiro valor, para chegar na categoria mais vendida dentro dos clientes top 10.
    - [x] Como você chegou nas categorias mais vendidas? (mapeamento da cadeia de chaves)
        - >[!TIP]
			> - A lógica que utilizei para pegar os clientes com diversidade mínima foi, primeiro gerei a consulta para pegar o ticket médio por customer_id.
			> - Depois gerei a consulta para pegar a diversidade de categorias (sem repetir valores) para cada customer_id.
			> - Juntei os resultados das duas consultas usando o customer_id como chave para ligar elas.
			> - Filtrei para mostrar apenas os valores com valor maior ou igual a 13 categorias.
    - [x] Como garantiu que a contagem de itens refletisse apenas os Top 10?
		- >[!TIP]
			> - Para garantir o Top 10, primeiro gerei a consulta para pegar o ticket médio por customer_id.
			> - Depois gerei a consulta para pegar a diversidade de categorias (sem repetir valores) para cada customer_id.
			> - Juntei os resultados das duas consultas usando o customer_id como chave para ligar elas.
			> - Filtrei para mostrar apenas os valores com valor maior ou igual a 13 categorias.
			> - Depois ordenei de forma Descendente pelo Ticket Médio, para deixar do maior valor do ticket para o menor.
			> - Depois ordenei de forma Ascendente pelo customer_id, para caso houvesse algum empate no valor do ticket médio.
			> - Por último, limitei para mostrar apenas os 10 primeiros.

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