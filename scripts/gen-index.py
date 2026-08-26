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
    <a href="kj/{k["id"].lower()}.html" class="text-xs font-semibold text-blue-600 dark:text-blue-500 hover:underline me-3">{e(k["id"])} &rarr;</a>{conf_badge(k["confidence"])}
  </div>
  <p class="mb-2 font-semibold text-gray-900 dark:text-white">{e(k["statement"])}</p>
  <p class="text-sm text-gray-500 dark:text-gray-400">{e(k["support"])}</p>
</div>''' for k in d['key_judgments'])

hyp = '\n'.join(f'''
<tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 last:border-b-0">
  <th scope="row" class="px-4 py-3 font-medium whitespace-nowrap align-top"><a href="hy/{h["id"].lower()}.html" class="text-blue-600 dark:text-blue-500 hover:underline">{e(h["id"])} &rarr;</a></th>
  <td class="px-4 py-3 align-top"><span class="font-medium text-gray-900 dark:text-white">{e(h["label"])}</span>
    <p class="mt-1 text-gray-500 dark:text-gray-400">{e(h["description"])}</p></td>
  <td class="px-4 py-3 align-top text-gray-500 dark:text-gray-400">{e(h.get("likelihood",""))}</td>
</tr>''' for h in d['alternative_hypotheses'])

# Flowbite vertical timeline component
tl = '\n'.join(f'''
<li class="mb-6 ms-4">
  <div class="absolute w-3 h-3 bg-gray-200 rounded-full mt-1.5 -start-1.5 border border-white dark:border-gray-900 dark:bg-gray-700"></div>
  <time class="mb-1 text-xs font-normal leading-none text-gray-400 dark:text-gray-500"><a href="tl/t{n+1}.html" class="hover:underline text-blue-600 dark:text-blue-500">{e(t["date"])} &rarr;</a></time>
  <p class="text-sm font-normal text-gray-900 dark:text-white">{e(t["event"])}</p>
  <span class="text-xs text-gray-400 dark:text-gray-500">{e(t.get("source",""))}</span>
</li>''' for n, t in enumerate(d['timeline']))

def ent(x):
    name = x.get('name') or x.get('id', '')
    role = x.get('role') or x.get('notes') or ''
    return (f'<li class="py-2"><span class="font-medium text-gray-900 dark:text-white">{e(name)}</span>'
            f'<span class="text-gray-500 dark:text-gray-400"> — {e(role)}</span></li>')
persons = ''.join(ent(p) for p in d.get('entities', {}).get('persons', []))
orgs = ''.join(ent(o) for o in d.get('entities', {}).get('organizations', []))

def _itxt(x): return x if isinstance(x, str) else x.get('text', '')
ind = '\n'.join(f'''
<li class="flex items-start gap-2.5 py-2 text-sm text-gray-700 dark:text-gray-300">
  <a href="ind/i{n+1}.html" class="shrink-0 mt-0.5 text-xs font-semibold text-blue-600 dark:text-blue-500 hover:underline">I{n+1} &rarr;</a>
  <span>{e(_itxt(x))}</span></li>''' for n, x in enumerate(d['indicators_to_watch']))

srcs = '\n'.join(
    f'<li class="py-2"><a href="src/s{n+1}.html" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">{e(s["outlet"])}</a>'
    f'<span class="text-gray-500 dark:text-gray-400"> — {e(s.get("title",""))}</span>'
    f' <a href="{e(s["url"])}" rel="noopener" class="text-xs text-gray-400 hover:underline">[original]</a></li>'
    for n, s in enumerate(d.get('sources', [])))

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


# ---- stats (infographic row) ----
conf_counts = {'High': 0, 'Medium': 0, 'Low': 0}
for k in d['key_judgments']:
    w = k['confidence'].split(' ')[0].split('\u2013')[0].split('-')[0].capitalize()
    conf_counts[w if w in conf_counts else 'Medium'] += 1
data_pulls = len(list(pathlib.Path('data').glob('*.json')))
stats = [
    (str(len(d['key_judgments'])), 'key judgments',
     f"{conf_counts['High']} high · {conf_counts['Medium']} medium · {conf_counts['Low']} low"),
    (str(len(d['alternative_hypotheses'])), 'hypotheses', 'scored by inconsistencies'),
    (str(len(d['indicators_to_watch'])), 'open indicators', 're-swept every cycle'),
    (str(n_sections), 'evidence sections', 'append-only, superseded never deleted'),
    (str(len(d.get('sources', []))), 'primary sources', 'graded A1\u2013F6'),
    (str(data_pulls), 'raw data pulls', 'timestamped, immutable'),
]
stats_html = '\n'.join(f"""
<div class="p-4 text-center bg-white border border-gray-200 rounded-lg shadow-sm dark:bg-gray-800 dark:border-gray-700">
  <p class="text-3xl font-extrabold text-blue-700 dark:text-blue-500">{v}</p>
  <p class="text-sm font-semibold text-gray-900 dark:text-white mt-1">{l}</p>
  <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">{sub}</p>
</div>""" for v, l, sub in stats)

# ---- pipeline stepper (Flowbite stepper pattern) ----
steps = [('Status', 'read judgments + open indicators'),
         ('Sweep', 'web \u00b7 GDELT \u00b7 Wayback, per indicator'),
         ('Trace', 'every claim back to a primary'),
         ('Red-team', '6 axioms + bias sweep gate'),
         ('Write', '\u00a78.N + confidence moves'),
         ('Mirror', 'data.json + 4 artifacts'),
         ('Publish', 'render \u00b7 check \u00b7 CI \u00b7 Pages')]
pipeline = '<ol class="flex flex-col gap-5 md:flex-row md:gap-0 items-start w-full">' + '\n'.join(f"""
<li class="flex md:flex-col items-start md:items-center flex-1 gap-3 md:gap-0 {'md:after:content-[\'\'] md:after:w-full md:after:h-0.5 md:after:bg-gray-200 dark:md:after:bg-gray-700 md:after:order-first md:after:translate-y-4' if i else ''}">
  <span class="flex items-center justify-center w-8 h-8 shrink-0 {'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300' if i == 0 else 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300'} rounded-full text-sm font-bold md:mb-2">{i+1}</span>
  <span class="md:text-center"><span class="block text-sm font-semibold text-gray-900 dark:text-white">{t}</span>
  <span class="block text-xs text-gray-500 dark:text-gray-400 md:px-2">{x}</span></span>
</li>""" for i, (t, x) in enumerate(steps)) + '</ol>'

# ---- quickstart (run your own case) ----
def codeblock(code):
    return (f'<pre class="p-4 overflow-x-auto text-sm text-gray-100 bg-gray-900 rounded-lg dark:bg-gray-950 '
            f'border border-gray-700"><code>{e(code)}</code></pre>')
quickstart = f"""
<div class="grid gap-6 lg:grid-cols-3">
  <div class="lg:col-span-2 space-y-4">
    <h3 class="text-sm font-semibold text-gray-900 dark:text-white">1 \u00b7 Clone and install the tooling</h3>
    {codeblock('git clone ' + REPO + chr(10) + 'cd osint-case-ratcliffe-moscow-2026' + chr(10) + 'brew install just jq yq weasyprint   # or apt/pip equivalents' + chr(10) + 'just                                  # list all tasks')}
    <h3 class="text-sm font-semibold text-gray-900 dark:text-white pt-2">2 \u00b7 Open it in Claude Code</h3>
    {codeblock('claude' + chr(10) + chr(10) + '> /update-case            # one call: sweep -> trace -> red-team -> write -> render -> check' + chr(10) + '> /publish                # commit, push, deploy GitHub Pages' + chr(10) + '> /new-case my-case "My subject"   # start your own case, same layout + rules')}
    <h3 class="text-sm font-semibold text-gray-900 dark:text-white pt-2">3 \u00b7 Inspect without Claude</h3>
    {codeblock('just status     # judgments + open indicators' + chr(10) + 'just gdelt      # GDELT DOC 2.0 pull into data/' + chr(10) + 'just watch      # Wayback CDX snapshots of watch URLs' + chr(10) + 'just pdf check  # render PDFs, run the consistency gate')}
  </div>
  <div class="space-y-3">
    <div class="p-4 bg-blue-50 border border-blue-200 rounded-lg dark:bg-gray-800 dark:border-blue-900">
      <h3 class="mb-1 text-sm font-semibold text-blue-800 dark:text-blue-400">What you get</h3>
      <ul class="text-sm text-blue-900 dark:text-gray-300 list-disc list-inside space-y-1">
        <li>Tradecraft as version-controlled skill files</li>
        <li>Three subagents with strict JSON contracts</li>
        <li>Guard hooks: scope, append-only data, no force-push</li>
        <li>Consistency gate (<code>just check</code>) incl. forbidden-terms scan</li>
        <li>CI that renders PDFs and deploys this page</li>
      </ul>
    </div>
    <div class="p-4 bg-white border border-gray-200 rounded-lg dark:bg-gray-800 dark:border-gray-700">
      <h3 class="mb-1 text-sm font-semibold text-gray-900 dark:text-white">Requirements</h3>
      <p class="text-sm text-gray-500 dark:text-gray-400"><code>curl</code>, <code>jq</code>, <code>yq</code>, <code>python3</code>, <code>weasyprint</code>, <code>just</code>; <code>gh</code> for publishing; <a href="https://claude.com/claude-code" class="text-blue-600 dark:text-blue-500 hover:underline">Claude Code</a> for the one-call workflow. No API keys needed \u2014 GDELT and Wayback are public.</p>
    </div>
  </div>
</div>"""


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

<section class="pb-2"><div class="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">{stats_html}</div></section>

{section('judgments', 'Key judgments', f'<div class="grid gap-4 md:grid-cols-2">{kj}</div>')}

{section('pipeline', 'How each update is produced', pipeline, 'Every cycle is one <code>/update-case</code> call; no step can be skipped and no confidence level moves without the red-team gate.')}

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

{section('quickstart', 'Run your own case', quickstart, 'This repository doubles as a reusable mini case app: fork it, keep the toolkit, replace the content.')}

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
