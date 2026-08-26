#!/usr/bin/env bash
# Sync/sanity gate: data.json valid, EN/CS artifact parity, forbidden terms absent,
# changelog references the latest section, last_updated present.
set -uo pipefail
cd "$(dirname "$0")/.."
fail=0; ok() { printf '  ok   %s\n' "$1"; }; bad() { printf '  FAIL %s\n' "$1"; fail=1; }
jq -e . data.json >/dev/null 2>&1 && ok "data.json is valid JSON" || bad "data.json is not valid JSON"
for pair in "report/brief/brief-en.html report/brief/brief-cs.html" "report/pdf/pdf-en.html report/pdf/pdf-cs.html"; do
  set -- $pair; a=$(grep -c '<h2' "$1"); b=$(grep -c '<h2' "$2")
  [ "$a" = "$b" ] && ok "$1 ($a h2) == $2 ($b h2)" || bad "$1 ($a h2) != $2 ($b h2)"
done
N=$(grep -oE '^## 8\.[0-9]+' report.md | sed 's/## 8\.//' | sort -n | tail -1)
tail -1 report.md | grep -q "8\.$N" && ok "changelog last line references §8.$N" || bad "changelog last line does not reference §8.$N"
jq -e '.last_updated and (.changelog|length>0) and (.key_judgments|length>0)' data.json >/dev/null 2>&1 && ok "data.json has last_updated/changelog/key_judgments" || bad "data.json missing last_updated/changelog/key_judgments"
TERMS=$(yq -r '.forbidden_terms[]?' case.yaml 2>/dev/null)
if [ -n "$TERMS" ]; then
  hits=0
  while IFS= read -r t; do
    [ -z "$t" ] && continue
    if grep -rniIq --exclude-dir=.git --exclude-dir=scratch --exclude-dir=_site --exclude-dir=data --exclude=case.yaml --exclude=check.sh -- "$t" .; then
      bad "forbidden term present: '$t'"; grep -rniI --exclude-dir=.git --exclude-dir=scratch --exclude-dir=_site --exclude-dir=data --exclude=case.yaml --exclude=check.sh -- "$t" . | cut -c1-120 | head -5; hits=1
    fi
  done <<< "$TERMS"
  [ $hits = 0 ] && ok "no forbidden terms"
fi
for f in report/pdf/report-en.pdf report/pdf/report-cs.pdf; do
  [ -f "$f" ] && [ "$f" -nt "${f/report-/pdf-}" ] 2>/dev/null || true
  [ -f "$f" ] && ok "$f exists" || bad "$f missing (run 'just pdf')"
done
exit $fail
