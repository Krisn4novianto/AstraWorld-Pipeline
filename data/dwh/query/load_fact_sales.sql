INSERT INTO dwh.fact_sales (
    vin,
    customer_id,
    model,
    date_id,
    amount
)

SELECT
    vin,
    customer_id,
    model,
    invoice_date AS date_id,
    price        AS amount
FROM staging.sales_raw
WHERE file_date = {{file_date}};