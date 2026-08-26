# Artifact sync checklist

`report.md` is the source of truth. Every update must be mirrored, in this order, and
`just check` must pass at the end.

| Artifact | What to touch |
|---|---|
| `report.md` | new `## 8.N` section (scaffolded by `just section`), KJ text/confidence in §2, ACH in §3 if re-scored, indicator statuses in §6, timeline rows in §4 if dated events were found, changelog line in §11 |
| `data.json` | new `<slug>_sweep` object (`method`, `findings[]`, `sources[]`, `unchanged[]`), updated `key_judgments[].confidence/support`, `indicators_to_watch`, `timeline`, `last_updated`, appended `changelog[]` entry |
| `report/brief/brief-en.html` | a short `<div class="section">` block for the new sweep (same `h2` count as before + 1, or extend the last sweep section) |
| `report/brief/brief-cs.html` | Czech mirror of the same block |
| `report/pdf/pdf-en.html` | matching `<h2><span class="num">NN</span>…</h2>` block |
| `report/pdf/pdf-cs.html` | Czech mirror |
| PDFs | `just pdf` regenerates `report/pdf/report-{en,cs}.pdf` |

## §8.N section template

```markdown
## 8.N <Title> (<YYYY-MM-DD HH:MM TZ>)

*(Method: <N> web searches, GDELT sweep <ts>, Wayback watch <from>; agents: sweeper/tracer/red-team.)*

### 8.N.1 <Indicator or lead> — <one-line verdict>
<finding, with source grade [B2] and link/outlet/date>. <what changed>. **KJx unchanged / KJx Medium → High (reason)**.

### 8.N.k Unchanged indicators
- <indicator> — still open; searched <terms/venues>.
```

## Brief block template (EN; mirror in CS)

```html
<div class="section">
  <div class="section-head"><span class="section-num">NN</span><h2>Re-sweep (<date>)</h2></div>
  <div class="section-body">
    <div class="kj-list">
      <div class="kj-item"><span class="kj-id">Lead</span><div><span class="pill medium">Status</span><p class="kj-text">…</p></div></div>
    </div>
    <p class="caveat">Unchanged: …</p>
  </div>
</div>
```

## Site layer (automatic — do not hand-edit)

`just site` regenerates `_site/` entirely from `data.json` + `report.md` + git history:
`scripts/gen-index.py` (landing) and `scripts/gen-detail-pages.py` (one page per key
judgment `kj/`, hypothesis `hy/`, indicator `ind/`, source `src/`, each with a
history timeline reconstructed from every committed revision of `data.json`).
Consequences for updates:
- keep entity `id`s stable (`KJ1`, `H2`); indicator order is the identity for `I<n>` pages —
  append new indicators at the end, never reorder; closing one = set its object form
  `{"id": "I<n>", "text": …, "status": "observed|refuted"}` (strings default to open)
- every committed `data.json` state becomes a history entry — commit via `/publish` only
- new sources appended to `sources[]` get a page automatically (`grade` field optional but preferred)

## Final gate

- `jq -e . data.json`
- both briefs and both PDF templates have the same number of `<h2>` as each other's language pair
- `grep` for forbidden terms from `case.yaml: forbidden_terms` returns nothing
- changelog last line matches the new section number
