
from datetime import timedelta
import logging
import os
from pathlib import Path

import pandas as pd
import pendulum # type: ignore

from airflow import DAG
from airflow.operators.python import PythonOperator # type: ignore
from airflow.providers.postgres.hooks.postgres import PostgresHook # type: ignore


# --------------------------------------------------
# Configuration
# --------------------------------------------------

DATA_DIR = Path(
    os.getenv("QUICKCART_DATA_DIR", "/opt/airflow/data")
)

SQL_FILE = Path(
    os.getenv(
        "QUICKCART_SQL_FILE",
        "/opt/airflow/sql/transform_quickcart.sql",
    )
)

POSTGRES_CONN_ID = "quickcart_postgres"

ALERT_EMAIL = os.getenv(
    "QUICKCART_ALERT_EMAIL",
    "your_email@example.com",
)

FILES = {
    "customers": {
        "filename": "customers.csv",
        "columns": [
            "customer_id",
            "customer_name",
            "email",
            "city",
            "signup_date",
        ],
    },
    "orders": {
        "filename": "orders.csv",
        "columns": [
            "order_id",
            "customer_id",
            "product_id",
            "order_date",
            "quantity",
            "unit_price",
            "payment_status",
        ],
    },
    "products": {
        "filename": "products.csv",
        "columns": [
            "product_id",
            "product_name",
            "category",
            "supplier_id",
            "cost_price",
            "selling_price",
        ],
    },
    "clickstream": {
        "filename": "clickstream.csv",
        "columns": [
            "event_id",
            "customer_id",
            "event_type",
            "page_url",
            "event_timestamp",
            "device_type",
        ],
    },
}


# --------------------------------------------------
# Task 1: Extract / check CSV files
# --------------------------------------------------

def extract_csv_files():
    logging.info("Starting QuickCart CSV extraction.")

    for name, config in FILES.items():
        filepath = DATA_DIR / config["filename"]

        if not filepath.is_file():
            raise FileNotFoundError(
                f"Missing {name} file: {filepath}"
            )

        logging.info("Found source file: %s", filepath)

    logging.info("All required CSV files are available.")


# --------------------------------------------------
# Task 2: Validate CSV files
# --------------------------------------------------

def validate_csv_files():
    logging.info("Starting CSV validation.")

    for name, config in FILES.items():
        filepath = DATA_DIR / config["filename"]

        df = pd.read_csv(filepath)

        if df.empty:
            raise ValueError(
                f"{config['filename']} contains no data rows."
            )

        missing_columns = set(config["columns"]) - set(df.columns)

        if missing_columns:
            raise ValueError(
                f"{config['filename']} is missing columns: "
                f"{sorted(missing_columns)}"
            )

        logging.info(
            "Validated %s: %s rows, %s columns.",
            name,
            len(df),
            len(df.columns),
        )

    logging.info("All CSV files passed schema validation.")


# --------------------------------------------------
# Task 3: Load raw data into PostgreSQL staging
# --------------------------------------------------

def load_staging_tables():
    logging.info("Starting staging-table load.")

    hook = PostgresHook(
        postgres_conn_id=POSTGRES_CONN_ID
    )

    # Raw staging columns use TEXT to preserve source values.
    # Create the tables before loading the CSV files.
    staging_schemas = {
        "customers": """
            CREATE TABLE IF NOT EXISTS staging_customers (
                customer_id TEXT,
                customer_name TEXT,
                email TEXT,
                city TEXT,
                signup_date TEXT
            )
        """,
        "orders": """
            CREATE TABLE IF NOT EXISTS staging_orders (
                order_id TEXT,
                customer_id TEXT,
                product_id TEXT,
                order_date TEXT,
                quantity TEXT,
                unit_price TEXT,
                payment_status TEXT
            )
        """,
        "products": """
            CREATE TABLE IF NOT EXISTS staging_products (
                product_id TEXT,
                product_name TEXT,
                category TEXT,
                supplier_id TEXT,
                cost_price TEXT,
                selling_price TEXT
            )
        """,
        "clickstream": """
            CREATE TABLE IF NOT EXISTS staging_clickstream (
                event_id TEXT,
                customer_id TEXT,
                event_type TEXT,
                page_url TEXT,
                event_timestamp TEXT,
                device_type TEXT
            )
        """,
    }

    # Create staging tables if they do not already exist.
    for name, ddl in staging_schemas.items():
        hook.run(ddl)
        logging.info("Staging table is ready: %s", name)

    # This mini-project version refreshes staging on each run.
    for name, config in FILES.items():
        table_name = f"staging_{name}"
        filepath = DATA_DIR / config["filename"]
        columns = ", ".join(config["columns"])

        hook.run(f"TRUNCATE TABLE {table_name}")

        copy_sql = (
            f"COPY {table_name} ({columns}) "
            "FROM STDIN WITH (FORMAT CSV, HEADER TRUE)"
        )

        hook.copy_expert(
            sql=copy_sql,
            filename=str(filepath),
        )

        logging.info(
            "Loaded %s into %s.",
            filepath.name,
            table_name,
        )

    logging.info("All staging tables loaded successfully.")


# --------------------------------------------------
# Task 4: Transform staging data using SQL
# --------------------------------------------------

def transform_quickcart_data():
    logging.info("Starting QuickCart SQL transformations.")

    if not SQL_FILE.is_file():
        raise FileNotFoundError(
            f"Transformation SQL file not found: {SQL_FILE}"
        )

    sql = SQL_FILE.read_text(encoding="utf-8")

    if not sql.strip():
        raise ValueError("Transformation SQL file is empty.")

    hook = PostgresHook(
        postgres_conn_id=POSTGRES_CONN_ID
    )

    hook.run(sql, split_statements=True)

    logging.info("QuickCart transformations completed.")


# --------------------------------------------------
# DAG definition
# --------------------------------------------------

default_args = {
    "owner": "quickcart_data_team",
    "depends_on_past": False,
    "email": [ALERT_EMAIL],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="quickcart_daily_elt",
    description="Daily QuickCart CSV ingestion and ELT pipeline",
    default_args=default_args,
    schedule="0 2 * * *",
    start_date=pendulum.datetime(
        2026, 10, 1, tz="Europe/Berlin"
    ),
    catchup=False,
    max_active_runs=1,
    tags=["quickcart", "elt", "postgres"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract_csv_files",
        python_callable=extract_csv_files,
    )

    validate_task = PythonOperator(
        task_id="validate_csv_files",
        python_callable=validate_csv_files,
    )

    load_task = PythonOperator(
        task_id="load_raw_data_to_staging",
        python_callable=load_staging_tables,
    )

    transform_task = PythonOperator(
        task_id="transform_staging_data",
        python_callable=transform_quickcart_data,
    )

    # Define the execution order.
    extract_task >> validate_task >> load_task >> transform_task
