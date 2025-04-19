-- Сводка по коду ответа
CREATE OR REPLACE VIEW view_status_code_summary AS
SELECT
    fl.status_code,
    COUNT(*) AS total_requests,
    SUM(CASE WHEN fl.is_failed_request THEN 1 ELSE 0 END) AS failures,
    ROUND(SUM(CASE WHEN fl.is_failed_request THEN 1 ELSE 0 END)::numeric / COUNT(*), 3) AS failure_rate
FROM fact_logs fl
GROUP BY fl.status_code
ORDER BY fl.status_code;
