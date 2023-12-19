CREATE USER test_user WITH PASSWORD 'postgresql';

CREATE DATABASE test_db;

\c test_db

CREATE SCHEMA recipe;

ALTER SCHEMA recipe OWNER TO test_user;

GRANT ALL PRIVILEGES ON DATABASE test_db TO test_user;

GRANT ALL PRIVILEGES ON SCHEMA recipe TO test_user;