# Q. 17 — Inspect a Spark Plan
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum

# 1. Create a SparkSession
spark = (
    SparkSession.builder
    .appName("britmart_inspect_plan")
    .master("local[*]")
    .getOrCreate()
)

# 2. Create the data
data = [
    (101, "London", 45.50, "complete"),
    (102, "Manchester", 18.00, "cancelled"),
    (103, "London", 62.25, "complete"),
]

# 3. Define column names
columns = ["order_id", "city", "amount_gbp", "status"]

# 4. Create a DataFrame
df = spark.createDataFrame(data, columns)

# 5. Filter completed orders
completed_df = df.filter(df.status == "complete")

# 6. Group by city and calculate total sales
result_df = completed_df.groupBy("city").agg(
    sum("amount_gbp").alias("total_sales")
)

# 7. Inspect the Spark execution plan
result_df.explain()     # Show me how you plan to execute these operations.

# 8. Display the results
result_df.show()

# 9. Stop Spark
spark.stop()
