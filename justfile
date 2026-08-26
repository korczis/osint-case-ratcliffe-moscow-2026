# Case tooling — run `just` for the list.
default:
    @just --list

status:        # one-screen case status from data.json
    scripts/status.sh

gdelt *ARGS:   # GDELT DOC 2.0 sweep (query/window from case.yaml)
    scripts/gdelt-sweep.sh {{ARGS}}

wayback URL *ARGS:   # snapshots of one URL
    scripts/wayback-cdx.sh {{URL}} {{ARGS}}

watch *ARGS:   # snapshots of all case.yaml watch_urls
    scripts/wayback-watch.sh {{ARGS}}

section:       # scaffold next §8.N + changelog line in report.md
    scripts/new-section.sh

pdf:           # render report/pdf/*.html -> PDF
    scripts/render-pdf.sh

check:         # gate: json valid, EN/CS parity, forbidden terms, changelog/section parity
    scripts/check.sh

site:          # build _site/ (index + briefs + PDFs + report) for GitHub Pages
    scripts/build-site.sh

serve:         # preview _site/ locally
    python3 -m http.server -d _site 8080

open:          # open case folder in Finder
    open .
