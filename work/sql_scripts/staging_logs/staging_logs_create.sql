-- создание staging_logs
CREATE TABLE staging_logs (
    id SERIAL PRIMARY KEY,
    ip_address VARCHAR(45),
    date DATE,
    t TIME,
    request_type VARCHAR(10),
    api_path TEXT DEFAULT NULL,
    protocol VARCHAR(20),
    referer_url TEXT default null,
    ua TEXT NOT NULL,
    device_brand VARCHAR(100) DEFAULT NULL,
    device_model VARCHAR(100) DEFAULT NULL,
    os_family VARCHAR(100) DEFAULT NULL,
    os_version VARCHAR(50) DEFAULT NULL,
    browser_family VARCHAR(100) DEFAULT NULL,
    browser_version VARCHAR(50) DEFAULT NULL,
    device_type VARCHAR(10),
    status_code INT,
    response_size INT,
    response_time INT,
    remote_user TEXT DEFAULT NULL,
    user_id TEXT DEFAULT NULL
);
