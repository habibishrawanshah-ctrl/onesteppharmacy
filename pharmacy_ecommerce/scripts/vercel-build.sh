#!/usr/bin/env bash
set -e
cd pharmacy_ecommerce
if [ -n "$VERCEL_PYTHON_VENV_PATH" ] && [ -x "$VERCEL_PYTHON_VENV_PATH/bin/python" ]; then
  PYTHON_BIN="$VERCEL_PYTHON_VENV_PATH/bin/python"
else
  PYTHON_BIN="python"
fi
unset DATABASE_URL
"$PYTHON_BIN" manage.py collectstatic --noinput --skip-checks --ignore=*.map 2>&1
mkdir -p ../public/static
cp -r staticfiles/. ../public/static/
