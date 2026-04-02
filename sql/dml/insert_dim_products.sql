-- Upsert distinct products from staging into product dimension.
INSERT INTO sales_dw.dim_products (
    product_id,
    product_name,
    category,
    brand,
    updated_at
)
SELECT DISTINCT
    sp.product_id,
    sp.product_name,
    sp.category,
    sp.brand,
    CURRENT_TIMESTAMP
FROM sales_dw.stg_products sp
WHERE sp.product_id IS NOT NULL
ON CONFLICT (product_id) DO UPDATE
SET product_name = EXCLUDED.product_name,
    category = EXCLUDED.category,
    brand = EXCLUDED.brand,
    updated_at = CURRENT_TIMESTAMP;
