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
SITE_PKGS="$("$PYTHON_BIN" -c "import site; print(site.getsitepackages()[0])")"
echo "site-packages: $SITE_PKGS"
echo "--- cffi in site-packages ---"
ls "$SITE_PKGS" 2>/dev/null | grep -i cffi || echo "NO cffi in site-packages"
echo "--- cffi dir contents ---"
ls "$SITE_PKGS/cffi/" 2>/dev/null || echo "no cffi dir"
echo "--- vendor dir (.vercel_python_packages) ---"
ls /vercel/path0/.vercel_python_packages/ 2>/dev/null | grep -iE "cffi|psycopg" || echo "vendor dir missing or empty"
echo "--- PYTHONPATH ---"
echo "$PYTHONPATH"
unset DATABASE_URL
"$PYTHON_BIN" manage.py collectstatic --noinput --skip-checks --ignore=*.map 2>&1
mkdir -p ../public/static
cp -r staticfiles/. ../public/static/
