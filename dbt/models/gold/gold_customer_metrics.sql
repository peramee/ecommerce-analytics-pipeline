select
  customer_id,
  min(invoice_ts) as first_purchase_ts,
  max(invoice_ts) as last_purchase_ts,
  count(distinct invoice_no) as orders,
  sum(case when is_return then 0 else line_total end) as gross_revenue,
  sum(line_total) as net_revenue,
  count(distinct country) as countries_shopped
from {{ ref('silver_online_retail') }}
where customer_id is not null
group by 1
