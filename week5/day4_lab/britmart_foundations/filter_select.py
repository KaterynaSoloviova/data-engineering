# Q. 10 — Filter and Select
from pyspark.sql import SparkSession

# 1. Create a SparkSession
spark = (
    SparkSession.builder
    .appName("britmart_filter_select")
    .master("local[*]")
    .getOrCreate()
)

# 2. Get the SparkContext
sc = spark.sparkContext

# 3 Crate the data
data = [
    (101, "London", 45.50, "complete"),
    (102, "Manchester", 18.00, "cancelled"),
    (103, "London", 62.25, "complete"),
]

# # 3. Define column names
columns = ["order_id", "city", "amount_gbp", "status"]

# 4. Create a DataFrame
df = spark.createDataFrame(data, columns)

# 5. Keep only completed orders
completed_df = df.filter(df.status == "complete")

# 6. Select only the required columns
result_df = completed_df.select("order_id", "city", "amount_gbp")

# 7. Display the result
result_df.show()

# 8. Stop Spark
spark.stop()
