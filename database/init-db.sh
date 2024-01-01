#!/bin/bash
set -e

# Substitute production environment variables and execute the SQL script
envsubst < /docker-entrypoint-initdb.d/init-prod-db.sql.template > /tmp/init-prod-db.sql
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" < /tmp/init-prod-db.sql

# Substitute the test environment variables and execute the SQL script
envsubst < /docker-entrypoint-initdb.d/init-test-db.sql.template > /tmp/init-test-db.sql
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" < /tmp/init-test-db.sql