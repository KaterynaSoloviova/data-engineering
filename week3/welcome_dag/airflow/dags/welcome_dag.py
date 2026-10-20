from airflow import DAG
from airflow.operators.python import PythonOperator # type: ignore
from datetime import datetime
import requests # type: ignore

def print_welcome():
    print('Welcome to Airflow!')

def print_date():
    print('Today is {}'.format(datetime.today().date()))

def print_random_quote():
    response = requests.get(
        "https://dummyjson.com/quotes/random",
        timeout=10,
    )
    response.raise_for_status()

    quote = response.json()["quote"]
    author = response.json()["author"]

    print(f'Quote of the day: "{quote}" — {author}')

dag = DAG(
    'welcome_dag',
    default_args={'start_date': datetime(2025, 1, 1)},
    schedule='0 23 * * *',
    catchup=False
)

print_welcome_task = PythonOperator(
    task_id='print_welcome',
    python_callable=print_welcome,
    dag=dag
)

print_date_task = PythonOperator(
    task_id='print_date',
    python_callable=print_date,
    dag=dag
)

print_random_quote = PythonOperator(
    task_id='print_random_quote',
    python_callable=print_random_quote,
    dag=dag
)

# Set the dependencies between the tasks
print_welcome_task >> print_date_task >> print_random_quote