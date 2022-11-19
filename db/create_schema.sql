CREATE TABLE IF NOT EXISTS users
(
    user_id       SERIAL PRIMARY KEY,
    username      VARCHAR(64) UNIQUE NOT NULL,
    password      VARCHAR(64) NOT NULL,
    uuid          VARCHAR(32) UNIQUE NOT NULL
);
CREATE INDEX ON users(username);

CREATE TABLE IF NOT EXISTS roles
(
    role_id       SERIAL PRIMARY KEY,
    role_name     TEXT CHECK (role_name IN ('admin', 'user'))
);
