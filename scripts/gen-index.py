#!/usr/bin/env python3
"""Generate _site/index.html and _site/report.html from data.json + report.md.
Landing page uses Flowbite (Tailwind CDN + Flowbite CSS/JS, typography plugin),
following the Flowbite quickstart conventions: https://flowbite.com/docs/getting-started/quickstart/"""
import html, json, pathlib, re, sys

out = pathlib.Path(sys.argv[1])
d = json.loads(pathlib.Path('data.json').read_text(encoding='utf-8'))
md = pathlib.Path('report.md').read_text(encoding='utf-8')
e = html.escape
REPO = "https://github.com/korczis/osint-case-ratcliffe-moscow-2026"

HEAD_ASSETS = '''<script src="https://cdn.tailwindcss.com?plugins=typography"></script>
<link href="https://cdn.jsdelivr.net/npm/flowbite@2.5.2/dist/flowbite.min.css" rel="stylesheet">
<script>tailwind.config={darkMode:'media'}</script>'''
BODY_JS = '<script src="https://cdn.jsdelivr.net/npm/flowbite@2.5.2/dist/flowbite.min.js"></script>'

# ---------------- report.html (Flowbite typography / prose) ----------------
try:
    import markdown
    body = markdown.markdown(md, extensions=['tables', 'fenced_code', 'toc'])
except Exception:
    body = '<pre class="whitespace-pre-wrap">' + e(md) + '</pre>'

(out / 'report.html').write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{e(d["title"])} — full report</title><meta name="viewport" content="width=device-width,initial-scale=1">
{HEAD_ASSETS}</head>
<body class="bg-white dark:bg-gray-900 antialiased">
<nav class="border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
  <div class="max-w-screen-lg mx-auto px-4 py-3 flex items-center justify-between">
    <a href="./" class="text-sm font-medium text-blue-600 dark:text-blue-500 hover:underline">&larr; case index</a>
    <a href="report.md" class="text-sm text-gray-500 dark:text-gray-400 hover:underline">raw markdown</a>
  </div>
</nav>
<main class="max-w-screen-lg mx-auto px-4 py-10">
  <article class="prose prose-gray dark:prose-invert max-w-none prose-table:text-sm prose-h2:border-b prose-h2:border-gray-200 dark:prose-h2:border-gray-700 prose-h2:pb-2">
    {body}
  </article>
</main>
{BODY_JS}</body></html>''', encoding='utf-8')

# ---------------- index.html components ----------------
def conf_badge(c):
    w = c.split(' ')[0].split('–')[0].split('-')[0].lower()
    color = {'high': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
             'low': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'}.get(
        w, 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300')
    return (f'<span class="text-xs font-medium me-2 px-2.5 py-0.5 rounded {color}" title="{e(c)}">'
            f'{e(c.split("(")[0].strip())} confidence</span>')

kj = '\n'.join(f'''
<div class="p-5 bg-white border border-gray-200 rounded-lg shadow-sm dark:bg-gray-800 dark:border-gray-700">
  <div class="flex items-center mb-2">
    <span class="text-xs font-semibold text-gray-500 dark:text-gray-400 me-3">{e(k["id"])}</span>{conf_badge(k["confidence"])}
  </div>
  <p class="mb-2 font-semibold text-gray-900 dark:text-white">{e(k["statement"])}</p>
  <p class="text-sm text-gray-500 dark:text-gray-400">{e(k["support"])}</p>
</div>''' for k in d['key_judgments'])

hyp = '\n'.join(f'''
<tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 last:border-b-0">
  <th scope="row" class="px-4 py-3 font-medium text-gray-900 dark:text-white whitespace-nowrap align-top">{e(h["id"])}</th>
  <td class="px-4 py-3 align-top"><span class="font-medium text-gray-900 dark:text-white">{e(h["label"])}</span>
    <p class="mt-1 text-gray-500 dark:text-gray-400">{e(h["description"])}</p></td>
  <td class="px-4 py-3 align-top text-gray-500 dark:text-gray-400">{e(h.get("likelihood",""))}</td>
</tr>''' for h in d['alternative_hypotheses'])

# Flowbite vertical timeline component
tl = '\n'.join(f'''
<li class="mb-6 ms-4">
  <div class="absolute w-3 h-3 bg-gray-200 rounded-full mt-1.5 -start-1.5 border border-white dark:border-gray-900 dark:bg-gray-700"></div>
  <time class="mb-1 text-xs font-normal leading-none text-gray-400 dark:text-gray-500">{e(t["date"])}</time>
  <p class="text-sm font-normal text-gray-900 dark:text-white">{e(t["event"])}</p>
  <span class="text-xs text-gray-400 dark:text-gray-500">{e(t.get("source",""))}</span>
</li>''' for t in d['timeline'])

def ent(x):
    name = x.get('name') or x.get('id', '')
    role = x.get('role') or x.get('notes') or ''
    return (f'<li class="py-2"><span class="font-medium text-gray-900 dark:text-white">{e(name)}</span>'
            f'<span class="text-gray-500 dark:text-gray-400"> — {e(role)}</span></li>')
persons = ''.join(ent(p) for p in d.get('entities', {}).get('persons', []))
orgs = ''.join(ent(o) for o in d.get('entities', {}).get('organizations', []))

ind = '\n'.join(f'''
<li class="flex items-start gap-2.5 py-2 text-sm text-gray-700 dark:text-gray-300">
  <svg class="w-4 h-4 mt-0.5 shrink-0 text-blue-600 dark:text-blue-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" d="M2.5 12s3.5-7 9.5-7 9.5 7 9.5 7-3.5 7-9.5 7-9.5-7-9.5-7z"/></svg>
  <span>{e(i)}</span></li>''' for i in d['indicators_to_watch'])

srcs = '\n'.join(
    f'<li class="py-2"><a href="{e(s["url"])}" rel="noopener" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">{e(s["outlet"])}</a>'
    f'<span class="text-gray-500 dark:text-gray-400"> — {e(s.get("title",""))}</span></li>'
    for s in d.get('sources', []))

chlog = '\n'.join(f'''
<li class="mb-5 ms-4">
  <div class="absolute w-3 h-3 bg-blue-200 rounded-full mt-1.5 -start-1.5 border border-white dark:border-gray-900 dark:bg-blue-900"></div>
  <time class="mb-1 text-xs font-normal leading-none text-gray-400 dark:text-gray-500">{e(c["date"][:16].replace("T"," "))} UTC</time>
  <p class="text-sm text-gray-600 dark:text-gray-300">{e(c["change"])}</p>
</li>''' for c in reversed(d['changelog']))

n_sections = len(re.findall(r'^#{2,3} 8\.\d+', md, re.M))
docs = [('brief/brief-en.html', 'Brief · EN', 'one-page shareable HTML'),
        ('brief/brief-cs.html', 'Brief · CS', 'jednostránkový přehled'),
        ('pdf/report-en.pdf', 'PDF · EN', 'print layout'),
        ('pdf/report-cs.pdf', 'PDF · CS', 'tisková verze'),
        ('report.html', 'Full report', 'source of truth'),
        ('data.json', 'data.json', 'structured mirror')]
doc_cards = '\n'.join(f'''
<a href="{u}" class="block p-4 bg-white border border-gray-200 rounded-lg shadow-sm hover:bg-gray-50 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700">
  <span class="block mb-1 text-sm font-semibold text-gray-900 dark:text-white">{t}</span>
  <span class="text-xs text-gray-500 dark:text-gray-400">{s}</span>
</a>''' for u, t, s in docs)

def section(sid, title, inner, sub=''):
    subhtml = f'<p class="mb-6 text-gray-500 dark:text-gray-400 text-sm">{sub}</p>' if sub else ''
    return f'''<section id="{sid}" class="py-10 border-t border-gray-200 dark:border-gray-700">
<h2 class="mb-2 text-xs font-semibold uppercase tracking-widest text-blue-700 dark:text-blue-500">{title}</h2>{subhtml}{inner}</section>'''

toolkit_rows = [
    ('/update-case', 'One call runs the whole cycle: status → sweep every open indicator (web, GDELT, Wayback) → trace claims to primary sources → adversarial red-team gate → write the evidence section → mirror into data.json and four HTML/PDF artifacts → render → check.'),
    ('/publish', 'Render PDFs, build this site, run the consistency gate, conventional commit, push, confirm the GitHub Pages deploy.'),
    ('/new-case', 'Scaffold a fresh case with the same layout, tooling and rules from a one-line subject.'),
    ('Subagents', 'indicator-sweeper, source-tracer and red-team run with strict JSON contracts; nothing changes a confidence level without passing the red-team gate.'),
    ('Guard hooks', 'Raw data pulls are append-only, PDFs are never hand-edited, no force-push or history rewrite, and reconnaissance tooling is blocked at the tool-call level.'),
    ('CI', 'GitHub Actions renders the PDFs with WeasyPrint, rebuilds this site from data.json and deploys Pages on every push.')]
toolkit = '\n'.join(f'''
<div class="p-5 bg-white border border-gray-200 rounded-lg shadow-sm dark:bg-gray-800 dark:border-gray-700">
  <h3 class="mb-2 text-sm font-semibold text-gray-900 dark:text-white"><code class="text-blue-700 dark:text-blue-400">{e(t)}</code></h3>
  <p class="text-sm text-gray-500 dark:text-gray-400">{e(x)}</p>
</div>''' for t, x in toolkit_rows)

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{e(d["title"])}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Living open-source intelligence assessment maintained end-to-end with a reusable Claude Code toolkit — key judgments, competing hypotheses, indicators, full sourcing.">
{HEAD_ASSETS}</head>
<body class="bg-gray-50 dark:bg-gray-900 antialiased">

<nav class="bg-white border-b border-gray-200 dark:bg-gray-900 dark:border-gray-700 sticky top-0 z-40">
  <div class="max-w-screen-xl mx-auto px-4 py-3 flex flex-wrap items-center justify-between">
    <span class="text-sm font-semibold text-gray-900 dark:text-white">{e(d["report_id"])}</span>
    <div class="flex items-center gap-4 text-sm">
      <a href="#judgments" class="text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white">Judgments</a>
      <a href="#timeline" class="text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white">Timeline</a>
      <a href="#indicators" class="text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white">Indicators</a>
      <a href="#method" class="text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white">Method</a>
      <a href="{REPO}" class="text-blue-600 dark:text-blue-500 hover:underline">GitHub</a>
    </div>
  </div>
</nav>

<header class="bg-white dark:bg-gray-800">
  <div class="max-w-screen-xl mx-auto px-4 py-14 lg:py-20">
    <span class="inline-block mb-4 text-xs font-medium px-2.5 py-0.5 rounded bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300">Open-source intelligence assessment</span>
    <h1 class="mb-4 text-3xl font-extrabold tracking-tight leading-tight text-gray-900 md:text-4xl dark:text-white max-w-3xl">{e(d["title"])}</h1>
    <p class="mb-3 text-lg text-gray-500 dark:text-gray-400 max-w-3xl">A living intelligence report built from public sources only — graded sourcing, explicit confidence levels, competing hypotheses, and indicators that are re-swept on every update.</p>
    <p class="mb-8 text-base text-gray-500 dark:text-gray-400 max-w-3xl">The whole case is maintained by a single <code class="text-sm">/update-case</code> call in <a href="https://claude.com/claude-code" class="text-blue-600 dark:text-blue-500 hover:underline">Claude Code</a>: skills carry the tradecraft, subagents sweep and red-team the evidence, guard hooks enforce scope, and CI publishes this page. Clone the repo and run your own case the same way.</p>
    <div class="flex flex-wrap gap-3 mb-10">
      <a href="report.html" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">Read the full report</a>
      <a href="{REPO}" class="py-2.5 px-5 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700">Use it for your own case</a>
    </div>
    <dl class="grid grid-cols-2 gap-6 sm:grid-cols-4 max-w-2xl">
      <div><dt class="text-xs text-gray-500 dark:text-gray-400 uppercase">Status</dt><dd class="text-sm font-semibold text-gray-900 dark:text-white">{e(d["status"])}</dd></div>
      <div><dt class="text-xs text-gray-500 dark:text-gray-400 uppercase">Created</dt><dd class="text-sm font-semibold text-gray-900 dark:text-white">{e(d["created"])}</dd></div>
      <div><dt class="text-xs text-gray-500 dark:text-gray-400 uppercase">Last updated</dt><dd class="text-sm font-semibold text-gray-900 dark:text-white">{e(d["last_updated"][:16].replace("T"," "))} UTC</dd></div>
      <div><dt class="text-xs text-gray-500 dark:text-gray-400 uppercase">Evidence sections</dt><dd class="text-sm font-semibold text-gray-900 dark:text-white">{n_sections}</dd></div>
    </dl>
  </div>
</header>

<main class="max-w-screen-xl mx-auto px-4">

<section class="py-10">
  <h2 class="mb-6 text-xs font-semibold uppercase tracking-widest text-blue-700 dark:text-blue-500">Documents</h2>
  <div class="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">{doc_cards}</div>
</section>

{section('judgments', 'Key judgments', f'<div class="grid gap-4 md:grid-cols-2">{kj}</div>')}

{section('hypotheses', 'Competing hypotheses (ACH)', f"""
<div class="relative overflow-x-auto border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm">
<table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
<thead class="text-xs text-gray-700 uppercase bg-gray-100 dark:bg-gray-700 dark:text-gray-400">
<tr><th class="px-4 py-3">ID</th><th class="px-4 py-3">Hypothesis</th><th class="px-4 py-3">Assessment</th></tr></thead>
<tbody>{hyp}</tbody></table></div>""",
'Ranked by fewest inconsistencies with graded evidence (Heuer), not by count of consistent items.')}

{section('timeline', 'Timeline', f'<ol class="relative border-s border-gray-200 dark:border-gray-700">{tl}</ol>')}

{section('entities', 'Entities', f"""
<div class="grid gap-8 md:grid-cols-2">
<div><h3 class="mb-2 text-sm font-semibold text-gray-900 dark:text-white">Persons</h3><ul class="divide-y divide-gray-200 dark:divide-gray-700 text-sm">{persons}</ul></div>
<div><h3 class="mb-2 text-sm font-semibold text-gray-900 dark:text-white">Organizations</h3><ul class="divide-y divide-gray-200 dark:divide-gray-700 text-sm">{orgs}</ul></div>
</div>""")}

{section('indicators', 'Indicators to watch', f'<ul class="max-w-3xl divide-y divide-gray-200 dark:divide-gray-700">{ind}</ul>',
'What would confirm or refute each hypothesis. Re-swept on every update; "still open" is a recorded finding.')}

{section('sources', 'Primary sourcing', f'<ul class="divide-y divide-gray-200 dark:divide-gray-700 text-sm max-w-3xl">{srcs}</ul>',
'Full graded sourcing, attribution chains and negative results are in the report, §7–§8.')}

{section('method', 'Method & scope', f"""
<div class="prose prose-sm prose-gray dark:prose-invert max-w-3xl">
<p><strong>What this project is.</strong> A worked, public example of running a rigorous intelligence assessment with an AI coding agent:
the analytic tradecraft lives in version-controlled skill files, the evidence work is done by subagents, and every artifact
(report, structured data, bilingual briefs, PDFs, this page) is kept in sync and published automatically.</p>
<p><strong>Tradecraft.</strong> Key judgments carry High / Medium / Low confidence with a one-line reason and move only on traced
primary sources. Every source is graded on the Admiralty scale (A1–F6); two outlets repeating one wire count as one source.
Commentary is logged but never counts as evidence. Each proposed change passes an adversarial review — six evidence axioms
plus a cognitive-bias sweep — before it lands. Negative results are findings.</p>
<p><strong>Scope.</strong> Public web, GDELT, Wayback CDX and published sanctions lists — strictly open sources.
No reconnaissance against anyone's infrastructure and no bypass of any access control, regardless of instruction.</p>
</div>
<div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3 mt-8">{toolkit}</div>""")}

{section('changelog', 'Changelog', f'<ol class="relative border-s border-gray-200 dark:border-gray-700 max-w-3xl">{chlog}</ol>',
f'{len(d["changelog"])} entries, newest first. Earlier findings are never deleted — they are superseded.')}

</main>

<footer class="bg-white border-t border-gray-200 dark:bg-gray-800 dark:border-gray-700 mt-4">
  <div class="max-w-screen-xl mx-auto px-4 py-6 flex flex-wrap items-center justify-between gap-3">
    <span class="text-sm text-gray-500 dark:text-gray-400">Open sources only · every claim carries its source · unsourced assertions are logged as such</span>
    <div class="flex gap-4 text-sm">
      <a href="{REPO}" class="text-gray-500 dark:text-gray-400 hover:underline">GitHub</a>
      <a href="{REPO}/blob/main/LICENSE" class="text-gray-500 dark:text-gray-400 hover:underline">MIT + CC BY 4.0</a>
    </div>
  </div>
</footer>
{BODY_JS}</body></html>'''
(out / 'index.html').write_text(page, encoding='utf-8')
print(f'index.html ({len(page)} bytes), report.html written (Flowbite)')
