CREATE TABLE dim_ip (
    id SERIAL PRIMARY KEY,
    ip_address VARCHAR(45) UNIQUE NOT NULL
);

CREATE TABLE dim_request_type (
    id SERIAL PRIMARY KEY,
    name VARCHAR(10) UNIQUE NOT NULL
);

CREATE TABLE dim_api (
    id SERIAL PRIMARY KEY,
    path TEXT UNIQUE NOT NULL
);

CREATE TABLE dim_protocol (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE dim_referer (
    id SERIAL PRIMARY KEY,
    url TEXT UNIQUE DEFAULT NULL
);

CREATE TABLE dim_device_type (
    id SERIAL PRIMARY KEY,
    name VARCHAR(10) UNIQUE NOT NULL
);

CREATE TABLE dim_user_agent (
    id SERIAL PRIMARY KEY,
    ua TEXT UNIQUE NOT NULL,
    device_brand VARCHAR(100) DEFAULT NULL,
    device_model VARCHAR(100) DEFAULT NULL,
    os_family VARCHAR(100) DEFAULT NULL,
    os_version VARCHAR(50) DEFAULT NULL,
    browser_family VARCHAR(100) DEFAULT NULL,
    browser_version VARCHAR(50) DEFAULT NULL,
    device_type_id SMALLINT REFERENCES dim_device_type(id)
);

CREATE TABLE fact_logs (
    id SERIAL PRIMARY KEY,
    ip_id INT REFERENCES dim_ip(id) NOT NULL,
    datetime TIMESTAMPTZ NOT NULL,
    year SMALLINT NOT NULL CHECK (year >= 1000 AND year <= 9999),
    month SMALLINT NOT NULL CHECK (month >= 1 AND month <= 12),
    day SMALLINT NOT NULL CHECK (day >= 1 AND day <= 31),
    request_type_id SMALLINT REFERENCES dim_request_type(id) NOT NULL,
    api_id INT REFERENCES dim_api(id) NOT NULL,
    protocol_id INT REFERENCES dim_protocol(id) NOT NULL,
    referer_id INT DEFAULT NULL REFERENCES dim_referer(id),
    user_agent_id INT NOT NULL REFERENCES dim_user_agent(id),
    status_code INT NOT NULL,
    response_size INT NOT NULL,
    response_time INT,
    is_failed_request BOOLEAN,
    remote_user TEXT DEFAULT NULL,
    user_id TEXT DEFAULT NULL
);

-- Вставляем возможные типы запросов
INSERT INTO dim_request_type (name) VALUES
('GET'),
('POST'),
('PUT'),
('DELETE');

-- Вставляем возможные типы устройств
INSERT INTO dim_device_type (name) VALUES
('PC'),
('mobile'),
('tablet'),
('bot'),
('other');