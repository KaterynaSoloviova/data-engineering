from airflow import DAG
from airflow.operators.python import PythonOperator # type: ignore
from airflow.operators.email import EmailOperator # type: ignore
from datetime import datetime, timedelta
import pandas as pd # type: ignore

PROCESSED_FILE = "/opt/airflow/data/processed/cleaned_sales.csv"

# Configure retries
default_args = {
    "owner": "analytics_team",
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

# Check total sales
def check_sales(**context):
    df = pd.read_csv(PROCESSED_FILE) # Reads cleaned_sales.csv into a Pandas DataFrame.
    total_sales = df["Total_Sales"].sum() # Selects the Total_Sales column and adds up all its values
    print(f"Total Sales = {total_sales}") # Prints the result in the Airflow task logs.

    # Trigger an alert if sales are low:
    """context contains information about the current task run.
       ti is the TaskInstance object.
       xcom_push() stores a value that another task can retrieve.
       key="alert_message" names the stored value"""


    if total_sales < 100000:
        context["ti"].xcom_push(
            key="alert_message",
            value=f"ALERT: Sales dropped to {total_sales}"
        )

with DAG(
    dag_id="retail_alert_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
) as dag:

    sales_check_task = PythonOperator(
        task_id="check_sales",
        python_callable=check_sales
    )

    send_email = EmailOperator(
        task_id="send_email_alert",
        to="manager@gmail.com",
        subject="Retail Sales Alert",
        html_content="""
        <h3>Sales Alert Triggered</h3>
        <p>Please check today's sales report.</p>
        """,
        retries=3,
    )

    sales_check_task >> send_email
