CREATE TABLE data_time (
    device_uuid uuid NOT NULL,
    generated_time TIMESTAMPTZ NOT NULL,
    normal_usage DOUBLE PRECISION NULL
);

SELECT create_hypertable('data_time', by_range('generated_time'));

CREATE INDEX id_time ON data_time (device_uuid, generated_time DESC);

CREATE TABLE user_table (
    username VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    electricity_meter VARCHAR NOT NULL,
    confirm_email BOOLEAN NOT NULL,
    creat_time TIMESTAMP NULL,
    last_login TIMESTAMP NULL,
    daylimit INT NULL,
    monthlimit INT NULL,
    period TIMESTAMP NOT NULL,
    PRIMARY KEY (username)
);