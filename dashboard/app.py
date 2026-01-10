from pathlib import Path
import duckdb
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Ecommerce Gold Layer Insights", layout="wide")

REPO_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = REPO_ROOT / "warehouse" / "ecommerce.duckdb"

st.title("Gold Layer Insights")
st.caption("Daily sales and customer KPIs from the gold layer.")

if not DB_PATH.exists():
    st.error(
        "DuckDB warehouse not found. Run dbt first to create gold tables: "
        "`dbt run --project-dir dbt --profiles-dir dbt`"
    )
    st.stop()

con = duckdb.connect(str(DB_PATH), read_only=True)

sales_daily = con.execute(
    """
    select sales_date, orders, line_items, gross_revenue, returns_value, net_revenue
    from gold_sales_daily
    order by sales_date
    """
).df()

customer_metrics = con.execute(
    """
    select customer_id, first_purchase_ts, last_purchase_ts, orders, gross_revenue,
           net_revenue, countries_shopped
    from gold_customer_metrics
    order by net_revenue desc nulls last
    """
).df()

if sales_daily.empty:
    st.warning("No data found in gold_sales_daily. Re-run dbt to populate.")
    st.stop()

sales_daily["sales_date"] = pd.to_datetime(sales_daily["sales_date"]).dt.date

min_date = sales_daily["sales_date"].min()
max_date = sales_daily["sales_date"].max()

st.sidebar.header("Filters")
start_date, end_date = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

filtered_sales = sales_daily[
    (sales_daily["sales_date"] >= start_date)
    & (sales_daily["sales_date"] <= end_date)
]

kpi_total_orders = int(filtered_sales["orders"].sum())
kpi_line_items = int(filtered_sales["line_items"].sum())
kpi_gross_revenue = float(filtered_sales["gross_revenue"].sum())
kpi_returns = float(filtered_sales["returns_value"].sum())
kpi_net_revenue = float(filtered_sales["net_revenue"].sum())

kpi_cols = st.columns(5)
kpi_cols[0].metric("Orders", f"{kpi_total_orders:,}")
kpi_cols[1].metric("Line Items", f"{kpi_line_items:,}")
kpi_cols[2].metric("Gross Revenue", f"{kpi_gross_revenue:,.2f}")
kpi_cols[3].metric("Returns", f"{kpi_returns:,.2f}")
kpi_cols[4].metric("Net Revenue", f"{kpi_net_revenue:,.2f}")

st.subheader("Daily Revenue")
st.line_chart(
    filtered_sales.set_index("sales_date")["net_revenue"],
    height=300,
)

st.subheader("Orders and Line Items")
orders_chart = filtered_sales.set_index("sales_date")[["orders", "line_items"]]
st.bar_chart(orders_chart, height=300)

st.subheader("Top Customers")
top_n = st.sidebar.slider("Top customers", min_value=5, max_value=50, value=15)
customer_metrics["first_purchase_ts"] = pd.to_datetime(
    customer_metrics["first_purchase_ts"]
)
customer_metrics["last_purchase_ts"] = pd.to_datetime(
    customer_metrics["last_purchase_ts"]
)

st.dataframe(
    customer_metrics.head(top_n),
    use_container_width=True,
    hide_index=True,
)
