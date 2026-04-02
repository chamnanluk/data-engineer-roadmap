-- Revenue grouped by product category.
SELECT
    COALESCE(dp.category, 'Unknown') AS category,
    SUM(fs.total_amount) AS category_revenue
FROM sales_dw.fact_sales fs
JOIN sales_dw.dim_products dp
  ON fs.product_key = dp.product_key
GROUP BY 1
ORDER BY category_revenue DESC;
