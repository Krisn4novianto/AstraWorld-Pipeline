CREATE SCHEMA IF NOT EXISTS staging;

CREATE TABLE IF NOT EXISTS staging.customer_addresses (
    id INT,
    customer_id INT,
    address TEXT,
    city VARCHAR(100),
    province VARCHAR(100),
    created_at TIMESTAMP,
    file_date DATE
);


DELETE FROM staging.customer_addresses
WHERE file_date = {{file_date}};

INSERT INTO staging.customer_addresses (id, customer_id, address, city, province, created_at, file_date)
SELECT
    id,
    customer_id,
    TRIM(address) AS address,
    UPPER(city) AS city,
    UPPER(province) AS province,
    created_at,
    file_date
FROM public.customer_addresses
WHERE address IS NOT NULL
  AND file_date = {{file_date}};