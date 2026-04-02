-- Dimension tables with surrogate keys and business key uniqueness.

CREATE TABLE IF NOT EXISTS sales_dw.dim_customers (
    customer_key     BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id      TEXT NOT NULL UNIQUE,
    customer_name    TEXT NOT NULL,
    city             TEXT,
    state            TEXT,
    country          TEXT,
    email            TEXT,
    created_at       TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at       TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sales_dw.dim_products (
    product_key      BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id       TEXT NOT NULL UNIQUE,
    product_name     TEXT NOT NULL,
    category         TEXT,
    brand            TEXT,
    created_at       TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at       TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
