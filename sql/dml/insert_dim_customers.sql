-- Upsert distinct customers from staging into customer dimension.
INSERT INTO sales_dw.dim_customers (
    customer_id,
    customer_name,
    city,
    state,
    country,
    email,
    updated_at
)
SELECT DISTINCT
    sc.customer_id,
    sc.customer_name,
    sc.city,
    sc.state,
    sc.country,
    sc.email,
    CURRENT_TIMESTAMP
FROM sales_dw.stg_customers sc
WHERE sc.customer_id IS NOT NULL
ON CONFLICT (customer_id) DO UPDATE
SET customer_name = EXCLUDED.customer_name,
    city = EXCLUDED.city,
    state = EXCLUDED.state,
    country = EXCLUDED.country,
    email = EXCLUDED.email,
    updated_at = CURRENT_TIMESTAMP;
