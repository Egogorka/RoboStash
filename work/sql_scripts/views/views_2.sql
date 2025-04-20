
-----------------------------------------------------------
CREATE OR REPLACE VIEW view_response_time_by_ip_month AS
SELECT
    di.ip_address,
    fl.year,
    fl.month,
    AVG(fl.response_time) AS avg_response_time,
    MAX(fl.response_time) AS max_response_time
FROM
    fact_logs fl
    JOIN dim_ip di ON fl.ip_id = di.id
GROUP BY
    di.ip_address, fl.year, fl.month
ORDER BY
    fl.year, fl.month, max_response_time DESC;
----------------------------------------------------------
CREATE OR REPLACE VIEW view_response_time_by_ip_day AS
SELECT
    di.ip_address,
    MAKE_DATE(fl.year, fl.month, fl.day) AS response_date,
    AVG(fl.response_time) AS avg_response_time,
    MAX(fl.response_time) AS max_response_time
FROM
    fact_logs fl
    JOIN dim_ip di ON fl.ip_id = di.id
GROUP BY
    di.ip_address, fl.year, fl.month, fl.day
ORDER BY
    fl.year, fl.month, fl.day, max_response_time DESC;
------------------------------------------------------------------
CREATE OR REPLACE VIEW view_requests_by_ip_month AS
SELECT
    ip.ip_address,
    fl.year,
    fl.month,
    COUNT(*) AS count,
    -- Подсчёт отказов, используя поле is_failed_request
    COUNT(CASE WHEN fl.is_failed_request = TRUE THEN 1 END) AS failure_count,
    -- Общее количество запросов для этого IP
    SUM(COUNT(*)) OVER (PARTITION BY ip.ip_address) AS total_requests
FROM fact_logs fl
JOIN dim_ip ip ON fl.ip_id = ip.id
GROUP BY ip.ip_address, fl.year, fl.month
ORDER BY ip.ip_address, fl.year, fl.month;
------------------------------------------------------------------------
CREATE OR REPLACE VIEW view_requests_by_ip_day AS
SELECT
    ip.ip_address,
    MAKE_DATE(fl.year, fl.month, fl.day) as date,
    COUNT(*) AS count,
    -- Подсчёт отказов, используя поле is_failed_request
    COUNT(CASE WHEN fl.is_failed_request = TRUE THEN 1 END) AS failure_count,
FROM fact_logs fl
JOIN dim_ip ip ON fl.ip_id = ip.id
GROUP BY fl.ip_id, fl.year, fl.month, fl.day
ORDER BY fl.ip_id, fl.year, fl.month, fl.day;
