#!/bin/sh
# Setup git hooks for OKF validation

HOOK_DIR=".git/hooks"
PRE_COMMIT_SRC="tools/pre-commit"
PRE_COMMIT_DST="$HOOK_DIR/pre-commit"

if [ ! -d "$HOOK_DIR" ]; then
    echo "[-] Error: .git directory not found. Please run this from the project root."
    exit 1
fi

# If core.hooksPath is set, git ignores .git/hooks entirely and installing there
# is a silent no-op. Report it rather than pretending the hook is active.
HOOKS_PATH=$(git config --get core.hooksPath)

echo "[+] Copying pre-commit hook to $PRE_COMMIT_DST..."
cp "$PRE_COMMIT_SRC" "$PRE_COMMIT_DST"
chmod +x "$PRE_COMMIT_DST"

if [ -n "$HOOKS_PATH" ]; then
    echo "============================================================"
    echo "[!] WARNING: core.hooksPath is set to '$HOOKS_PATH'."
    echo "[!] Git ignores .git/hooks when this is set, so the OKF"
    echo "[!] pre-commit hook installed above will NOT run."
    echo "[!]"
    echo "[!] Until this is reconciled, validate manually before every commit:"
    echo "[!]     python tools/okf_manifest.py"
    echo "[!]     python tools/validate_okf.py"
    echo "[!]"
    echo "[!] To use repo-local hooks instead, copy the global hooks into a"
    echo "[!] repo directory alongside tools/pre-commit and point"
    echo "[!] core.hooksPath at it, so global hooks are preserved."
    echo "============================================================"
    exit 1
fi

echo "[+] Pre-commit hook successfully configured!"
exit 0
