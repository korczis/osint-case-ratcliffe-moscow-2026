#!/usr/bin/env bash
# GDELT DOC 2.0 sweep: article list + tone chart for the case query.
# Usage: scripts/gdelt-sweep.sh [query] [start YYYYMMDDHHMMSS] [end YYYYMMDDHHMMSS]
set -euo pipefail
cd "$(dirname "$0")/.."
Q="${1:-$(yq -r .gdelt_query case.yaml 2>/dev/null || echo 'Ratcliffe Moscow')}"
START="${2:-$(yq -r .window.start case.yaml 2>/dev/null || echo 20260825000000)}"
END="${3:-$(date -u +%Y%m%d%H%M%S)}"
ENC=$(python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))' "$Q")
TS=$(date -u +%Y%m%dT%H%M%SZ)
BASE="https://api.gdeltproject.org/api/v2/doc/doc?query=${ENC}&format=json&startdatetime=${START}&enddatetime=${END}"
curl -sfL "${BASE}&mode=artlist&maxrecords=250" -o "data/gdelt-artlist-${TS}.json"
curl -sfL "${BASE}&mode=tonechart" -o "data/gdelt-tonechart-${TS}.json"
echo "articles: $(jq '.articles|length' data/gdelt-artlist-${TS}.json)  countries: $(jq -r '[.articles[].sourcecountry]|unique|length' data/gdelt-artlist-${TS}.json)"
jq -r '.articles[] | "\(.seendate)  \(.sourcecountry)  \(.domain)  \(.title)"' "data/gdelt-artlist-${TS}.json" | sort | tail -40
