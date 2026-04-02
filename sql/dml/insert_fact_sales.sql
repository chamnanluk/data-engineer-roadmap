-- Insert sales facts by resolving business keys to surrogate keys.
-- Idempotent behavior is controlled with ON CONFLICT (sales_id).
INSERT INTO sales_dw.fact_sales (
    sales_id,
    order_date,
    customer_key,
    product_key,
    quantity,
    unit_price,
    total_amount
)
SELECT
    ss.sales_id,
    ss.order_date,
    dc.customer_key,
    dp.product_key,
    ss.quantity,
    ss.unit_price,
    ss.quantity * ss.unit_price AS total_amount
FROM sales_dw.stg_sales ss
JOIN sales_dw.dim_customers dc
  ON ss.customer_id = dc.customer_id
JOIN sales_dw.dim_products dp
  ON ss.product_id = dp.product_id
ON CONFLICT (sales_id) DO UPDATE
SET order_date = EXCLUDED.order_date,
    customer_key = EXCLUDED.customer_key,
    product_key = EXCLUDED.product_key,
    quantity = EXCLUDED.quantity,
    unit_price = EXCLUDED.unit_price,
    total_amount = EXCLUDED.total_amount;
