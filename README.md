# CIA Director's unannounced Moscow visit (2026-08-25) — open-source intelligence assessment

A living OSINT intelligence assessment, maintained entirely with Claude Code skills and a
few shell scripts. Open sources only; every claim carries its source and a grade.

**Read it:** the published site (GitHub Pages) has the EN/CS briefs, PDFs and the full report.
Source of truth is [`report.md`](report.md); [`data.json`](data.json) is its structured mirror.

## Reuse this repository for your own case

The case-specific content is `report.md`, `data.json`, `case.yaml`, `data/` and `report/`.
Everything else is a reusable, brand-neutral OSINT-assessment toolkit:

| Piece | What it gives you |
|---|---|
| `.claude/skills/update-case/` | **One call updates the whole case**: status → sweep every open indicator (web, GDELT, Wayback) → trace sources to primaries → red-team proposed changes → write §8.N → mirror into data.json + 4 HTML artifacts → render → check |
| `.claude/skills/update-case/references/` | The tradecraft: Admiralty source grading, ICD-203-style confidence rules, minimal ACH, indicator statuses, negative-result logging, ethics/scope hard stops, six-axiom red-team checklist, artifact sync checklist |
| `.claude/agents/` | `indicator-sweeper`, `source-tracer`, `red-team` subagents with strict JSON contracts |
| `.claude/hooks/` + `.claude/settings.json` | Guards: `data/` append-only, no hand-edited PDFs, no force-push/history rewrite, no recon tooling; post-turn sync check; permission allowlist so the cycle runs without prompts |
| `.claude/skills/publish/` | Render → build site → check → conventional commit → push → confirm Pages deploy |
| `.claude/skills/new-case/` | Scaffold a fresh case with the same layout |
| `scripts/`, `justfile` | `just status / gdelt / watch / wayback / section / pdf / site / check` |
| `.github/workflows/pages.yml` | CI: renders PDFs with WeasyPrint, builds `_site/`, deploys GitHub Pages |

### Quick start

```bash
git clone <this repo> && cd <repo>
brew install just jq yq weasyprint   # or apt/pip equivalents
just                                  # list tasks
just status                           # current judgments + open indicators
claude                                # then: /update-case   (or /new-case my-case "Title")
```

### Method in one paragraph

Key judgments carry High/Medium/Low confidence with a one-line reason and move only on
traced primary sources. Competing hypotheses are scored by inconsistencies (Heuer). Every
source is graded A1–F6. Commentary is logged but never counts as evidence. Indicators are
re-swept each cycle; "still open — searched X, Y, Z" is a recorded finding. Every proposed
change passes an adversarial review (six evidence axioms + bias sweep) before it lands.
Scope is strictly open-source: no reconnaissance against anyone's infrastructure.

## Layout

```
report.md          source of truth        report/brief/brief-{en,cs}.html   shareable briefs
data.json          structured mirror      report/pdf/pdf-{en,cs}.html       PDF templates → report-{en,cs}.pdf
case.yaml          query/window/watch     data/                             raw pulls, timestamped, append-only
.claude/           skills, agents, hooks  scripts/ + justfile               tooling
```

## Licence

Report text and data: CC BY 4.0. Tooling (`.claude/`, `scripts/`, `justfile`, workflow): MIT.
