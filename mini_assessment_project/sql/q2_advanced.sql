
-- Query 1: Rank customers based on total revenue

with customer_revenue as (
	select o.customer_id, c.customer_name, sum(o.quantity * o.unit_price) as total_revenue
	from orders o
	join customers c
	on o.customer_id = c.customer_id
	group by o.customer_id, c.customer_name
	order by total_revenue
)
select 
	customer_id,
    customer_name,
    total_revenue,
    rank() over (order by total_revenue desc) as revenue_rank
from customer_revenue
order by revenue_rank;


-- Query 2: Running total sales by month

with monthly_sales as (
    select DATE_TRUNC('month', order_date)::date as order_month, sum(quantity * unit_price) as total_sales
    from orders
    group by DATE_TRUNC('month', order_date)::date
    order by DATE_TRUNC('month', order_date)::date
)
select
    order_month,
    total_sales,
    SUM(total_sales) over (
        order by order_month
        rows between unbounded preceding and current row
    ) as running_total_sales
from monthly_sales
order by order_month;

-- Query 3: The highest selling product per category

with product_revenue as (
	select p.product_id, p.product_name, p.category, sum(o.quantity * o.unit_price) as total_sales from orders o
	join products p on o.product_id = p.product_id
	group by p.product_id, p.product_name, p.category
	order by total_sales desc
),
ranked_products as (
    select
        product_id,
        product_name,
        category,
        total_sales,
        rank() over (
            partition by category
            order by total_sales desc
        ) as category_rank
    from product_revenue
)
select
    product_id,
    product_name,
    category,
    total_sales
from ranked_products
where category_rank = 1
order by category, product_name;


-- Query 4: 7-day rolling average sales

with daily_sales as (
select order_date::date as sales_date , sum(quantity * unit_price) as daily_sales
from orders
group by order_date::date 
order by order_date::date asc
),

calendar as (
    select
        generate_series(
            (select min(sales_date) from daily_sales),
            (select max(sales_date) from daily_sales),
            interval '1 day'
        )::date as sales_date
),

daily_sales_calendar as (
    select
        c.sales_date,
        COALESCE(ds.daily_sales, 0) as daily_sales
    from calendar as c
    left join daily_sales as ds
        on c.sales_date = ds.sales_date
)

select
    sales_date,
    daily_sales,
    round(
        avg(daily_sales) over(
            order by sales_date
            rows between 6 preceding and current row
        ),
        2
    ) as rolling_7_day_avg
from daily_sales_calendar
order by sales_date;
