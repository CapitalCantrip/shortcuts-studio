# Fork baseline, 2026-11-02

The numbers #1–#3 are measured against, taken from upstream 1.2.1 on the day of the fork.

## Build cost

Brief "Capture Card": Take Photo, Ask for Input, menu for a back photo, Resize Image 1600 px, Convert Image JPEG 0.7, dated filename, Save File, notification. 37 actions of 16 types.

| Run | Tokens | Tool calls | Time | Outcome |
|---|---|---|---|---|
| 1 | 140k | 13 | ~12 min | BLOCKED: the stop-and-ask rule fired for Take Photo and Resize Image, which have ToolKit keys but no documented schema |
| 2 | 188k | 8 | ~7 min | COMPLETE, signed |
| Total | ~330k | 21 | ~19 min | |

Where the cost came from:
- **The stop-and-ask rule** in `agents/shortcut-builder.md`: a whole extra run, with run 2 re-reading what run 1 had read.
- **Always-read instructions:** `SKILL.md` 45 KB, `BEST_PRACTICES.md` 48 KB (first in the reading order), the builder agent 16 KB.
- **Total Markdown** in the skill is about 670 KB; `APPINTENTS.md` alone is 168 KB, though it is read on demand.

## Defects found during the build

- **Contradictory date-format guidance.** `BEST_PRACTICES.md` says `WFDateFormat=Custom` plus `WFDateFormatString`. ToolKit v78 has no `WFDateFormatString`, and golden sample `2e0fb675e45948aaacee7e534f910492.xml` puts the pattern in `WFDateFormat` with `WFDateFormatStyle=Custom`. The build used the golden shape; it is not yet confirmed on a device.
- **Unfilled placeholder.** The builder's step-0 command contains an unfilled `${user_config.signing_mode}`, which Claude Code's safety check refuses as unparseable.
- **Validator false positive.** "MM" inside a quoted `yyyy-MM-dd` in a Comment was flagged as a unit conversion (millimetres).

## Technical debt (quality-gates v0.11.1)

| Measure | Value |
|---|---|
| Python | 13 files, about 24,000 lines |
| Functions over CC 8 | 77 unique of about 320 (139 counting the `codex/` copy) |
| By band | 9–15: 50 · 16–30: 22 · 31–60: 4 · over 60: 1 |
| Worst | `validate_shortcut.py:validate` CC 864; `lookup_action_grounding.py` `main` 54, `print_markdown_entry` 52, `entry_search_text` 39; `test_wiring_regressions.py:build_cases` 41 |
| Comment lines | 539 in 13 files |
| Duplication | `claude/` and `codex/` carry identical scripts; `test_shared_codex_and_claude_skill_files_do_not_drift` enforces it |
| Tests | 68 upstream, all passing in CI (macOS, 7 s) |
| Coverage | Not measured yet |

Policy for this debt: [ADR-001](../adr/ADR-001-gates-ratchet-upstream-debt.md).

## Apple platform drift

Upstream data stops at 2026-06-15 (OS 27 betas, ToolKit v78). Since then iOS/macOS 27.0 shipped, and iOS 27.2 shipped on 2026-10-26 with new triggers: phone open/close, Fitness workout start, and which app closed. No evidence yet of a change to the `.shortcut` format or signing; that comes from secondary sources only. Detail and sources are in #3.
