#!/usr/bin/env bash
# refresh_digest — keep the local digest site fresh and (optionally) open the latest issue.
#
#   refresh_digest.sh           # pull + rebuild, then open the newest digest in the browser
#   refresh_digest.sh --no-open # pull + rebuild only (for a silent daily cron/LaunchAgent)
#
# Designed to be run at login / daily by a LaunchAgent (see com.dbmsdigest.daily.plist),
# or set your browser's homepage to docs/latest.html and just run this on a schedule.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(dirname "$SCRIPT_DIR")"
cd "$REPO" || exit 1

# 1. Best-effort sync (ignore failure: offline / no creds / local-only repo).
git pull --ff-only --quiet 2>/dev/null || true

# 2. Rebuild docs/ (needs the `markdown` module: pip3 install markdown).
python3 scripts/build_feed.py || { echo "build failed — is 'markdown' installed?"; exit 1; }

# 3. Open the always-newest page in the default browser, unless --no-open.
if [ "${1:-}" != "--no-open" ]; then
  open "$REPO/docs/latest.html"
fi
