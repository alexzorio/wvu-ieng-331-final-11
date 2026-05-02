/*
we needed a query to show change over time. This one shows monthly revenue which we can use to identify busy seasons.
*/

SELECT
    STRFTIME(o.order_purchase_timestamp, '%Y-%m') AS order_month,
    SUM(oi.price) AS total_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
--  AND o.order_purchase_timestamp >= CAST($1 AS TIMESTAMP)
--  AND o.order_purchase_timestamp <= CAST($2 AS TIMESTAMP)
GROUP BY 1
ORDER BY 1;
