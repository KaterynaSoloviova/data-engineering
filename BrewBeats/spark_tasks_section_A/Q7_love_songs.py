"""
Project: BrewBeats
File: Q7_love_songs.py
Section: A - Spark RDD
Question: Q7 - Count Songs with 'Love' in Title

Description:
This script counts songs that contain the word 'love'
in their titles using Apache Spark RDD.

Tasks:
- Load the Spotify dataset.
- Convert the DataFrame into an RDD.
- Filter songs containing 'love' in their titles.
- Count the matching songs.
- Display the results.

Technologies:
- Python
- Apache Spark
- PySpark RDD
"""

from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as spark_sum

# Create a Spark session
spark = SparkSession.builder \
    .appName("BrewBeats Q7 - Love Songs") \
    .getOrCreate()

# Define the dataset path
PROJECT_DIR = Path(__file__).parent.parent
DATA_PATH = PROJECT_DIR / "data" / "Spotify data_project.csv"

# Load the CSV file into a Spark DataFrame
spotify_df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv(str(DATA_PATH))

spotify_df.show(5)

# Convert the DataFrame into an RDD
spotify_rdd = spotify_df.rdd

# Filter songs containing 'love' in their titles
love_songs = spotify_rdd.filter(lambda row: "love" in row["song_title"].lower())

# Count the matching songs
love_songs_count = love_songs.count()

print("Number of love songs:", love_songs_count)

spark.stop()