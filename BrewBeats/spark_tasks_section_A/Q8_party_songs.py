"""
Project: BrewBeats
File: Q8_party_songs.py
Section: A - Spark RDD
Question: Q8 - Curate Party Songs

Description:
This script selects energetic and danceable songs
for BrewBeats' 5th birthday party using Apache Spark RDD.

Tasks:
- Load the Spotify dataset.
- Convert the DataFrame into an RDD.
- Calculate a party score using danceability, energy, and liveness.
- Select the top 20 songs.
- Display the selected party songs.

Technologies:
- Python
- Apache Spark
- PySpark RDD
"""

from pathlib import Path
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("BrewBeats Q8 - Party Songs") \
    .getOrCreate()

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_DIR / "data" / "Spotify data_project.csv"

spotify_df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv(str(DATA_PATH))

spotify_rdd = spotify_df.rdd

# Calculate a party score for each song
party_songs = spotify_rdd.map(
    lambda row: (
        row["song_title"],
        row["artist"],
        (row["danceability"] + row["energy"] + row["liveness"]) / 3
    )
)

# Select the top 20 party songs
top_20 = party_songs.takeOrdered(20, key=lambda song: -song[2])

# Display song titles and artists
for song in top_20:
    print(song[0], "-", song[1])

# Stop Spark session
spark.stop()