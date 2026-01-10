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

## Local run (dbt)
1) Install dbt + duckdb adapter:

```bash
pip install dbt-duckdb
```

2) Run dbt from the repo root:

```bash
dbt run --project-dir dbt --profiles-dir dbt
```

3) (Optional) Run tests:

```bash
dbt test --project-dir dbt --profiles-dir dbt
```

## Airflow
- DAG: `airflow/dags/dbt_medallion_dag.py`
- Requires `dbt` in the Airflow worker environment.
- The DAG runs bronze -> silver -> gold daily.
