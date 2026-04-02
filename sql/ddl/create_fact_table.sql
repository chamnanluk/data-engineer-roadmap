-- Fact table stores transactional measures and connects to dimensions.

CREATE TABLE IF NOT EXISTS sales_dw.fact_sales (
    sales_key        BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    sales_id         TEXT NOT NULL UNIQUE,
    order_date       DATE NOT NULL,
    customer_key     BIGINT NOT NULL,
    product_key      BIGINT NOT NULL,
    quantity         NUMERIC(12, 2) NOT NULL,
    unit_price       NUMERIC(12, 2) NOT NULL,
    total_amount     NUMERIC(14, 2) NOT NULL,
    created_at       TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_fact_sales_customer
        FOREIGN KEY (customer_key)
        REFERENCES sales_dw.dim_customers (customer_key),
    CONSTRAINT fk_fact_sales_product
        FOREIGN KEY (product_key)
        REFERENCES sales_dw.dim_products (product_key)
);

CREATE INDEX IF NOT EXISTS idx_fact_sales_order_date
    ON sales_dw.fact_sales (order_date);

CREATE INDEX IF NOT EXISTS idx_fact_sales_customer_key
    ON sales_dw.fact_sales (customer_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_product_key
    ON sales_dw.fact_sales (product_key);
