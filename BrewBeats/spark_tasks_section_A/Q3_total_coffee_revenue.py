
"""
Project: BrewBeats
File: Q3_total_coffee_revenue.py
Section: A - Spark DataFrames
Question: Q3 - Calculate Total Coffee Revenue

Description:
This script calculates the total revenue from coffee sales
using Apache Spark DataFrames.

Tasks:
- Load the coffee sales dataset from a CSV file.
- Create a Spark DataFrame.
- Calculate the total revenue.
- Display the result.

Technologies:
- Python
- Apache Spark
- PySpark DataFrames
"""

from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as spark_sum, round as spark_round

# Create a Spark session
spark = SparkSession.builder \
    .appName("BrewBeats Q3 - Total Coffee Revenue") \
    .getOrCreate()


# Define the dataset path
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_DIR / "data" / "coffee_sales.csv"

# Load the CSV file into a Spark DataFrame
df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv(str(DATA_PATH))

# Display the first five rows
df.show(5)

# Calculate the total revenue
total_revenue = df.agg(spark_round(spark_sum("money"), 2).alias("total_revenue"))
total_revenue.show()

# Stop the Spark session
spark.stop()