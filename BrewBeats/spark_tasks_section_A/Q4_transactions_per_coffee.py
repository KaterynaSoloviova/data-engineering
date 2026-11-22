"""
Project: BrewBeats
File: Q4_transactions_per_coffee.py
Section: A - Spark DataFrames
Question: Q4 - Count Transactions per Coffee

Description:
This script counts the number of transactions
for each coffee type using Apache Spark DataFrames.

Tasks:
- Load the coffee sales dataset.
- Group transactions by coffee name.
- Count transactions for each coffee type.
- Display the results.

Technologies:
- Python
- Apache Spark
- PySpark DataFrames
"""
from pathlib import Path
from pyspark.sql import SparkSession

# Create a Spark session
spark = SparkSession.builder \
    .appName("BrewBeats Q4 - Transactions per Coffee") \
    .getOrCreate()

# Define the dataset path
PROJECT_PATH = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_PATH / "data" / "coffee_sales.csv"

# Load the CSV file into a Spark DataFrame
df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv(str(DATA_PATH))

df.show(5)

# Count transactions for each coffee type.
transactions_per_coffee = df.groupBy("coffee_name").count()
transactions_per_coffee.show()

# Stop the Spark session
spark.stop()