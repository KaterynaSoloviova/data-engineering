
    

    create  table
      "sales"."main"."customer_sales__dbt_tmp"
  
    
    as (
      SELECT
    customer,
    COUNT(order_id) AS total_orders,
    SUM(total_amount) AS revenue,
    AVG(total_amount) AS average_order
FROM "sales"."main"."stg_sales"
GROUP BY customer
    );
    
  