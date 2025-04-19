CREATE OR REPLACE VIEW view_response_time_stats AS
SELECT
    di.ip_address,
    fl.date,
    AVG(fl.response_time) AS avg_response_time,
    MAX(fl.response_time) AS max_response_time
FROM
    fact_logs fl
    JOIN dim_ip di ON fl.ip_id = di.id
GROUP BY
    di.ip_address, fl.date
ORDER BY
    di.ip_address, fl.date;
