#!/usr/bin/env bash
# Wayback CDX: list snapshots (and digest changes) of a URL in a date window.
# Usage: scripts/wayback-cdx.sh <url> [from YYYYMMDD] [to YYYYMMDD] [prefix]
set -euo pipefail
URL="$1"; FROM="${2:-20260824}"; TO="${3:-$(date -u +%Y%m%d)}"; MT="${4:-exact}"
curl -sfL "https://web.archive.org/cdx/search/cdx?url=${URL}&matchType=${MT}&from=${FROM}&to=${TO}&output=json&limit=200&fl=timestamp,original,statuscode,digest" \
 | jq -r '.[1:][] | "\(.[0])  \(.[2])  \(.[3][0:10])  \(.[1])"'
