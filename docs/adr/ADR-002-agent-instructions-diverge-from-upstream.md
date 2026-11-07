---
status: accepted
date: 2026-11-03
---

# ADR-002: The Claude plugin's agent instructions diverge from upstream

## Context

ADR-001 keeps upstream merges cheap by leaving upstream files alone. Issue #1 found that the always-read instructions (builder agent, `SKILL.md`, `BEST_PRACTICES.md`, remixer agent; 109 KB for a build) cost most of a build's tokens and caused a stop-and-ask on a schema gap. Fixing that means rewriting them.

## Decision

Rewrite the Claude plugin's instruction files and treat them as ours from now on:

- `claude/agents/*.md`, `claude/commands/*.md`, `claude/skills/shortcuts-playground/SKILL.md`, `BEST_PRACTICES.md` and the new `rules/*.md`.
- Upstream instruction changes are ported by hand into the matching rule file, not merged.
- Scripts, the validator, data, golden examples and the reference docs (`ACTIONS.md`, `DATE_TIME.md` …) stay upstream-shaped, so ADR-001 still holds for them. Single-line fact fixes in reference docs (the Format Date shape) are allowed.
- The settings call with its `${user_config.*}` placeholders stays in each agent file, where upstream had it and where substitution is known to work; whether skills get the same substitution is unverified.

## Rejected

- **Leave the instructions as upstream wrote them.** The token cost and the stop-and-ask stay.
- **Rewrite the Codex plugin too.** Out of scope for #1; tracked in #6. The drift test makes `codex/.../rules/` a byte copy, unused by Codex until then.

## Consequences

- An upstream release that edits `SKILL.md` or `BEST_PRACTICES.md` conflicts. Resolve by taking ours and moving any new rule into its rule file, listed in the rule ledger (`docs/research/2026-11-03-instruction-rule-ledger.md`).
- Codex and Claude instruction text now differ beyond the drift test's exemptions.
