# Instruction rule ledger, 2026-11-03

Where each rule in the four always-read files (plugin 1.2.1) went in the rewrite for #1. Paths are relative to `claude/skills/shortcuts-playground/` unless they start with `claude/`. "SKILL" means the new `SKILL.md`; `rules/x` means `rules/x.md`.

## Sizes

| File | Before (bytes) | After (bytes) | Always read? |
|---|---|---|---|
| `claude/agents/shortcut-builder.md` | 15,998 | 1,547 | yes, for builds |
| `SKILL.md` | 44,830 | 11,992 | yes, preloaded by both agents |
| `BEST_PRACTICES.md` | 48,205 | ~1,000 (index) | was first in the reading order; now nothing requires it |
| `claude/agents/shortcut-remixer.md` | 20,281 | 4,375 | yes, for remixes |
| **Always read for a build** | **109,033** | **13,539** | |

The rules moved behind pointers total about 22.7 KB across `rules/`; a build reads only the files whose branch it touches. The Capture Card brief touches three branches (control-flow, files-and-media, dates): 13,539 + 9,204 = 22,743 bytes read in all. A brief touching all six authoring branches would read about 34 KB.

## Old `shortcut-builder.md`

| Rule | Now |
|---|---|
| Role; decline non-shortcut requests | builder intro |
| Read SKILL.md first | no-op: the skill is preloaded through `skills:` |
| BEST_PRACTICES is the policy authority | removed: each rule has one home, so there is nothing to arbitrate |
| Identifiers only from snapshots or the three reference docs | SKILL *Evidence* |
| Always set icon keys via resolve-icon | SKILL pipeline step 3 |
| Craig Loop, 5 iterations, stop on a repeated error | SKILL pipeline step 6 |
| Archive + sign with `sign-shortcut` | SKILL pipeline step 7 |
| Filename = display name, no `_signed`/`_final` | SKILL pipeline, closing paragraph |
| Pipeline beats polish; build budget discipline (4 bullets) | SKILL pipeline: *Done* line and closing paragraph |
| Step 0 output-settings script | `claude/bin/resolve-output`, called from builder step 1 (change 5) |
| Step 1 research external APIs | builder step 2; `rules/web-apis` *Research* |
| Step 2 reading list, grounding helper | SKILL branch table and *Evidence* |
| Step 3 golden index | SKILL pipeline step 2 |
| Step 4 plan the action list | SKILL pipeline step 2 |
| Step 5 icon | SKILL pipeline step 3 |
| Step 6 uuidgen, no repeating-hex UUIDs | SKILL pipeline step 4 |
| Step 7 write draft with disclaimer Comment | SKILL pipeline step 5; *Comments* |
| Step 8 Craig Loop with targeted edits | SKILL pipeline step 6 |
| Step 9 sign with `--output-dir`/`--mode` | SKILL pipeline step 7 |
| Step 10 verify with `ls`, report | SKILL pipeline step 8; *Report* |
| Gate: 5 iterations | SKILL pipeline step 6 |
| Gate: false positive without an escape hatch | SKILL pipeline step 6 → `rules/known-gaps` |
| Gate: identifier in no snapshot or doc | SKILL *Evidence* (offer the nearest documented action) |
| Gate: third-party app not verifiable | SKILL *Evidence* (ask before drafting) |
| Gate: allowlisted action without a documented schema → stop and ask | **changed (change 3):** SKILL *Evidence* — build from ToolKit parameter keys and list each unverified setting on the on-device checklist |
| Keep drafts XML; no manual pre-conversion | SKILL pipeline step 5 |
| Never skip resolve-icon / the second Comment | SKILL pipeline step 3; *Comments* |
| Never invent identifiers | SKILL *Evidence* |
| Never commit, push or touch plugin files | SKILL *Where you look* |
| Never inspect Shortcuts.sqlite, ToolKit DBs, cloud or system folders; never search outside the plugin and the draft; no `sqlite3`/`objc` | SKILL *Where you look*, stated once for both agents |
| 8-call research budget | builder step 2; remixer step 5. Changed: running out means drafting with gaps on the checklist, not stopping |
| When you return control | SKILL *Report* (adds the on-device checklist) |

## Old `SKILL.md`

| Rule | Now |
|---|---|
| Command/agent table, wrapper table | SKILL intro (one line); `README.md` keeps the tables |
| Auto-validation hook | SKILL intro |
| "Follow BEST_PRACTICES; it wins conflicts" | removed, as above |
| Definition of done; pipeline-first rule | SKILL pipeline |
| Recommended reading order | SKILL branch table; BEST_PRACTICES no longer mandatory |
| Quick Start XML, Hello World | SKILL *Root plist* summary; full shapes stay in `PLIST_FORMAT.md` and `EXAMPLES.md` |
| Core concepts (actions, variable references, control flow) | SKILL *Actions and wiring*; `rules/control-flow` |
| Common actions table | SKILL *Evidence* key table (identifier + main keys); Use Model's OS 27 keys → SKILL *Targets*; Repeat/If/Menu keys → `rules/control-flow` and `CONTROL_FLOW.md` (linked from it); Translate keys → `rules/text-and-data`; Delete Photos `photos` key → `rules/files-and-media` |
| Detailed reference file list | SKILL *Deeper reference* line. `TOOLKIT_SNAPSHOT.md` and `CHANGELOG.md` dropped from it: background for maintainers, not authoring |
| Golden library (index first, no bulk load, may predate rules) | SKILL pipeline step 2 |
| Icon resolver | SKILL pipeline step 3 |
| Craig Loop protocol and anti-patterns | SKILL pipeline step 6 ("each run follows a real change", targeted edits) |
| Data sources / target gating | SKILL *Targets*. The per-catalog notes (enum cases, trigger keys, trigger samples) are reached through the grounding helper and `rules/apple-apps` *Automation triggers* |
| Escape-hatch comments | SKILL *Escape hatches* |
| Wiring regression and random stress suites | skill `README.md` *Regression suites*: maintainer tooling, not authoring |
| Signing commands and gotchas | SKILL pipeline step 7; `rules/signing` |
| Archive raw XML layout | `rules/signing` *What sign-shortcut does* (the wrapper does it) |
| Workflow 0–10 | SKILL pipeline |
| Comment blocks | SKILL *Comments* |
| Key rule 1 UUIDs | SKILL pipeline step 4 |
| 2 integer `WFControlFlowMode`; 5 matching ends | `rules/control-flow` *Every control-flow block* |
| 3, 4, 6, 7, 15, 20 placeholders and ranges | SKILL *Actions and wiring*; recount after edits in `rules/text-and-data` |
| 8 no empty placeholders | SKILL *Actions and wiring* |
| 9 `WFURL` token string | `rules/web-apis` |
| 10, 11, 26, 28 form/array/JSON bodies | `rules/web-apis` |
| 12, 27 Format Date | `rules/dates` (**changed, change 4**) |
| 13 Repeat Item in loops | `rules/control-flow` *Repeats* |
| 14 reuse extractions | `rules/web-apis`; SKILL unused outputs |
| 16, 41 dot notation, error guard | `rules/web-apis` *Reading the response* |
| 17 conditional inputs and codes | `rules/control-flow` *If* |
| 18 icon keys | SKILL pipeline step 3 |
| 19 Select File | `rules/files-and-media` |
| 21 no unrequested services | SKILL *Scope*; `rules/web-apis` |
| 22, 23 Notion | `rules/web-apis` *Research* |
| 24, 25 API research and string checks | `rules/web-apis` |
| 29, 31 Get Name extension / web title | `rules/web-apis` |
| 30 Count `WFInput` + `Input` | `rules/control-flow` *Repeats* |
| 32 Match Text + Count workaround | `rules/control-flow` *If* |
| 33, 35, 47(b) Replace Text, input keys | `rules/text-and-data` table |
| 34 Base64 | `rules/text-and-data` table |
| 36 Adjust Date; 39 Time Between Dates | `rules/dates` |
| 37 Convert Image; 40 Extract Text | `rules/files-and-media` |
| 38 Weather detail | `rules/apple-apps` |
| 42–45 JSON continuation and sanitizing | `rules/web-apis` *JSON text templates* |
| 46(a) URL schemes; 47(a) JavaScript on webpage | `rules/apple-apps` |
| 46(b) ShowHeaders + Detect Dictionary | `rules/web-apis` |
| 48 Split Text separator | `rules/text-and-data` table |
| 49 Find Notes filter | `rules/apple-apps` *Notes* |
| 50 direct variable wiring | SKILL *Actions and wiring* |
| 51 Location | `rules/apple-apps` |
| 52 Set Name vs Rename File | `rules/files-and-media` |
| 53 Math operators | `rules/control-flow` *Math* |
| 54 local-system inspection; schema gap → stop | SKILL *Where you look*; gap handling **changed (change 3)** |
| 55 automation triggers | `rules/apple-apps` |
| 56 Combine Images flip trick | `rules/files-and-media` |
| 57 Reminders setters | `rules/apple-apps` |
| 58 HealthKit | `rules/apple-apps` *Health* → `HEALTHKIT.md` (unit-only additional quantity and category enumeration live there) |

## Old `BEST_PRACTICES.md`

| Section / rule | Now |
|---|---|
| "Source of truth over other docs" | removed, as above |
| APIs: "use SerpAPI + Firecrawl when available" | no-op: the agent already uses the search tools it has |
| APIs: everything else | `rules/web-apis` |
| Actions: first-party, modern, cross-platform | SKILL *Scope* |
| Actions: icon from the resolver, honour explicit icon/color | SKILL pipeline step 3 |
| Actions: Comments (all bullets, good/bad examples) | SKILL *Comments* (examples cut to one) |
| Actions: vCard | `rules/text-and-data`; SKILL *Escape hatches* |
| Actions: unfillable parameter → empty with Comment | SKILL *Actions and wiring* (fields the user fills on device) and the on-device checklist |
| Actions: token validation, offsets | SKILL *Actions and wiring*; `rules/text-and-data` |
| Actions: required-input offender list | SKILL "set every required input"; each offender's own rule is in its branch file |
| Actions: detect.link, Store Content | `rules/text-and-data`; `rules/apple-apps` *Notes* |
| Actions: Convert Image, Base64, Weather, Health, Location, Calendar, Time Between, Extract Text | branch files as listed for SKILL rules |
| Actions: empty placeholder actions, `WFAskActionDefaultAnswer` | SKILL "omit keys you have no value for" |
| Actions: conditional bullets, If wrapper, list `contains`, integer codes, clipboard | `rules/control-flow` *If* |
| Actions: `is.workflow.actions.input`, identifier gotchas, Unknown Action | SKILL *Evidence* |
| Actions: AppIntent keys must be verified | **changed (change 3):** SKILL *Evidence* |
| Actions: Music | `rules/apple-apps` |
| Actions: unit conversion, Measurement | `rules/control-flow` *Math* |
| Actions: don't simplify requirements | SKILL *Scope* |
| Actions: Set Dictionary Value, dictionary wrappers | `rules/text-and-data` |
| Actions: unused outputs | SKILL *Actions and wiring* |
| Actions: Adjust Date, Format Date | `rules/dates` |
| Actions: URL schemes, JavaScript | `rules/apple-apps` |
| Actions: Send Email, Translate | `rules/text-and-data` |
| Actions: Repeat Results, Repeat Index | `rules/control-flow` *Repeats* |
| Actions: Shortcut Input classes | SKILL *Root plist* |
| Actions: Notes create, `markdownContents` | `rules/apple-apps` *Notes* |
| Critical wiring: Repeat Index as Variable | `rules/control-flow` *Repeats* |
| Critical wiring: display vs data serialization | SKILL *Actions and wiring*. The "46 Alerts / 41 Notifications in 127 shortcuts" evidence line dropped: background, not an instruction |
| Critical wiring: text in If branches consumed | `rules/control-flow` *If* |
| Critical wiring: UUID for referenced actions | SKILL *Actions and wiring* |
| Critical wiring: Comment before control flow | SKILL *Comments* |
| Preflight checklist | each item is a rule above, mostly enforced by the validator. "Type=Variable wrapper only for If" and "Set Variable from a constant via Text/Number" → SKILL *Actions and wiring*. Date-only API formats and `ALLOW_DATETIME_FORMAT` → `rules/dates`. Todoist → `rules/web-apis` |
| Preflight: condition code table | `rules/control-flow` *If*. The "Any-of-two ≥ N and ≤ N" equality tip was wrong (Any is OR); it now says All |
| Preflight: run `python3 scripts/validate_shortcut.py` | no-op: the hook runs the `validate-shortcut` wrapper |
| Preflight: validator is mandatory | SKILL intro (the hook) and pipeline step 6 |
| Comment guidance | SKILL *Comments* |
| Control flow & menus | `rules/control-flow` (Otherwise/Nothing, menus, confirmations, Count guard, nested repeats); Ask for Input date picker → `rules/dates` |
| Lists & dictionaries | `rules/control-flow` *Repeats*; `rules/text-and-data` |
| Messages & Send Message | `rules/text-and-data` |
| Text & parsing | `rules/text-and-data`; Find Notes → `rules/apple-apps` |
| Files & output | `rules/files-and-media`; Notes fallback → `rules/apple-apps` |
| Signing & install naming | `rules/signing` |
| Numbers & accumulators | `rules/control-flow` *Repeats* and *Math*; Notes markdown → `rules/apple-apps` |
| Shortcut building techniques | SKILL *Comments* and *Scope*; PDFs and videos → `rules/files-and-media` |
| Known validator gaps | `rules/known-gaps` (now lists the `MM` false positive from change 6) |
| Positive-only phrasing | "Equals 1" for JSON booleans was not a real condition code; `rules/web-apis` now says `is greater than 0` or a text compare |

## Old `shortcut-remixer.md`

| Rule | Now |
|---|---|
| Diff, not rewrite; preserve UUIDs, icon, metadata, comments, formatting | remixer intro |
| No source path → reply and stop | remixer step 2 |
| Read SKILL first, then only needed references; grounding helper; 8-call budget | preloaded skill; remixer step 5; SKILL *Evidence* |
| Source is ground truth; preserve unknown patterns | remixer intro |
| New identifiers from the allowlist; existing ones kept | SKILL *Evidence* ("each new identifier"); remixer intro |
| Never regenerate UUIDs for untouched actions | remixer intro and step 7 |
| Never change workflow metadata or rename unless asked | remixer intro; step 8 (the old file both forbade renaming and required `WFWorkflowName` = new name; step 8 keeps the latter, which is what the old workflow did) |
| Output name `<stem> Remix` | remixer step 8 |
| Hook errors: fix yours, leave the source's | remixer steps 4 and 10 |
| Path parsing rules and the escalation message | remixer step 2. Option 3 ("name the shortcut and I'll ask you to export it") dropped: it was option 2 restated |
| Source checks (exists, not AEA1, has `WFWorkflowActions`) | remixer step 3 |
| Step 0 output settings | `resolve-output`, remixer step 1 |
| Read in chunks above 2,000 lines | remixer step 4; step 9 copies the source with one Python call so a long source is never truncated |
| Baseline validation | remixer step 4 |
| Examples of which reference file to load | replaced by the SKILL branch table |
| Plan the diff | remixer step 6 |
| Placeholder-UUID audit (grep, then Python fallback) | remixer step 7 keeps the Python form only: the grep form does not work on macOS, as the old note said |
| Mint UUIDs in one batch | remixer step 7 → SKILL pipeline step 4 |
| Write draft, Case A / Case B with the remap | remixer step 9 (one `Write` with the map applied; covers both cases) |
| One Edit per logical change; Comments at index 0 and 1 | remixer step 10 |
| Sign; verify with `ls` | SKILL pipeline steps 7–8 |
| Report | SKILL *Report* + source path and diff summary |
| Gates (no path, bad source, 5 iterations, unknown identifier, missing schema, un-rewirable delete) | remixer steps 2–3 and 6; SKILL pipeline step 6 and *Evidence* (schema gap **changed, change 3**) |
| Never read signed files, mine archives, search outside, inspect DBs, `sqlite3`/`objc`, overwrite the source, reformat, clean up, hand off signing, commit/push | remixer steps 3, 4 and 9; SKILL *Where you look* |
