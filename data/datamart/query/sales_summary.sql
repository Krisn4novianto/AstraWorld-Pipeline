CREATE TABLE IF NOT EXISTS datamart.sales_summary AS
SELECT
    TO_CHAR(d.date_id, 'YYYY-MM') AS periode,
    c.customer_name,
    v.model,
    SUM(f.amount) AS total,

    CASE
        WHEN SUM(f.amount) < 250000000 THEN 'LOW'
        WHEN SUM(f.amount) BETWEEN 250000000 AND 400000000 THEN 'MEDIUM'
        ELSE 'HIGH'
    END AS class_range

FROM dwh.fact_sales f
JOIN dwh.dim_customer c
    ON f.customer_id = c.customer_id
JOIN dwh.dim_vehicle v
    ON f.vin = v.vehicle_id
JOIN dwh.dim_date d
    ON f.date_id = d.date_id

GROUP BY
    TO_CHAR(d.date_id, 'YYYY-MM'),
    c.customer_name,
    v.model

ORDER BY
    periode,
    customer_name,
    model;