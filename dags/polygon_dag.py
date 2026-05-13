from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
import sys
import os

# project path
sys.path.insert(0, '/root/polygon_project')

def run_stock_pipeline():
    from load import load_to_mongo
    load_to_mongo()

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2026, 1, 1),
}

with DAG(
    dag_id='polygon_stock',
    default_args=default_args,
    schedule='@hourly',
    catchup=False,
) as dag:
    
    run_pipeline = PythonOperator(
        task_id='run_stock_prices_pipeline',
        python_callable=run_stock_pipeline,
    )
