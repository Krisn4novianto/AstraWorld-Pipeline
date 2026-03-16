CREATE TABLE IF NOT EXISTS dwh.fact_sales (
    vin VARCHAR(50),
    customer_id INT,
    model VARCHAR(100),
    date_id DATE,
    amount NUMERIC(18,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);