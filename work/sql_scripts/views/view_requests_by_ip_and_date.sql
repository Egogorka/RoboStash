CREATE OR REPLACE VIEW view_requests_by_ip_and_date AS -- пункт 6
SELECT
    ip.ip_address,
    fl.date,
    COUNT(*) AS count
FROM fact_logs fl
JOIN dim_ip ip ON fl.ip_id = ip.id
GROUP BY ip.ip_address, fl.date
ORDER BY ip.ip_address, fl.date;





