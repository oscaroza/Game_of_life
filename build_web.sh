#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
WEBAPP_DIR="$ROOT_DIR/webapp"

mkdir -p "$WEBAPP_DIR"

# Keep web entrypoint in sync with desktop/web source files.
cp "$ROOT_DIR/launcher_web" "$WEBAPP_DIR/main.py"
cp "$ROOT_DIR/grid.py" "$WEBAPP_DIR/grid.py"

if [ -x "$ROOT_DIR/.venv/bin/python" ]; then
  PYTHON_BIN="$ROOT_DIR/.venv/bin/python"
else
  PYTHON_BIN="${PYTHON_BIN:-python3}"
fi

WEB_DIST_DIR="$WEBAPP_DIR/build/web"

"$PYTHON_BIN" -m pygbag --build --html "$WEBAPP_DIR" &
PYGBAG_PID=$!

# Some pygbag versions may keep running after writing output files.
for _ in $(seq 1 180); do
  if [ -f "$WEB_DIST_DIR/webapp.html" ]; then
    break
  fi
  sleep 1
done

if [ ! -f "$WEB_DIST_DIR/webapp.html" ]; then
  echo "Erreur: webapp.html n'a pas été généré dans $WEB_DIST_DIR"
  if kill -0 "$PYGBAG_PID" 2>/dev/null; then
    kill "$PYGBAG_PID" >/dev/null 2>&1 || true
  fi
  wait "$PYGBAG_PID" 2>/dev/null || true
  exit 1
fi

# Keep pygbag entrypoint filename (webapp.html) so embed autodetection works.
# Provide index.html as a thin redirect for Netlify root.
cat > "$WEB_DIST_DIR/index.html" <<'HTML'
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta http-equiv="refresh" content="0; url=webapp.html" />
    <title>Game of Life</title>
  </head>
  <body>
    <p>Redirecting to <a href="webapp.html">webapp.html</a>...</p>
  </body>
</html>
HTML

if kill -0 "$PYGBAG_PID" 2>/dev/null; then
  kill "$PYGBAG_PID" >/dev/null 2>&1 || true
fi
wait "$PYGBAG_PID" 2>/dev/null || true
