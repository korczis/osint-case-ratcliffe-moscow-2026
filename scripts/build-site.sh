#!/usr/bin/env bash
# Build _site/ for GitHub Pages: index + briefs + PDFs + report (HTML if python-markdown is
# available, otherwise the raw Markdown) + data.json. No external assets.
set -euo pipefail
cd "$(dirname "$0")/.."
OUT=_site; rm -rf "$OUT"; mkdir -p "$OUT/brief" "$OUT/pdf"
cp report/brief/brief-en.html report/brief/brief-cs.html "$OUT/brief/"
cp report/pdf/report-en.pdf report/pdf/report-cs.pdf "$OUT/pdf/" 2>/dev/null || echo "warn: PDFs missing (run 'just pdf')"
cp report.md data.json case.yaml "$OUT/"
TITLE=$(yq -r .title case.yaml); ID=$(yq -r .id case.yaml); STATUS=$(yq -r .status case.yaml)
UPD=$(jq -r .last_updated data.json); LASTCHG=$(jq -r '.changelog[-1].change' data.json)
KJ=$(jq -r '.key_judgments[] | "<li><span class=\"id\">\(.id)</span> <span class=\"conf\">\(.confidence|split(" ")[0])</span> \(.statement)</li>"' data.json)
IND=$(jq -r '.indicators_to_watch[] | "<li>\(.)</li>"' data.json)
python3 - "$OUT" <<'PY'
import sys, html, pathlib
out = pathlib.Path(sys.argv[1]); md = pathlib.Path('report.md').read_text(encoding='utf-8')
try:
    import markdown
    body = markdown.markdown(md, extensions=['tables', 'fenced_code', 'toc'])
except Exception:
    body = '<pre style="white-space:pre-wrap">' + html.escape(md) + '</pre>'
(out / 'report.html').write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Report</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{{max-width:900px;margin:2rem auto;padding:0 1rem;font:16px/1.55 system-ui,sans-serif;color:#1a1a1a;background:#fff}}
table{{border-collapse:collapse;width:100%;font-size:.92em}}td,th{{border:1px solid #ddd;padding:.35rem .5rem;vertical-align:top}}
code{{background:#f3f3f3;padding:.1em .3em}}blockquote{{border-left:3px solid #ccc;margin:0;padding:.2rem 1rem;color:#555}}
a{{color:#0b57d0}}@media(prefers-color-scheme:dark){{body{{background:#111;color:#e6e6e6}}td,th{{border-color:#333}}code{{background:#222}}a{{color:#8ab4f8}}}}</style></head>
<body><p><a href="./">← index</a></p>{body}</body></html>''', encoding='utf-8')
PY
cat > "$OUT/index.html" <<HTML
<!doctype html><html lang="en"><head><meta charset="utf-8"><title>${TITLE}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{max-width:860px;margin:2.5rem auto;padding:0 1rem;font:16px/1.55 system-ui,sans-serif;color:#1a1a1a;background:#fff}
h1{font-size:1.6rem;line-height:1.25}.meta{color:#666;font-size:.9rem}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:.8rem;margin:1.5rem 0}
.card{border:1px solid #ddd;border-radius:8px;padding:1rem}.card a{font-weight:600;text-decoration:none;color:#0b57d0}
.card small{display:block;color:#666;margin-top:.3rem}
ul.kj{list-style:none;padding:0}ul.kj li{margin:.5rem 0;padding-left:.2rem}
.id{font-family:ui-monospace,monospace;font-size:.8em;color:#666;margin-right:.4rem}
.conf{font-family:ui-monospace,monospace;font-size:.75em;border:1px solid #bbb;border-radius:4px;padding:0 .35em;margin-right:.4rem}
ul.ind li{margin:.3rem 0;font-size:.92rem}
footer{margin-top:2.5rem;color:#666;font-size:.85rem;border-top:1px solid #ddd;padding-top:1rem}
@media(prefers-color-scheme:dark){body{background:#111;color:#e6e6e6}.card{border-color:#333}.card a{color:#8ab4f8}.meta,.card small,.id,footer{color:#9a9a9a}.conf{border-color:#555}footer{border-color:#333}}
</style></head><body>
<h1>${TITLE}</h1>
<p class="meta">Open-source intelligence assessment · case <code>${ID}</code> · status: ${STATUS} · last updated ${UPD}</p>
<div class="grid">
  <div class="card"><a href="brief/brief-en.html">Brief (EN)</a><small>shareable one-page HTML</small></div>
  <div class="card"><a href="brief/brief-cs.html">Brief (CS)</a><small>sdílitelný HTML přehled</small></div>
  <div class="card"><a href="pdf/report-en.pdf">Report PDF (EN)</a><small>print layout</small></div>
  <div class="card"><a href="pdf/report-cs.pdf">Report PDF (CS)</a><small>tisková verze</small></div>
  <div class="card"><a href="report.html">Full report</a><small>source of truth · <a href="report.md">.md</a></small></div>
  <div class="card"><a href="data.json">data.json</a><small>structured mirror</small></div>
</div>
<h2>Key judgments</h2><ul class="kj">${KJ}</ul>
<h2>Indicators to watch</h2><ul class="ind">${IND}</ul>
<p><strong>Last change:</strong> ${LASTCHG}</p>
<footer>Open sources only. Every claim carries its source; unsourced assertions are logged as such. Methodology and tooling: see the repository README.</footer>
</body></html>
HTML
touch "$OUT/.nojekyll"; echo "site built in $OUT/"; ls "$OUT" "$OUT/brief" "$OUT/pdf"
