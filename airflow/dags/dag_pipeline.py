from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "daily_pipeline",
    default_args=default_args,
    description="Pipeline Landing → Staging → DWH → Datamart",
    schedule_interval="0 2 * * *",
    start_date=datetime(2026, 3, 1),
    catchup=False,
)

BASE_DIR = "/opt/airflow"


def run_landing():
    os.system(
        f"python {BASE_DIR}/pipeline/ingest_customer_addresses.py {datetime.now().strftime('%Y%m%d')}"
    )


def run_staging():
    os.system(
        f"python {BASE_DIR}/pipeline/staging_customer_addresses.py {datetime.now().strftime('%Y%m%d')}"
    )


def run_dwh():
    os.system(
        f"python {BASE_DIR}/pipeline/run_dwh.py {datetime.now().strftime('%Y%m%d')}"
    )


def run_datamart_sales():
    os.system(
        f"python {BASE_DIR}/pipeline/run_datamart.py sales_summary"
    )


def run_datamart_service():
    os.system(
        f"python {BASE_DIR}/pipeline/run_datamart.py service_priority"
    )


t1 = PythonOperator(
    task_id="landing",
    python_callable=run_landing,
    dag=dag,
)

t2 = PythonOperator(
    task_id="staging",
    python_callable=run_staging,
    dag=dag,
)

t3 = PythonOperator(
    task_id="dwh_loading",
    python_callable=run_dwh,
    dag=dag,
)

t4 = PythonOperator(
    task_id="datamart_sales_summary",
    python_callable=run_datamart_sales,
    dag=dag,
)

t5 = PythonOperator(
    task_id="datamart_service_priority",
    python_callable=run_datamart_service,
    dag=dag,
)


t1 >> t2 >> t3 >> [t4, t5]