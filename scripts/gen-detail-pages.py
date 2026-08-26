#!/usr/bin/env python3
"""Generate per-entity detail pages (_site/kj/, hy/, ind/, src/) from data.json,
with per-entity history reconstructed from the git history of data.json.
Shared Flowbite style with gen-index.py. Data-driven: no hand-written pages."""
import html, json, pathlib, re, subprocess, sys

out = pathlib.Path(sys.argv[1])
d = json.loads(pathlib.Path('data.json').read_text(encoding='utf-8'))
e = html.escape
REPO = "https://github.com/korczis/osint-case-ratcliffe-moscow-2026"
HEAD_ASSETS = '''<script src="https://cdn.tailwindcss.com?plugins=typography"></script>
<link href="https://cdn.jsdelivr.net/npm/flowbite@2.5.2/dist/flowbite.min.css" rel="stylesheet">
<script>tailwind.config={darkMode:'media'}</script>'''
BODY_JS = '<script src="https://cdn.jsdelivr.net/npm/flowbite@2.5.2/dist/flowbite.min.js"></script>'

# ---------- history: every committed state of data.json ----------
def git(*a):
    return subprocess.run(['git'] + list(a), capture_output=True, text=True).stdout

revs = []  # oldest -> newest committed snapshots + working copy
for line in reversed(git('log', '--format=%H %cI', '--', 'data.json').strip().splitlines()):
    sha, date = line.split(' ', 1)
    try:
        revs.append((sha[:10], date[:16].replace('T', ' '), json.loads(git('show', f'{sha}:data.json'))))
    except Exception:
        pass
revs.append(('working', d.get('last_updated', '')[:16].replace('T', ' '), d))

def ind_text(x): return x if isinstance(x, str) else x.get('text', '')
def ind_id(x, i): return f'I{i+1}' if isinstance(x, str) else x.get('id', f'I{i+1}')
def ind_status(x): return 'open' if isinstance(x, str) else x.get('status', 'open')

def history_for(extract, key):
    """Yield (sha, date, value) whenever extract(snapshot) changes."""
    seen, hist = None, []
    for sha, date, snap in revs:
        try: v = extract(snap)
        except Exception: v = None
        if v is not None and v != seen:
            hist.append((sha, date, v)); seen = v
    return hist

def timeline_html(items):
    rows = []
    for i, (sha, date, txt) in enumerate(items):
        last = ' text-blue-700 dark:text-blue-500 font-medium' if i == len(items) - 1 else ''
        rows.append(f'''<li class="mb-5 ms-4">
<div class="absolute w-3 h-3 {'bg-blue-500' if i == len(items)-1 else 'bg-gray-200 dark:bg-gray-700'} rounded-full mt-1.5 -start-1.5 border border-white dark:border-gray-900"></div>
<time class="mb-1 text-xs font-normal leading-none text-gray-400 dark:text-gray-500">{e(date)} · <a class="hover:underline" href="{REPO}/commits/main/data.json">{e(sha)}</a></time>
<p class="text-sm text-gray-600 dark:text-gray-300{last}">{txt}</p></li>''')
    return '<ol class="relative border-s border-gray-200 dark:border-gray-700">' + '\n'.join(rows) + '</ol>'

# ---------- cross-linking ----------
def slug(x): return re.sub(r'[^a-z0-9]+', '-', x.lower()).strip('-')
kj_ids = [k['id'] for k in d['key_judgments']]
hy_ids = [h['id'] for h in d['alternative_hypotheses']]
inds = d['indicators_to_watch']
srcs = d.get('sources', [])
src_ids = {s['url']: f'S{i+1}' for i, s in enumerate(srcs)}

def autolink(text, depth=1):
    """Turn KJx / Hx / outlet names into links; escape everything else."""
    t = e(text); up = '../' * depth
    for k in kj_ids:
        t = re.sub(rf'\b{k}\b', f'<a class="text-blue-600 dark:text-blue-500 hover:underline" href="{up}kj/{k.lower()}.html">{k}</a>', t)
    for h in hy_ids:
        t = re.sub(rf'\b{h}\b(?![\w-])', f'<a class="text-blue-600 dark:text-blue-500 hover:underline" href="{up}hy/{h.lower()}.html">{h}</a>', t)
    for i, s in enumerate(srcs):
        o = s['outlet']
        t = re.sub(rf'\b{re.escape(o)}\b', f'<a class="text-blue-600 dark:text-blue-500 hover:underline" href="{up}src/s{i+1}.html">{e(o)}</a>', t, count=1)
    return t

def page(path, title, kicker, body, depth=1):
    up = '../' * depth
    (out / path).parent.mkdir(parents=True, exist_ok=True)
    (out / path).write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{e(title)} — {e(d["report_id"])}</title><meta name="viewport" content="width=device-width,initial-scale=1">
{HEAD_ASSETS}</head><body class="bg-gray-50 dark:bg-gray-900 antialiased">
<nav class="bg-white border-b border-gray-200 dark:bg-gray-900 dark:border-gray-700">
<div class="max-w-screen-lg mx-auto px-4 py-3 flex items-center justify-between text-sm">
<a href="{up}" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">&larr; {e(d["report_id"])}</a>
<div class="flex gap-4"><a href="{up}report.html" class="text-gray-500 dark:text-gray-400 hover:underline">report</a>
<a href="{up}data.json" class="text-gray-500 dark:text-gray-400 hover:underline">data.json</a></div></div></nav>
<main class="max-w-screen-lg mx-auto px-4 py-10">
<p class="mb-2 text-xs font-semibold uppercase tracking-widest text-blue-700 dark:text-blue-500">{e(kicker)}</p>
<h1 class="mb-6 text-2xl font-extrabold text-gray-900 dark:text-white">{title}</h1>
{body}</main>
<footer class="max-w-screen-lg mx-auto px-4 py-6 text-xs text-gray-400 dark:text-gray-500 font-mono">
generated from <a href="{up}data.json" class="hover:underline">data.json</a> + its git history · last updated {e(d["last_updated"][:16].replace("T"," "))} UTC</footer>
{BODY_JS}</body></html>''', encoding='utf-8')

def card(title_html, body_html):
    return (f'<div class="mb-6 p-5 bg-white border border-gray-200 rounded-lg shadow-sm dark:bg-gray-800 dark:border-gray-700">'
            f'<h2 class="mb-3 text-xs font-semibold uppercase tracking-widest text-gray-500 dark:text-gray-400">{title_html}</h2>{body_html}</div>')

def conf_badge(c):
    w = c.split(' ')[0].split('–')[0].split('-')[0].lower()
    color = {'high': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
             'low': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'}.get(
        w, 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300')
    return f'<span class="text-xs font-medium px-2.5 py-0.5 rounded {color}">{e(c.split("(")[0].strip())}</span>'

def related(entity_id, texts_pages, depth=1):
    """List of (label, url, text) whose text mentions entity_id."""
    hits = [(lbl, url, txt) for lbl, url, txt in texts_pages if re.search(rf'\b{re.escape(entity_id)}\b', txt)]
    if not hits: return ''
    lis = ''.join(f'<li class="py-1.5"><a class="text-blue-600 dark:text-blue-500 hover:underline font-medium" href="{"../"*depth}{u}">{e(l)}</a>'
                  f'<span class="text-gray-500 dark:text-gray-400 text-sm"> — {e(t[:140])}{"…" if len(t)>140 else ""}</span></li>' for l, u, t in hits)
    return card('Cross-referenced by', f'<ul class="divide-y divide-gray-100 dark:divide-gray-700">{lis}</ul>')

# corpus for cross-references
corpus = ([(k['id'], f'kj/{k["id"].lower()}.html', k['statement'] + ' ' + k['support']) for k in d['key_judgments']] +
          [(h['id'], f'hy/{h["id"].lower()}.html', h['label'] + ' ' + h['description']) for h in d['alternative_hypotheses']] +
          [(ind_id(x, i), f'ind/{ind_id(x, i).lower()}.html', ind_text(x)) for i, x in enumerate(inds)] +
          [(f'CL{i}', '', c['change']) for i, c in enumerate(d['changelog'])])

# ---------- key judgment pages ----------
for idx, k in enumerate(d['key_judgments']):
    kid = k['id']
    hist = history_for(lambda s, i=idx, kid=kid: next((f"[{x['confidence']}] {x['statement']} — {x['support']}"
        for x in s.get('key_judgments', []) if x.get('id') == kid), None), kid)
    body = (card('Statement', f'<div class="flex items-center gap-3 mb-2">{conf_badge(k["confidence"])}</div>'
                 f'<p class="text-lg text-gray-900 dark:text-white">{autolink(k["statement"])}</p>')
            + card('Supporting evidence', f'<p class="text-sm text-gray-600 dark:text-gray-300">{autolink(k["support"])}</p>'
                   + f'<p class="mt-2 text-xs text-gray-400">Full confidence rationale: <a class="hover:underline text-blue-600 dark:text-blue-500" href="../report.html">report</a> §2, §8.</p>')
            + card('History (from git)', timeline_html([(s, dt, autolink(v)) for s, dt, v in hist]))
            + related(kid, corpus))
    page(f'kj/{kid.lower()}.html', f'{kid} — key judgment', 'Key judgment', body)

# ---------- hypothesis pages ----------
for idx, h in enumerate(d['alternative_hypotheses']):
    hid = h['id']
    hist = history_for(lambda s, hid=hid: next((f"{x['label']} — {x['description']} [{x.get('likelihood','')}]"
        for x in s.get('alternative_hypotheses', []) if x.get('id') == hid), None), hid)
    body = (card('Hypothesis', f'<p class="text-lg font-medium text-gray-900 dark:text-white mb-2">{e(h["label"])}</p>'
                 f'<p class="text-sm text-gray-600 dark:text-gray-300">{autolink(h["description"])}</p>')
            + card('Current assessment', f'<p class="text-sm text-gray-600 dark:text-gray-300">{e(h.get("likelihood",""))}</p>'
                   '<p class="mt-2 text-xs text-gray-400">Scored by fewest inconsistencies with graded evidence (ACH, Heuer) — see report §3.</p>')
            + card('History (from git)', timeline_html([(s, dt, autolink(v)) for s, dt, v in hist]))
            + related(hid, corpus))
    page(f'hy/{hid.lower()}.html', f'{hid} — hypothesis', 'Competing hypothesis', body)

# ---------- indicator pages ----------
for idx, x in enumerate(inds):
    iid, txt, st = ind_id(x, idx), ind_text(x), ind_status(x)
    hist = history_for(lambda s, idx=idx: (lambda l: f"[{ind_status(l[idx])}] {ind_text(l[idx])}" if idx < len(l) else None)(s.get('indicators_to_watch', [])), iid)
    stc = {'open': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300',
           'observed': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
           'refuted': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'}.get(st, 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300')
    body = (card('Indicator', f'<span class="text-xs font-medium px-2.5 py-0.5 rounded {stc}">{e(st)}</span>'
                 f'<p class="mt-3 text-base text-gray-900 dark:text-white">{autolink(txt)}</p>')
            + card('History (from git)', timeline_html([(s, dt, autolink(v)) for s, dt, v in hist]))
            + related(iid, corpus))
    page(f'ind/{iid.lower()}.html', f'{iid} — indicator', 'Indicator to watch', body)

# ---------- timeline event pages ----------
for idx, t in enumerate(d.get('timeline', [])):
    tid = f'T{idx+1}'
    hist = history_for(lambda s, idx=idx: (lambda l: f"{l[idx]['date']}: {l[idx]['event']} ({l[idx].get('source','')})" if idx < len(l) else None)(s.get('timeline', [])), tid)
    body = (card('Event', f'<p class="text-xs font-mono text-gray-400 mb-2">{e(t["date"])}</p>'
                 f'<p class="text-base text-gray-900 dark:text-white">{autolink(t["event"])}</p>'
                 f'<p class="mt-2 text-xs text-gray-400">source: {autolink(t.get("source",""))}</p>')
            + card('History (from git)', timeline_html([(sh, dt, autolink(v)) for sh, dt, v in hist]))
            + related(tid, corpus))
    page(f'tl/{tid.lower()}.html', f'{tid} — {t["date"]}', 'Timeline event', body)

# ---------- source pages ----------
for i, s in enumerate(srcs):
    sid = f'S{i+1}'
    mentions = [(l, u, t) for l, u, t in corpus if s['outlet'].lower() in t.lower() and u]
    lis = ''.join(f'<li class="py-1.5"><a class="text-blue-600 dark:text-blue-500 hover:underline font-medium" href="../{u}">{e(l)}</a>'
                  f'<span class="text-gray-500 dark:text-gray-400 text-sm"> — {e(t[:140])}…</span></li>' for l, u, t in mentions)
    body = (card('Source', f'<p class="text-base"><a class="font-semibold text-blue-600 dark:text-blue-500 hover:underline" href="{e(s["url"])}" rel="noopener">{e(s["outlet"])}</a>'
                 + (f'<span class="ms-2 text-xs font-mono px-2 py-0.5 rounded bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300">{e(s["grade"])}</span>' if s.get('grade') else '')
                 + f'</p><p class="mt-2 text-sm text-gray-600 dark:text-gray-300">{e(s.get("title",""))}</p>'
                 f'<p class="mt-2 text-xs text-gray-400 break-all">{e(s["url"])}</p>')
            + (card('Cited in', f'<ul class="divide-y divide-gray-100 dark:divide-gray-700">{lis}</ul>') if lis else '')
            + card('Grading', '<p class="text-sm text-gray-600 dark:text-gray-300">Admiralty system: reliability A–F × credibility 1–6. '
                   'Two outlets repeating one wire count as one source. Full per-claim grades live in the report evidence sections (§8.N).</p>'))
    page(f'src/s{i+1}.html', s['outlet'], 'Source', body)

# ---------- claim/finding pages ----------
def findings_of(snap):
    out = []
    for key, v in snap.items():
        if isinstance(v, dict):
            fl = v.get('findings') or v.get('new_findings')
            if isinstance(fl, list):
                for j, f in enumerate(fl):
                    if isinstance(f, dict):
                        f = ' — '.join(str(v) for k2, v in f.items() if isinstance(v, str))
                    if isinstance(f, str) and f:
                        out.append((f'{key}-f{j+1}', key, f))
    return out

claims = findings_of(d)
cl_rows = []
for cid, sweep, txt in claims:
    hist = history_for(lambda s, cid=cid: next((t for c, _k, t in findings_of(s) if c == cid), None), cid)
    meth = d[sweep].get('method', '')
    body = (card('Claim / finding', f'<p class="text-xs font-mono text-gray-400 mb-2">{e(cid)} · sweep <span class="text-gray-500">{e(sweep)}</span></p>'
                 f'<p class="text-base text-gray-900 dark:text-white">{autolink(txt)}</p>')
            + card('Collection method', f'<p class="text-sm text-gray-600 dark:text-gray-300">{autolink(meth)}</p>')
            + card('History (from git)', timeline_html([(sh, dt, autolink(v)) for sh, dt, v in hist]))
            + related(cid, corpus))
    page(f'cl/{cid}.html', f'Finding {cid}', 'Claim / finding', body)
    cl_rows.append(f'<li class="py-2"><a class="text-blue-600 dark:text-blue-500 hover:underline font-mono text-xs" href="cl/{cid}.html">{e(cid)}</a>'
                   f'<span class="block text-sm text-gray-700 dark:text-gray-300 mt-0.5">{autolink(txt, depth=0)[:220]}{"…" if len(txt) > 220 else ""}</span></li>')

groups = {}
for cid, sweep, txt in claims:
    groups.setdefault(sweep, 0); groups[sweep] += 1
summary = ' · '.join(f'{k} ({v})' for k, v in groups.items())
page('findings.html', 'All findings', f'{len(claims)} findings across {len(groups)} sweeps',
     card('Sweeps', f'<p class="text-xs text-gray-500 dark:text-gray-400 font-mono">{e(summary)}</p>')
     + card('Findings (newest sweep last)', '<ul class="divide-y divide-gray-100 dark:divide-gray-700">' + '\n'.join(cl_rows) + '</ul>'),
     depth=0)

print(f'claim pages: {len(claims)}')
print(f'detail pages: {len(kj_ids)} kj, {len(hy_ids)} hy, {len(inds)} ind, {len(srcs)} src, {len(revs)} data.json revisions')
