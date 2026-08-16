WITH metricas_pedido AS (
    -- Calcula faturamento e frequência direto na tabela de pedidos (sem duplicar)
    SELECT 
        customer_id,
        CAST(SUM(total) / COUNT(id) AS DECIMAL(12,2)) AS ticket_medio
    FROM
    	orders
    GROUP BY 
        customer_id
),
diversidade_produtos AS (
    -- Calcula a diversidade de categorias abrindo os itens do pedido
    SELECT 
        o.customer_id,
        COUNT(DISTINCT p.category_id) AS diversidade_categorias
    FROM 
        orders o
    INNER JOIN order_items o_i ON o.id = o_i.order_id
    INNER JOIN product_variants p_v ON o_i.product_variant_id = p_v.id
    INNER JOIN products p ON p_v.product_id = p.id
    GROUP BY 
        o.customer_id
)
-- Junta as duas partes pelo ID do cliente
SELECT 
    mp.customer_id,
    mp.ticket_medio,
    COALESCE(dp.diversidade_categorias, 0) AS diversidade_categorias
FROM 
    metricas_pedido mp
LEFT JOIN 
    diversidade_produtos dp ON mp.customer_id = dp.customer_id
WHERE 
    -- Filtro de Elite: Apenas clientes com 13 ou mais categorias distintas
    COALESCE(dp.diversidade_categorias, 0) >= 13
ORDER by
    mp.ticket_medio DESC,   -- Ordenação principal (maior para o menor)
    mp.customer_id ASC      -- Desempate (ordem crescente do ID)
LIMIT 10;                   -- Apenas o top 10 clientes