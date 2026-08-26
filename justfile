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

check:         # sanity: json valid, pdf templates + briefs have same section count
    jq -e . data.json >/dev/null && echo "data.json ok"
    @for f in report/brief/brief-en.html report/brief/brief-cs.html report/pdf/pdf-en.html report/pdf/pdf-cs.html; do printf '%-32s %s h2\n' "$f" "$(grep -c '<h2' $f)"; done

open:          # open case folder in Finder
    open .
