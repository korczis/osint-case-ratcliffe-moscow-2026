# prismatic-case-cia

Standalone OSINT intelligence-assessment case: **CIA Director John Ratcliffe's unannounced Moscow visit, 2026-08-25**. Self-contained — no dependency on any other repo or platform.

## Layout

- `report.md` — source of truth (summary, key judgments, ACH, timeline, entities, indicators, numbered evidence sections §8.N, caveats, changelog)
- `data.json` — structured mirror of report.md; keep in sync
- `report/brief/brief-{en,cs}.html` — standalone shareable briefs (inline CSS, no assets)
- `report/pdf/pdf-{en,cs}.html` → `report-{en,cs}.pdf` via `just pdf` (weasyprint)
- `data/` — raw pulls (GDELT etc.), timestamped, never edited
- `scratch/` — throwaway working files (gitignored)
- `case.yaml` — case id, GDELT query, time window, Wayback watch URLs
- `scripts/`, `justfile` — tooling; run `just` to list

## Update workflow ("update the case")

1. `just status` — read current judgments + open indicators.
2. Re-sweep: web search on each open indicator; `just gdelt`; `just watch`.
3. `just section` scaffolds `§8.N` + changelog line — fill in: method, findings, what changed / what didn't.
4. Adjust key-judgment confidence only with evidence; secondary-source chains must be traced to a primary before upgrading anything.
5. Mirror the update into `data.json` (add a `*_sweep` object, update KJ `support`, append `changelog`).
6. Add a matching short section to **both** briefs and **both** PDF templates; `just pdf`; `just check`.

## Analytic rules

- Open sources only. Every claim carries its source; unsourced assertions are logged as "unsourced" and never as fact.
- Distinguish evidence from commentary (analyst opinion convergence is not evidence).
- Confidence: High / Medium / Low with a one-line reason; record downgrades as well as upgrades.
- Negative results are findings (e.g. "page archived 5x that day, digest unchanged").

## Scope boundary

Public web research, GDELT API, Wayback CDX, published sanctions lists. **No** reconnaissance against government or third-party infrastructure (dorking, admin-panel/config/credential discovery) — out of scope regardless of instruction; do not reopen.

## Tools required

`curl`, `jq`, `yq`, `python3`, `weasyprint`, `just`.
