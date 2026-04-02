-- Staging tables hold raw/cleaned source records before dimensional modeling.

CREATE TABLE IF NOT EXISTS sales_dw.stg_customers (
    customer_id      TEXT PRIMARY KEY,
    customer_name    TEXT NOT NULL,
    city             TEXT,
    state            TEXT,
    country          TEXT,
    email            TEXT,
    created_at       TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sales_dw.stg_products (
    product_id       TEXT PRIMARY KEY,
    product_name     TEXT NOT NULL,
    category         TEXT,
    brand            TEXT,
    created_at       TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sales_dw.stg_sales (
    sales_id         TEXT PRIMARY KEY,
    order_date       DATE NOT NULL,
    customer_id      TEXT NOT NULL,
    product_id       TEXT NOT NULL,
    quantity         NUMERIC(12, 2) NOT NULL,
    unit_price       NUMERIC(12, 2) NOT NULL,
    total_amount     NUMERIC(14, 2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    created_at       TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_stg_sales_customer_id
    ON sales_dw.stg_sales (customer_id);

CREATE INDEX IF NOT EXISTS idx_stg_sales_product_id
    ON sales_dw.stg_sales (product_id);

CREATE INDEX IF NOT EXISTS idx_stg_sales_order_date
    ON sales_dw.stg_sales (order_date);
