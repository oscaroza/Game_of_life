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
mkdir -p "$WEB_DIST_DIR"

# Ensure we wait for a fresh file from the current pygbag run.
rm -f "$WEB_DIST_DIR/webapp.html" "$WEB_DIST_DIR/index.html"

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

# Stop pygbag once the output file exists so it cannot overwrite our fixes.
if kill -0 "$PYGBAG_PID" 2>/dev/null; then
  kill "$PYGBAG_PID" >/dev/null 2>&1 || true
fi
wait "$PYGBAG_PID" 2>/dev/null || true

# Some pygbag builds miss embedding main.py in webapp.html.
# Inject it explicitly if absent to avoid "NameError: main is not defined".
"$PYTHON_BIN" - "$WEBAPP_DIR" "$WEB_DIST_DIR/webapp.html" <<'PY'
import base64
import sys
from pathlib import Path

webapp_dir = Path(sys.argv[1])
html_path = Path(sys.argv[2])

html = html_path.read_text(encoding="utf-8")
if 'with open("main.py"' not in html:
    main_code = (webapp_dir / "main.py").read_text(encoding="utf-8")
    encoded = base64.b64encode(main_code.encode("utf-8")).decode("ascii")
    injection = (
        "import base64\n"
        f'with open("main.py","wb") as fs:fs.write(base64.b64decode("{encoded}"))\n\n'
    )
    marker = "# fmt:on"
    if marker not in html:
        raise RuntimeError(f"Marker '{marker}' not found in {html_path}")
    html = html.replace(marker, injection + marker, 1)

bootstrap = (
    "import pygame\n"
    "try:\n"
    "    import pygame_ce as _pygame_ce\n"
    "except Exception:\n"
    "    _pygame_ce = None\n"
    "if not hasattr(pygame, 'init') and _pygame_ce is not None:\n"
    "    pygame = _pygame_ce\n"
    "import importlib\n"
    "main = importlib.import_module(\"main\").main\n\n"
)

legacy_bootstraps = (
    "import importlib\nmain = importlib.import_module(\"main\").main\n\n",
    "import importlib\nmain = importlib.import_module('main').main\n\n",
)
for legacy in legacy_bootstraps:
    html = html.replace(legacy, bootstrap)

while (bootstrap + bootstrap) in html:
    html = html.replace(bootstrap + bootstrap, bootstrap)

if bootstrap not in html:
    marker = "# fmt:on"
    if marker not in html:
        raise RuntimeError(f"Marker '{marker}' not found in {html_path}")
    html = html.replace(marker, bootstrap + marker, 1)

html_path.write_text(html, encoding="utf-8")
PY

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
