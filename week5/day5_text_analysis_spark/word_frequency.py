"""Task:
1. Read a local text file using Apache Spark.
2. Perform text analysis using Spark to find the five most frequent words in an article,
excluding English stop words such as the, is, and, of, to, etc.
"""

from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,    # allows us to select or refer to a column in a Spark DataFrame.
    lower,
    regexp_replace, # This function replaces characters that match a regular expression. We use it to remove punctuation and unwanted characters.
    split,
    explode, # takes an array of values and creates a separate row for each value.
    desc
)

import nltk # Natural Language Toolkit
from nltk.corpus import stopwords


# 1. Create a SparkSession
spark = (
    SparkSession.builder 
    .appName("MariaPrymachenkoAnalysis")
    .master("local[*]") # It tells Spark where to run
    .getOrCreate() # Creates a new Spark session if one doesn't exist, or reuses an existing one
)

# 2. Reading a local file using Spark
article_path = Path(__file__).parent / "article.txt"
df = spark.read.text(str(article_path))

# 3. Display the result
df.show(truncate=False) # tells Spark not to shorten long text. Without truncate=False, Spark might display only part of a long line.

# 4. Downloading stopwords using NLTK
nltk.download("stopwords")
stop_words = stopwords.words("english")

# 5. Cleaning the text
cleaned_df = df.select(
    lower(
        regexp_replace( # This removes unwanted characters
            col("value"),
            "[^a-zA-Z\\s]",
            ""
        )
    ).alias("text")
)

# 6. Splitting the text into individual words

words_df = cleaned_df.select(
    explode(
        split(col("text"), "\\s+")
    ).alias("word")
)

print("INDIVIDUAL WORDS:")
words_df.show()


# 7. Removing stopwords

filtered_words = words_df.filter(
    (col("word") != "") &          # This checks that the word is not empty.
    (~col("word").isin(stop_words)) # Checks whether a word exists in the stopwords list.
)

print("WORDS AFTER REMOVING STOPWORDS:")
filtered_words.show()


# 9. Count word frequency

word_counts = filtered_words.groupBy("word") \
    .count() \
    .orderBy(desc("count"))


# 10. Display all word frequencies

print("ALL WORD FREQUENCIES:")
word_counts.show()


# 11. Displaying top 5 words

print("TOP 5 MOST FREQUENT WORDS:")

top_5_words = word_counts.limit(5)

top_5_words.show()


# 12. Stoping Spark session

spark.stop()


"""
Answer:
TOP 5 MOST FREQUENT WORDS:
+-----------+-----+
|       word|count|
+-----------+-----+
|  paintings|    4|
|        art|    3|
|prymachenko|    3|
|  ukrainian|    3|
|        war|    3
"""



