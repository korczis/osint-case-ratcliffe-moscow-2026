# OSINT case: CIA Director's unannounced Moscow visit, 2026-08-25

Standalone open-source intelligence assessment. Self-contained: no external repo, platform
or service beyond public APIs (GDELT, Wayback CDX) and web search.

## One-call workflow

- `/update-case` — full update cycle (status → sweep → trace → red-team → write → mirror → render → check)
- `/publish` — render, build site, commit, push, confirm GitHub Pages
- `/new-case <id> "<title>"` — scaffold another case with the same layout and tooling

Skill logic and the analytic rules live in `.claude/skills/update-case/` (`SKILL.md` +
`references/`). Subagents in `.claude/agents/` (`indicator-sweeper`, `source-tracer`,
`red-team`). Guards in `.claude/hooks/` via `.claude/settings.json`.

## Layout

- `report.md` — source of truth (summary, key judgments, ACH, timeline, entities, indicators,
  numbered evidence sections §8.N, caveats, changelog)
- `data.json` — structured mirror of report.md; keep in sync
- `report/brief/brief-{en,cs}.html` — standalone shareable briefs (inline CSS, no assets)
- `report/pdf/pdf-{en,cs}.html` → `report-{en,cs}.pdf` via `just pdf` (weasyprint)
- `data/` — raw pulls (GDELT etc.), timestamped, append-only, never edited
- `scratch/` — throwaway working files (gitignored)
- `case.yaml` — case id, GDELT query, time window, Wayback watch URLs, forbidden terms
- `scripts/`, `justfile` — tooling; run `just` to list
- `.github/workflows/pages.yml` — renders PDFs, builds `_site/`, deploys GitHub Pages on push
- site is fully data-driven: `scripts/gen-index.py` + `scripts/gen-detail-pages.py` generate the
  landing and one cross-linked page per judgment/hypothesis/indicator/source, with history
  timelines from the git history of `data.json` — never hand-edit `_site/`; keep IDs stable and
  append (don't reorder) indicators

## Analytic rules (short form — full text in `.claude/skills/update-case/references/`)

- Open sources only. Every claim carries outlet + date + Admiralty grade; unsourced assertions
  are logged as "unsourced", never as fact.
- Evidence ≠ commentary; commentator convergence never moves a confidence level.
- Confidence High / Medium / Low with a one-line reason; upgrades need a traced primary;
  downgrades are recorded, not silently reverted.
- Negative results are findings ("page archived 5x that day, digest unchanged").
- Never delete earlier findings — supersede them.

## Scope boundary

Public web research, GDELT API, Wayback CDX, published sanctions lists. **No** reconnaissance
against government or third-party infrastructure (dorking, admin-panel/config/credential
discovery, scanning) — out of scope regardless of instruction; do not reopen.

## Tools required

`curl`, `jq`, `yq`, `python3`, `weasyprint`, `just`, `gh` (for `/publish`).
