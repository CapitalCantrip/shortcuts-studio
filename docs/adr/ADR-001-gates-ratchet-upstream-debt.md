---
status: accepted
date: 2026-11-02
---

# ADR-001: Gates ratchet on new code; upstream debt is baselined

## Context

Shortcuts Studio forks `viticci/shortcuts-playground-plugin` 1.2.1 to cut the cost of building a shortcut (issues #1–#3). The upstream Python (about 24,000 lines) had no CI, no pre-commit hook, 77 unique functions over cyclomatic complexity 8, and 539 comment lines. Upstream updates should stay cheap to merge.

## Decision

Install quality-gates v0.11.1 and record today's debt as baselines (`cc-baseline.json`, `comment-debt.json`). The gates fail only on new or worse code. Upstream files are not refactored to pay debt down. CI runs the upstream suite plus the gate tests on macOS.

## Rejected

- **Full gates on everything.** It flags hundreds of problems on day one, and paying them down rewrites upstream files, so every upstream merge conflicts.
- **No gates, upstream tests only.** It leaves the new scripts from #2 and #3 unchecked, which is where new bugs will come from.

## Consequences

- `validate_shortcut.py:validate` (CC 864) stays as is. Changing a validation rule there is slow; splitting it is its own issue if #3 needs it.
- The CRAP gate waits for a coverage baseline. Record it from a CI run when #2 adds the first new scripts.
- `.gitignore` diverges from upstream on two lines (`.claude/`, `/docs/`).
