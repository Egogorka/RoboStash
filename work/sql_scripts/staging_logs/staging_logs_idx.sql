-- создание индексов staging_logs
-- Ускоряет JOIN по IP
CREATE INDEX idx_staging_logs_ip_address ON staging_logs (ip_address);

-- Ускоряет JOIN по User-Agent 
-- (UNIQUE уже создаёт btree-индекс)
-- CREATE UNIQUE INDEX idx_staging_logs_ua ON staging_logs (ua);

-- Ускоряет JOIN по типу запроса (GET, POST и т.п.)
CREATE INDEX idx_staging_logs_request_type ON staging_logs (request_type);

-- Ускоряет JOIN по пути API
CREATE INDEX idx_staging_logs_api_path ON staging_logs (api_path);

-- Ускоряет JOIN по протоколу (HTTP/1.1, HTTP/2 и т.п.)
CREATE INDEX idx_staging_logs_protocol ON staging_logs (protocol);

-- Ускоряет JOIN по типу устройства
CREATE INDEX idx_staging_logs_device_type ON staging_logs (device_type);

-- Ускоряет JOIN по дате и возможно фильтрацию по диапазону
CREATE INDEX idx_staging_logs_date ON staging_logs (date);

