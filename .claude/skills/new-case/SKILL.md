---
name: new-case
description: Bootstrap a fresh OSINT assessment case in this repository layout (case.yaml, report.md skeleton with key judgments/ACH/timeline/entities/indicators/evidence/caveats/changelog, data.json skeleton, brief and PDF templates) from a one-line subject. Use for "new case", "start a case about …".
argument-hint: "<case-id> \"<title>\" [--query=\"<gdelt query>\"] [--start=YYYYMMDD] [--langs=en,cs]"
allowed-tools: Bash, Read, Edit, Write, Grep, Glob, WebSearch, WebFetch
---

# /new-case — scaffold a case

Creates a sibling case directory `../<case-id>/` (or the current directory if it is empty
apart from `.claude/`) with the same layout as this repository, so every case gets the same
tooling and the same `/update-case` cycle.

1. Copy `justfile`, `scripts/`, `.claude/`, `.gitignore`, `.github/` verbatim.
2. Write `case.yaml` from the arguments (`id`, `title`, `type: osint-intelligence-assessment`,
   `status: in-progress`, `created: <today>`, `classification: open-source-only`, `languages`,
   `gdelt_query`, `window.start/end`, empty `watch_urls`, `forbidden_terms: []`).
3. Write `report.md` with the canonical headings (`# Intelligence Assessment: <title>`,
   metadata block, `## 1. Summary`, `## 2. Key Judgments`, `## 3. Alternative Hypotheses (ACH)`,
   `## 4. Timeline`, `## 5. Entities`, `## 6. Indicators to Watch`, `## 7. Sourcing`,
   `## 8. Evidence sections` (empty, `just section` will add `8.1`), `## 9. Caveats`,
   `## 10. Tooling note`, `## 11. Changelog`) and one changelog line "case created".
4. Write `data.json` with keys `report_id, title, created, last_updated, status,
   classification, entities{persons[],organizations[]}, timeline[], key_judgments[],
   alternative_hypotheses[], indicators_to_watch[], sources[], changelog[]`.
5. Copy `report/brief/brief-en.html` and `report/pdf/pdf-en.html` as **structure-only**
   templates: keep `<head>`/CSS, replace every section body with a placeholder, keep one
   example of each component (kj-item, pill, timeline row, entity group). Do the same for
   the Czech pair if `cs` is in `--langs`.
6. Run an initial collection: 5–8 WebSearches on the subject, one `just gdelt`, and write
   `## 1`–`## 6` as a first cut with graded sources (see
   `../update-case/references/methodology.md`). Then `just check`.
7. Print the tree and the next step (`/update-case`).
