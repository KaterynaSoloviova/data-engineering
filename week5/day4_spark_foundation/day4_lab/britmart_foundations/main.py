# Imports SparkSession from PySpark
from pyspark.sql import SparkSession  

# Q. 3 — Create a Local Spark Application

# Create a Spark session
spark = (
    SparkSession.builder                # Starts building a Spark session
    .appName("britmart_foundations")    # Gives your application its name
    .master("local[*]")                 # Runs Spark locally on your Mac, using available CPU cores
    .getOrCreate()                      # Creates a session or reuses an existing one
)

# Create the data: we are creating a Python list containing three tuples
data = [
    (101, "London", 45.50),
    (102, "Manchester", 18.00),
    (103, "Leeds", 30.00),
]

# Create column names
columns = ["id", "city", "amount"]

# Create the DataFrame
df = spark.createDataFrame(data, columns) # This converts our Python data into a Spark DataFrame.

# Display the DataFrame
df.show()

# Stop the Spark session
spark.stop()


