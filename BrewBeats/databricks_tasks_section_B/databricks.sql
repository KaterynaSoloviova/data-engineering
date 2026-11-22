-- =========================================
-- Section B: SQL on Databricks
-- Project: BrewBeats
-- =========================================

-- 1. DATBRICKS SETUP AND DATA PREPARATION

-- Step 1: Create a schema for the BrewBeats project
CREATE SCHEMA IF NOT EXISTS workspace.brewbeats;

-- Step 2: Upload coffee_sales.csv using the
-- Databricks "Add or upload data" interface.

-- Step 3: Create a table named coffee_sales
-- in the workspace.brewbeats schema.
-- The first row of the CSV was used as column headers.

-- Step 4: Preview the uploaded data
SELECT *
FROM workspace.brewbeats.coffee_sales
LIMIT 10;

-- 2. SQL ANALYSIS

-- Q1: Find the top 5 best-selling coffee types by revenue

SELECT
    coffee_name,
    ROUND(SUM(money), 2) AS total_revenue
FROM workspace.brewbeats.coffee_sales
GROUP BY coffee_name
ORDER BY total_revenue DESC
LIMIT 5;

-- Q2: Calculate total revenue by payment type

SELECT 
  cash_type,
  ROUND(SUM(money), 2) AS total_revenue
FROM workspace.brewbeats.coffee_sales
GROUP BY cash_type
ORDER BY total_revenue DESC;

-- Q3: Calculate monthly revenue using a CTE

WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('MONTH', date) AS month,
        ROUND(SUM(money), 2) AS total_revenue
    FROM workspace.brewbeats.coffee_sales
    GROUP BY DATE_TRUNC('MONTH', date)
)

SELECT
    month,
    total_revenue
FROM monthly_revenue
ORDER BY month;

-- Q4: Find the day with the highest number of transactions

SELECT
    date,
    COUNT(*) AS total_transactions
FROM workspace.brewbeats.coffee_sales
GROUP BY date
ORDER BY total_transactions DESC
LIMIT 1;