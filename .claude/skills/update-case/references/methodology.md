# Analytic methodology

Standard open-source intelligence-assessment tradecraft, compressed to what an update
sweep actually needs. Apply every rule; when two conflict, the more conservative one wins.

## 1. Evidence vs. commentary

- **Evidence**: a primary source (official statement, court/registry record, dated archive
  snapshot, the outlet that *originated* a claim with a named/on-record basis).
- **Commentary**: analyst opinion, "experts say", op-eds, think-tank framing, anonymous
  "sources familiar with". Commentary may be *logged* (it shows what narratives are forming)
  but never moves a confidence level on its own. Convergence of five commentators is still
  commentary.
- **Unsourced**: a claim whose chain cannot be traced to a primary. Log as `unsourced`,
  keep it out of key judgments, never restate it as fact.

## 2. Source grading (Admiralty / NATO system, simplified)

Grade every new source `[reliability][credibility]`, e.g. `B2`.

| Reliability | Meaning |
|---|---|
| A | Completely reliable (official primary, established wire with on-record basis) |
| B | Usually reliable (major outlet, named reporter, history of accuracy on this beat) |
| C | Fairly reliable (regional/specialist outlet, mixed record) |
| D | Not usually reliable (anonymous channels, aggregators, partisan outlets) |
| E | Unreliable |
| F | Cannot be judged |

| Credibility | Meaning |
|---|---|
| 1 | Confirmed by other independent sources |
| 2 | Probably true (consistent, plausible, no independent confirmation) |
| 3 | Possibly true |
| 4 | Doubtful |
| 5 | Improbable |
| 6 | Cannot be judged |

Independence rule: two outlets paraphrasing the same wire story are **one** source.
Trace the chain (`who first said it → who repeated it`) before counting.

## 3. Confidence levels (ICD 203 style)

| Level | Use when |
|---|---|
| **High** | Multiple independent A/B sources, consistent, no credible contradiction, low deception risk |
| **Medium** | Plausible and sourced, but single-sourced, partially corroborated, or with an open contradiction |
| **Low** | Fragmentary, uncorroborated, or resting on C/D sources; plausible but readily overturned |

Rules:
- Every level carries a **one-line reason** ("High — Peskov denial repeated independently by TASS and WaPo").
- **Upgrade** only when a new *primary* source is traced; secondary-source chains must reach a
  primary first.
- **Downgrade** as soon as a credible contradiction appears; restore only after it is resolved.
  Record both directions in the judgment text ("dipped to Medium mid-investigation, restored").
- Estimative language: *almost certainly / very likely / likely / roughly even / unlikely /
  very unlikely / remote*. Do not mix probability words with confidence words in one sentence.

## 4. Analysis of Competing Hypotheses (Heuer, minimal form)

1. List hypotheses H1..Hn (exhaustive, mutually exclusive where possible).
2. List evidence items E1..Em, each with source grade.
3. Matrix: for each (E, H) mark `C` consistent / `I` inconsistent / `N` neutral.
4. Rank hypotheses by **fewest inconsistencies**, not most consistencies.
5. Note diagnosticity: evidence consistent with *all* hypotheses proves nothing.
6. Re-run when new evidence lands; a hypothesis is dropped only when its inconsistencies
   are primary-sourced.

## 5. Indicators

- Each indicator states what it would support if observed (`would support H3`).
- Status per sweep: `open` / `observed (source, date)` / `refuted (source, date)` / `stale`.
- A sweep that finds nothing produces a line "still open — searched X, Y, Z" — that is a finding.

## 6. Negative results

"Page archived 5x that day, digest unchanged" is evidence of no statement. Always log:
what was searched, where, when, and what was *not* found. Absence of evidence is weak but
non-zero evidence of absence when the search was targeted and the venue is where the
evidence would appear.

## 7. Writing rules

- Lead with the judgment, then the evidence, then the caveat.
- Dates in ISO (`2026-08-26`), times in UTC unless a local zone is stated.
- Name the outlet and, where possible, the reporter/official for every claim.
- Never delete prior findings; supersede them ("revised in §8.6").
- Changelog line per update: what changed, what did not, confidence moves.
