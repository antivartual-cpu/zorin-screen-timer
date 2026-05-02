#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [[ -x "$SCRIPT_DIR/.venv/bin/python" ]]; then
    exec "$SCRIPT_DIR/.venv/bin/python" "$SCRIPT_DIR/app.py"
fi

echo "Warning: bundled virtual environment was not found." >&2
echo "Falling back to system python3. If PySide6 is missing, run ./install.sh first." >&2
exec python3 "$SCRIPT_DIR/app.py"
