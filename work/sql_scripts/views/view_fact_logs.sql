CREATE OR REPLACE VIEW view_fact_logs AS -- полное представление всей таблицы
SELECT 
    fl.id AS log_id,
    di.ip_address AS ip_address,
    fl.datetime,
    fl.year,
    fl.month,
    fl.day,
    drt.name AS request_type,
    da.path AS api_path,
    dp.name AS protocol_name,
    COALESCE(dr.url, NULL) AS referer_url,  -- Если referer_id IS NULL, выводим '-'
    dua.ua AS user_agent,
    dua.device_brand,
    dua.device_model,
    dua.os_family,
    dua.os_version,
    dua.browser_family,
    dua.browser_version,
    ddt.name AS device_type,
    fl.status_code,
    fl.response_size,
    fl.response_time,
    fl.is_failed_request,
    fl.remote_user,
    fl.user_id
FROM
    fact_logs fl
    LEFT JOIN dim_ip di ON fl.ip_id = di.id
    LEFT JOIN dim_request_type drt ON fl.request_type_id = drt.id
    LEFT JOIN dim_api da ON fl.api_id = da.id
    LEFT JOIN dim_protocol dp ON fl.protocol_id = dp.id
    LEFT JOIN dim_referer dr ON fl.referer_id = dr.id
    LEFT JOIN dim_user_agent dua ON fl.user_agent_id = dua.id
    LEFT JOIN dim_device_type ddt ON dua.device_type_id = ddt.id;

-- Комментарии к представлению view_fact_logs
COMMENT ON VIEW view_fact_logs IS 'Полное представление таблицы fact_logs со связями и описанием всех полей';

COMMENT ON COLUMN view_fact_logs.log_id IS 'Уникальный идентификатор записи лога';
COMMENT ON COLUMN view_fact_logs.ip_address IS 'IP-адрес клиента, сделавшего запрос';
COMMENT ON COLUMN view_fact_logs.datetime IS 'Дата и время запроса';
COMMENT ON COLUMN view_fact_logs.year IS 'Год запроса';
COMMENT ON COLUMN view_fact_logs.month IS 'Месяц запроса';
COMMENT ON COLUMN view_fact_logs.day IS 'День запроса';
COMMENT ON COLUMN view_fact_logs.request_type IS 'Тип HTTP-запроса (GET, POST и т.д.)';
COMMENT ON COLUMN view_fact_logs.api_path IS 'Путь к API-методу';
COMMENT ON COLUMN view_fact_logs.protocol_name IS 'Протокол, использованный при запросе (например, HTTP, HTTPS)';
COMMENT ON COLUMN view_fact_logs.referer_url IS 'URL источника перехода (Referer), если есть';
COMMENT ON COLUMN view_fact_logs.user_agent IS 'Строка User-Agent запроса';
COMMENT ON COLUMN view_fact_logs.device_brand IS 'Бренд устройства клиента';
COMMENT ON COLUMN view_fact_logs.device_model IS 'Модель устройства клиента';
COMMENT ON COLUMN view_fact_logs.os_family IS 'Семейство операционной системы клиента';
COMMENT ON COLUMN view_fact_logs.os_version IS 'Версия операционной системы клиента';
COMMENT ON COLUMN view_fact_logs.browser_family IS 'Семейство браузера клиента';
COMMENT ON COLUMN view_fact_logs.browser_version IS 'Версия браузера клиента';
COMMENT ON COLUMN view_fact_logs.device_type IS 'Тип устройства (например, ПК, смартфон)';
COMMENT ON COLUMN view_fact_logs.status_code IS 'HTTP статус-код ответа сервера';
COMMENT ON COLUMN view_fact_logs.response_size IS 'Размер ответа сервера в байтах';
COMMENT ON COLUMN view_fact_logs.response_time IS 'Время обработки запроса сервером (мс)';
COMMENT ON COLUMN view_fact_logs.is_failed_request IS 'Флаг неуспешного запроса (true/false)';
COMMENT ON COLUMN view_fact_logs.remote_user IS 'Имя удалённого пользователя (если присутствует)';
COMMENT ON COLUMN view_fact_logs.user_id IS 'ID пользователя, если авторизован';
