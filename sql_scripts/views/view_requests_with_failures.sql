CREATE OR REPLACE VIEW view_requests_with_failures AS
SELECT
    ip.ip_address,
    fl.date,
    COUNT(*) AS count,
    -- Подсчёт отказов, используя поле is_failed_request
    COUNT(CASE WHEN fl.is_failed_request = TRUE THEN 1 END) AS failure_count,
    -- Общее количество запросов для этого IP
    SUM(COUNT(*)) OVER (PARTITION BY ip.ip_address) AS total_requests
FROM fact_logs fl
JOIN dim_ip ip ON fl.ip_id = ip.id
GROUP BY ip.ip_address, fl.date
ORDER BY ip.ip_address, fl.date;