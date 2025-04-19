-- IP адреса
INSERT INTO dim_ip (ip_address)
SELECT DISTINCT ip_address
FROM staging_logs
ON CONFLICT DO NOTHING;