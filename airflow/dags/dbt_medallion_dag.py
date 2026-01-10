from __future__ import annotations

from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.bash import BashOperator

DAG_ID = "dbt_medallion_pipeline"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DBT_PROJECT_DIR = PROJECT_ROOT / "dbt"
DBT_PROFILES_DIR = DBT_PROJECT_DIR

with DAG(
    dag_id=DAG_ID,
    description="Medallion architecture pipeline for Online Retail data",
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args={"retries": 1},
    tags=["dbt", "medallion"],
) as dag:
    run_bronze = BashOperator(
        task_id="run_bronze",
        bash_command=(
            "dbt run --select bronze_online_retail "
            "--project-dir {{ params.dbt_project_dir }} "
            "--profiles-dir {{ params.dbt_profiles_dir }}"
        ),
        params={
            "dbt_project_dir": str(DBT_PROJECT_DIR),
            "dbt_profiles_dir": str(DBT_PROFILES_DIR),
        },
    )

    run_silver = BashOperator(
        task_id="run_silver",
        bash_command=(
            "dbt run --select silver_online_retail "
            "--project-dir {{ params.dbt_project_dir }} "
            "--profiles-dir {{ params.dbt_profiles_dir }}"
        ),
        params={
            "dbt_project_dir": str(DBT_PROJECT_DIR),
            "dbt_profiles_dir": str(DBT_PROFILES_DIR),
        },
    )

    run_gold = BashOperator(
        task_id="run_gold",
        bash_command=(
            "dbt run --select gold_sales_daily gold_customer_metrics "
            "--project-dir {{ params.dbt_project_dir }} "
            "--profiles-dir {{ params.dbt_profiles_dir }}"
        ),
        params={
            "dbt_project_dir": str(DBT_PROJECT_DIR),
            "dbt_profiles_dir": str(DBT_PROFILES_DIR),
        },
    )

    run_bronze >> run_silver >> run_gold
