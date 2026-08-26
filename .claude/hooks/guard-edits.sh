#!/usr/bin/env bash
# PreToolUse guard: raw pulls under data/ are append-only; generated PDFs are never hand-edited;
# no force-push or history rewrite; no reconnaissance tooling.
set -euo pipefail
IN=$(cat)
TOOL=$(printf '%s' "$IN" | jq -r '.tool_name // empty')
deny() { jq -n --arg r "$1" '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"deny",permissionDecisionReason:$r}}'; exit 0; }
case "$TOOL" in
  Edit|Write|MultiEdit)
    P=$(printf '%s' "$IN" | jq -r '.tool_input.file_path // empty')
    case "$P" in
      */data/*|data/*) deny "data/ holds raw timestamped pulls and is append-only via scripts; do not edit by hand." ;;
      *.pdf) deny "PDFs are rendered with 'just pdf'; edit report/pdf/*.html instead." ;;
    esac ;;
  Bash)
    C=$(printf '%s' "$IN" | jq -r '.tool_input.command // empty')
    printf '%s' "$C" | grep -Eq 'git push[^|;&]*(--force|-f\b|\+[a-zA-Z])' && deny "force-push is not allowed on this case repo."
    printf '%s' "$C" | grep -Eq 'git (rebase|reset --hard|filter-branch|commit --amend)' && deny "history rewriting is not allowed; make a new commit."
    printf '%s' "$C" | grep -Eq '\brm -rf? +(\./)?data\b' && deny "data/ is append-only."
    printf '%s' "$C" | grep -Eiq '\b(nmap|masscan|shodan|censys|sqlmap|nikto|dirb|gobuster|hydra)\b' && deny "Reconnaissance tooling is outside the open-source scope of this case (see .claude/skills/update-case/references/ethics-scope.md)." ;;
esac
exit 0
