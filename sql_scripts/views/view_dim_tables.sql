-- Представление для таблицы dim_ip
CREATE OR REPLACE VIEW view_dim_ip AS
SELECT * FROM dim_ip;

-- Представление для таблицы dim_request_type
CREATE OR REPLACE VIEW view_dim_request_type AS
SELECT * FROM dim_request_type;

-- Представление для таблицы dim_api
CREATE OR REPLACE VIEW view_dim_api AS
SELECT * FROM dim_api;

-- Представление для таблицы dim_protocol
CREATE OR REPLACE VIEW view_dim_protocol AS
SELECT * FROM dim_protocol;

-- Представление для таблицы dim_referer
CREATE OR REPLACE VIEW view_dim_referer AS
SELECT * FROM dim_referer;

-- Представление для таблицы dim_device_type
CREATE OR REPLACE VIEW view_dim_device_type AS
SELECT * FROM dim_device_type;

-- Представление для таблицы dim_user_agent
CREATE OR REPLACE VIEW view_dim_user_agent AS
SELECT * FROM dim_user_agent;

-- Комментарии к представлениям
COMMENT ON VIEW view_dim_ip IS 'Представление для справочника уникальных IP-адресов.';
COMMENT ON VIEW view_dim_request_type IS 'Представление для справочника типов HTTP-запросов (GET, POST и т.д.).';
COMMENT ON VIEW view_dim_api IS 'Представление для справочника API (пути запросов).';
COMMENT ON VIEW view_dim_protocol IS 'Представление для справочника протоколов (HTTP, HTTPS и т.д.).';
COMMENT ON VIEW view_dim_referer IS 'Представление для справочника рефереров.';
COMMENT ON VIEW view_dim_device_type IS 'Представление для справочника типов устройств.';
COMMENT ON VIEW view_dim_user_agent IS 'Представление для справочника строк User-Agent.';
