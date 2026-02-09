"""Airflow DAG to orchestrate the sales ETL pipeline."""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


DEFAULT_ARGS = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="sales_etl_pipeline",
    default_args=DEFAULT_ARGS,
    description="Daily sales ETL pipeline",
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["sales", "etl"],
) as dag:
    extract_task = BashOperator(
        task_id="extract_sales",
        bash_command="python scripts/extract_sales.py",
    )

    transform_task = BashOperator(
        task_id="transform_sales",
        bash_command="python scripts/transform_sales.py",
    )

    load_task = BashOperator(
        task_id="load_sales",
        bash_command="python scripts/load_sales.py",
    )

    extract_task >> transform_task >> load_task
