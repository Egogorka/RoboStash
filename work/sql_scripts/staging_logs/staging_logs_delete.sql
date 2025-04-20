-- удаление staging_logs
DROP TABLE IF EXISTS staging_logs;

-- кластеризация fact_logs
-- CLUSTER fact_logs USING idx_fact_logs_date;
