WITH calendar AS (
    -- Gera todos os dias de 2020-01-01 até 2026-12-31
    SELECT 
        d::date AS data,
        EXTRACT(ISODOW FROM d)::integer AS numero_dia_semana,
        CASE EXTRACT(ISODOW FROM d)
            WHEN 1 THEN 'Segunda-feira'
            WHEN 2 THEN 'Terça-feira'
            WHEN 3 THEN 'Quarta-feira'
            WHEN 4 THEN 'Quinta-feira'
            WHEN 5 THEN 'Sexta-feira'
            WHEN 6 THEN 'Sábado'
            WHEN 7 THEN 'Domingo'
        END AS nome_dia_semana
    FROM GENERATE_SERIES('2020-01-01'::date, '2026-12-31'::date, '1 day'::interval) d
),
calendario_com_vendas AS (
    -- Junta o calendário de tamanho fixo com os dados da tabela order
    SELECT 
        c.data,
        c.numero_dia_semana,
        c.nome_dia_semana, 
        CAST(COALESCE(SUM(o.total), 0) AS DECIMAL(12,2)) AS venda_diarias
    FROM calendar c
    LEFT JOIN orders o ON c.data = o.placed_at::date AND o.channel = 'pos'
--    WHERE o.channel = 'pos'
    GROUP BY c.data, c.numero_dia_semana, c.nome_dia_semana
)
-- Retorna os totais acumulados e médias calculadas sobre o período exato solicitado
SELECT 
    nome_dia_semana,
    ROUND(AVG(venda_diarias), 2) AS media_vendas_diaria
FROM calendario_com_vendas
GROUP BY numero_dia_semana, nome_dia_semana
ORDER BY numero_dia_semana;