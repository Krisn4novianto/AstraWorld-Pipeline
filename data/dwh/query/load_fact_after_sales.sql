INSERT INTO dwh.fact_after_sales (
    service_ticket,
    vin,
    customer_id,
    model,
    service_date,
    service_type,
    created_at
)

SELECT
    service_ticket,
    vin,
    customer_id,
    model,
    service_date,
    service_type,
    created_at

FROM staging.after_sales_raw

ON CONFLICT (service_ticket) DO NOTHING;