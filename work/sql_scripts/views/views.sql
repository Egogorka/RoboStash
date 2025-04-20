-- 0. Представление: Количество запросов и отказов по каждому IP и дню
-- используется для пункта 3
CREATE OR REPLACE VIEW view_requests_by_ip_day AS
SELECT
    ip.ip_address, -- IP-адрес клиента
    MAKE_DATE(fl.year, fl.month, fl.day) as date, -- Дата запроса (год, месяц, день)
    COUNT(*) AS count, -- Общее количество запросов от IP в этот день
FROM fact_logs fl
JOIN dim_ip ip ON fl.ip_id = ip.id
GROUP BY ip.ip_address, fl.year, fl.month, fl.day
ORDER BY ip.ip_address, fl.year, fl.month, fl.day;


-- 1. Представление: Общее количество запросов по каждому дню
CREATE OR REPLACE VIEW view_count_requests_by_day AS
SELECT
    MAKE_DATE(fl.year, fl.month, fl.day) AS date, -- Дата запроса
    COUNT(*) AS total_requests -- Общее количество запросов ко всем серверам в этот день
FROM fact_logs AS fl
GROUP BY fl.year, fl.month, fl.day
ORDER BY date; -- Сортировка по дате (убрана ошибка с ORDER BY count)


-- 2. Представление: Топ IP-адресов по количеству запросов
CREATE OR REPLACE VIEW view_top_ips AS
SELECT
    ip.ip_address, -- IP-адрес клиента
    COUNT(*) AS total_requests -- Общее количество запросов с этого IP-адреса
FROM fact_logs fl
JOIN dim_ip ip ON fl.ip_id = ip.id
GROUP BY ip.ip_address
ORDER BY total_requests DESC; -- Сортировка от самых активных IP


-- 3. Представление: Сводная информация по IP-адресу
CREATE OR REPLACE VIEW view_count_ip_requests AS
SELECT
    ip.ip_address AS ip, -- IP-адрес клиента
    proto.name AS protocol, -- Используемый протокол (например, HTTP, HTTPS)
    dt.name AS device_type, -- Тип устройства (например, смартфон, ПК)
    ua.os_family, -- Операционная система (семейство), например Windows, Android
    ua.os_version, -- Версия ОС
    ua.browser_family, -- Браузер (семейство), например Chrome, Safari
    ua.browser_version, -- Версия браузера
    ua.device_brand, -- Бренд устройства
    ua.device_model, -- Модель устройства
    COUNT(*) AS total -- Общее количество запросов с таким сочетанием IP, устройства, ОС и браузера
FROM fact_logs f
JOIN dim_ip ip ON f.ip_id = ip.id
JOIN dim_protocol proto ON f.protocol_id = proto.id
JOIN dim_user_agent ua ON f.user_agent_id = ua.id
JOIN dim_device_type dt ON ua.device_type_id = dt.id
GROUP BY ip.ip_address, proto.name, dt.name,
         ua.os_family, ua.os_version, ua.browser_family,
         ua.browser_version, ua.device_brand, ua.device_model
ORDER BY total DESC; -- Сортировка по популярности сочетания


-- 4. Представление: Количество неуспешных запросов по дням
CREATE OR REPLACE VIEW view_count_failed_requests_by_day AS
SELECT
    MAKE_DATE(fl.year, fl.month, fl.day) AS date, -- Дата
    COUNT(*) AS total_failed -- Количество неуспешных запросов (is_failed_request = TRUE)
FROM fact_logs fl
WHERE fl.is_failed_request = TRUE
GROUP BY fl.year, fl.month, fl.day
ORDER BY date;


-- 5. Представление: Количество запросов по каждому статус-коду
CREATE OR REPLACE VIEW view_count_status_code AS
SELECT
    status_code, -- HTTP статус-код ответа (например, 200, 404, 500)
    COUNT(*) AS total -- Общее количество запросов с этим статус-кодом
FROM fact_logs
GROUP BY status_code
ORDER BY total DESC; -- Сортировка по убыванию частоты

-- Комментарии к представлению view_requests_by_ip_day
COMMENT ON VIEW view_requests_by_ip_day IS 'Количество запросов и отказов по каждому IP и дню';
COMMENT ON COLUMN view_requests_by_ip_day.ip_address IS 'IP-адрес клиента';
COMMENT ON COLUMN view_requests_by_ip_day.date IS 'Дата запроса (год, месяц, день)';
COMMENT ON COLUMN view_requests_by_ip_day.count IS 'Общее количество запросов от IP в этот день';
COMMENT ON COLUMN view_requests_by_ip_day.failure_count IS 'Количество неуспешных (ошибочных) запросов от IP в этот день';


-- Комментарии к представлению view_count_requests_by_day
COMMENT ON VIEW view_count_requests_by_day IS 'Общее количество запросов по каждому дню';
COMMENT ON COLUMN view_count_requests_by_day.date IS 'Дата запроса';
COMMENT ON COLUMN view_count_requests_by_day.total_requests IS 'Общее количество запросов ко всем серверам в этот день';


-- Комментарии к представлению view_top_ips
COMMENT ON VIEW view_top_ips IS 'Топ IP-адресов по количеству запросов';
COMMENT ON COLUMN view_top_ips.ip_address IS 'IP-адрес клиента';
COMMENT ON COLUMN view_top_ips.total_requests IS 'Общее количество запросов с этого IP-адреса';


-- Комментарии к представлению view_count_ip_requests
COMMENT ON VIEW view_count_ip_requests IS 'Сводная информация по IP-адресу и устройству';
COMMENT ON COLUMN view_count_ip_requests.ip IS 'IP-адрес клиента';
COMMENT ON COLUMN view_count_ip_requests.protocol IS 'Используемый протокол (например, HTTP, HTTPS)';
COMMENT ON COLUMN view_count_ip_requests.device_type IS 'Тип устройства (например, смартфон, ПК)';
COMMENT ON COLUMN view_count_ip_requests.os_family IS 'Операционная система (семейство), например Windows, Android';
COMMENT ON COLUMN view_count_ip_requests.os_version IS 'Версия операционной системы';
COMMENT ON COLUMN view_count_ip_requests.browser_family IS 'Браузер (семейство), например Chrome, Safari';
COMMENT ON COLUMN view_count_ip_requests.browser_version IS 'Версия браузера';
COMMENT ON COLUMN view_count_ip_requests.device_brand IS 'Бренд устройства';
COMMENT ON COLUMN view_count_ip_requests.device_model IS 'Модель устройства';
COMMENT ON COLUMN view_count_ip_requests.total IS 'Общее количество запросов с таким сочетанием IP, устройства, ОС и браузера';


-- Комментарии к представлению view_count_failed_requests_by_day
COMMENT ON VIEW view_count_failed_requests_by_day IS 'Количество неуспешных запросов по дням';
COMMENT ON COLUMN view_count_failed_requests_by_day.date IS 'Дата';
COMMENT ON COLUMN view_count_failed_requests_by_day.total_failed IS 'Количество неуспешных запросов (is_failed_request = TRUE)';


-- Комментарии к представлению view_count_status_code
COMMENT ON VIEW view_count_status_code IS 'Количество запросов по каждому статус-коду';
COMMENT ON COLUMN view_count_status_code.status_code IS 'HTTP статус-код ответа (например, 200, 404, 500)';
COMMENT ON COLUMN view_count_status_code.total IS 'Общее количество запросов с этим статус-кодом';
