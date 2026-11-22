# BrewBeats — Project Journal
# Section D: dbt + Airflow

## 1. Project Overview
### 1.1. Project Objective

The objective of this section is to build an automated data transformation pipeline using dbt and Apache Airflow, with Snowflake as the cloud data warehouse.

The pipeline takes raw coffee sales data stored in Snowflake, transforms it into structured analytical models using dbt, validates data quality, and orchestrates the workflow using Airflow.

The final objective is to create a reliable and repeatable process that can run automatically on a daily schedule.

### 1.2. Technologies Used
| Technology | Purpose |
|---|---|
| Snowflake | Cloud data warehouse used to store raw and transformed data |
| dbt Core | SQL-based data transformation and data modeling |
| dbt Snowflake Adapter | Connects dbt to Snowflake |
| Apache Airflow | Workflow orchestration and task scheduling |
| SQL | Data querying, transformation and validation |
| Python | Pipeline configuration and automation |
| YAML | dbt project configuration and data quality test definitions |

### 1.3. General Data Architecture

```text
coffee_sales.csv
       |
       v
Snowflake RAW schema
       |
       v
dbt Source Definition
       |
       v
Staging Model
stg_coffee_sales
       |
       v
Daily Revenue Mart
daily_revenue
       |
       v
dbt Data Quality Tests
       |
       v
Airflow DAG
       |
       v
Automated Pipeline Validation
```

### 1.4. How the Technologies Work Together

Each technology has a different responsibility:

- Snowflake stores the source data and the transformed analytical tables.
- dbt defines how raw data should be transformed into useful analytical models.
- SQL performs the actual transformations.
- YAML describes sources, models and data quality tests.
- Airflow controls the order in which the pipeline tasks are executed and schedules them.

**Important distinction:**

dbt performs the data transformations, while Airflow orchestrates when and in what order those transformations and tests run.

Airflow does not replace dbt, and dbt does not replace Snowflake.

---

## 2. Environment Setup
### 2.1. Understanding Python Virtual Environments

Two separate Python virtual environments were created for this project.
A virtual environment isolates Python packages and dependencies. This means that installing a library in one environment does not automatically make it available in another.

#### Environment 1: dbt
Location:
`data-engineering/.venv`

Purpose:
- Run dbt commands.
- Connect dbt to Snowflake.
- Execute dbt models and tests.

Creation:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
Installation:
```bash
python -m pip install dbt-snowflake
```
Verification:
```bash
dbt --version
```
Installed components:
- dbt Core
- Snowflake adapter

#### Environment 2: Airflow
Location:
`BrewBeats/airflow/airflow_venv`
Purpose:
- Run Apache Airflow.
- Load and execute DAGs.
- Run Python and Bash tasks.
- Use the Snowflake Python Connector for direct Snowflake communication.

Creation:
```bash
cd BrewBeats/airflow

python3 -m venv airflow_venv
source airflow_venv/bin/activate
```
Airflow installation:
```bash
pip install "apache-airflow==3.4.0" \
  --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.4.0/constraints-3.13.txt"
```

Verification:
```bash
airflow version
```
Expected version:
`3.4.0`
Snowflake Connector installation:
```bash
python -m pip install snowflake-connector-python
```
Verification:
```bash
python -c "import snowflake.connector; print(snowflake.connector.__version__)"
```
Verified version:
`5.2.0`

**Why are two environments necessary?**
The environments keep the dependencies of dbt and Airflow separate. Both tools can use different Python packages without interfering with each other.
The Airflow DAG calls the dbt executable using its absolute path, so Airflow can execute dbt even though dbt is installed in a different virtual environment.

### 2.2. dbt Project Structure

Project location:
`BrewBeats/airflow/brewbeats_dbt`

```text
brewbeats_dbt/
│
├── dbt_project.yml
│
├── models/
│   ├── staging/
│   │   ├── _sources.yml
│   │   └── stg_coffee_sales.sql
│   │
│   └── marts/
│       ├── daily_revenue.sql
│       └── schema.yml
│
└── tests/
    └── check_mart_data.sql
```

Important files:

- `dbt_project.yml` — the main file with dbt project settings.
- `_sources.yml` — tells dbt where to find the raw data in Snowflake.
- `stg_coffee_sales.sql` — prepares and cleans the raw coffee sales data(transformations).
- `daily_revenue.sql` — calculates daily revenue and the number of transactions.
- `schema.yml` — describes the daily revenue model and checks data quality.
- `check_mart_data.sql`- checks whether the daily revenue mart contains records for the current date.

### 2.3. Snowflake Connection Configuration
dbt connection settings are stored outside the project in:
`~/.dbt/profiles.yml`
The profile name must match the profile specified in `dbt_project.yml`.
Configuration structure:

```yaml
brewbeats_dbt:
  outputs:
    dev:
      account: <SNOWFLAKE_ACCOUNT>
      authenticator: OAUTH_AUTHORIZATION_CODE
      database: BREWBEATS_DB
      role: ACCOUNTADMIN
      schema: DBT_DEV
      threads: 1
      type: snowflake
      user: <SNOWFLAKE_USER>
      warehouse: DBT_WH
  target: dev
```

Explanation:

- `brewbeats_dbt` — profile name used by the dbt project.
- `outputs` — available connection configurations.
- `dev` — development environment configuration.
- `account` — Snowflake account identifier.
- `authenticator` — authentication method. OAuth Authorization Code was used with Google authentication.
- `database` — target Snowflake database.
- `role` — Snowflake role used for permissions.
- `schema` — default schema for dbt-generated models.
- `threads` — number of concurrent dbt execution threads.
- `type` — dbt adapter type.
- `user` — Snowflake username.
- `warehouse` — Snowflake virtual warehouse used for computation.
- `target` — tells dbt which output configuration to use by default.

**Security note:**
The actual account and username values are stored in the local profile. Credentials and tokens should not be committed to GitHub or included in the project journal.

### 2.4. Testing the dbt Connection
Command:
```bash
dbt debug
```
Purpose:
`dbt debug` checks whether dbt can find and read its configuration files and establish a connection to Snowflake.

It verifies:
- The dbt project configuration.
- The profiles configuration.
- The Snowflake adapter.
- The connection settings.
- The actual connection to Snowflake.

**Execution result:**
- profiles.yml: OK
- dbt_project.yml: OK
- Snowflake connection: OK
- All checks passed.
This confirmed that dbt could successfully connect to Snowflake.

---

## 3. Snowflake Data Architecture for dbt

### 3.1. Database and Schema Organization

Database:

`BREWBEATS_DB`
Two schemas are relevant to this section:

| Schema | Purpose |
|---|---|
| RAW | Stores original source tables and raw data |
| DBT_DEV | Stores dbt-generated models |

Source table:
`BREWBEATS_DB.RAW.COFFEE_SALES_FROM_STAGE`

Staging model:
`BREWBEATS_DB.DBT_DEV.STG_COFFEE_SALES`

Mart:
`BREWBEATS_DB.DBT_DEV.DAILY_REVENUE`

### 3.2. Why Use Separate RAW and DBT_DEV Schemas?
The RAW schema preserves the original source data.
The DBT_DEV schema contains transformed data generated by dbt.
This separation is useful because:

- Original source data remains unchanged.
- Transformations can be developed independently.
- Staging and analytical models are easier to organize.
- The data lineage is easier to understand.
- The original data can be used again if transformations need to be modified.

### 3.3. What Is dbt?
dbt stands for Data Build Tool.

It is used to transform data that already exists inside a data warehouse.
Instead of extracting data into Python and transforming it outside the warehouse, dbt sends SQL statements to Snowflake, where the transformations are executed.
dbt helps organize SQL transformations into reusable models with clear dependencies.
A dbt model is usually a SQL file that defines a query.

For example:
`stg_coffee_sales.sql`

defines how raw coffee sales data should be transformed.
When dbt executes the model, it creates the corresponding database object in Snowflake.
---

## 4. Staging Model

### 4.1. Objective

The purpose of the staging model is to prepare raw coffee sales data for further analysis.

The staging model:

- Selects the required source columns.
- Renames columns to make them easier to understand.
- Explicitly defines data types.
- Creates a clean and consistent structure.
- Keeps the original RAW table unchanged.

The staging model does not aggregate the data. It prepares individual transaction records for downstream transformations.

### 4.2. Source Configuration
File:
`models/staging/_sources.yml`

Code:

```yaml
version: 2

sources:
  - name: raw
    database: BREWBEATS_DB
    schema: RAW
    tables:
      - name: coffee_sales
        identifier: COFFEE_SALES_FROM_STAGE
```

Explanation:

- `version: 2` — version of the dbt properties file format.
- `sources` — declares external data sources available to dbt.
- `name: raw` — logical source name inside dbt.
- `database` — Snowflake database containing the source.
- `schema` — Snowflake schema containing the source table.
- `tables` — lists the tables available within this source.
- `name: coffee_sales` — logical table name used by dbt.
- `identifier` — actual physical table name in Snowflake.

**Important distinction:**
`coffee_sales` is the logical name used inside dbt.
`COFFEE_SALES_FROM_STAGE` is the actual table name in Snowflake.
The `source()` function connects the dbt model to this source definition.

### 4.3. Staging SQL Model
File:
`models/staging/stg_coffee_sales.sql`

Code:
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

Detailed explanation:
**SELECT**
Specifies which columns should be included in the output.

**DATE::DATE AS transaction_date**
- `DATE` is the original source column.
- `::DATE` explicitly casts the value to the DATE data type.
- `AS transaction_date` renames the column.

**DATETIME::TIMESTAMP_NTZ AS transaction_timestamp**
- Converts the original datetime value to a Snowflake timestamp without timezone information.
- `TIMESTAMP_NTZ` means timestamp without time zone.

**CASH_TYPE AS cash_type**
Renames the payment type column.

**CARD AS card**
Keeps the card information under a lowercase column name.

**MONEY::NUMBER(10, 2) AS revenue**
- Converts the original money value to a numeric data type.
- `NUMBER(10, 2)` allows up to 10 digits in total, including 2 digits after the decimal point.
- `revenue` is a more descriptive name for the financial value.

**COFFEE_NAME AS coffee_name**
Renames the coffee product column.

**FROM {{ source('raw', 'coffee_sales') }}**
This is a dbt Jinja expression.
It tells dbt to retrieve data from the source declared in `_sources.yml`.
dbt resolves the expression into the fully qualified Snowflake source table.

### 4.4. Understanding dbt Materialization

A materialization defines how dbt creates a model in the database.

Common materializations:
| Materialization | Meaning |
|---|---|
| view | Creates a database view |
| table | Creates a physical database table |
| incremental | Updates a table using new or changed data |
| ephemeral | Does not create a separate database object; its SQL is incorporated into downstream models |

Our staging model uses the default view materialization.
This means Snowflake stores the view definition rather than a separate copy of all the transformed rows.

### 4.5. Parsing the dbt Project
Command:

```bash
dbt parse
```

Purpose:
Parse the dbt project and check whether its structure, YAML configuration, and model references can be interpreted.
Parsing does not execute the SQL transformations in Snowflake.

**Execution result:**
Parsing completed successfully.

### 4.6. Executing the Staging Model

Command:
```bash
dbt run --select stg_coffee_sales
```

Explanation:
- `dbt run` executes dbt models.
- `--select` limits execution to selected models.
- `stg_coffee_sales` is the model we want to execute.

**Execution result:**
```text
1 of 1 OK created sql view model DBT_DEV.stg_coffee_sales

Completed successfully
PASS=1
WARN=0
ERROR=0
SKIP=0
TOTAL=1
```
**Result:**
Successfully created the Snowflake view:
`BREWBEATS_DB.DBT_DEV.STG_COFFEE_SALES`
Materialization:
`VIEW`

### 4.7. Staging Model Validation
The staging model was checked in Snowsight.
Row count query:
```sql
SELECT
    COUNT(*) AS TOTAL_ROWS
FROM BREWBEATS_DB.DBT_DEV.STG_COFFEE_SALES;
```

The number of rows was also compared with the original RAW table.

**Validation results:**
| Table | Rows |
|---|---:|
| RAW.COFFEE_SALES_FROM_STAGE | 3,636 |
| DBT_DEV.STG_COFFEE_SALES | 3,636 |

**Validation status: SUCCESS**
The staging model contains the same number of records as the source table.
This confirms that the staging transformation preserved all 3,636 transaction records.

---

## 5. Daily Revenue Mart
### 5.1. Objective
The purpose of the Daily Revenue Mart is to transform individual coffee sales transactions into daily business metrics.

Instead of analyzing thousands of individual transactions every time, the mart stores aggregated results for each transaction date.

This makes the data easier to use for reporting and business intelligence.

### 5.2. Model Information
File:
`models/marts/daily_revenue.sql`

Snowflake table:
`BREWBEATS_DB.DBT_DEV.DAILY_REVENUE`

Materialization:
`TABLE`

### 5.3. SQL Model

Code:

```sql
-- Configure dbt to create a physical table in Snowflake
{{ config(materialized='table') }}

-- Calculate daily revenue and transaction count
SELECT
    transaction_date,

    -- Calculate total revenue for each day
    ROUND(SUM(revenue), 2) AS total_revenue,

    -- Count the number of transactions for each day
    COUNT(*) AS total_transactions

FROM {{ ref('stg_coffee_sales') }}

-- Group transactions by date
GROUP BY transaction_date
```

Detailed explanation:
**{{ config(materialized='table') }}**

Tells dbt to create a physical table in Snowflake.
Unlike a view, a table stores the result of the transformation.

**SELECT transaction_date**
Selects the date that will be used to group the sales.

**SUM(revenue)**
Adds all transaction revenue values for each date.

**ROUND(..., 2)**
Rounds the calculated revenue to two decimal places.

**AS total_revenue**
Gives the calculated column a descriptive name.

**COUNT(*)**
Counts the number of rows in each group.

Since one row in the source represents one transaction, this calculates the number of transactions per date.

**AS total_transactions**
Names the calculated transaction count.

**FROM {{ ref('stg_coffee_sales') }}**
The `ref()` function references another dbt model.
Here, it references the staging model.
dbt uses `ref()` to understand dependencies between models and determine their execution order.

**GROUP BY transaction_date**
Groups all transactions belonging to the same date.

The result contains one record per transaction date.

### 5.4. Why Use a Mart?

A mart is an analytical model prepared for a specific reporting or business purpose.
In our project:
- Staging contains cleaned individual transactions.
- Daily Revenue Mart contains daily aggregated metrics.

The mart is easier for reporting tools to consume because the calculations have already been performed.

### 5.5. Executing the Mart
Command:
```bash
dbt run --select daily_revenue
```

**Execution result:**
- PASS: 1
- WARN: 0
- ERROR: 0
- Rows created: 381

The table was successfully created in Snowflake.

### 5.6. Snowflake Validation
The mart was checked directly in Snowsight.
Validation query:
```sql
SELECT
    ROUND(SUM(TOTAL_REVENUE), 2) AS TOTAL_REVENUE,
    SUM(TOTAL_TRANSACTIONS) AS TOTAL_TRANSACTIONS
FROM BREWBEATS_DB.DBT_DEV.DAILY_REVENUE;
```

Results:
| Metric | Result |
|---|---:|
| Total revenue | 115,431.58 |
| Total transactions | 3,636 |
| Daily records | 381 |

Additional date validation:
```sql
SELECT
    MIN(TRANSACTION_DATE) AS FIRST_TRANSACTION_DATE,
    MAX(TRANSACTION_DATE) AS LATEST_TRANSACTION_DATE,
    COUNT(*) AS TOTAL_DAYS
FROM BREWBEATS_DB.DBT_DEV.DAILY_REVENUE;
```

Results:
| Metric | Result |
|---|---|
| First transaction date | 2024-03-01 |
| Latest transaction date | 2025-03-23 |
| Total days | 381 |

**Validation status: SUCCESS**
The daily mart successfully aggregates all 3,636 transactions into 381 daily records.
The total revenue and transaction count match the source dataset.

---

## 6. Data Quality Tests

### 6.1. Objective
Data quality tests verify that transformed data meets basic expectations before it is used for reporting.
A successful model execution does not automatically mean that the resulting data is correct.
For example, a model may execute without SQL errors but still contain missing values or duplicate dates.
dbt provides built-in tests to identify these problems.

### 6.2. Test Configuration
File:
`models/marts/schema.yml`

Code:
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

Explanation:
- `version: 2` — dbt properties file format version.
- `models` — describes dbt models.
- `name: daily_revenue` — identifies the model.
- `description` — explains the purpose of the model.
- `columns` — lists the columns to document and test.
- `tests` — defines data quality checks.

### 6.3. Understanding the Tests

**not_null**
Checks that a column does not contain NULL values.

For example:
`not_null` on `total_revenue` ensures that every daily record has a revenue value.

**unique**
Checks that every value in the selected column is unique.

For `transaction_date`, this ensures that the mart contains only one record per date.
This is important because the mart is designed to contain one aggregated row for each transaction date.

### 6.4. Configured Tests
| Column | Test | Purpose |
|---|---|---|
| transaction_date | not_null | Dates must not be missing |
| transaction_date | unique | Each date must appear only once |
| total_revenue | not_null | Daily revenue must not be missing |
| total_transactions | not_null | Transaction counts must not be missing |

Total configured tests: 4.

### 6.5. Executing Data Quality Tests
Command:

```bash
dbt test --select daily_revenue
```

Explanation:
- `dbt test` executes the configured data quality tests.
- `--select daily_revenue` selects tests associated with the daily revenue model.

**Execution result:**

```text
PASS=4
WARN=0
ERROR=0
SKIP=0
TOTAL=4
```

**Validation status: SUCCESS**

All four tests passed.

This confirms that:
- The tested columns contain no NULL values.
- Every transaction date is unique.
- The daily revenue mart meets the configured data quality requirements.

**Important distinction:**
`dbt run` builds models.
`dbt test` checks the data quality of those models.
They are separate operations.

---

## 7. Apache Airflow Setup
### 7.1. What Is Apache Airflow?

Apache Airflow is a workflow orchestration platform.
It allows data engineers to define, schedule, monitor and manage workflows.
A workflow is represented by a DAG.
DAG stands for Directed Acyclic Graph.
- Directed means tasks have a defined execution direction.
- Acyclic means the dependency structure does not contain circular loops.
- Graph means the workflow consists of tasks connected by dependencies.

Airflow controls when tasks execute and what must finish before the next task can start.

### 7.2. Why Do We Need Airflow?
Before Airflow, dbt commands had to be executed manually in the terminal.
Airflow allows us to automate these operations.
For BrewBeats, Airflow is responsible for:

- Starting the dbt transformation process.
- Running data quality tests after transformations.
- Monitoring task execution.
- Scheduling the workflow.
- Showing successful and failed tasks in the web interface.

### 7.3. Airflow Environment

Installed version:
`Apache Airflow 3.4.0`

Python version:
`3.13.4`

Virtual environment:
`BrewBeats/airflow/airflow_venv`

Airflow home:
`BrewBeats/airflow/airflow_home`

DAG folder:
`BrewBeats/airflow/dags`

Metadata database:
`SQLite`

### 7.4. Airflow Metadata Database
Airflow uses a metadata database to store information about workflow execution.
In this project, SQLite is used for local development.
The metadata database stores information such as:
- DAG definitions and execution metadata.
- DAG runs.
- Task execution states.
- Scheduling information.
- Other Airflow operational metadata.

The metadata database is separate from our business data in Snowflake.

**Important distinction:**
Snowflake stores BrewBeats coffee sales data and analytical models.
SQLite stores Airflow's operational metadata.
SQLite is not used as the analytical data warehouse in this project.

### 7.5. Initializing Airflow
Created folders:
```bash
mkdir -p dags airflow_home
```

Set the Airflow environment variables:
```bash
export AIRFLOW_HOME="$PWD/airflow_home"
export AIRFLOW__CORE__DAGS_FOLDER="$PWD/dags"
```

Explanation:
- `AIRFLOW_HOME` defines where Airflow stores its local configuration, metadata database and other files.
- `AIRFLOW__CORE__DAGS_FOLDER` defines where Airflow looks for DAG files.

Initialized the metadata database:
```bash
airflow db migrate
```

Execution result:
```text
Airflow database tables created
Database migration done!
```
This created the local Airflow metadata database.

### 7.6. Starting Airflow
Command:

```bash
airflow standalone
```
This command starts the local Airflow components required for development.
The Airflow web interface is available at:
`http://localhost:8080`
The standalone command is intended for local development and testing.

### 7.7. First Airflow Test
Initially, a simple test DAG was created to confirm that Airflow could:

- Discover a Python DAG file.
- Display the DAG in the web interface.
- Execute a Python task.
- Record its execution status.

The test task was called `say_hello`.
It was successfully executed and received the `SUCCESS` status.
This confirmed that the local Airflow environment was working.
The temporary test task was later replaced by the actual dbt pipeline tasks.

---

## 8. Integrating dbt with Airflow
### 8.1. Objective
The next step was to integrate the dbt project with Airflow.
Instead of executing dbt manually, Airflow should run the dbt commands automatically.
The integration uses `BashOperator`.

### 8.2. What Is BashOperator?
`BashOperator` is an Airflow operator that executes a shell command.
In our project, it is used to execute dbt commands from the terminal.
This allows Airflow to run dbt even though dbt and Airflow are installed in separate Python virtual environments.

### 8.3. Why Use Absolute Paths?

The dbt executable is installed in:
`data-engineering/.venv/bin/dbt`

The dbt project is located in:
`BrewBeats/airflow/brewbeats_dbt`

Airflow must know exactly where to find both.

We therefore define:

- `DBT_EXECUTABLE` — full path to the dbt command.
- `DBT_PROJECT_DIR` — full path to the dbt project.

This avoids relying on the current terminal directory or the active Python environment.

### 8.4. Actual Airflow DAG

File:

`airflow/dags/brewbeats_dag.py`

Current code:

```python
# Import datetime to define the DAG start date
from datetime import datetime

# Import the main DAG class
from airflow import DAG

# Import BashOperator to execute terminal commands
from airflow.providers.standard.operators.bash import BashOperator  # type: ignore


# Define paths to the dbt executable and dbt project
DBT_EXECUTABLE = (
    "/Users/katerynasoloviova/Documents/"
    "ironhack_DE/data-engineering/.venv/bin/dbt"
)

DBT_PROJECT_DIR = (
    "/Users/katerynasoloviova/Documents/"
    "ironhack_DE/data-engineering/BrewBeats/"
    "airflow/brewbeats_dbt"
)


# Define the BrewBeats daily data pipeline
with DAG(
    dag_id="brewbeats_pipeline",
    start_date=datetime(2026, 11, 19),
    schedule="@daily",
    catchup=False,
    tags=["BrewBeats", "dbt", "Snowflake"],
) as dag:

    # Task 1: Build the staging and daily revenue models
    run_dbt_models = BashOperator(
        task_id="run_dbt_models",
        bash_command=(
            f"{DBT_EXECUTABLE} run "
            "--select stg_coffee_sales daily_revenue"
        ),
        cwd=DBT_PROJECT_DIR,
    )

    # Task 2: Run generic data quality tests
    test_dbt_models = BashOperator(
        task_id="test_dbt_models",
        bash_command=(
            f"{DBT_EXECUTABLE} test "
            "--select test_type:generic"
        ),
        cwd=DBT_PROJECT_DIR,
    )

    # Task 3: Check whether the mart contains today's data
    check_mart_data = BashOperator(
        task_id="check_mart_data",
        bash_command=(
            f"{DBT_EXECUTABLE} test "
            "--select check_mart_data"
        ),
        cwd=DBT_PROJECT_DIR,
    )

    # Define the execution order
    run_dbt_models >> test_dbt_models >> check_mart_data
```

### 8.5. Understanding the DAG Configuration

**dag_id**

`brewbeats_pipeline`

Unique identifier of the workflow.

**start_date**

`datetime(2026, 11, 19)`

Defines the date from which Airflow can schedule the DAG.

**schedule**

`@daily`

Defines a daily schedule.

**catchup**

`False`

Prevents Airflow from automatically creating historical scheduled runs for every missed interval.

**tags**

Used to organize and filter DAGs in the Airflow interface.

### 8.6. Understanding the Tasks

**Task 1: run_dbt_models**

```python
run_dbt_models = BashOperator(
    task_id="run_dbt_models",
    bash_command=(
        f"{DBT_EXECUTABLE} run "
        "--select stg_coffee_sales daily_revenue"
    ),
    cwd=DBT_PROJECT_DIR,
)
```

Purpose:

Execute the two BrewBeats dbt models.

The command:

```bash
dbt run --select stg_coffee_sales daily_revenue
```

This builds:

1. `stg_coffee_sales`
2. `daily_revenue`

dbt understands the dependency between these models and builds the staging model before the mart.

**Task 2: test_dbt_models**

```python
test_dbt_models = BashOperator(
    task_id="test_dbt_models",
    bash_command=(
        f"{DBT_EXECUTABLE} test "
        "--select daily_revenue"
    ),
    cwd=DBT_PROJECT_DIR,
)
```

Purpose:

Execute the four configured data quality tests for `daily_revenue`.

The command:

```bash
dbt test --select daily_revenue
```

### 8.7. Task Dependencies

Code:

```python
run_dbt_models >> test_dbt_models
```

The `>>` operator defines the execution order.

It means:

- First, Airflow executes `run_dbt_models`.
- After it succeeds, Airflow executes `test_dbt_models`.

If the first task fails, the second task will not run under the default dependency behavior.

This ensures that data quality tests are executed only after the models have been successfully built.

### 8.8. Airflow Execution Results

The DAG was successfully discovered in the Airflow web interface.

The workflow was manually triggered.

**Task 1: run_dbt_models**

Result:

```text
1 of 2 OK created sql view model DBT_DEV.stg_coffee_sales
2 of 2 OK created sql table model DBT_DEV.daily_revenue

Completed successfully

PASS=2
WARN=0
ERROR=0
```

**Task 2: test_dbt_models**

The task was successfully executed after the model-building task.

The four dbt data quality tests had previously been verified successfully:

```text
PASS=4
WARN=0
ERROR=0
TOTAL=4
```

**Airflow status: SUCCESS**

Both DAG tasks were confirmed with green `Success` status in the Airflow interface.

### 8.9. Current DAG Status

| Task | Purpose | Status |
|---|---|---|
| run_dbt_models | Build staging and daily revenue models | SUCCESS |
| test_dbt_models | Execute four data quality tests | SUCCESS |
| check_mart_data | Additional Snowflake mart validation | Planned |

The first two tasks are implemented and successfully executed.

The additional direct Snowflake validation task has not yet been implemented.

---

## 9. Additional Mart Validation

### 9.1. Objective

The objective was to add an additional data quality check to verify whether the `DAILY_REVENUE` mart contains records for the current date.

### 9.2. Implementation

Instead of creating a separate direct Snowflake connection in Python, I implemented this validation as a dbt singular test.

File:

`tests/check_mart_data.sql`

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

The test uses:

- `CURRENT_DATE()` to get the current date.
- `NOT EXISTS` to check whether that date is present in the mart.
- `ref()` to reference the `daily_revenue` model.

### 9.3. How the Test Works

- If a record for today exists, the query returns zero rows and the test passes.
- If no record exists for today, the query returns one row and the test fails.

### 9.4. Airflow Integration

The test was added as the third task in the Airflow DAG:
`check_mart_data`

It executes the command:
```bash
dbt test --select check_mart_data
```

The task runs after the model-building and generic data quality test tasks.

Task order:
```python
run_dbt_models >> test_dbt_models >> check_mart_data
```

### 9.5. Execution Results

| Task | Result |
|---|---|
| `run_dbt_models` | SUCCESS |
| `test_dbt_models` | SUCCESS |
| `check_mart_data` | FAILED |

### 9.6. Explanation of the Result

The source dataset contains historical records from **2024-03-01 to 2025-03-23**.
The current date at the time of execution was **2026-11-20**.
Therefore, the `DAILY_REVENUE` table does not contain a record for the current date.
The test failed as expected because it detected missing current-date data.
This is an expected validation result, not a SQL transformation error.
The first two Airflow tasks completed successfully. However, the overall DAG run received a **Failed** status because the third task failed.

### 9.7. Conclusion
The additional mart validation was successfully implemented and executed.
It demonstrates that dbt can detect missing current-date data and that Airflow can orchestrate this validation as part of the pipeline.

---

## 10. Final Pipeline Validation

### 10.1. Current Results

| Component | Validation | Status |
|---|---|---|
| dbt connection | `dbt debug` | SUCCESS |
| dbt staging model | `dbt run --select stg_coffee_sales` | SUCCESS |
| Staging row count | RAW vs staging | SUCCESS |
| Daily Revenue Mart | `dbt run --select daily_revenue` | SUCCESS |
| Mart aggregation | Revenue and transaction totals | SUCCESS |
| Data quality tests | `dbt test --select daily_revenue` | SUCCESS |
| Airflow environment | Airflow web interface and DAG discovery | SUCCESS |
| Airflow dbt execution | `run_dbt_models` | SUCCESS |
| Airflow dbt tests | `test_dbt_models` | SUCCESS |
| Direct Snowflake mart check | `check_mart_data` | FAILED — expected |

### 10.2. Current Conclusion

The dbt transformation project and its integration with Airflow have been successfully implemented and tested.
The raw coffee sales data is transformed into a staging model and a daily revenue mart in Snowflake.
Four data quality tests have passed.
Airflow successfully orchestrates the two implemented tasks: dbt model execution and data quality testing.
An additional direct Snowflake validation task remains to be implemented.

---

## 11. Key Concepts Learned

### Snowflake

- Cloud data warehouse.
- Databases and schemas.
- Tables and views.
- Virtual warehouses.
- Separating raw and transformed data.

### dbt

- dbt Core and adapters.
- dbt profiles.
- Sources and source definitions.
- SQL models.
- `source()` and `ref()`.
- Model dependencies.
- Materializations.
- Views and tables.
- Parsing and execution.
- Data quality tests.

### SQL

- SELECT and FROM.
- Column aliases.
- Data type casting.
- SUM and COUNT.
- ROUND.
- GROUP BY.
- Aggregation.
- Data validation.

### YAML

- Project configuration.
- Source definitions.
- Model descriptions.
- Data quality test configuration.

### Apache Airflow

- DAGs.
- Tasks.
- Operators.
- BashOperator.
- Task dependencies.
- Scheduling.
- Manual triggering.
- Task execution statuses.
- Airflow metadata database.
- Local Airflow environment.

### Python

- Virtual environments.
- Package installation.
- Python imports.
- Connecting external tools.
- Workflow automation.

---

## 12. Presentation Notes

### 12.1. Project Objective

"The objective of Section D was to build an automated data transformation pipeline using dbt and Apache Airflow, with Snowflake as the data warehouse."

### 12.2. dbt Integration

"I configured dbt locally and connected it to Snowflake using the Snowflake adapter and OAuth authentication.

I created a staging model to prepare the raw coffee sales data and a daily revenue mart to aggregate transactions by date."

### 12.3. Data Quality

"I implemented four data quality tests using dbt.

The tests check for missing values and duplicate transaction dates.

All four tests passed successfully."

### 12.4. Airflow Integration

"I integrated the dbt project with Apache Airflow using BashOperator.

The first task builds the staging and daily revenue models.

The second task runs the data quality tests.

I configured a dependency to ensure that the tests execute only after the models have been successfully built."

### 12.5. Current Project Result

"The Airflow DAG was successfully executed locally. Both implemented tasks finished with a Success status.

The dbt models and data quality tests were successfully executed against Snowflake."

### 12.6. Additional Work

"An additional task to validate the daily revenue mart directly in Snowflake is planned as the final part of the pipeline."

---

## 13. Important Commands Reference

### dbt Environment

```bash
source .venv/bin/activate

dbt --version

dbt debug

dbt parse

dbt run --select stg_coffee_sales

dbt run --select daily_revenue

dbt test --select daily_revenue
```

Run all models in the project:

```bash
dbt run
```

Note: Running all models also executes the default example models generated by `dbt init`. The Airflow DAG selects only the two BrewBeats models.

### Airflow Environment

```bash
cd BrewBeats/airflow

source airflow_venv/bin/activate

export AIRFLOW_HOME="$PWD/airflow_home"

export AIRFLOW__CORE__DAGS_FOLDER="$PWD/dags"

airflow version

airflow dags list

airflow tasks list brewbeats_pipeline

airflow standalone
```

Stop Airflow:

`Ctrl + C` in the terminal running `airflow standalone`.

### Important Project Paths

| Component | Location |
|---|---|
| dbt virtual environment | `data-engineering/.venv` |
| dbt executable | `data-engineering/.venv/bin/dbt` |
| dbt project | `BrewBeats/airflow/brewbeats_dbt` |
| Airflow virtual environment | `BrewBeats/airflow/airflow_venv` |
| Airflow home | `BrewBeats/airflow/airflow_home` |
| Airflow DAG | `BrewBeats/airflow/dags/brewbeats_dag.py` |
| dbt profile | `~/.dbt/profiles.yml` |

---

## 14. Learning Notes and Future Improvements

The main purpose of this project was not only to create working models, but also to understand the responsibilities of each technology.

The important architectural distinction is:

- Snowflake stores and processes the data.
- dbt transforms and tests the data.
- Airflow orchestrates and monitors the workflow.

The next improvement is to complete the direct Snowflake validation task in Airflow and verify the full three-task pipeline.

Further possible improvements include:

- Adding additional data quality tests.
- Removing unused example dbt models.
- Improving authentication for scheduled Snowflake connections.
- Adding logging and error handling.
- Connecting the final mart to a BI dashboard.

**End of current Section D documentation.**