#!/usr/bin/env bash
set -e
cd pharmacy_ecommerce
pip install -r ../requirements.txt 2>&1 | tail -3
unset DATABASE_URL
python manage.py collectstatic --noinput --skip-checks --ignore=*.map 2>&1
mkdir -p ../public/static
cp -r staticfiles/. ../public/static/
