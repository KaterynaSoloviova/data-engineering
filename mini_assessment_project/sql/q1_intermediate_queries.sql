-- Top 10 customers by revenue

select o.customer_id, c.customer_name, SUM(o.quantity * o.unit_price) as total_revenue
from orders o join customers c on o.customer_id = c.customer_id
group by o.customer_id, c.customer_name
order by total_revenue desc
limit 10;

-- Month-over-month sales growth

with monthly_sales as (
	select DATE_TRUNC('month', order_date)::date AS sales_month, SUM(quantity * unit_price) as total_sales
	from orders
	group by sales_month
	order by sales_month
),
sales_with_previous_month as (
	select 
	sales_month,
	total_sales,
	LAG(total_sales) OVER (ORDER BY sales_month) as previous_month_sales
	from monthly_sales
)
select
    sales_month,
    total_sales,
    previous_month_sales,
    total_sales - previous_month_sales as diff,
    round((total_sales - previous_month_sales) * 100 / NULLIF(previous_month_sales, 0), 2) as growth_percentage
from sales_with_previous_month
order by sales_month;


-- Customers who ordered in consecutive months

with customer_months as (
select customer_id, DATE_TRUNC('month', order_date)::date as order_month from orders group by customer_id, DATE_TRUNC('month', order_date)::date
)
select c1.customer_id, c1.order_month, c2.order_month as next_month 
from customer_months c1
join customer_months c2 on c1.customer_id = c2.customer_id and c2.order_month = c1.order_month + INTERVAL '1 month'
order by c1.customer_id, c1.order_month;

-- Products never ordered

select p.product_id, p.product_name
from orders o
right join products p on o.product_id = p.product_id
where o.order_id is null;


-- Revenue contribution percentage by category

with category_revenue as (
	select p.category, sum(o.quantity * o.unit_price) as total_revenue from orders o
	join products p on o.product_id = p.product_id
	group by p.category
)
select category, total_revenue, round(total_revenue * 100 / sum(total_revenue) OVER (), 2) as revenue_contribution
from category_revenue
order by revenue_contribution desc;
