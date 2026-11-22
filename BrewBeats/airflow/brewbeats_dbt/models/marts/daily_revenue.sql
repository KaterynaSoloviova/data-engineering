

-- Configure dbt to create a physical table in Snowflake
{{ config(materialized='table') }}

-- Calculate daily revenue and transaction count
SELECT
    transaction_date,

    -- Calculate total revenue for each day
    ROUND(SUM(revenue), 2) AS total_revenue,

    -- Count the number of transactions for each day
    COUNT(*) AS total_transactions
    
 -- references a staging model. dbt understands the dependency between models.
FROM {{ ref('stg_coffee_sales') }}

-- Group transactions by date
GROUP BY transaction_date

