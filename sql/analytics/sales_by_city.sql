-- Revenue grouped by customer city.
SELECT
    COALESCE(dc.city, 'Unknown') AS city,
    SUM(fs.total_amount) AS city_revenue
FROM sales_dw.fact_sales fs
JOIN sales_dw.dim_customers dc
  ON fs.customer_key = dc.customer_key
GROUP BY 1
ORDER BY city_revenue DESC;
