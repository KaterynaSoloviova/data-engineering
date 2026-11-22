
"""
Project: BrewBeats
File: Q2_average_danceability.py
Section: A - Spark RDD
Question: Q2 - Calculate Average Danceability

Description:
This script calculates the average danceability
of songs in the Spotify dataset using Apache Spark RDD.

Tasks:
- Load the Spotify dataset from a CSV file.
- Create a Spark DataFrame.
- Convert the DataFrame into an RDD.
- Extract danceability values.
- Calculate the average danceability using RDD transformations.
- Display the result.

Technologies:
- Python
- Apache Spark
- PySpark RDD
"""

from pyspark.sql import SparkSession
from pathlib import Path

# Create a Spark session
spark = SparkSession.builder \
    .appName("BrewBeats Q2 - Average Danceability") \
    .getOrCreate()

# Define the dataset path
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_DIR / "data" / "Spotify data_project.csv"

# Load the CSV file into a Spark DataFrame 
spotify_df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv(str(DATA_PATH))

# Convert the DataFrame into an RDD
spotify_rdd = spotify_df.rdd

# Extract danceability names from the RDD
danceability_rdd = spotify_rdd.map(lambda row: row["danceability"])
print(danceability_rdd.take(5))

# Calculate the sum of danceability values
total_danceability = danceability_rdd.sum()

# Count the number of songs
total_songs = danceability_rdd.count()

# Calculate the average danceability
average_danceability = round(total_danceability / total_songs, 2)

# Display the result
print("Average danceability:", average_danceability)

# Stop the Spark session
spark.stop()

