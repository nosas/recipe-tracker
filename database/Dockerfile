FROM postgres:latest

# Environment variables for database names
ENV TEST_DB=test_db

# Run initial SQL scripts
COPY init-test-db.sql /docker-entrypoint-initdb.d/
