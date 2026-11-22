"""
Project: BrewBeats
File: Q1_count_songs_per_artist.py
Section: A - Spark RDD
Question: Q1 - Count Songs per Artist

Description:
This script analyzes Spotify data using Apache Spark RDD.
It calculates the number of songs for each artist.

Tasks:
- Load the Spotify dataset from a CSV file.
- Create a Spark DataFrame.
- Inspect the dataset.
- Convert the DataFrame into an RDD.
- Count the number of songs for each artist.
- Display the results.

Technologies:
- Python
- Apache Spark
- PySpark RDD
"""

from pyspark.sql import SparkSession
from pathlib import Path

# Create a Spark session
spark = SparkSession.builder \
    .appName("BrewBeats Q1 - Songs per Artist")\
    .getOrCreate()

# Define the dataset path
PROJECT_DIR = Path(__file__).resolve().parent.parent # type: ignore
DATA_PATH = PROJECT_DIR / "data" / "Spotify data_project.csv"

spotify_df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv(str(DATA_PATH))

# Display the first 5 rows
spotify_df.show(5)

# Display the number of rows and columns
print("Number of rows:", spotify_df.count())
print("Number of columns:", len(spotify_df.columns))

# Display column names
print(spotify_df.columns)

# Display data types
spotify_df.printSchema()

# Convert the DataFrame into an RDD
spotify_rdd = spotify_df.rdd
print(spotify_rdd.first())

# Extract artist names from the RDD
artists_rdd = spotify_rdd.map(lambda row: row["artist"])
print(artists_rdd.take(5))

# Display the number of records in the RDD
print("Number of RDD records:", spotify_rdd.count())

# Assign a value of 1 to each artist
artists_with_count = artists_rdd.map(lambda artist: (artist, 1))
print(artists_with_count.take(5))

# Count songs for each artist
songs_per_artist = artists_with_count.reduceByKey(lambda a, b: a + b)

# Display the results
print("Songs per artist:")
for artist, count in songs_per_artist.collect():
    print(f"{artist}: {count}")

# Stop the Spark session
spark.stop()
