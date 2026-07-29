#!/usr/bin/env bash
set -e
cd pharmacy_ecommerce
pip install --break-system-packages -r requirements.txt 2>&1 | tail -2
# Build step doesn't need the database, unset to use SQLite
unset DATABASE_URL
python manage.py collectstatic --noinput --skip-checks --ignore=*.map 2>&1
mkdir -p ../public/static
cp -r staticfiles/. ../public/static/
