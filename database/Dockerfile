FROM postgres:latest

# Install gettext for envsubst
RUN apt-get update && apt-get install -y gettext-base

# Environment variables for database names
ENV TEST_DB=test_db

# Copy and grant execution rights to the shell script
COPY init-db.sh /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/init-db.sh

# Copy SQL template
COPY init-prod-db.sql.template /docker-entrypoint-initdb.d/
COPY init-test-db.sql.template /docker-entrypoint-initdb.d/
