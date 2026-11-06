# Q. 7 — Use an RDD

from pyspark.sql import SparkSession

# 1. Create a SparkSession
spark = (
    SparkSession.builder
    .appName("britmart_rdd_exercise")
    .master("local[*]")
    .getOrCreate()
)

# 2. Get the SparkContext
sc = spark.sparkContext

# 3. Create a Python list
amounts = [45.50, 18.00, 62.25, 12.00]

# 4. Convert the list into an RDD
rdd = sc.parallelize(amounts)

# 5. Keep only amounts greater than 20
filtered_rdd = rdd.filter(lambda x: x > 20)

# 6. Increase the remaining amounts by 10%
updated_rdd = filtered_rdd.map(lambda x: round(x * 1.10, 2))

# 7. Collect and print the results
result = updated_rdd.collect()
print("Final amounts:", result)

# 8. Stop Spark
spark.stop()