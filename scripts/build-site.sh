#!/usr/bin/env bash
# Build _site/ for GitHub Pages: full landing page (judgments, hypotheses, timeline,
# entities, indicators, sources, methodology, toolkit) + briefs + PDFs + report + data.
set -euo pipefail
cd "$(dirname "$0")/.."
OUT=_site; rm -rf "$OUT"; mkdir -p "$OUT/brief" "$OUT/pdf"
cp report/brief/brief-en.html report/brief/brief-cs.html "$OUT/brief/"
cp report/pdf/report-en.pdf report/pdf/report-cs.pdf "$OUT/pdf/" 2>/dev/null || echo "warn: PDFs missing (run 'just pdf')"
cp report.md data.json case.yaml "$OUT/"
python3 scripts/gen-index.py "$OUT"
touch "$OUT/.nojekyll"; echo "site built in $OUT/"; ls "$OUT"
