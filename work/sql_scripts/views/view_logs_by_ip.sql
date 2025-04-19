CREATE OR REPLACE VIEW view_logs_by_ip AS
SELECT
    ip.ip_address,
    fl.date,
    fl.t,
    drt.name AS request_type,
    da.path AS api_path,
    dp.name AS protocol,
    fl.status_code,
    fl.response_time,
    fl.response_size,
    dr.url AS referer,
    fl.is_failed_request
FROM fact_logs fl
JOIN dim_ip ip ON fl.ip_id = ip.id
JOIN dim_request_type drt ON fl.request_type_id = drt.id
JOIN dim_api da ON fl.api_id = da.id
JOIN dim_protocol dp ON fl.protocol_id = dp.id
LEFT JOIN dim_referer dr ON fl.referer_id = dr.id;
