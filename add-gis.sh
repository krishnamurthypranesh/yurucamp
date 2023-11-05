#!/bin/bash
echo "creating extension postgis on yurucamp...";

PGPASSWORD=root1234 psql -U postgres -d yurucamp -c "CREATE EXTENSION postgis;"
