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
    dr.id AS referer_id,
    dua.id,
    sl.status_code,
    sl.response_size,
    sl.response_time,
    (sl.status_code >= 400) AS is_failed_request,
    sl.remote_user,
    sl.user_id
FROM staging_logs sl
JOIN dim_ip di ON sl.ip_address = di.ip_address
JOIN dim_request_type drt ON sl.request_type = drt.name
JOIN dim_api da ON sl.api_path = da.path
JOIN dim_protocol dp ON sl.protocol = dp.name
LEFT JOIN dim_referer dr ON sl.referer_url = dr.url  -- <-- LEFT JOIN для referer
JOIN dim_user_agent dua ON sl.ua = dua.ua;
