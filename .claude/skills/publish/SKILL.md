---
name: publish
description: Render PDFs, build the static site (index + briefs + PDFs + report), run checks, commit with a conventional message, push to origin, and confirm the GitHub Pages deployment. Use after /update-case, or for "publish", "push the report", "deploy pages".
argument-hint: "[--no-push] [-m \"<commit message>\"]"
allowed-tools: Bash, Read, Grep, Glob
---

# /publish — render, commit, push, deploy

1. `just pdf && just site && just check` — abort on any failure and show the output.
2. `git status --short` — refuse if files under `data/` were modified (raw pulls are
   append-only; new timestamped files are fine).
3. Stage everything except `scratch/` and `_site/`; commit as
   `docs(case): <section or summary>` (or `-m` text) with the co-author footer
   `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`. Never `--no-verify`, never amend.
4. Unless `--no-push`: `git push origin HEAD`, then
   `gh run watch --exit-status $(gh run list --workflow=pages.yml -L1 --json databaseId -q '.[0].databaseId')`
   and print the Pages URL from `gh api repos/{owner}/{repo}/pages -q .html_url`.
5. Report: commit hash, Pages URL, and the `just check` summary.
