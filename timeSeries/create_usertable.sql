CREATE TABLE user_table (
    username VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    electricity_meter VARCHAR NOT NULL,
    confirm_email BOOLEAN NOT NULL,
    creat_time TIMESTAMP NULL,
    last_login TIMESTAMP NULL,
    daylimit INT NULL,
    monthlimit INT NULL,
    PRIMARY KEY (username)
);