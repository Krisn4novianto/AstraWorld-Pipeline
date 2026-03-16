INSERT INTO dwh.dim_customer (
    customer_id,
    customer_name,
    city,
    province
)

SELECT DISTINCT
    c.id,
    c.name,
    ca.city,
    ca.province
FROM staging.customer_addresses ca
JOIN staging.customers_raw c
    ON ca.customer_id = c.id
WHERE ca.file_date = {{file_date}}
AND NOT EXISTS (
    SELECT 1
    FROM dwh.dim_customer d
    WHERE d.customer_id = c.id
);