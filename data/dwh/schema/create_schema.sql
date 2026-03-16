INSERT INTO dwh.dim_customer (
    customer_id,
    customer_name,
    city,
    state
)

SELECT DISTINCT
    customer_id,
    customer_name,
    city,
    state
FROM staging.customer_addresses
WHERE file_date = {{file_date}};