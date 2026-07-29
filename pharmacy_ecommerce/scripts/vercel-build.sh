#!/usr/bin/env bash
set -e
cd pharmacy_ecommerce
apt-get update -qq && apt-get install -y -qq libpq-dev gcc 2>/dev/null
pip install --break-system-packages --no-binary psycopg2 -r requirements.txt
python manage.py migrate --noinput --skip-checks
python manage.py collectstatic --noinput --skip-checks
mkdir -p ../public/static
cp -r staticfiles/. ../public/static/
