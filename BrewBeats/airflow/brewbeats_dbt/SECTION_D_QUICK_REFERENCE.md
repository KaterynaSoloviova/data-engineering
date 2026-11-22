# Section D — dbt + Airflow Quick Reference

## 1. Project Goal
The goal of Section D is to build a data transformation pipeline using **dbt, Snowflake, and Airflow**.

The pipeline:
1. Reads raw coffee sales data from Snowflake.
2. Prepares and transforms the data using dbt.
3. Creates a daily revenue table.
4. Checks data quality.
5. Uses Airflow to run the dbt models and tests.

## 2. Technologies
| Technology | Purpose |
|---|---|
| Snowflake | Stores the raw and transformed data |
| dbt | Transforms data using SQL and tests the results |
| Airflow | Runs and manages the pipeline |
| Python | Defines the Airflow DAG |

## 3. Important Files
| File | Purpose |
|---|---|
| `dbt_project.yml` | Main dbt project settings |
| `_sources.yml` | Tells dbt where the raw data is in Snowflake |
| `stg_coffee_sales.sql` | Prepares raw coffee sales data |
| `daily_revenue.sql` | Calculates daily revenue and transaction count |
| `schema.yml` | Describes the model and checks data quality |
| `brewbeats_dag.py` | Defines the Airflow pipeline |

## 4. Q1 — Create a Staging Model
**Goal:** Prepare raw coffee sales data for further transformations.

**What I did**: 
- Created `stg_coffee_sales.sql`.
- Read data from
`BREWBEATS_DB.RAW.COFFEE_SALES_FROM_STAGE`.
- Renamed columns and
converted data types.
- Used source() to reference the raw data source.

It:
- Renames columns.
- Converts data types.
- Makes the data easier to use in other models.

**SQL:**
```sql
SELECT
    DATE::DATE AS transaction_date,
    DATETIME::TIMESTAMP_NTZ AS transaction_timestamp,
    CASH_TYPE AS cash_type,
    CARD AS card,
    MONEY::NUMBER(10, 2) AS revenue,
    COFFEE_NAME AS coffee_name
FROM {{ source('raw', 'coffee_sales') }}
```
**Why**: The staging model standardizes raw data and makes it easier to
use in later models

**Result:**
- Model created: `STG_COFFEE_SALES`
- Snowflake location: `BREWBEATS_DB.DBT_DEV`
- Materialization: View
- Raw data rows: 3,636
- Staging model rows: 3,636

The staging model contains the same number of rows as the source, but with clearer column names and data types.

## 5. Q2 — Create a Daily Revenue Mart
**Goal:** Calculate total revenue and the number of transactions for each day.
The model uses the staging model as its input.

**What I did**:
- Created `daily_revenue.sql`.
- Used
`ref('stg_coffee_sales')` to read from the staging model.
- Grouped
transactions by date.
- Calculated daily revenue and transaction
count.
- Materialized the result as a table.

**SQL:**
```sql
{{ config(materialized='table') }}

SELECT
    transaction_date,
    ROUND(SUM(revenue), 2) AS total_revenue,
    COUNT(*) AS total_transactions
FROM {{ ref('stg_coffee_sales') }}
GROUP BY transaction_date
```
**Why**: The mart provides a simple daily summary that can be used for
reporting and analysis.

**Result:**
- Model created: `DAILY_REVENUE`
- Snowflake location: `BREWBEATS_DB.DBT_DEV`
- Materialization: Table
- Daily records: 381
- Total revenue: 115,431.58
- Total transactions: 3,636
- Date range: 2024-03-01 to 2025-03-23

The mart contains one record per transaction date.

**Why a table?**
The staging model is an intermediate layer, so a view is suitable. The
daily revenue mart is a prepared analytical result, so I stored it as a
table.

## 6. Q3 — Add Data Quality Tests

**Goal:** Check that the daily revenue data is reliable.

**What I did**:
Added four generic tests in `schema.yml`.

```yaml
version: 2

models:
  - name: daily_revenue
    description: "Daily coffee sales revenue and transaction summary."
    columns:
      - name: transaction_date
        description: "Date of the coffee sales transactions."
        tests:
          - not_null
          - unique

      - name: total_revenue
        description: "Total revenue generated on each day."
        tests:
          - not_null

      - name: total_transactions
        description: "Number of transactions recorded on each day."
        tests:
          - not_null
```

**Tests used:**
| Test | What it checks |
|---|---|
| `not_null` | The column does not contain NULL values |
| `unique` | Every value in the column is unique |

**Result:**

<badge color="success">All 4 tests passed</badge>
- PASS: 4
- WARN: 0
- ERROR: 0

The tests confirmed that:
- Every transaction date is unique.
- Required values are not NULL.

## 7. Q4 — Create an Airflow DAG
**Goal:** Automate the dbt models and tests using Airflow.

**What I did**:
- Created `airflow/dags/brewbeats_dag.py`.
- Defined a DAG named `brewbeats_pipeline`.
- Used `BashOperator` to run dbt
commands.
- Set the schedule to @daily.
- Set `catchup=False` to prevent automatic runs for past scheduled dates.

**Why**: Airflow manages task execution, dependencies, scheduling, and
monitoring in one workflow.

It contains two tasks:
| Task | Action |
|---|---|
| `run_dbt_models` | Runs the staging and daily revenue models |
| `test_dbt_models` | Runs data quality tests on the daily revenue model |

**Task order:**
```python
run_dbt_models >> test_dbt_models >> check_mart_data
```
This means that the tests run only after the dbt models have finished successfully.

**Schedule:**
```python
schedule="@daily"
```

This tells Airflow to schedule the DAG once per day.

**Result:**
- DAG created successfully.
- DAG loaded in the Airflow UI.
- DAG was triggered manually.
- `run_dbt_models`: Success.
- `test_dbt_models`: Success.

Both tasks completed successfully during the manual test.
Note: The daily schedule is configured, but a scheduled daily run has not yet been confirmed.

## 8. Q5 — Check the Mart Data
**Goal:** Add an additional check to verify the data in the `DAILY_REVENUE` table.

Planned approach:
- Connect Airflow to Snowflake.
- Read the latest transaction date from `DAILY_REVENUE`.
- Check that the mart contains data.

**What I did**:
- Created `tests/check_mart_data.sql`.
- Used `CURRENT_DATE()` to get today's date.
- Used NOT EXISTS to check whether that date is present in the mart.
- Added a third Airflow task named check_mart_data.

```sql
-- Fail the test if the mart table has no records for today

SELECT
    CURRENT_DATE() AS missing_transaction_date
WHERE NOT EXISTS (
    SELECT 1
    FROM {{ ref('daily_revenue') }}
    WHERE transaction_date = CURRENT_DATE()
)
```
**How the test works**:
- If today's date exists in the mart, the query returns zero rows and the test passes.
- If today's date is missing, the query returns one row and the test fails.

**Why**: This check validates data freshness, not just data structure or
completeness.

**Execution result**:
Airflow task Result Explanation:

run_dbt_models    PASS     Both dbt models ran successfully
test_dbt_models   PASS     All four generic tests passed
check_mart_data   FAIL     No record exists for the current date

**Why did the final test fail?**
The source dataset contains records from 2024-03-01 to 2025-03-23.
The current date at the time of the test was 2026-11-20. Therefore,
the mart has no record for today.

This is an expected validation failure: the test correctly detected that
the dataset is not up to date. The overall Airflow DAG run is marked
Failed because its final task failed, even though the first two
tasks succeeded.

## 9. Pipeline Flow
```text
Snowflake RAW data
        |
        v
dbt: stg_coffee_sales
        |
        v
dbt: daily_revenue
        |
        v
dbt generic data quality tests
        |
        v
Airflow: brewbeats_pipeline
        |
        v
check_mart_data
        |
        v
Check for records dated today
```

## 10. Important Concepts — Quick Answers
**What is dbt?**
dbt is a tool that transforms data using SQL.

**What is a staging model?**
A staging model prepares raw data by renaming columns and converting data types.

**What is a mart?**
A mart is a table prepared for reporting and analysis.

**What is materialization?**
Materialization defines how dbt creates a model in the database.
- View: Stores the SQL query, not a separate physical copy of the result.
- Table: Stores the query result as a database table.

**What is `source()`?**
`source()` tells dbt to read data from a source defined in `_sources.yml`.

**What is `ref()`?**
`ref()` connects one dbt model to another and creates a dependency between them.

**What is a data quality test?**
A test checks whether the data meets certain rules, such as having no NULL values or duplicate dates.

**What is Airflow?**
Airflow schedules, runs, and monitors workflows.

**What is a DAG?**
A DAG (Directed Acyclic Graph) defines tasks and their execution order.

**What does `@daily` mean?**
It tells Airflow to schedule the DAG once per day.

## 11. Final Progress Summary
| Task | Status | Result |
|---|---|---|
| Q1 — Staging model | Completed | 3,636 rows |
| Q2 — Daily revenue mart | Completed | 381 daily records |
| Q3 — Data quality tests | Completed | 4 tests passed |
| Q4 — Airflow DAG | Completed and manually tested | Both tasks successful |
| Q5 — Mart data check | Pending | Not implemented yet |

**Main results:**
- Raw coffee sales data: 3,636 rows.
- Staging model: 3,636 rows.
- Daily revenue mart: 381 records.
- Total revenue: 115,431.58.
- Total transactions: 3,636.
- dbt data quality tests: 4 passed.
- Airflow manual run: 2 tasks successful.

**Conclusion:**
The main BrewBeats dbt and Airflow pipeline has been created and successfully tested. The staging model, daily revenue mart, data quality tests, and two Airflow tasks are working. The additional mart data check is still pending.