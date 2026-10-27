-- Lab 1 — Customer Revenue Analytics

SELECT
    customer,
    COUNT(order_id) AS total_orders,
    SUM(amount) AS total_sales,
    AVG(amount) AS avg_order_value
FROM {{ ref('sales_data') }}
GROUP BY customer
ORDER BY total_sales DESC
