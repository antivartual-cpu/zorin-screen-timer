#!/usr/bin/env bash
set -euo pipefail

VERSION="${1:-1.0.0}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RELEASE_ROOT="$SCRIPT_DIR/release"
PACKAGE_DIR="$RELEASE_ROOT/ZorinScreenTimer"
ZIP_PATH="$RELEASE_ROOT/ZorinScreenTimer-v$VERSION.zip"

rm -rf "$PACKAGE_DIR" "$ZIP_PATH"
mkdir -p "$PACKAGE_DIR"

cp "$SCRIPT_DIR/app.py" "$PACKAGE_DIR/"
cp "$SCRIPT_DIR/README.md" "$PACKAGE_DIR/"
cp "$SCRIPT_DIR/run_zorin_screen_timer.sh" "$PACKAGE_DIR/"
cp "$SCRIPT_DIR/install.sh" "$PACKAGE_DIR/"
cp "$SCRIPT_DIR/uninstall.sh" "$PACKAGE_DIR/"
cp "$SCRIPT_DIR/create_release.sh" "$PACKAGE_DIR/"
cp "$SCRIPT_DIR/Zorin Screen Timer.desktop" "$PACKAGE_DIR/"
cp "$SCRIPT_DIR/icon.svg" "$PACKAGE_DIR/"
cp "$SCRIPT_DIR/LICENSE" "$PACKAGE_DIR/"
cp "$SCRIPT_DIR/CHANGELOG.md" "$PACKAGE_DIR/"

chmod +x "$PACKAGE_DIR/run_zorin_screen_timer.sh"
chmod +x "$PACKAGE_DIR/install.sh"
chmod +x "$PACKAGE_DIR/uninstall.sh"
chmod +x "$PACKAGE_DIR/create_release.sh"

if command -v zip >/dev/null 2>&1; then
    (
        cd "$RELEASE_ROOT"
        zip -r "ZorinScreenTimer-v$VERSION.zip" "ZorinScreenTimer"
    )
    echo "Created $ZIP_PATH"
else
    echo "zip command not found. Created release folder only: $PACKAGE_DIR"
fi
