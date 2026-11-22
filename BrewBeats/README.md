## BrewBeats — Complete Project Journal
### Mini Project 2
### Technology stack: Apache Spark · Databricks · Snowflake · Snowpark · dbt · Apache Airflow · Power BI / Tableau

## Project Brief
### Business Case
BrewBeats is a coffee kiosk chain that also curates in-store music playlists to encourage customers to stay longer. The business needs a more reliable way to understand its sales and improve reporting.

The main challenges are:

- Daily sales reporting is manual and slow.
- Data processing and reporting tasks are run by hand rather than through an automated workflow.
- As data volume grows, queries and analysis can become slower.
- There are no consistent data quality checks before reports are shared.
The goal of this mini project is to explore a modern data engineering workflow: process data with Spark, query it with SQL, store sales data in Snowflake, transform it with dbt, orchestrate the workflow with Airflow, and present business metrics in a BI dashboard.

### Datasets
Two CSV files are provided for different parts of the assignment.

1. **coffee_sales.csv**

Columns:
- date — date of the transaction
- datetime — transaction timestamp
- cash_type — payment type
- card — card information, where provided
- money — transaction revenue
- coffee_name — coffee product purchased
This dataset is used for coffee sales analysis, SQL exercises, Snowflake ingestion, dbt transformations, and the business intelligence dashboard.

2. **Spotify_data.csv**

Columns include acousticness, danceability, duration_ms, energy, instrumentalness, key, liveness, loudness, mode, speechiness, tempo, time_signature, valence, target, song_title, and artist.
This dataset is used for the Spark RDD exercises, including artist counts, average danceability, song-title searches, and playlist curation.

**Dataset separation**: 
coffee_sales.csv is used for the sales and data pipeline questions. 
Spotify_data.csv is used for the Spark RDD questions.

### End-to-End Project Architecture

Spotify_data.csv ───────────────> Spark RDD analysis
                                      |
                                      └── Artist/song analysis and playlist task

coffee_sales.csv
      |
      v
Spark DataFrame analysis (Databricks / local Spark)
      |
      v
SQL analysis (Databricks SQL)
      |
      v
Snowflake stage and RAW table
      |
      v
dbt staging model
      |
      v
dbt daily revenue mart
      |
      v
dbt data quality tests
      |
      v
Apache Airflow DAG
      |
      v
BI dashboard (Power BI / Tableau)

The diagram combines the assignment's individual exercises with the implemented Snowflake–dbt–Airflow workflow. The Spotify analysis is a separate Spark exercise; it is not part of the coffee sales pipeline.

### What's included

- Project overview and business case
- Section A: Spark RDDs and DataFrames
- Section B: Databricks SQL
- Section C: Snowflake SQL and Snowpark
- Section D: Your existing detailed dbt + Airflow documentation
- Section E: Business case, architecture, dashboard requirements and results
- Final deliverables checklist and learning outcomes