-- Протоколы
INSERT INTO dim_protocol (name)
SELECT DISTINCT protocol
FROM staging_logs
ON CONFLICT DO NOTHING;