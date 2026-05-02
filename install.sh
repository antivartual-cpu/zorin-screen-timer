#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$HOME/.local/share/zorin-screen-timer"
APPLICATIONS_DIR="$HOME/.local/share/applications"
DESKTOP_DIR="$HOME/デスクトップ"
XDG_DESKTOP_DIR="$(xdg-user-dir DESKTOP 2>/dev/null || true)"
DESKTOP_NAME="Zorin Screen Timer.desktop"
APP_DESKTOP_FILE="$APPLICATIONS_DIR/zorin-screen-timer.desktop"
USER_DESKTOP_FILE="$DESKTOP_DIR/$DESKTOP_NAME"

mkdir -p "$APP_DIR" "$APPLICATIONS_DIR" "$DESKTOP_DIR"

cp "$SCRIPT_DIR/app.py" "$APP_DIR/"
cp "$SCRIPT_DIR/README.md" "$APP_DIR/"
cp "$SCRIPT_DIR/run_zorin_screen_timer.sh" "$APP_DIR/"
cp "$SCRIPT_DIR/uninstall.sh" "$APP_DIR/"
cp "$SCRIPT_DIR/icon.svg" "$APP_DIR/"
chmod +x "$APP_DIR/run_zorin_screen_timer.sh" "$APP_DIR/uninstall.sh"

python3 -m venv "$APP_DIR/.venv"
"$APP_DIR/.venv/bin/python" -m pip install --upgrade pip
"$APP_DIR/.venv/bin/python" -m pip install PySide6

sed \
    -e "s|__APP_DIR__|$APP_DIR|g" \
    -e "s|__ICON_PATH__|$APP_DIR/icon.svg|g" \
    "$SCRIPT_DIR/$DESKTOP_NAME" > "$APP_DESKTOP_FILE"

cp "$APP_DESKTOP_FILE" "$USER_DESKTOP_FILE"
chmod +x "$APP_DESKTOP_FILE" "$USER_DESKTOP_FILE"

if [[ -n "$XDG_DESKTOP_DIR" && "$XDG_DESKTOP_DIR" != "$DESKTOP_DIR" ]]; then
    mkdir -p "$XDG_DESKTOP_DIR"
    cp "$APP_DESKTOP_FILE" "$XDG_DESKTOP_DIR/$DESKTOP_NAME"
    chmod +x "$XDG_DESKTOP_DIR/$DESKTOP_NAME"
fi

echo "Installation complete."
