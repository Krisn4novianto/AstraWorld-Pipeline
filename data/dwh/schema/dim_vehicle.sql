CREATE TABLE IF NOT EXISTS dwh.dim_vehicle (
    vehicle_key SERIAL PRIMARY KEY,
    vehicle_id VARCHAR(50) UNIQUE,
    brand VARCHAR(100),
    model VARCHAR(100),
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);