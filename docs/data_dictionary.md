# Data Dictionary

Definitions for staging and warehouse tables used in the project.

## `sales_dw.stg_customers`

| Column | Data Type | Definition |
|---|---|---|
| customer_id | TEXT | Source customer business identifier (primary key in staging). |
| customer_name | TEXT | Customer display name. |
| city | TEXT | Customer city. |
| state | TEXT | Customer state/province. |
| country | TEXT | Customer country. |
| email | TEXT | Customer email address. |
| created_at | TIMESTAMPTZ | Row insertion timestamp in staging. |

## `sales_dw.stg_products`

| Column | Data Type | Definition |
|---|---|---|
| product_id | TEXT | Source product business identifier (primary key in staging). |
| product_name | TEXT | Product display name. |
| category | TEXT | Product category label. |
| brand | TEXT | Product brand/manufacturer. |
| created_at | TIMESTAMPTZ | Row insertion timestamp in staging. |

## `sales_dw.stg_sales`

| Column | Data Type | Definition |
|---|---|---|
| sales_id | TEXT | Source sales transaction identifier (primary key in staging). |
| order_date | DATE | Date the order was placed. |
| customer_id | TEXT | Source customer business identifier. |
| product_id | TEXT | Source product business identifier. |
| quantity | NUMERIC(12, 2) | Units sold for the transaction line. |
| unit_price | NUMERIC(12, 2) | Unit price at sale time. |
| total_amount | NUMERIC(14, 2) | Stored generated column: `quantity * unit_price`. |
| created_at | TIMESTAMPTZ | Row insertion timestamp in staging. |

## `sales_dw.dim_customers`

| Column | Data Type | Definition |
|---|---|---|
| customer_key | BIGINT | Surrogate primary key for customer dimension. |
| customer_id | TEXT | Natural/business customer identifier (unique). |
| customer_name | TEXT | Standardized customer name. |
| city | TEXT | Customer city attribute for analytics slices. |
| state | TEXT | Customer state/province attribute. |
| country | TEXT | Customer country attribute. |
| email | TEXT | Customer email attribute. |
| created_at | TIMESTAMPTZ | Dimension row creation timestamp. |
| updated_at | TIMESTAMPTZ | Dimension row update timestamp. |

## `sales_dw.dim_products`

| Column | Data Type | Definition |
|---|---|---|
| product_key | BIGINT | Surrogate primary key for product dimension. |
| product_id | TEXT | Natural/business product identifier (unique). |
| product_name | TEXT | Standardized product name. |
| category | TEXT | Product category attribute for analytics slices. |
| brand | TEXT | Product brand attribute. |
| created_at | TIMESTAMPTZ | Dimension row creation timestamp. |
| updated_at | TIMESTAMPTZ | Dimension row update timestamp. |

## `sales_dw.fact_sales`

| Column | Data Type | Definition |
|---|---|---|
| sales_key | BIGINT | Surrogate primary key for fact row. |
| sales_id | TEXT | Source transaction identifier (unique at fact grain). |
| order_date | DATE | Date of transaction. |
| customer_key | BIGINT | Foreign key to `dim_customers.customer_key`. |
| product_key | BIGINT | Foreign key to `dim_products.product_key`. |
| quantity | NUMERIC(12, 2) | Transaction quantity measure. |
| unit_price | NUMERIC(12, 2) | Transaction unit price measure. |
| total_amount | NUMERIC(14, 2) | Revenue measure (`quantity * unit_price`). |
| created_at | TIMESTAMPTZ | Fact row creation timestamp. |
