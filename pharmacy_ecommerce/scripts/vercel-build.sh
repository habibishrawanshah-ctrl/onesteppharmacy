#!/usr/bin/env bash
set -e
cd pharmacy_ecommerce
pip install --break-system-packages -r requirements.txt
python manage.py migrate --noinput --skip-checks
python manage.py collectstatic --noinput --skip-checks
mkdir -p ../public/static
cp -r staticfiles/. ../public/static/
