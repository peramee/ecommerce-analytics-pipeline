# Ecommerce Analytics Pipeline

A medallion-style analytics data pipeline demo project for ecommerce transactions using dbt and DuckDB, with a streamlit dashboard for final gold layer insights.

Data used as input: a free online retail transactions dataset from Kaggle (https://www.kaggle.com/datasets/abhishekrp1517/online-retail-transactions-dataset).

## Structure
- `data-sources/online-retail.csv`: raw input dataset.
- `dbt/`: transformation project (bronze, silver, gold).
- `warehouse/`: DuckDB database output.
- `dashboard/`: Streamlit dashboard for gold layer results.

## Medallion layers
- Bronze: raw CSV ingested into a DuckDB table (`bronze_online_retail`).
- Silver: cleaned and typed rows with derived metrics (`silver_online_retail`).
- Gold: analytics-ready aggregates (`gold_sales_daily`, `gold_customer_metrics`).

## Local run (venv + dbt)

### Option A:

Use the shell file that runs the Python environment setup, runs the transformations (in DBT only), and opens the streamlit dashboard of the results:

```bash
chmod +x run_local.sh
./run_local.sh
```

### Option B:

Setup the environment manually:

1) Create and activate a virtual environment:

dbt-duckdb currently supports Python 3.10–3.12. If your system default is newer, use `python3.12` or `python3.11` for the venv.

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

## Dashboard (gold insights)
Run the Streamlit dashboard after `dbt run` has created the gold tables:

```bash
streamlit run dashboard/app.py
```
