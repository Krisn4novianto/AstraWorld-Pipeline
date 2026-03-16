INSERT INTO dwh.dim_vehicle (
    vehicle_id,
    brand,
    model,
    category
)

SELECT DISTINCT
    vin AS vehicle_id,
    'Toyota' AS brand,
    model,

    CASE
        WHEN model IN ('RAIZA', 'RANGGO') THEN 'SUV'
        WHEN model IN ('INNAVO', 'VELOS') THEN 'MPV'
        ELSE 'OTHER'
    END AS category

FROM (
    SELECT vin, model FROM public.sales_raw
    UNION
    SELECT vin, model FROM public.after_sales_raw
) src

ON CONFLICT (vehicle_id) DO NOTHING;