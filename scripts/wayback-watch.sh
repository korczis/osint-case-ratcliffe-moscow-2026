#!/usr/bin/env bash
# Run wayback-cdx over every watch_urls entry in case.yaml.
set -euo pipefail
cd "$(dirname "$0")/.."
for u in $(yq -r '.watch_urls[]' case.yaml); do
  echo "== $u"; scripts/wayback-cdx.sh "$u" "${1:-20260824}" || echo "(no snapshots / error)"
done
