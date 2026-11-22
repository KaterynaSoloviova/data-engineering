
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

    # Task 1: Build the staging and daily revenue dbt models
    run_dbt_models = BashOperator(
        task_id="run_dbt_models",
        bash_command=(
            f"{DBT_EXECUTABLE} run "
            "--select stg_coffee_sales daily_revenue"
        ),
        cwd=DBT_PROJECT_DIR,
    )

    # Task 2: Run data quality tests for the daily revenue model
    test_dbt_models = BashOperator(
        task_id="test_dbt_models",
        bash_command=(
            f"{DBT_EXECUTABLE} test "
            "--select test_type:generic"
        ),
        cwd=DBT_PROJECT_DIR,
    )

    # Task 3: Check whether the mart table has data for today
    check_mart_data = BashOperator(
        task_id="check_mart_data",
        bash_command=(
            f"{DBT_EXECUTABLE} test "
            "--select check_mart_data"
        ),
        cwd=DBT_PROJECT_DIR,
    )

    # Define the execution order of all three tasks
    run_dbt_models >> test_dbt_models >> check_mart_data
