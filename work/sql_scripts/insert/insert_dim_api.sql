-- API пути
INSERT INTO dim_api (path)
SELECT DISTINCT api_path
FROM staging_logs
ON CONFLICT DO NOTHING;