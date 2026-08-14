#!/bin/sh
# Setup git hooks for OKF validation

HOOK_DIR=".git/hooks"
PRE_COMMIT_SRC="tools/pre-commit"
PRE_COMMIT_DST="$HOOK_DIR/pre-commit"

if [ ! -d "$HOOK_DIR" ]; then
    echo "[-] Error: .git directory not found. Please run this from the project root."
    exit 1
fi

echo "[+] Copying pre-commit hook to $PRE_COMMIT_DST..."
cp "$PRE_COMMIT_SRC" "$PRE_COMMIT_DST"
chmod +x "$PRE_COMMIT_DST"

echo "[+] Pre-commit hook successfully configured!"
exit 0
