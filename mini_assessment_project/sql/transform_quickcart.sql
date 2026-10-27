CREATE TABLE IF NOT EXISTS analytics_orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    order_date DATE,
    quantity INTEGER,
    unit_price NUMERIC(10, 2),
    payment_status TEXT
);

TRUNCATE TABLE analytics_orders;

INSERT INTO analytics_orders (
    order_id,
    customer_id,
    product_id,
    order_date,
    quantity,
    unit_price,
    payment_status
)
SELECT
    order_id::INTEGER,
    customer_id::INTEGER,
    product_id::INTEGER,
    order_date::DATE,
    quantity::INTEGER,
    unit_price::NUMERIC(10, 2),
    payment_status
FROM staging_orders
WHERE order_id ~ '^[0-9]+$'
  AND customer_id ~ '^[0-9]+$'
  AND product_id ~ '^[0-9]+$'
  AND quantity ~ '^[0-9]+$'
  AND unit_price ~ '^[0-9]+(\.[0-9]+)?$'
  AND order_date ~ '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'
ON CONFLICT (order_id) DO NOTHING;
