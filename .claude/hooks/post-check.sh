#!/usr/bin/env bash
# Stop hook: after a turn that touched report artifacts, run the sync check and surface problems.
set -uo pipefail
cd "$(dirname "$0")/../.."
if git status --porcelain 2>/dev/null | grep -Eq 'report\.md|data\.json|report/'; then
  OUT=$(scripts/check.sh 2>&1) || { printf '%s\n' "$OUT" | tail -20 >&2; exit 2; }
fi
exit 0
