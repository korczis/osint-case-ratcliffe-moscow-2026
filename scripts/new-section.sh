#!/usr/bin/env bash
# Scaffold the next §8.N heading in report.md and a changelog stub, so every update lands in the same shape.
set -euo pipefail
cd "$(dirname "$0")/.."
N=$(grep -oE '^## 8\.[0-9]+' report.md | sed 's/## 8\.//' | sort -n | tail -1); N=$((N+1))
TS=$(date '+%Y-%m-%d %H:%M %Z')
python3 - "$N" "$TS" <<'PY'
import sys; n,ts=sys.argv[1],sys.argv[2]
md=open('report.md').read()
sec=f"## 8.{n} Indicator re-sweep ({ts})\n\n_(method, findings, unchanged indicators)_\n\n"
md=md.replace("## 9. Caveats",sec+"## 9. Caveats",1).rstrip('\n')+f"\n- **{ts}** — §8.{n}: _(summary)_\n"
open('report.md','w').write(md); print(f"scaffolded §8.{n} + changelog line in report.md")
PY
