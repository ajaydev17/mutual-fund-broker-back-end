#!/bin/sh

export PGUSER=postgres

# Create the database
psql -c "CREATE DATABASE mutual_fund_backend;"

# Create the uuid-ossp extension in the newly created database
psql -d mutual_fund_backend -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"