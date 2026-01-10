# Ecommerce Data Platform

Medallion-style data platform for Online Retail transactions using Airflow and dbt.

## Structure
- `data sources/Online Retail.csv`: raw input dataset.
- `dbt/`: transformation project (bronze, silver, gold).
- `airflow/dags/`: DAG that orchestrates the dbt layers.
- `warehouse/`: DuckDB database output.

## Medallion layers
- Bronze: raw CSV ingested into a DuckDB table (`bronze_online_retail`).
- Silver: cleaned and typed rows with derived metrics (`silver_online_retail`).
- Gold: analytics-ready aggregates (`gold_sales_daily`, `gold_customer_metrics`).

## Local run (venv + dbt)
dbt-duckdb currently supports Python 3.10–3.12. If your system default is newer, use `python3.12` or `python3.11` for the venv.

1) Create and activate a virtual environment:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

2) Install dependencies:

```bash
pip install -r requirements.txt
```

3) Run dbt from the repo root:

```bash
dbt run --project-dir dbt --profiles-dir dbt
```

4) (Optional) Run tests:

```bash
dbt test --project-dir dbt --profiles-dir dbt
```

## Airflow
- DAG: `airflow/dags/dbt_medallion_dag.py`
- Requires `dbt` in the Airflow worker environment.
- The DAG runs bronze -> silver -> gold daily.

To run Airflow in the same venv, install it using the official constraints file for your Python version:

```bash
PYTHON_VERSION=$(python -c 'import sys; print(f\"{sys.version_info.major}.{sys.version_info.minor}\")')
AIRFLOW_VERSION=2.9.3
pip install \"apache-airflow==${AIRFLOW_VERSION}\" \\
  --constraint \"https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt\"
```
