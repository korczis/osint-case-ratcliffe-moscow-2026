#!/usr/bin/env bash
# One-screen case status: last update, key judgments, open indicators, last changelog entry.
set -euo pipefail
cd "$(dirname "$0")/.."
jq -r '"\(.title)\nlast_updated: \(.last_updated)  status: \(.status)\n\nKEY JUDGMENTS", (.key_judgments[] | "  \(.id) [\(.confidence|split(" ")[0])] \(.statement)"), "\nOPEN INDICATORS", (.indicators_to_watch[] | if type == "object" then "  - [\(.status // "open")] \(.text)" else "  - \(.)" end), "\nLAST CHANGE", "  \(.changelog[-1].date): \(.changelog[-1].change)"' data.json
