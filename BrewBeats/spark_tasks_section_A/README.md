## Section A: Spark RDDs and DataFrames

### A.1. Objective

This section introduces Apache Spark for distributed data processing. It uses two Spark data abstractions:

- RDD (Resilient Distributed Dataset): a lower-level distributed collection that supports transformations and actions.
- DataFrame: a higher-level, structured representation of data organized into named columns. It supports SQL-like operations and query optimization.
The Spotify dataset is used for the RDD questions, while the coffee sales dataset is used for DataFrame analysis.

### A.2. RDD analysis of Spotify data

**Q1. Count the number of songs per artist**

**Goal**: Find how many tracks are associated with each artist.

Approach:

1. Load Spotify_data.csv as an RDD.
2. Remove or account for the header row.
3. Parse each record and identify the artist field.
4. Map each artist to a count of one.
5. Use reduceByKey to add the counts for each artist.

Concepts demonstrated: RDD creation, mapping, key-value pairs, and aggregation with reduceByKey.

**Q2. Calculate average danceability**

**Goal**: Calculate the average danceability value across all songs.

Approach:

1. Read the Spotify CSV data as an RDD.
2. Extract the danceability field from each valid row.
3. Convert the value to a numeric type.
4. Aggregate the sum and count, then divide the sum by the count.

A sum-and-count aggregation is preferable to collecting all values to the driver because it can be performed across partitions.
Concepts demonstrated: parsing records, numeric conversion, RDD transformations, and aggregation.

**Q7. Count song titles containing the word “love”**

**Goal**: Count how many song titles contain the word love.

Approach:
1. Extract the song_title field.
2. Apply a case-insensitive text check so titles containing Love, LOVE, or love are treated consistently.
3. Filter matching titles.
4. Count the matching records.

This is a simple example of text filtering on a distributed dataset. The exact count should be taken from the executed notebook output.

**Q8. Curate a playlist for BrewBeats' fifth birthday**

**Goal**: Create a party playlist using the Spotify dataset.

Approach: Use the available song and artist information, together with audio features such as danceability, energy, and valence, to identify suitable upbeat tracks. Review the resulting titles and artists and present a curated list.

The final playlist should be based on the records actually present in Spotify_data.csv; song selections should not be invented.

### A.3. DataFrame analysis of coffee sales

**Q3. Load coffee sales and calculate total revenue**

Goal: Read coffee_sales.csv into a Spark DataFrame and calculate total sales revenue.

Approach:

1. Load the CSV with a header.
2. Inspect the inferred or explicitly defined schema.
3. Convert the money column to a numeric type if necessary.
4. Aggregate the column using sum.

The total revenue recorded during the later Snowflake/dbt work was 115,431.58 across 3,636 transactions. This provides a useful cross-check when the same source data and filtering rules are used.

**Q4. Count transactions for each coffee**

**Goal**: Find the number of transactions for every coffee_name.

Approach: Group the DataFrame by coffee_name and count the records in each group. The resulting table shows the transaction volume for each coffee product.

**Q5. Calculate monthly revenue**

**Goal**: Create a month value from the transaction date and calculate revenue per month.

Approach:

1. Convert date to a date type if required.
2. Derive a month field from the date.
3. Group records by month.
4. Sum money within each month.

This converts transaction-level records into a monthly summary suitable for trend analysis.

### A.4. RDD versus DataFrame

An RDD is a lower-level distributed collection that gives the developer more control over transformations, but usually requires more manual handling of data. A DataFrame stores data in named columns and provides a structured API similar to a database table. DataFrames can benefit from Spark's query optimizer, making them generally easier and often more efficient for structured data analysis. RDDs are useful when lower-level control is needed.

### A.5. Section A deliverables and evidence

The expected deliverable is a Spark notebook or notebooks showing the RDD and DataFrame operations. The notebook should include the code, the resulting output, and short explanations.

Record the executed notebook outputs here: artist counts, average danceability, total revenue, transaction counts by coffee, monthly revenue, count of titles containing “love”, and the final birthday playlist. Exact Spotify results are not present in the project journal currently available, so they should be copied from the actual notebook rather than guessed.