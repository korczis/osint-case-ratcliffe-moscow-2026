#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../report/pdf"
weasyprint pdf-en.html report-en.pdf
weasyprint pdf-cs.html report-cs.pdf
ls -la report-en.pdf report-cs.pdf
