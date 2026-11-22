
-- ============================================================
-- BREWBEATS PROJECT
-- SECTION D: DBT + AIRFLOW
-- SNOWFLAKE VALIDATION WORKSHEET
-- ============================================================
--
-- PROJECT OBJECTIVE:
-- Build a data transformation pipeline using dbt and Apache
-- Airflow, with Snowflake as the cloud data warehouse.
--
-- This worksheet contains SQL commands and queries used to:
-- 1. Create and configure the Snowflake database and schemas.
-- 2. Validate the dbt staging model.
-- 3. Validate the Daily Revenue Mart.
-- 4. Check data quality.
-- 5. Validate the final transformed dataset.
-- 6. Document the Airflow pipeline status.
--
-- IMPORTANT:
-- dbt model SQL files are maintained in the dbt project
-- and executed from the VS Code terminal.
--
-- This worksheet is used for SQL-based inspection and
-- validation directly in Snowflake Snowsight.
--
-- TECHNOLOGIES:
-- Snowflake | dbt | Apache Airflow | SQL | Python
--
-- DATABASE: BREWBEATS_DB
-- SOURCE SCHEMA: RAW
-- DBT OUTPUT SCHEMA: DBT_DEV
--
-- SOURCE TABLE:
-- BREWBEATS_DB.RAW.COFFEE_SALES_FROM_STAGE
--
-- STAGING VIEW:
-- BREWBEATS_DB.DBT_DEV.STG_COFFEE_SALES
--
-- ANALYTICAL MART:
-- BREWBEATS_DB.DBT_DEV.DAILY_REVENUE
--
-- ============================================================
-- 1. SNOWFLAKE DATABASE AND SCHEMA CONFIGURATION
-- ============================================================
--
-- OBJECTIVE:
-- Create and configure the Snowflake database and schemas
-- used by the BrewBeats project.
--
-- DATABASE:
-- BREWBEATS_DB stores all BrewBeats project data.
--
-- RAW SCHEMA:
-- RAW stores the original source data.
--
-- DBT_DEV SCHEMA:
-- DBT_DEV stores the models created by dbt.
--
-- IMPORTANT:
-- CREATE DATABASE and CREATE SCHEMA create empty containers.
-- They do not automatically copy or load any data.
--
-- ============================================================


-- ------------------------------------------------------------
-- 1.1. Create the project database
-- ------------------------------------------------------------

CREATE DATABASE IF NOT EXISTS BREWBEATS_DB;


-- ------------------------------------------------------------
-- 1.2. Create the RAW schema
-- ------------------------------------------------------------

CREATE SCHEMA IF NOT EXISTS BREWBEATS_DB.RAW;


-- ------------------------------------------------------------
-- 1.3. Create the dbt output schema
-- ------------------------------------------------------------

CREATE SCHEMA IF NOT EXISTS BREWBEATS_DB.DBT_DEV;


-- ------------------------------------------------------------
-- 1.4. Configure the Snowflake session
-- ------------------------------------------------------------

USE ROLE ACCOUNTADMIN;

USE WAREHOUSE DBT_WH;

USE DATABASE BREWBEATS_DB;

USE SCHEMA DBT_DEV;


-- ------------------------------------------------------------
-- 1.5. Verify created schemas
-- ------------------------------------------------------------

SHOW SCHEMAS IN DATABASE BREWBEATS_DB;


-- ------------------------------------------------------------
-- 1.6. Verify tables and views in DBT_DEV
-- ------------------------------------------------------------

SHOW TABLES IN SCHEMA BREWBEATS_DB.DBT_DEV;

SHOW VIEWS IN SCHEMA BREWBEATS_DB.DBT_DEV;

-- EXPECTED OBJECTS:
-- STG_COFFEE_SALES (VIEW)
-- DAILY_REVENUE (TABLE)
--
-- NOTE:
-- dbt creates the staging view and daily revenue table
-- inside DBT_DEV when dbt run is executed.


-- ============================================================
-- Q1. STAGING MODEL VALIDATION
-- ============================================================
--
-- OBJECTIVE:
-- Verify that the dbt staging model was created successfully
-- and preserves all source records.
--
-- SOURCE:
-- BREWBEATS_DB.RAW.COFFEE_SALES_FROM_STAGE
--
-- DBT FILE:
-- models/staging/stg_coffee_sales.sql
--
-- SNOWFLAKE OBJECT:
-- BREWBEATS_DB.DBT_DEV.STG_COFFEE_SALES
--
-- MATERIALIZATION: VIEW
--
-- TRANSFORMATIONS:
-- 1. Rename columns to descriptive names.
-- 2. Convert columns to appropriate data types.
-- 3. Reference the source using dbt source().
-- 4. Preserve individual transaction records.
--
-- DBT EXECUTION:
-- dbt parse
-- Result: Successful parsing.
--
-- dbt run --select stg_coffee_sales
-- Result: PASS=1, WARN=0, ERROR=0.
--
-- VERIFIED RESULT:
-- RAW ROWS: 3,636
-- STAGING ROWS: 3,636
--
-- ============================================================


-- ------------------------------------------------------------
-- Q1.1. Preview staging data
-- ------------------------------------------------------------

SELECT *
FROM BREWBEATS_DB.DBT_DEV.STG_COFFEE_SALES
LIMIT 10;


-- ------------------------------------------------------------
-- Q1.2. Count staging records
-- ------------------------------------------------------------

SELECT
    COUNT(*) AS STAGING_ROWS
FROM BREWBEATS_DB.DBT_DEV.STG_COFFEE_SALES;


-- ------------------------------------------------------------
-- Q1.3. Compare RAW and staging record counts
-- ------------------------------------------------------------

SELECT
    (SELECT COUNT(*)
     FROM BREWBEATS_DB.RAW.COFFEE_SALES_FROM_STAGE)
        AS RAW_ROWS,

    (SELECT COUNT(*)
     FROM BREWBEATS_DB.DBT_DEV.STG_COFFEE_SALES)
        AS STAGING_ROWS;

-- VERIFIED RESULT:
-- RAW_ROWS = 3,636
-- STAGING_ROWS = 3,636
--
-- CONCLUSION:
-- The staging model preserves all source records.


-- ============================================================
-- Q2. DAILY REVENUE MART VALIDATION
-- ============================================================
--
-- OBJECTIVE:
-- Validate the analytical mart created by dbt.
--
-- DBT FILE:
-- models/marts/daily_revenue.sql
--
-- SNOWFLAKE TABLE:
-- BREWBEATS_DB.DBT_DEV.DAILY_REVENUE
--
-- MATERIALIZATION: TABLE
--
-- TRANSFORMATIONS:
-- 1. Group transactions by transaction_date.
-- 2. Calculate daily revenue using SUM(revenue).
-- 3. Round revenue to two decimal places.
-- 4. Count transactions using COUNT(*).
--
-- DBT EXECUTION:
-- dbt run --select daily_revenue
--
-- VERIFIED RESULT:
-- PASS=1, WARN=0, ERROR=0.
-- DAILY RECORDS: 381
--
-- ============================================================


-- ------------------------------------------------------------
-- Q2.1. Preview the Daily Revenue Mart
-- ------------------------------------------------------------

SELECT *
FROM BREWBEATS_DB.DBT_DEV.DAILY_REVENUE
ORDER BY TRANSACTION_DATE
LIMIT 10;


-- ------------------------------------------------------------
-- Q2.2. Count daily records
-- ------------------------------------------------------------

SELECT
    COUNT(*) AS TOTAL_DAYS
FROM BREWBEATS_DB.DBT_DEV.DAILY_REVENUE;


-- ------------------------------------------------------------
-- Q2.3. Calculate total revenue and transactions
-- ------------------------------------------------------------

SELECT
    ROUND(SUM(TOTAL_REVENUE), 2) AS TOTAL_REVENUE,
    SUM(TOTAL_TRANSACTIONS) AS TOTAL_TRANSACTIONS
FROM BREWBEATS_DB.DBT_DEV.DAILY_REVENUE;

-- VERIFIED RESULTS:
-- TOTAL_REVENUE = 115,431.58
-- TOTAL_TRANSACTIONS = 3,636
--
-- CONCLUSION:
-- The mart contains aggregated revenue and transaction
-- counts for the dataset.


-- ============================================================
-- Q3. DATA QUALITY VALIDATION
-- ============================================================
--
-- OBJECTIVE:
-- Check that the Daily Revenue Mart meets basic
-- data quality requirements.
--
-- DBT FILE:
-- models/marts/schema.yml
--
-- CONFIGURED DBT TESTS:
-- 1. not_null on TRANSACTION_DATE.
-- 2. unique on TRANSACTION_DATE.
-- 3. not_null on TOTAL_REVENUE.
-- 4. not_null on TOTAL_TRANSACTIONS.
--
-- DBT EXECUTION:
-- dbt test --select daily_revenue
--
-- VERIFIED RESULT:
-- PASS=4, WARN=0, ERROR=0.
--
-- NOTE:
-- The following SQL queries are additional manual checks.
-- They do not replace the formal dbt tests.
--
-- ============================================================


-- ------------------------------------------------------------
-- Q3.1. Check NULL values
-- ------------------------------------------------------------

SELECT
    COUNT_IF(TRANSACTION_DATE IS NULL) AS NULL_DATES,
    COUNT_IF(TOTAL_REVENUE IS NULL) AS NULL_REVENUE,
    COUNT_IF(TOTAL_TRANSACTIONS IS NULL) AS NULL_TRANSACTIONS
FROM BREWBEATS_DB.DBT_DEV.DAILY_REVENUE;


-- ------------------------------------------------------------
-- Q3.2. Check duplicate dates
-- ------------------------------------------------------------

SELECT
    TRANSACTION_DATE,
    COUNT(*) AS DATE_COUNT
FROM BREWBEATS_DB.DBT_DEV.DAILY_REVENUE
GROUP BY TRANSACTION_DATE
HAVING COUNT(*) > 1;


-- ------------------------------------------------------------
-- Q3.3. Check invalid business metrics
-- ------------------------------------------------------------

SELECT *
FROM BREWBEATS_DB.DBT_DEV.DAILY_REVENUE
WHERE TOTAL_REVENUE < 0
   OR TOTAL_TRANSACTIONS <= 0;


-- ============================================================
-- Q4. AIRFLOW PIPELINE STATUS
-- ============================================================
--
-- OBJECTIVE:
-- Automate dbt model execution and data quality tests.
--
-- PYTHON FILE:
-- airflow/dags/brewbeats_dag.py
--
-- DAG ID:
-- brewbeats_pipeline
--
-- SCHEDULE:
-- @daily
--
-- IMPLEMENTED TASKS:
--
-- 1. run_dbt_models
--    Executes:
--    dbt run --select stg_coffee_sales daily_revenue
--
-- 2. test_dbt_models
--    Executes:
--    dbt test --select daily_revenue
--
-- TASK DEPENDENCY:
-- run_dbt_models >> test_dbt_models
--
-- VERIFIED AIRFLOW RESULT:
-- run_dbt_models: SUCCESS
-- test_dbt_models: SUCCESS
--
-- Both tasks completed successfully during a manual DAG run.
--
-- IMPORTANT:
-- The daily schedule is configured, but a scheduled daily
-- execution has not yet been confirmed.
--
-- ADDITIONAL PLANNED TASK:
-- check_mart_data
--
-- PURPOSE:
-- A Python task to connect to Snowflake and validate
-- the Daily Revenue Mart.
--
-- STATUS:
-- Not implemented yet.
--
-- NOTE:
-- Airflow tasks are defined and executed in Python.
-- This section documents the pipeline; it does not execute
-- Airflow tasks in Snowflake.
--
-- ============================================================


-- ============================================================
-- Q5. FINAL MART DATA VALIDATION
-- ============================================================
--
-- OBJECTIVE:
-- Perform additional checks on the final Daily Revenue Mart.
--
-- These SQL checks will help us design the additional
-- Airflow task: check_mart_data.
--
-- CHECKS:
-- 1. Verify that the mart contains records.
-- 2. Find the latest transaction date.
-- 3. Validate the main business metrics.
-- 4. Check basic data quality conditions.
--
-- ============================================================


-- ------------------------------------------------------------
-- Q5.1. Check whether the mart contains data
-- ------------------------------------------------------------

SELECT
    COUNT(*) AS TOTAL_ROWS
FROM BREWBEATS_DB.DBT_DEV.DAILY_REVENUE;

-- EXPECTED RESULT:
-- TOTAL_ROWS = 381
--
-- PURPOSE:
-- Verify that the mart is not empty.


-- ------------------------------------------------------------
-- Q5.2. Check the latest available transaction date
-- ------------------------------------------------------------

SELECT
    MAX(TRANSACTION_DATE) AS LATEST_TRANSACTION_DATE
FROM BREWBEATS_DB.DBT_DEV.DAILY_REVENUE;

-- EXPECTED RESULT:
-- LATEST_TRANSACTION_DATE = 2025-03-23
--
-- IMPORTANT:
-- The dataset contains historical transactions.
-- We check the latest available date rather than comparing
-- it with the current calendar date.


-- ------------------------------------------------------------
-- Q5.3. Validate the mart summary
-- ------------------------------------------------------------

SELECT
    COUNT(*) AS TOTAL_DAYS,
    SUM(TOTAL_TRANSACTIONS) AS TOTAL_TRANSACTIONS,
    ROUND(SUM(TOTAL_REVENUE), 2) AS TOTAL_REVENUE,
    MIN(TRANSACTION_DATE) AS FIRST_TRANSACTION_DATE,
    MAX(TRANSACTION_DATE) AS LATEST_TRANSACTION_DATE
FROM BREWBEATS_DB.DBT_DEV.DAILY_REVENUE;

-- EXPECTED RESULTS:
-- TOTAL_DAYS = 381
-- TOTAL_TRANSACTIONS = 3,636
-- TOTAL_REVENUE = 115,431.58
-- FIRST_TRANSACTION_DATE = 2024-03-01
-- LATEST_TRANSACTION_DATE = 2025-03-23


-- ------------------------------------------------------------
-- Q5.4. Check basic mart validation conditions
-- ------------------------------------------------------------

SELECT
    CASE
        WHEN COUNT(*) > 0
         AND COUNT_IF(TRANSACTION_DATE IS NULL) = 0
         AND COUNT_IF(TOTAL_REVENUE IS NULL) = 0
         AND COUNT_IF(TOTAL_TRANSACTIONS IS NULL) = 0
         AND COUNT_IF(TOTAL_TRANSACTIONS <= 0) = 0
         AND COUNT_IF(TOTAL_REVENUE < 0) = 0
        THEN 'PASS'
        ELSE 'FAIL'
    END AS VALIDATION_STATUS
FROM BREWBEATS_DB.DBT_DEV.DAILY_REVENUE;

-- EXPECTED RESULT:
-- VALIDATION_STATUS = PASS
--
-- NOTE:
-- This is a manual Snowflake validation for now.
-- We will later use the same logic in an Airflow task.
--
-- Q5 STATUS:
-- SQL checks prepared.
-- Execution and results still need to be confirmed.


-- ============================================================
-- FINAL SECTION D VALIDATION SUMMARY
-- ============================================================
--
-- Q1. STAGING MODEL:
-- Status: COMPLETED
-- RAW SOURCE ROWS: 3,636
-- STAGING VIEW ROWS: 3,636
--
-- Q2. DAILY REVENUE MART:
-- Status: COMPLETED
-- DAILY MART RECORDS: 381
-- TOTAL REVENUE: 115,431.58
-- TOTAL TRANSACTIONS: 3,636
--
-- Q3. DATA QUALITY:
-- Status: COMPLETED
-- DBT TESTS: 4 PASSED
-- PASS=4, WARN=0, ERROR=0
--
-- Q4. AIRFLOW PIPELINE:
-- Status: TWO TASKS IMPLEMENTED AND MANUALLY TESTED
-- run_dbt_models: SUCCESS
-- test_dbt_models: SUCCESS
--
-- Q5. FINAL MART DATA VALIDATION:
-- Status: SQL CHECKS PREPARED
-- EXECUTION AND RESULTS: PENDING
--
-- REMAINING WORK:
-- 1. Execute and verify Q5 SQL checks in Snowflake.
-- 2. Implement the direct Snowflake validation task in Airflow.
-- 3. Test the complete three-task pipeline.
--
-- ============================================================
-- END OF SECTION D SNOWFLAKE VALIDATION WORKSHEET
-- ============================================================
