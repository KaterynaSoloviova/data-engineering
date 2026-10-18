# Part 1 — Query Performance, Full Scans, and Indexes

## Q. 1 — Create a Table for Query Testing

```sql
CREATE TABLE orders_perf (
order_id INT primary key,
customer_id INT NOT NULL,
order_date DATE NOT NULL,
city VARCHAR(50)NOT NULL,
amount_gbp DECIMAL(8,2) NOT NULL,
status VARCHAR(50) NOT NULL
);

INSERT INTO orders_perf (order_id, customer_id, order_date,city, amount_gbp,status) VALUES 
    (1, 101, '2026-08-01', 'London',     45.50, 'complete'),
    (2, 102, '2026-08-01', 'Manchester', 18.00, 'cancelled'),
    (3, 101, '2026-08-02', 'London',     62.25, 'complete'),
    (4, 103, '2026-08-02', 'Leeds',      30.00, 'complete'),
    (5, 104, '2026-08-03', 'Bristol',    55.50, 'complete'),
    (6, 102, '2026-08-03', 'Manchester', 12.00, 'pending'),
    (7, 101, '2026-08-04', 'London',     80.00, 'complete'),
    (8, 105, '2026-08-04', 'Leeds',      20.00, 'complete'),
    (9, 106, '2026-08-05', 'Bristol',   100.00, 'complete'),
    (10, 102, '2026-08-05', 'Manchester', 40.00, 'complete');
```

## Q. 2 — Inspect a Query Before Adding an Index
 
```sql
EXPLAIN
SELECT
    order_id,
    order_date,
    amount_gbp
FROM orders_perf
WHERE customer_id = 101;
```
```
-> Filter: (orders_perf.customer_id = 101)  (cost=1.25 rows=1)
-> Table scan on orders_perf  (cost=1.25 rows=10)

What we have here:
1. MySQL scans 10 rows of the table. For this we need optimiser's estimated cost=1.25
2.Filtering: customer_id = 101
3.Returning matching rows
```

## Q. 3 — Add an Index and Compare

```sql
CREATE INDEX idx_orders_customer ON orders_perf(customer_id);

EXPLAIN
SELECT
    order_id,
    order_date,
    amount_gbp
FROM orders_perf
WHERE customer_id = 101;
```
```
-> Index lookup on orders_perf using idx_orders_customer (customer_id = 101)  (cost=0.8 rows=3)

Difference:
                        Before index	After index
Access method:          Table scan	    Index lookup
Rows scanned:           10	             3
cost                    1.25            0.8
- Before: The database checks the table rows to find the matching customer_id.
- After: The database uses the index to find matching rows faster.
```

## Q. 4 — MCQ: Index
When is an index most likely to help?

```
Answer:  B. A query filters a large table using a selective column.
```

# Part 2 — Filtering Early, Selecting Columns, and Join Keys

## Q. 5 — Compare SELECT * with Required Columns

```sql
SELECT *
FROM orders_perf
WHERE status = 'complete';
```

```sql
SELECT
    order_id,
    order_date,
    amount_gbp
FROM orders_perf
WHERE status = 'complete';
```

```
Query B is better, because this can reduce unnecessary data transfer and makes the query intent clearer.
```

## Q. 6 — Filter Before Returning Data

```sql
SELECT order_id, customer_id, order_date, amount_gbp FROM orders_perf
WHERE status = 'complete' AND order_date >= '2026-08-03'
AND amount_gbp >= 40 ORDER BY order_date;
```

## Q. 7 — Choose the Correct Join Key

```sql
CREATE TABLE customers_perf (
customer_id INT primary key,
customer_name VARCHAR(100) NOT NULL,
city VARCHAR(50) NOT NULL
);

INSERT INTO customers_perf (customer_id, customer_name, city) VALUES
(101, 'Amelia Clarke', 'London'),
(102, 'Oliver Bennett', 'Manchester'),
(103, 'Aisha Khan', 'Leeds'),
(104, 'Harry Thompson', 'Bristol'),
(105, 'Emily Wilson', 'Leeds'),
(106, 'Noah Davies', 'Bristol');

SELECT o.order_id, c.customer_name, o.amount_gbp, o.status FROM orders_perf o INNER JOIN customers_perf c ON o.customer_id = c.customer_id
```
```
Joining on city would be unsafe because several customers can live in the same city
```

## Q. 8 — MCQ: Required Columns
Why should a query select only the columns it needs?

```
Answer: C. It can reduce unnecessary data read or transferred.
```

# Part 3 — Partitioning, Small Files, Columnar Storage, and Compression

## Q. 9 — Choose a Partitioning Column
Most reports filter by:
order_date

Consider these possible partition columns:
order_id
order_date
customer_name
amount_gbp

Which is the best starting choice for the stated access pattern? Explain why.

```
Answer: We should choose order_date because it matches how BritMart usually searches its order data and can improve query performance through partition pruning
```

## Q. 10 — Design a Date-Based Layout
BritMart has these three daily batches:

2026-08-01 -> 100,000 rows
2026-08-02 -> 120,000 rows
2026-08-03 -> 90,000 rows

Create a simple storage layout using the date.

```
Answer: Each day's orders are stored in a separate partition
Orders:
            Order date	Number of rows
	        2026-08-01	100,000
	        2026-08-02	120,000
	        2026-08-03	90,000
```

## Q. 11 — Find the Small-Files Problem
Two designs contain the same amount of data.
Design A
100 files of about 100 MB each
Design B
100,000 files of about 0.1 MB each

Which design is more likely to create excessive file-management and task overhead? Explain why.

```
Design B  - small-filles problems
Therefore the design A is better - easier to manage files
```

## Q. 12 — MCQ: Compression
What is the main storage benefit of compression?

```
Answer: A. It reduces the amount of storage required for compressible data
```

# Part 4 — CSV, Parquet, Avro, and ORC

## Q. 13 — Compare the Formats
Complete the table.

```
Format	    Text or binary?	        Row or column oriented?	        Common strength
CSV			text                    row                             widely support, easy to inspect
Parquet		binary	                column                          analytical reads, compression
Avro		binary	                row                             event exchange with schema
ORC			binary                  column                          analytical storage and compression
```

## Q. 14 — Choose a Format for Each Requirement
Choose CSV, Parquet, Avro, or ORC.

```
A. A simple file that a business user can open easily. - CSV
B. Analytical data where queries often read only a few columns. - Parquet
C. Record-oriented data exchange where schema travels with the data. - Avro
D. Columnar analytical storage used with systems that support ORC well. - ORC
```

## Q. 15 — Inspect a CSV and List Its Limitations

```
order_sample.csv

order_id,order_date,city,amount_gbp,status
1,2026-08-01,London,45.50,complete
2,2026-08-01,Manchester,18.00,cancelled
3,2026-08-02,Leeds,30.00,complete
```

```
How the schema is represented - The first row contains column names separated by commas, followed by the data.
whether the file is human-readable  - yes, it is
two limitations compared with a binary analytical format:
- no type check;
- hard to write multi lines data;
- large file size;
- slower queries
```
## Q. 16 — MCQ: Parquet
Why is Parquet commonly used for analytical data?

```
Answer: D. Its columnar layout can help queries read only needed columns.
```

# Optional Practice

## Q. 17 — Build and Compare a Composite Index
BritMart stores three years of orders as:
one folder
500,000 tiny CSV files
no date organisation

Most reports filter by date and select only a few columns.
Using only today's concepts, suggest three improvements.

```
1. Use date-based partitioning: organise orders into folders by year, month, or day so reports can find data for specific dates more quickly.
2. Reduce the number of small files: combine tiny CSV files into fewer, larger files to reduce file-management overhead.
3. Use Parquet instead of CSV: parquet is a binary columnar format that allows reports to read only the columns they need, reducing the amount of data scanned.
```

## Q. 18 — Find an Index That May Not Help Much

```sql
SELECT
    SUM(amount_gbp)
FROM orders_perf;
```
Would an index on customer_id make this full-table total automatically fast? Explain why or why not.

```
No. An index on customer_id won't automatically speed up the query because it calculates the total of all amount_gbp values and doesn't filter by customer_id
```

## Q. 19 — Review a Poor Storage Layout
BritMart stores three years of orders as:
one folder
500,000 tiny CSV files
no date organisation
Most reports filter by date and select only a few columns.
Using only today's concepts, suggest three improvements.

```
1. Partition by date - organise orders into year or month folders.
2. Reduce small files — combine tiny CSV files into fewer, larger files.
3. Use Parquet — read only the columns needed for reports, improving query speed.
```

## Q. 20 — Choose the Complete Design
BritMart has:

daily order data
reports usually filter by date
reports select 5 columns from a 60-column dataset
data is retained for several years

Choose and explain:

```
1. Partitioning approach: Partition by order_date (year/month) so date-based reports scan less data.
2. File format: Use Parquet because reports read only 5 of 60 columns.
3. Compression need: Use compression to reduce storage space and data-reading costs.
4. Query habit: Select only the required 5 columns and filter by date using WHERE to improve performance.
```