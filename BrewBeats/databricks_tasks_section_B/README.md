## Section B: SQL on Databricks

### B.1. Objective

This section uses SQL to answer business questions about the coffee sales dataset. It reinforces aggregation, grouping, sorting, common table expressions (CTEs), and date-based analysis.

The queries should run against the coffee sales data registered or loaded in the Databricks environment.

### B.2. Top five coffee types by revenue

Business question: Which five coffee products generate the most revenue?

Approach:

1. Group transactions by coffee_name.
2. Calculate SUM(money) for each coffee.
3. Sort the totals from highest to lowest.
4. Return the first five rows.

This query ranks products by revenue, not by the number of transactions. A product with fewer but higher-value sales may rank differently from a product with more transactions.
B.3. Revenue by payment type
Business question: How much revenue is associated with each payment type?

Approach:

1. Group the data by cash_type.
2. Sum the money column for each group.
3. Sort or display the resulting payment-type totals.

The result can be used to compare revenue recorded under the payment categories in the source data. The interpretation of each category should follow the actual values and definitions in the dataset.

### B.4. Monthly revenue using a CTE

Business question: What is the total revenue for each month?

Approach:

1. Use a Common Table Expression (WITH) to define an intermediate monthly aggregation.
2. Group transactions by year and month.
3. Calculate total revenue for each month.

4. Select the monthly results, optionally ordered chronologically.
A CTE makes a query easier to read by separating the intermediate calculation from the final selection.

### B.5. Day with the highest number of transactions

Business question: Which calendar date had the greatest number of sales transactions?

Approach:

1. Group records by transaction date.
2. Count the rows for each date.
3. Sort the counts in descending order.
4. Return the date with the highest count.

This identifies the busiest sales day by transaction volume. It does not necessarily identify the day with the highest revenue.

### B.6. Section B deliverables and evidence

The expected deliverable is a set of Databricks SQL scripts or a notebook containing the four queries and their outputs.

Record the executed query outputs here: top five coffees by revenue, revenue by payment type, monthly revenue, and the date with the highest transaction count. These exact rankings and values are not included in the available project journal and should be copied from the Databricks results.