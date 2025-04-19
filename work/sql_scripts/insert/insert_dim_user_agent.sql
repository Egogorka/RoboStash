-- User-Agent + парсинг и device_type (в NULL по ТЗ)
INSERT INTO dim_user_agent (
    ua, device_brand, device_model,
    os_family, os_version,
    browser_family, browser_version,
    device_type_id
)
SELECT DISTINCT
    s.ua,
    s.device_brand,
    s.device_model,
    s.os_family,
    s.os_version,
    s.browser_family,
    s.browser_version,
    d.id AS device_type_id
FROM staging_logs s
LEFT JOIN dim_device_type d ON s.device_type = d.name
ON CONFLICT DO NOTHING;