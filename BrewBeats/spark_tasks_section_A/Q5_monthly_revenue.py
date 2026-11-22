"""
Project: BrewBeats
File: Q5_monthly_revenue.py
Section: A - Spark DataFrames
Question: Q5 - Calculate Monthly Revenue

Description:
This script calculates monthly revenue from coffee sales
using Apache Spark DataFrames.

Tasks:
- Load the coffee sales dataset.
- Extract the month from the date column.
- Group sales by month.
- Calculate total revenue for each month.
- Display the results.

Technologies:
- Python
- Apache Spark
- PySpark DataFrames
"""

from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import month, sum as spark_sum, round as spark_round

# Create a Spark session
spark = SparkSession.builder \
    .appName("BrewBeats Q5 - Monthly Revenue") \
    .getOrCreate()

# Define the dataset path
PROJECT_DIR = Path(__file__).parent.parent
DATA_PATH = PROJECT_DIR / "data" / "coffee_sales.csv"

# Load the CSV file into a Spark DataFrame
df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv(str(DATA_PATH))

df.show(5)
df.printSchema()

# Extract the month from the date column

df = df.withColumn("month", month("date"))
df.select("date", "month").show(10)

# Group sales by month
sales_by_month = df.groupBy("month")

# Calculate total revenue for each month
total_revenue = sales_by_month.agg(spark_round(
    spark_sum("money"), 2).alias("total_revenue")
)
total_revenue.orderBy("month").show()

# Stop the Spark session
spark.stop()