-- IP адреса
INSERT INTO dim_ip (ip_address)
SELECT DISTINCT ip_address
FROM staging_logs
ON CONFLICT DO NOTHING;

-- API пути
INSERT INTO dim_api (path)
SELECT DISTINCT api_path
FROM staging_logs
ON CONFLICT DO NOTHING;

-- Протоколы
INSERT INTO dim_protocol (name)
SELECT DISTINCT protocol
FROM staging_logs
ON CONFLICT DO NOTHING;

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
JOIN dim_device_type d ON s.device_type = d.name
ON CONFLICT DO NOTHING;

-- Referer — игнорируем, но NULL оставляем как есть
INSERT INTO dim_referer (url)
SELECT DISTINCT NULL
WHERE FALSE;  -- ничего не вставит

-- Факт-таблица
INSERT INTO fact_logs (
    ip_id,
    date,
    year,
    month,
    t,
    request_type_id,
    api_id,
    protocol_id,
    referer_id,
    user_agent_id,
    status_code,
    response_size,
    response_time,
    is_failed_request,
    remote_user,
    user_id
)
SELECT
    di.id,
    sl.date,
    EXTRACT(YEAR FROM sl.date)::SMALLINT,
    EXTRACT(MONTH FROM sl.date)::SMALLINT,
    sl.t,
    drt.id,
    da.id,
    dp.id,
    NULL AS referer_id,
    dua.id,
    sl.status_code,
    sl.response_size,
    sl.response_time,
    (sl.status_code >= 400) AS is_failed_request,
    NULL AS remote_user,
    NULL AS user_id
FROM staging_logs sl
JOIN dim_ip di ON sl.ip_address = di.ip_address
JOIN dim_request_type drt ON sl.request_type = drt.name
JOIN dim_api da ON sl.api_path = da.path
JOIN dim_protocol dp ON sl.protocol = dp.name
JOIN dim_user_agent dua ON sl.ua = dua.ua;
