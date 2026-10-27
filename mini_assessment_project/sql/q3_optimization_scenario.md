## SQL Optimization Scenario

```sql
SELECT c.customer_name, 
 SUM(o.quantity * o.unit_price) 
FROM orders o 
JOIN customers c 
ON o.customer_id = c.customer_id
WHERE order_date >= '2025-01-01' 
GROUP BY c.customer_name; 
```

```
1. Bottleneck:                         	
Missing index on `orders.order_date`
Why this could be a problem:
The database might have to scan many rows to find orders from January 1, 2025.

2. Bottleneck:
Missing index on `orders.customer_id`
Why this could be a problem:
Joining orders with customers may require more processing.

3. Bottleneck: 
Large `orders` table
Why this could be a problem:
If the table contains millions of rows, filtering, joining and aggregation can be computationally expensive.

4.Bottleneck:
`GROUP BY c.customer_name`
Why this could be a problem:
Two different customers with the same name could be combined into a single group.
```

## Suggested indexes

```sql
CREATE INDEX idx_orders_order_date
ON orders (order_date);

CREATE INDEX idx_orders_customer_id
ON orders (customer_id)
```
```
A composite index on (order_date, customer_id) could also be tested.
We do not need to create all three indexes immediately. Additional indexes consume space and slow down INSERT, UPDATE, and DELETE operations. It is advisable to check the execution plan and compare the results before and after the changes.
```

## Explain execution plan analysis

1. Analyze the original execution plan:
We use the EXPLAIN command to analyze the original execution plan without executing the query. This helps identify how PostgreSQL plans to retrieve, join, and aggregate the data. The purpose of this step is to examine how PostgreSQL plans to execute the SQL query and identify potential performance bottlenecks before running the query.

```sql
EXPLAIN
SELECT
    c.customer_id,
    c.customer_name,
    SUM(o.quantity * o.unit_price) AS total_revenue
FROM orders AS o
JOIN customers AS c
    ON o.customer_id = c.customer_id
WHERE o.order_date >= DATE '2025-01-01'
GROUP BY
    c.customer_id,
    c.customer_name;
```

We have the result:
```
HashAggregate  (cost=20.77..22.02 rows=100 width=52)
  Group Key: c.customer_id
  ->  Hash Join  (cost=4.25..15.85 rows=492 width=29)
        Hash Cond: (o.customer_id = c.customer_id)
        ->  Seq Scan on orders o  (cost=0.00..10.25 rows=492 width=13)
              Filter: (order_date >= '2025-01-01'::date)
        ->  Hash  (cost=3.00..3.00 rows=100 width=20)
              ->  Seq Scan on customers c  (cost=0.00..3.00 rows=100 width=20)
```
Execution plan analysis:
```
The original execution plan contains four main operations:
- Sequential Scan on orders:
PostgreSQL performs a sequential scan on the orders table and applies the filter order_date >= '2025-01-01'. The plan estimates that 492 rows will remain after filtering.
A sequential scan reads the table's rows and checks whether they satisfy the filter condition. This approach can be efficient for small tables or when most rows need to be processed. However, it may become expensive when the table grows significantly, especially if the date condition selects only a small proportion of the records.
An index on orders(order_date) could be considered if measurements show that date filtering is a performance bottleneck.
- Sequential Scan on customers
PostgreSQL scans the customers table and estimates that it will retrieve 100 rows.
Because the estimated table size is small, a sequential scan is a reasonable choice. Creating an additional index solely to avoid this scan would probably provide little benefit.
- Hash Join
PostgreSQL uses a hash join to combine records from orders and customers based on the condition o.customer_id = c.customer_id.
A hash join builds a hash table from one input and uses it to find matching records from the other input. This is a common join strategy and is often efficient when joining tables of these sizes.
The plan estimates that the join will produce 492 rows.
- Hash Aggregate
After joining the tables, PostgreSQL groups the records by customer_id and customer_name and calculates total revenue using SUM(o.quantity * o.unit_price).
The plan estimates that the final result will contain 100 groups, corresponding to approximately 100 customers.
The estimated cost of the final operation is 22.02. PostgreSQL cost values are internal planning estimates, not execution times in milliseconds or seconds.
```

Conclusion:
```
The sequential scan on orders is the main operation worth investigating because it applies the date filter. If the table is large, this operation could become a performance bottleneck. However, the execution plan alone does not prove that it is a bottleneck. Therefore we should use EXPLAIN (ANALYZE, BUFFERS) to measure actual execution time and buffer usage before deciding whether an index on orders(order_date) would improve performance.
```

2. Analyze the execution plan with query
 We use EXPLAIN (ANALYZE, BUFFERS) to examine the query execution plan and compare the estimated performance with the actual execution results.The goal of this step is to measure the actual query performance, compare estimated and actual row counts, and identify potential performance bottlenecks.

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT
    c.customer_id,
    c.customer_name,
    SUM(o.quantity * o.unit_price) AS total_revenue
FROM orders AS o
JOIN customers AS c
    ON o.customer_id = c.customer_id
WHERE o.order_date >= DATE '2025-01-01'
GROUP BY
    c.customer_id,
    c.customer_name;
```
We have the result:
```
HashAggregate  (cost=20.77..22.02 rows=100 width=52) (actual time=1.839..1.906 rows=100 loops=1)
  Group Key: c.customer_id
  Batches: 1  Memory Usage: 80kB
  Buffers: shared hit=6
  ->  Hash Join  (cost=4.25..15.85 rows=492 width=29) (actual time=0.085..1.106 rows=491 loops=1)
        Hash Cond: (o.customer_id = c.customer_id)
        Buffers: shared hit=6
        ->  Seq Scan on orders o  (cost=0.00..10.25 rows=492 width=13) (actual time=0.012..0.751 rows=491 loops=1)
              Filter: (order_date >= '2025-01-01'::date)
              Rows Removed by Filter: 9
              Buffers: shared hit=4
        ->  Hash  (cost=3.00..3.00 rows=100 width=20) (actual time=0.063..0.064 rows=100 loops=1)
              Buckets: 1024  Batches: 1  Memory Usage: 14kB
              Buffers: shared hit=2
              ->  Seq Scan on customers c  (cost=0.00..3.00 rows=100 width=20) (actual time=0.006..0.025 rows=100 loops=1)
                    Buffers: shared hit=2
Planning:
  Buffers: shared hit=151
Planning Time: 3.872 ms
Execution Time: 1.991 ms
```
Execution plan analysis:
```
- Sequential Scan on orders: PostgreSQL scanned the orders table and applied the date filter. The query returned 491 rows, while 9 rows were removed by the filter. The scan took approximately 0.751 ms. Since the table contains around 500 records, a sequential scan is reasonable.
- Sequential Scan on customers: PostgreSQL retrieved all 100 customer records in approximately 0.025 ms. This operation is efficient for a small table, so an additional index is unnecessary.
- Hash Join: PostgreSQL joined the two tables using customer_id. The join returned 491 rows and completed in approximately 1.106 ms. The actual row count was close to the estimated 492 rows, indicating an accurate estimate.
- Hash Aggregate: PostgreSQL grouped the records by customer and calculated total revenue. The operation produced 100 groups and used approximately 80 kB of memory.

The total execution time was 1.991 ms, and the planning time was 3.872 ms. The query used six shared buffer hits during execution. The estimated and actual row counts were very similar, suggesting that PostgreSQL's estimates were accurate for this dataset.
```

Conclusion:
```
The SQL query is already performing efficiently, so no additional indexes are needed at this stage.
The actual execution time is only 1.991 ms, and the estimated row counts are close to the actual results. Although the sequential scan on orders could become a bottleneck as the dataset grows, it is not currently a significant performance issue. An index on orders(order_date) should be considered only if future performance measurements show that it would improve query execution.
```
