CREATE OR REPLACE VIEW view_fact_logs AS -- полное представление всей таблицы
SELECT 
    fl.id AS log_id,
    di.ip_address AS ip_address,
    fl.date,
    fl.year,
    fl.month,
    fl.t AS request_time,
    drt.name AS request_type,
    da.path AS api_path,
    dp.name AS protocol_name,
    COALESCE(dr.url, NULL) AS referer_url,  -- Если referer_id IS NULL, выводим '-'
    dua.ua AS user_agent,
    dua.device_brand,
    dua.device_model,
    dua.os_family,
    dua.os_version,
    dua.browser_family,
    dua.browser_version,
    ddt.name AS device_type,
    fl.status_code,
    fl.response_size,
    fl.response_time,
    fl.is_failed_request,
    fl.remote_user,
    fl.user_id
FROM 
    fact_logs fl
    LEFT JOIN dim_ip di ON fl.ip_id = di.id
    LEFT JOIN dim_request_type drt ON fl.request_type_id = drt.id
    LEFT JOIN dim_api da ON fl.api_id = da.id
    LEFT JOIN dim_protocol dp ON fl.protocol_id = dp.id
    LEFT JOIN dim_referer dr ON fl.referer_id = dr.id
    LEFT JOIN dim_user_agent dua ON fl.user_agent_id = dua.id
    LEFT JOIN dim_device_type ddt ON dua.device_type_id = ddt.id;  