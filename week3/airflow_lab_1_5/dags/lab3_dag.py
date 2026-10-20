from airflow import DAG
from airflow.operators.python import PythonOperator # type: ignore
from datetime import datetime, timedelta

default_args = {
    "owner": "healthcare_team",
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

def collect_patient_vitals():
    print("Collecting patient vitals...")
    print("Patient monitoring data collected.")

def validate_patient_records():
    print("Validating patient records...")

    heart_rate = 75
    temperature = 37.0

    if heart_rate <= 0:
        raise ValueError("Invalid heart rate")

    if not 30 <= temperature <= 45:
        raise ValueError("Invalid temperature")

    print("Patient records validated successfully.")


def store_patient_data():
    print("Storing validated patient data in database...")
    print("Patient data storage completed.")


def generate_patient_report():
    print("Generating patient report...")
    print("Patient report generated successfully.")


with DAG(
    dag_id="healthcare_patient_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
    tags=["healthcare", "patient-data", "monitoring"],
) as dag:

    collect_task = PythonOperator(
        task_id="collect_patient_vitals",
        python_callable=collect_patient_vitals,
    )

    validate_task = PythonOperator(
        task_id="validate_patient_records",
        python_callable=validate_patient_records,
    )

    store_task = PythonOperator(
        task_id="store_patient_data",
        python_callable=store_patient_data,
    )

    report_task = PythonOperator(
        task_id="generate_patient_report",
        python_callable=generate_patient_report,
    )

    
    collect_task >> validate_task >> store_task >> report_task
