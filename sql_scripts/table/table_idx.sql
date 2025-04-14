-- Индексы по ip
CREATE INDEX idx_fact_logs_date ON fact_logs (ip_id, date);
--CLUSTER fact_logs USING idx_fact_logs_date;
CREATE INDEX idx_fact_logs_year_month ON fact_logs (ip_id, year, month);
-- для внешних ключей
CREATE INDEX idx_fact_logs_api_id ON fact_logs (api_id);
CREATE INDEX idx_fact_logs_request_type_id ON fact_logs (request_type_id);
CREATE INDEX idx_fact_logs_user_agent_id ON fact_logs (user_agent_id);
