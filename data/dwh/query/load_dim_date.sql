INSERT INTO dwh.dim_date (
    date_id,
    year,
    month,
    day,
    quarter,
    day_of_week
)

SELECT DISTINCT
    invoice_date,
    EXTRACT(YEAR FROM invoice_date),
    EXTRACT(MONTH FROM invoice_date),
    EXTRACT(DAY FROM invoice_date),
    EXTRACT(QUARTER FROM invoice_date),
    EXTRACT(DOW FROM invoice_date)
FROM staging.sales_raw;