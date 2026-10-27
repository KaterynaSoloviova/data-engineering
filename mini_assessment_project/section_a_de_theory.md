# Q1. OLTP vs OLAP Architecture 
The company currently stores transactional and analytical workloads in the same SQL  database. 
Tasks
1. Explain why this creates performance issues.
When transactional and analytical tasks use the same database, they compete for resources. Large reports can slow down daily operations, such as placing orders or updating customer information.

2. Compare OLTP and OLAP workloads. 
- OLTP (Online Transaction Processing): Handles daily transactions, such as creating orders and updating customer details. It needs fast responses.-
- OLAP (Online Analytical Processing): Handles large queries and reports to analyze sales, customers, and business performance.

3. Suggest an improved architecture.
Separate the operational database from the analytical system. This allows daily transactions to run quickly while reports are processed separately.

4. Explain where:  
-PostgreSQL /SQLServer/MySql
-Data warehouse  
-Data lake 
should be used.  

- PostgreSQL / SQL Server / MySQL: Store and manage daily transactions, such as customers, products, and orders.
- Data warehouse: Store organized data from different sources for reporting and business analysis.
- Data lake: Store large amounts of raw data, such as CSV files, logs, and clickstream events, in different formats.

# Q2. ACID vs BASE in Distributed Systems
QuickCart wants to store clickstream events from millions of users.
Tasks 
1. Explain why BASE systems are preferred for clickstream systems.
BASE systems can handle large amounts of data across many servers. They are scalable and available, making them suitable for storing millions of clickstream events.

2. Which workloads require ACID compliance?
ACID is important for transactions where data must be accurate and reliable, such as:
- Processing customer payments.
- Creating orders.
- Updating product stock.
- Managing customer account balances.

3. Give examples where eventual consistency is acceptable.
Eventual consistency means data may take some time to update across systems, but eventually becomes consistent.
It could be:
- Updating website visit statistics.
- Showing popular products.
- Generating sales dashboards.
- Tracking customer browsing behavior.

# Q3. Storage Formats & Querying 
Tasks 
1. Compare:  
 -CSV  
 -JSON  
 -Avro  
 -Parquet 

- CSV: Stores data in rows and columns. It is simple and easy to read, but does not support complex data types well.
- JSON: Stores data as key-value pairs. It is flexible and useful for nested data, such as website events.
- Avro: Stores data in a compact binary format with a schema. It is useful for data exchange and streaming.
- Parquet: Stores data in columns instead of rows. It is efficient for analytical queries and saves storage space.

2. Why do analytical systems prefer columnar storage?  
Columnar storage keeps values from the same column together. Analytical queries often read only a few columns from large datasets, so this reduces the amount of data read and improves performance.

3. Explain avro vs json format.
JSON is human-readable and easy to understand. Avro uses a compact binary format and a schema to define the data structure. Avro is often more efficient for large-scale data processing, while JSON is convenient for APIs and debugging.

4. Explain compression benefits in Parquet. 
Parquet stores similar column values together, making compression more effective. This reduces storage costs and the amount of data read from disk, which can make analytical queries faster.

# Q4. Partitioning, Indexing 
Tasks 
1. Design a partitioning strategy for:  
-orders table  
-clickstream data 

- Orders table: Partition by order_date, for example, monthly partitions. This helps queries find orders within a specific date range.
- Clickstream data: Partition by event date, such as daily or monthly partitions, depending on data volume. This makes it easier to query recent events and remove old data.

2. Suggest indexing strategy for: 
 -customer lookups 
 -order filtering  
 -joins  

- Customer lookups: Create an index on customer_id.
- Order filtering: Create an index on order_date if queries frequently filter by date.
- Joins: Create indexes on foreign key columns, such as orders.customer_id, to help queries join tables efficiently.

3. Explain when indexes negatively affect performance.  
Indexes use extra storage and must be updated when data is inserted, updated, or deleted. Too many indexes can slow down these operations. Indexes may also provide little benefit for small tables or queries that return a large part of the table.