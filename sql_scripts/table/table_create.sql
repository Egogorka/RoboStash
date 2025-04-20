-- Таблица для хранения уникальных IP-адресов
CREATE TABLE dim_ip (
    id SERIAL PRIMARY KEY,  -- Уникальный идентификатор IP-адреса
    ip_address VARCHAR(45) UNIQUE NOT NULL  -- IP-адрес (максимальная длина для IPv6)
);

-- Таблица для хранения типов запросов
CREATE TABLE dim_request_type (
    id SERIAL PRIMARY KEY,  -- Уникальный идентификатор типа запроса
    name VARCHAR(10) UNIQUE NOT NULL  -- Тип запроса (GET, POST, PUT, DELETE и т.д.)
);

-- Таблица для хранения информации о API
CREATE TABLE dim_api (
    id SERIAL PRIMARY KEY,  -- Уникальный идентификатор API
    path TEXT UNIQUE NOT NULL  -- Путь API
);

-- Таблица для хранения информации о протоколах
CREATE TABLE dim_protocol (
    id SERIAL PRIMARY KEY,  -- Уникальный идентификатор протокола
    name VARCHAR(20) UNIQUE NOT NULL  -- Название протокола (например, HTTP, HTTPS)
);

-- Таблица для хранения информации о реферерах
CREATE TABLE dim_referer (
    id SERIAL PRIMARY KEY,  -- Уникальный идентификатор реферера
    url TEXT UNIQUE DEFAULT NULL  -- URL реферера, может быть NULL
);

-- Таблица для хранения типов устройств
CREATE TABLE dim_device_type (
    id SERIAL PRIMARY KEY,  -- Уникальный идентификатор типа устройства
    name VARCHAR(10) UNIQUE NOT NULL  -- Тип устройства (PC, мобильное устройство, планшет и т.д.)
);

-- Таблица для хранения информации о User-Agent'ах
CREATE TABLE dim_user_agent (
    id SERIAL PRIMARY KEY,  -- Уникальный идентификатор User-Agent'а
    ua TEXT UNIQUE NOT NULL,  -- Строка User-Agent
    device_brand VARCHAR(100) DEFAULT NULL,  -- Марка устройства (если доступно)
    device_model VARCHAR(100) DEFAULT NULL,  -- Модель устройства (если доступно)
    os_family VARCHAR(100) DEFAULT NULL,  -- Семейство операционной системы (например, Windows, Linux)
    os_version VARCHAR(50) DEFAULT NULL,  -- Версия операционной системы
    browser_family VARCHAR(100) DEFAULT NULL,  -- Семейство браузера (например, Chrome, Firefox)
    browser_version VARCHAR(50) DEFAULT NULL,  -- Версия браузера
    device_type_id SMALLINT REFERENCES dim_device_type(id)  -- Ссылка на тип устройства из таблицы dim_device_type
);

-- Основная таблица для фактических логов
CREATE TABLE fact_logs (
    id SERIAL PRIMARY KEY,  -- Уникальный идентификатор записи в логе
    ip_id INT REFERENCES dim_ip(id) NOT NULL,  -- Ссылка на IP-адрес из таблицы dim_ip
    datetime TIMESTAMPTZ NOT NULL,  -- Дата и время запроса с учётом временной зоны
    year SMALLINT NOT NULL CHECK (year >= 1000 AND year <= 9999),  -- Год запроса
    month SMALLINT NOT NULL CHECK (month >= 1 AND month <= 12),  -- Месяц запроса
    day SMALLINT NOT NULL CHECK (day >= 1 AND day <= 31),  -- День запроса
    request_type_id SMALLINT REFERENCES dim_request_type(id) NOT NULL,  -- Ссылка на тип запроса из таблицы dim_request_type
    api_id INT REFERENCES dim_api(id) NOT NULL,  -- Ссылка на API из таблицы dim_api
    protocol_id INT REFERENCES dim_protocol(id) NOT NULL,  -- Ссылка на протокол из таблицы dim_protocol
    referer_id INT DEFAULT NULL REFERENCES dim_referer(id),  -- Ссылка на реферер из таблицы dim_referer (может быть NULL)
    user_agent_id INT NOT NULL REFERENCES dim_user_agent(id),  -- Ссылка на User-Agent из таблицы dim_user_agent
    status_code INT NOT NULL,  -- Код статуса HTTP-ответа
    response_size INT NOT NULL,  -- Размер ответа
    response_time INT,  -- Время отклика в миллисекундах
    is_failed_request BOOLEAN,  -- Признак неудачного запроса
    remote_user TEXT DEFAULT NULL,  -- Имя удалённого пользователя (если доступно)
    user_id TEXT DEFAULT NULL,  -- Идентификатор пользователя (если доступно)

    -- Уникальность записи для конкретного IP, времени и типа запроса
    CONSTRAINT unique_ip_datetime_request UNIQUE (ip_id, datetime, request_type_id)
);

-- Вставляем возможные типы запросов
INSERT INTO dim_request_type (name) VALUES
('GET'),  -- Запрос для получения данных
('POST'),  -- Запрос для отправки данных
('PUT'),  -- Запрос для обновления данных
('DELETE');  -- Запрос для удаления данных

-- Вставляем возможные типы устройств
INSERT INTO dim_device_type (name) VALUES
('PC'),  -- Персональный компьютер
('mobile'),  -- Мобильное устройство
('tablet'),  -- Планшет
('bot'),  -- Бот (например, поисковый робот)
('other');  -- Прочие устройства (например, устройства IoT)

-- Комментарии к таблицам и полям

-- Комментарии для таблицы dim_ip
COMMENT ON TABLE dim_ip IS 'Таблица для хранения уникальных IP-адресов.';
COMMENT ON COLUMN dim_ip.id IS 'Уникальный идентификатор IP-адреса.';
COMMENT ON COLUMN dim_ip.ip_address IS 'IP-адрес (максимальная длина для IPv6).';

-- Комментарии для таблицы dim_request_type
COMMENT ON TABLE dim_request_type IS 'Таблица для хранения типов запросов (GET, POST, PUT, DELETE).';
COMMENT ON COLUMN dim_request_type.id IS 'Уникальный идентификатор типа запроса.';
COMMENT ON COLUMN dim_request_type.name IS 'Тип запроса (GET, POST, PUT, DELETE и т.д.).';

-- Комментарии для таблицы dim_api
COMMENT ON TABLE dim_api IS 'Таблица для хранения информации о API.';
COMMENT ON COLUMN dim_api.id IS 'Уникальный идентификатор API.';
COMMENT ON COLUMN dim_api.path IS 'Путь API.';

-- Комментарии для таблицы dim_protocol
COMMENT ON TABLE dim_protocol IS 'Таблица для хранения информации о протоколах.';
COMMENT ON COLUMN dim_protocol.id IS 'Уникальный идентификатор протокола.';
COMMENT ON COLUMN dim_protocol.name IS 'Название протокола (например, HTTP, HTTPS).';

-- Комментарии для таблицы dim_referer
COMMENT ON TABLE dim_referer IS 'Таблица для хранения информации о реферерах.';
COMMENT ON COLUMN dim_referer.id IS 'Уникальный идентификатор реферера.';
COMMENT ON COLUMN dim_referer.url IS 'URL реферера, может быть NULL.';

-- Комментарии для таблицы dim_device_type
COMMENT ON TABLE dim_device_type IS 'Таблица для хранения типов устройств (ПК, мобильное устройство, планшет и т.д.).';
COMMENT ON COLUMN dim_device_type.id IS 'Уникальный идентификатор типа устройства.';
COMMENT ON COLUMN dim_device_type.name IS 'Тип устройства (ПК, мобильное устройство, планшет и т.д.).';

-- Комментарии для таблицы dim_user_agent
COMMENT ON TABLE dim_user_agent IS 'Таблица для хранения информации о строках User-Agent.';
COMMENT ON COLUMN dim_user_agent.id IS 'Уникальный идентификатор User-Agent.';
COMMENT ON COLUMN dim_user_agent.ua IS 'Строка User-Agent.';
COMMENT ON COLUMN dim_user_agent.device_brand IS 'Марка устройства (если доступно).';
COMMENT ON COLUMN dim_user_agent.device_model IS 'Модель устройства (если доступно).';
COMMENT ON COLUMN dim_user_agent.os_family IS 'Семейство операционной системы (например, Windows, Linux).';
COMMENT ON COLUMN dim_user_agent.os_version IS 'Версия операционной системы.';
COMMENT ON COLUMN dim_user_agent.browser_family IS 'Семейство браузера (например, Chrome, Firefox).';
COMMENT ON COLUMN dim_user_agent.browser_version IS 'Версия браузера.';
COMMENT ON COLUMN dim_user_agent.device_type_id IS 'Ссылка на тип устройства из таблицы dim_device_type.';

-- Комментарии для таблицы fact_logs
COMMENT ON TABLE fact_logs IS 'Основная таблица для фактических логов.';
COMMENT ON COLUMN fact_logs.id IS 'Уникальный идентификатор записи в логе.';
COMMENT ON COLUMN fact_logs.ip_id IS 'Ссылка на IP-адрес из таблицы dim_ip.';
COMMENT ON COLUMN fact_logs.datetime IS 'Дата и время запроса с учётом временной зоны.';
COMMENT ON COLUMN fact_logs.year IS 'Год запроса.';
COMMENT ON COLUMN fact_logs.month IS 'Месяц запроса.';
COMMENT ON COLUMN fact_logs.day IS 'День запроса.';
COMMENT ON COLUMN fact_logs.request_type_id IS 'Ссылка на тип запроса из таблицы dim_request_type.';
COMMENT ON COLUMN fact_logs.api_id IS 'Ссылка на API из таблицы dim_api.';
COMMENT ON COLUMN fact_logs.protocol_id IS 'Ссылка на протокол из таблицы dim_protocol.';
COMMENT ON COLUMN fact_logs.referer_id IS 'Ссылка на реферер из таблицы dim_referer (может быть NULL).';
COMMENT ON COLUMN fact_logs.user_agent_id IS 'Ссылка на User-Agent из таблицы dim_user_agent.';
COMMENT ON COLUMN fact_logs.status_code IS 'Код статуса HTTP-ответа.';
COMMENT ON COLUMN fact_logs.response_size IS 'Размер ответа.';
COMMENT ON COLUMN fact_logs.response_time IS 'Время отклика в миллисекундах.';
COMMENT ON COLUMN fact_logs.is_failed_request IS 'Признак неудачного запроса.';
COMMENT ON COLUMN fact_logs.remote_user IS 'Имя удалённого пользователя (если доступно).';
COMMENT ON COLUMN fact_logs.user_id IS 'Идентификатор пользователя (если доступно).';
