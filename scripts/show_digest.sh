#!/usr/bin/env bash
# show_digest — read the weekly DBMS digests right in the terminal.
#
# Usage:
#   digest            # show the newest digest
#   digest latest     # same as above
#   digest list       # list all available digest weeks (newest first)
#   digest 2026-06-08 # show a specific week (by its Monday date)
#   digest open       # open the published site in the browser
#
# Renders with `glow` if installed (nicest), else `bat`, else falls back to
# `less`. Reads the local digests/ folder, so it works offline.
set -euo pipefail

# Repo root = the parent of this script's directory, resolved no matter where
# the command is invoked from.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(dirname "$SCRIPT_DIR")"
DIGESTS="$REPO/digests"

render() {
  if command -v glow >/dev/null 2>&1; then
    glow -p "$1"
  elif command -v bat >/dev/null 2>&1; then
    bat --style=plain --paging=always --language=markdown "$1"
  else
    less -R "$1"
  fi
}

newest() { ls -1 "$DIGESTS"/*.md 2>/dev/null | sort | tail -1; }

cmd="${1:-latest}"
case "$cmd" in
  latest)
    f="$(newest)"
    [ -n "$f" ] || { echo "No digests found in $DIGESTS"; exit 1; }
    render "$f"
    ;;
  list|ls)
    ls -1 "$DIGESTS"/*.md 2>/dev/null | xargs -n1 basename | sed 's/\.md$//' | sort -r
    ;;
  open|web)
    open "https://danolivo.github.io/dbms-digest/"
    ;;
  -h|--help|help)
    sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'
    ;;
  *)
    f="$DIGESTS/$cmd.md"
    if [ -f "$f" ]; then
      render "$f"
    else
      echo "No digest for '$cmd'. Try: digest list"
      exit 1
    fi
    ;;
esac
