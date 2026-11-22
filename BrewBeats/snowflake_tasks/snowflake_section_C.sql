
-- ============================================================
-- BREWBEATS PROJECT
-- SECTION C: SNOWFLAKE
-- ============================================================
--
-- OBJECTIVE:
-- 1. Create stages and load coffee sales and Spotify datasets.
-- 2. Analyze coffee sales revenue.
-- 3. Find the top 3 songs by Drake.

-- NOTE:
-- SQL statements were tested in the Snowflake Worksheet.
-- CSV files are uploaded using the Snowsight interface.


-- ============================================================
-- DATABASE AND SCHEMA SETUP
-- ============================================================

-- Create the project database.

CREATE DATABASE IF NOT EXISTS BREWBEATS_DB;

-- Create a schema for raw project data.

CREATE SCHEMA IF NOT EXISTS BREWBEATS_DB.RAW;

-- Set the active database and schema.

USE DATABASE BREWBEATS_DB;
USE SCHEMA RAW;


-- ============================================================
-- Q1: CREATE A STAGE AND LOAD COFFEE_SALES.CSV
-- INTO A SNOWFLAKE TABLE
-- ============================================================

-- Step 1: Create an internal stage for the coffee sales CSV file.

CREATE STAGE IF NOT EXISTS BREWBEATS_DB.RAW.COFFEE_STAGE;


-- Step 2: Create a CSV file format.

CREATE OR REPLACE FILE FORMAT BREWBEATS_DB.RAW.COFFEE_CSV_FORMAT
    TYPE = CSV
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"';


-- Step 3: Upload coffee_sales.csv to the stage using Snowsight.
-- Databases -> BREWBEATS_DB -> RAW -> Stages -> COFFEE_STAGE
-- -> Upload Files.


-- Step 4: Create a table with the same structure as the original table.

CREATE TABLE IF NOT EXISTS BREWBEATS_DB.RAW.COFFEE_SALES_FROM_STAGE
LIKE BREWBEATS_DB.RAW.COFFEE_SALES;


-- Step 5: Load the CSV data from the stage into the Snowflake table.

COPY INTO BREWBEATS_DB.RAW.COFFEE_SALES_FROM_STAGE
FROM @BREWBEATS_DB.RAW.COFFEE_STAGE
FILE_FORMAT = (
    FORMAT_NAME = 'BREWBEATS_DB.RAW.COFFEE_CSV_FORMAT'
)
ON_ERROR = 'ABORT_STATEMENT';


-- Step 6: Verify the number of loaded records.

SELECT COUNT(*) AS TOTAL_ROWS
FROM BREWBEATS_DB.RAW.COFFEE_SALES_FROM_STAGE;


-- ============================================================
-- Q2: FIND THE TOP 3 COFFEE TYPES BY TOTAL REVENUE
-- ============================================================

-- SUM(MONEY) calculates the total revenue for each coffee type.
-- GROUP BY combines transactions with the same coffee name.
-- ROUND(..., 2) rounds the revenue to two decimal places.
-- ORDER BY sorts the results from highest to lowest revenue.
-- LIMIT 3 returns only the three highest-revenue coffee types.

SELECT
    COFFEE_NAME,
    ROUND(SUM(MONEY), 2) AS TOTAL_REVENUE
FROM BREWBEATS_DB.RAW.COFFEE_SALES_FROM_STAGE
GROUP BY COFFEE_NAME
ORDER BY TOTAL_REVENUE DESC
LIMIT 3;


-- ============================================================
-- Q3: CREATE A STAGE AND LOAD SPOTIFY.CSV
-- INTO A SNOWFLAKE TABLE
-- ============================================================

-- Step 1: Create an internal stage for the Spotify CSV file.

CREATE STAGE IF NOT EXISTS BREWBEATS_DB.RAW.SPOTIFY_STAGE;


-- Step 2: Create a table for Spotify data.
-- The first CSV column is skipped because it has no column name.

CREATE TABLE IF NOT EXISTS BREWBEATS_DB.RAW.SPOTIFY_DATA (
    ACOUSTICNESS FLOAT,
    DANCEABILITY FLOAT,
    DURATION_MS NUMBER,
    ENERGY FLOAT,
    INSTRUMENTALNESS FLOAT,
    KEY NUMBER,
    LIVENESS FLOAT,
    LOUDNESS FLOAT,
    MODE NUMBER,
    SPEECHINESS FLOAT,
    TEMPO FLOAT,
    TIME_SIGNATURE NUMBER,
    VALENCE FLOAT,
    TARGET NUMBER,
    SONG_TITLE VARCHAR,
    ARTIST VARCHAR
);


-- Step 3: Upload the Spotify CSV file to the stage using Snowsight.
-- Databases -> BREWBEATS_DB -> RAW -> Stages -> SPOTIFY_STAGE
-- -> Upload Files.


-- Step 4: Load the CSV data into the Snowflake table.

COPY INTO BREWBEATS_DB.RAW.SPOTIFY_DATA (
    ACOUSTICNESS,
    DANCEABILITY,
    DURATION_MS,
    ENERGY,
    INSTRUMENTALNESS,
    KEY,
    LIVENESS,
    LOUDNESS,
    MODE,
    SPEECHINESS,
    TEMPO,
    TIME_SIGNATURE,
    VALENCE,
    TARGET,
    SONG_TITLE,
    ARTIST
)
FROM (
    SELECT
        $2, $3, $4, $5, $6, $7, $8, $9,
        $10, $11, $12, $13, $14, $15, $16, $17
    FROM @BREWBEATS_DB.RAW.SPOTIFY_STAGE
)
FILE_FORMAT = (
    TYPE = CSV
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
)
ON_ERROR = 'ABORT_STATEMENT';


-- Step 5: Verify the number of loaded records.

SELECT COUNT(*) AS TOTAL_ROWS
FROM BREWBEATS_DB.RAW.SPOTIFY_DATA;


-- ============================================================
-- Q4: FIND THE TOP 3 SONGS BY DRAKE
-- Ranked by danceability.
-- ============================================================

SELECT
    SONG_TITLE,
    ARTIST,
    DANCEABILITY
FROM BREWBEATS_DB.RAW.SPOTIFY_DATA
WHERE LOWER(TRIM(ARTIST)) = 'drake'
ORDER BY DANCEABILITY DESC
LIMIT 3;
