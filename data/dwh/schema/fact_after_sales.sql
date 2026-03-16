CREATE TABLE IF NOT EXISTS dwh.fact_after_sales (
    service_ticket VARCHAR(20) PRIMARY KEY,
    vin VARCHAR(20),
    customer_id INT,
    model VARCHAR(50),
    service_date DATE,
    service_type VARCHAR(10),
    created_at TIMESTAMP
);