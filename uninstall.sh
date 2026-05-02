#!/usr/bin/env bash
set -euo pipefail

XDG_DESKTOP_DIR="$(xdg-user-dir DESKTOP 2>/dev/null || true)"

rm -rf "$HOME/.local/share/zorin-screen-timer"
rm -f "$HOME/.local/share/applications/zorin-screen-timer.desktop"
rm -f "$HOME/デスクトップ/Zorin Screen Timer.desktop"

if [[ -n "$XDG_DESKTOP_DIR" && "$XDG_DESKTOP_DIR" != "$HOME/デスクトップ" ]]; then
    rm -f "$XDG_DESKTOP_DIR/Zorin Screen Timer.desktop"
fi

echo "Uninstalled."
