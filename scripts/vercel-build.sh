#!/usr/bin/env bash
set -e
cd pharmacy_ecommerce
pip install --break-system-packages -r requirements.txt
VERCEL= python manage.py migrate
VERCEL= python scripts/seed_prod.py
python manage.py collectstatic --noinput
mkdir -p ../public/static
cp -r staticfiles/. ../public/static/
