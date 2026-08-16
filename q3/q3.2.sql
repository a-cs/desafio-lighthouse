SELECT SUM(count) AS total_linhas FROM (
    SELECT COUNT(*) FROM customers
    UNION ALL
    SELECT COUNT(*) FROM orders
    UNION ALL
    SELECT COUNT(*) FROM order_items
    UNION ALL
    SELECT COUNT(*) FROM payments
);