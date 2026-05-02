/*
we needed a query to show change over time. This one shows monthly revenue which we can use to identify busy seasons.
*/

SELECT
    STRFTIME(o.order_purchase_timestamp, '%Y-%m') AS order_month,
    SUM(oi.price) AS total_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_purchase_timestamp >= $1::TIMESTAMP
  AND o.order_purchase_timestamp <= $2::TIMESTAMP
  AND o.order_status = 'delivered'
GROUP BY 1
ORDER BY 1;
