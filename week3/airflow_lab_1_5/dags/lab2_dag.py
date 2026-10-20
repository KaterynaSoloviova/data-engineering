from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator # type: ignore
from datetime import datetime, timedelta

default_args = {
    "owner": "bank_team",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="fraud_detection_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@hourly",
    catchup=False,
    default_args=default_args,
) as dag:

    read_transactions = BashOperator(
        task_id="read_transactions",
        bash_command='echo "Reading bank transactions..."',
    )

    run_fraud_checks = BashOperator(
        task_id="run_fraud_checks",
        bash_command='echo "Checking transactions for suspicious activity..."',
    )

    generate_alerts = BashOperator(
        task_id="generate_alerts",
        bash_command='echo "Generating fraud alerts..."',
    )

    notify_risk_team = BashOperator(
        task_id="notify_risk_team",
        bash_command='echo "Notifying the risk team..."',
    )

    read_transactions >> run_fraud_checks >> generate_alerts >> notify_risk_team