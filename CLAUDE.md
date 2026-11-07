## Agent skills

### Issue tracker

GitHub Issues on this repo, through the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

The five triage roles and the label string each uses here. See `docs/agents/triage-labels.md`.

### Domain docs

Where the glossary and ADRs live, and how to use their vocabulary. See `docs/agents/domain.md`.

### Decisions and findings

Why the gates ratchet instead of paying upstream debt: `docs/adr/`. The fork's starting numbers (build cost, defects, debt) that #1–#3 are measured against: `docs/research/2026-11-02-fork-baseline.md`.

### Pull requests

Write every PR body with the `pr` skill: Summary, Evidence, Merge Danger. `.github/pull_request_template.md` holds the same headings.

**Asking the builder:** ask when uncertain about anything irreversible, outward-facing or large in scope, and proceed on reversible work with a stated default. Every question gives what is at stake in plain words, two or three options with only the pros and cons the builder would notice, and a recommendation with its reason (`standards` skill, *ask the builder*).
