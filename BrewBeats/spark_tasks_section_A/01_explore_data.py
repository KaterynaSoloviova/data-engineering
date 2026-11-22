"""
Project: BrewBeats - Coffee Sales Data Pipeline
File: 01_explore_data.py
Section: A - Spark RDD & DataFrames
        (Databricks and Local Spark)

Description:
This script performs an initial exploration of the
coffee sales dataset using Apache Spark.

The script includes:
- Loading the CSV file;
- Displaying the first few rows;
- Inspecting column names;
- Checking data types;
- Identifying missing values;
- Checking for duplicate records.

Technologies:
- Python
- Apache Spark (PySpark)
"""


from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum, when

# Creating a SparkSession
spark = SparkSession.builder \
    .appName("BrewBeats Coffee Sales Analysis") \
    .getOrCreate()

# Upload CSV
df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
   .csv("BrewBeats/data/coffee_sales.csv")


# Display the first 5 rows
df.show(5)

# Display the number of rows and columns
print("Number of rows:", df.count())
print("Number of columns:", len(df.columns))

# Display column names
print(df.columns)

# Display data types
df.printSchema()


# Check missing values in each column
missing_values = df.select([
    spark_sum(
        when(col(column).isNull(), 1).otherwise(0)
    ).alias(column)
    for column in df.columns
])

missing_values.show()

# Check duplicate records
total_rows = df.count()
unique_rows = df.dropDuplicates().count()

print("Total rows:", total_rows)
print("Unique rows:", unique_rows)
print("Duplicate rows:", total_rows - unique_rows)


# Stop the Spark session
spark.stop()
