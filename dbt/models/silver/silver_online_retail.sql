select
  cast(invoice_no as varchar) as invoice_no,
  cast(stock_code as varchar) as stock_code,
  nullif(trim(description), '') as description,
  try_cast(quantity as integer) as quantity,
  try_cast(invoice_date as timestamp) as invoice_ts,
  try_cast(unit_price as double) as unit_price,
  try_cast(customer_id as bigint) as customer_id,
  nullif(trim(country), '') as country,
  case when try_cast(quantity as integer) < 0 then true else false end as is_return,
  try_cast(quantity as integer) * try_cast(unit_price as double) as line_total
from {{ ref('bronze_online_retail') }}
where invoice_no is not null
