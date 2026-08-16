SELECT 
    COUNT(*) AS total_linhas,
    MIN(created_at)::DATE AS data_minima,
    MAX(created_at)::DATE AS data_maxima,
    MIN(total) AS valor_minimo,
    MAX(total) AS valor_maximo,
    AVG(total) AS valor_medio
FROM orders;