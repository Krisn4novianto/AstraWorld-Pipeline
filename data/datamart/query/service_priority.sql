CREATE TABLE IF NOT EXISTS datamart.service_priority AS
SELECT
    EXTRACT(YEAR FROM f.service_date) AS periode,
    f.vin,
    c.customer_name,
    COUNT(*) AS count_service,

    CASE
        WHEN COUNT(*) > 10 THEN 'HIGH'
        WHEN COUNT(*) BETWEEN 5 AND 10 THEN 'MEDIUM'
        ELSE 'LOW'
    END AS priority

FROM dwh.fact_after_sales f
JOIN dwh.dim_customer c
    ON f.customer_id = c.customer_id

GROUP BY
    EXTRACT(YEAR FROM f.service_date),
    f.vin,
    c.customer_name

ORDER BY
    periode,
    f.vin;