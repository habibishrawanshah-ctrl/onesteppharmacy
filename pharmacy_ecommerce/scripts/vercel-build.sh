#!/usr/bin/env bash
set -e
cd pharmacy_ecommerce
PYTHON_BIN=""
for p in \
  "${VERCEL_PYTHON_VENV_PATH}/bin/python" \
  "/vercel/path0/.vercel/python/.venv/bin/python" \
  "$(pwd)/../.vercel/python/.venv/bin/python"; do
  if [ -n "$p" ] && [ -x "$p" ]; then
    PYTHON_BIN="$p"
    break
  fi
done
if [ -z "$PYTHON_BIN" ]; then
  PYTHON_BIN="python"
fi
echo "Using python: $PYTHON_BIN"
"$PYTHON_BIN" -c "import sys; print('Interpreter:', sys.version)"
unset DATABASE_URL
"$PYTHON_BIN" manage.py collectstatic --noinput --skip-checks --ignore=*.map 2>&1
mkdir -p ../public/static
cp -r staticfiles/. ../public/static/
