# Q. 11 — Group and Aggregate

from pyspark.sql import SparkSession
from pyspark.sql.functions import sum

# 1. Create a SparkSession
spark = (
    SparkSession.builder
    .appName("britmart_group_aggregate")
    .master("local[*]")
    .getOrCreate()
)

# 2. Create the data
data = [
    (101, "London", 45.50),
    (102, "Leeds", 30.00),
    (103, "London", 62.25),
    (104, "Leeds", 20.00),
]

# 3. Define column names
columns = ["order_id", "city", "amount_gbp"]

# 4. Create a DataFrame
df = spark.createDataFrame(data, columns)

# 5. Group rows by city and calculate total sales
result_df = df.groupBy("city").agg(
    sum("amount_gbp").alias("total_sales") # alias() simply renames the result column
)

# 6. Display the result
result_df.show()

# 7. Stop Spark
spark.stop()


