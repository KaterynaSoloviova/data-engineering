from airflow import DAG
from airflow.operators.python import PythonOperator # type: ignore
from datetime import datetime, timedelta

default_args = {
    "owner": "retail_team",
    "retries": 3,
    "retry_delay": timedelta(minutes=2),
}

def extract_sales_data():
    print("Extracting sales data from stores...")

def transform_sales_data():
    print("Cleaning and transforming sales data...")

def load_sales_data():
    print("Loading data into warehouse...")

with DAG(
    dag_id="retail_sales_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@hourly",
    catchup=False,
    default_args=default_args,
) as dag:

    extract_data = PythonOperator(
        task_id="extract_sales_data",
        python_callable=extract_sales_data
    )

    transform_data = PythonOperator(
        task_id="transform_sales_data",
        python_callable=transform_sales_data
    )

    load_data = PythonOperator(
        task_id="load_sales_data",
        python_callable=load_sales_data
    )

    extract_data >> transform_data >> load_data