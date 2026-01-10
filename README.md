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

### Option A (MacOS/Linux only):

Use the shell file that runs the Python environment setup, runs the dbt transformations, and opens the streamlit dashboard of the results (run this in terminal from the repo root):

```bash
chmod +x run_local.sh
./run_local.sh
```

### Option B:

Setup the environment manually:

1) Create and activate a Python virtual environment (dbt-duckdb currently supports only Python 3.10–3.12):

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

2) Install dependencies:

```bash
pip install -r requirements.txt
```

3) Run dbt:

```bash
dbt run --project-dir dbt --profiles-dir dbt
```

4) Run the Streamlit dashboard for gold layer insights

```bash
streamlit run dashboard/app.py
```
