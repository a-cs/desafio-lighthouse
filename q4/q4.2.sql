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
),
top_10_clientes AS (
    -- Isola o ID dos 10 clientes fiéis identificados no passo anterior
    SELECT 
        mp.customer_id
    FROM 
        metricas_pedido mp
    LEFT JOIN 
        diversidade_produtos dp ON mp.customer_id = dp.customer_id
    WHERE 
        COALESCE(dp.diversidade_categorias, 0) >= 13
    ORDER BY 
        mp.ticket_medio DESC,   
        mp.customer_id ASC
    LIMIT 10
)
-- Consulta final: Descobre a categoria campeã de vendas para o grupo isolado
SELECT 
    p.category_id,
    SUM(o_i.quantity) AS quantidade_total_itens
FROM 
    orders o
INNER JOIN top_10_clientes tc ON o.customer_id = tc.customer_id  -- Filtra apenas os 10 clientes
INNER JOIN order_items o_i ON o.id = o_i.order_id
INNER JOIN product_variants p_v ON o_i.product_variant_id = p_v.id
INNER JOIN products p ON p_v.product_id = p.id
GROUP BY 
    p.category_id
ORDER BY 
    quantidade_total_itens DESC  -- Ordena da maior quantidade para a menor
LIMIT 1;