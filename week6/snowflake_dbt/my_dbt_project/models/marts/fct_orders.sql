select
    p.order_id,
    p.customer_id,
    c.customer_name,
    c.email,
    c.city,
    p.order_date,
    p.product_id,
    p.quantity,
    p.unit_price,
    p.order_amount,
    p.net_amount,
    p.order_status

from {{ ref('int_order_payments') }} p

left join {{ ref('stg_customers') }} c
    on p.customer_id = c.customer_id