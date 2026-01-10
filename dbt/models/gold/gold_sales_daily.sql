select
  date_trunc('day', invoice_ts) as sales_date,
  count(distinct invoice_no) as orders,
  count(*) as line_items,
  sum(case when is_return then 0 else line_total end) as gross_revenue,
  sum(case when is_return then -line_total else 0 end) as returns_value,
  sum(line_total) as net_revenue
from {{ ref('silver_online_retail') }}
where invoice_ts is not null
group by 1
