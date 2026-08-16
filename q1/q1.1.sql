SELECT 
    COUNT(*) AS total_linhas,
    MIN(created_at)::DATE AS data_minima,
    MAX(created_at)::DATE AS data_maxima,
    CAST(MIN(total) AS DECIMAL(12,2)) AS valor_minimo,
    CAST(MAX(total) AS DECIMAL(12,2)) AS valor_maximo,
    CAST(AVG(total) AS DECIMAL(12,2)) AS valor_medio
FROM orders;