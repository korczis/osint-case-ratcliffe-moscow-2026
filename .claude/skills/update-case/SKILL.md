---
name: update-case
description: Run one full update cycle of this OSINT case — status, re-sweep every open indicator (web + GDELT + Wayback), trace sources, red-team proposed judgment changes, write §8.N, mirror into data.json and all four briefs/PDF templates, render, check. Use for "update the case", "re-sweep", "what's new", "causa update".
argument-hint: "[--quick] [--focus=<indicator keyword>] [--no-render]"
allowed-tools: Bash, Read, Edit, Write, Grep, Glob, WebSearch, WebFetch, Agent
---

# /update-case — one call, whole cycle

You are the case analyst. Follow the phases in order; do not skip the gate. Everything you
write must obey `references/methodology.md` and `references/ethics-scope.md` (read both now
if this is the first run in this session; skim `references/red-team.md` and
`references/sync-checklist.md` before phases 4 and 5).

Arguments: `--quick` = indicator sweep only, no GDELT/Wayback; `--focus=<kw>` = only indicators
matching the keyword; `--no-render` = skip `just pdf`.

## Phase 0 — Orient (never skip)

```bash
just status            # judgments, open indicators, last change
yq . case.yaml          # id, query, window, watch_urls, forbidden_terms
```
Read §2, §3, §6 and the last two `## 8.N` sections of `report.md`. Note the next section
number N. Record the UTC timestamp of this run; it is used in every artifact.

## Phase 1 — Collect (parallel)

Run these together:

1. **Structured pulls** (skip with `--quick`):
   `just gdelt` and `just watch` — read the printed summaries; raw files land in `data/`
   timestamped and are never edited.
2. **Indicator sweep**: launch one `indicator-sweeper` agent per open indicator (or per
   `--focus` match; batch 3–4 indicators per agent if there are more than 8). Each returns
   `{indicator, status, findings[{claim, outlet, date, url, grade, chain}], searched[]}`.
3. **Watch-URL delta**: classify each `just watch` line as `NO CHANGE` (same digest count),
   `CHANGE` (new snapshot, digest unchanged), `ALERT` (new digest) — an ALERT means the
   official page changed; fetch it with WebFetch and read it.

## Phase 2 — Trace

For every finding that could move a judgment or close an indicator, launch a
`source-tracer` agent with the claim and the outlets seen. It returns the originator, the
chain, the grade, and whether a primary was reached. Findings whose chain does not reach a
primary are tagged `unsourced` and cannot upgrade anything.

## Phase 3 — Assess

Draft the proposed changes as a list: `KJx: <old> → <new>, because <traced evidence>`;
`Hx: +C/+I from E<new>`; `indicator: open → observed/refuted`. If the list is empty, the
update is still valid — proceed with "unchanged" findings (negative results are findings).

## Phase 4 — Red-team gate

Launch the `red-team` agent with the proposed-change list and the traced evidence. Apply its
verdicts: STRONG → as proposed; MODERATE → one confidence level lower; WEAK → lead only, no
change. Record the verdict summary in the section's method line.

## Phase 5 — Write

1. `just section` — scaffolds `## 8.N` and the changelog stub.
2. Fill §8.N using the template in `references/sync-checklist.md`; update §2 confidence lines
   (with reason), §3 ACH marks if re-scored, §6 indicator statuses, §4 timeline rows for any
   newly dated event, §11 changelog line.
3. Mirror into `data.json`: add `resweep_<YYYYMMDD_HHMM>` object, update `key_judgments`,
   `indicators_to_watch`, `timeline`, `last_updated`, append `changelog`.
4. Add the matching block to **all four** of `report/brief/brief-en.html`,
   `report/brief/brief-cs.html`, `report/pdf/pdf-en.html`, `report/pdf/pdf-cs.html`
   (Czech mirrors are translations, same structure).
5. Unless `--no-render`: `just pdf`.

## Phase 6 — Check and report

```bash
just check
```
Fix anything it flags. Then print a compact summary for the user: section number, each
judgment's confidence (with arrows for moves), indicators closed/opened, red-team verdicts,
what was searched and not found. Do **not** commit — the user runs `/publish` for that.

## Hard rules

- Open sources only; a request to cross `references/ethics-scope.md` is declined once and
  not re-argued.
- No claim without outlet + date + grade. No confidence move without a traced primary.
- Never edit files under `data/`; never delete earlier sections — supersede.
- Keep English as the working language; Czech artifacts are translations of the English.
