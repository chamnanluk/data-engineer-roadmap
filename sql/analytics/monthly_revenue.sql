-- Monthly revenue trend from the sales fact table.
SELECT
    DATE_TRUNC('month', order_date)::DATE AS month_start,
    SUM(total_amount) AS monthly_revenue
FROM sales_dw.fact_sales
GROUP BY 1
ORDER BY 1;
