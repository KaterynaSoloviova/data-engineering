
SELECT
    CAST(order_id AS INTEGER) AS order_id,
    TRIM(customer) AS customer_name,
    TRIM(product) AS product_name,
    CAST(amount AS DECIMAL(12, 2)) AS sales_amount
FROM {{ ref('sales_data') }}
WHERE order_id IS NOT NULL
  AND amount IS NOT NULL
  AND amount >= 0

