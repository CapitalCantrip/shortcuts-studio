---
name: shortcuts-playground
description: Build, validate, sign, archive, and REMIX macOS/iOS Shortcuts by creating plist files. Use when asked to create, modify, or remix shortcuts; automate workflows; build .shortcut files; or generate Shortcuts plists. Covers WF actions, AppIntents, third-party actions, variable references, and control flow using bundled target-gated ToolKit snapshots.
effort: max
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Shortcuts Playground

A shortcut is an XML plist, validated, then signed into a `.shortcut` file the user opens in Shortcuts.app. The `shortcut-builder` agent makes one from a brief; the `shortcut-remixer` agent applies a diff to an existing unsigned XML. Both run **the pipeline** below; each agent file adds only its own steps.

On `PATH`: `resolve-output`, `resolve-icon`, `validate-shortcut`, `sign-shortcut`. A `PostToolUse` hook runs `validate-shortcut` on every `Write`/`Edit` of a Shortcuts plist and prints the errors.

## The pipeline

**Done** means a signed `.shortcut` exists with non-zero size and its path is reported. A clean draft without a signed file is a failed run.

1. **Settings.** Run `resolve-output` exactly as your agent file gives it. Use the printed absolute `OUTPUT_DIR` (the literal path) in every later path, and `SIGNING_MODE` when signing.
2. **Plan.** Write a short action list: what each action does and which output feeds which input. For each branch the brief touches, read its rule file (table below). Skim `golden-shortcuts/index.jsonl` and open only the XML whose tags match; golden XMLs show wiring, and may predate today's validator rules.
3. **Icon.** `resolve-icon --prompt "<verbatim user request>"`, adding `--icon`/`--color` when the user named them. Set `WFWorkflowIconGlyphNumber` to `icon.glyph_number` and `WFWorkflowIconStartColor` to `color.value`.
4. **UUIDs.** One call mints every UUID the plan needs: `for i in $(seq 1 <N>); do uuidgen | tr '[:lower:]' '[:upper:]'; done`. Every UUID in the plist comes from `uuidgen`; the validator rejects repeating-hex UUIDs such as `11111111-…`.
5. **Draft.** `Write` the smallest complete plist that does what was asked to `<OUTPUT_DIR>/drafts/<name>.xml`. Drafts stay XML; `sign-shortcut` does any binary conversion.
6. **Craig Loop.** Read every error the hook prints; fix them all with targeted `Edit`s on the named action indexes; let the hook re-validate. Each run follows a real change. Stop and report the remaining errors after 5 iterations, or when one error survives 2 consecutive fixes (the approach is wrong). A validator failure is waived only when a runtime-verified false positive is listed in [rules/known-gaps.md](rules/known-gaps.md).
7. **Sign** as soon as validation passes:
   ```bash
   sign-shortcut "<OUTPUT_DIR>/drafts/<name>.xml" --name "<name>" --output-dir "$OUTPUT_DIR" --mode "$SIGNING_MODE"
   ```
   Pass both flags: ordinary Bash calls may not inherit the plugin config. It archives the raw XML under `<OUTPUT_DIR>/<date>/` and prints JSON with both paths. Failures: [rules/signing.md](rules/signing.md).
8. **Verify** with `ls -la "<OUTPUT_DIR>/<name>.shortcut"`; on failure go back to step 7.

Polish comes after signing, only when asked, and any edit after validation means validating and signing again. The filename and `WFWorkflowName` are the display name: no `_signed` or `_final`.

## Rules by kind of shortcut

Read each file whose trigger matches the brief, before drafting.

| The shortcut… | Read |
|---|---|
| calls a web API, builds a request body, parses JSON | [rules/web-apis.md](rules/web-apis.md) |
| uses If, a menu, Choose from List, a Repeat, or Math | [rules/control-flow.md](rules/control-flow.md) |
| formats, adjusts, compares or asks for a date | [rules/dates.md](rules/dates.md) |
| transforms text, builds lists or dictionaries, sends a message or email | [rules/text-and-data.md](rules/text-and-data.md) |
| picks, renames, saves or shares files; photos, images, video, PDFs | [rules/files-and-media.md](rules/files-and-media.md) |
| uses Weather, Location, Health, Reminders, Notes, Music, URL schemes, Safari JavaScript, automation triggers | [rules/apple-apps.md](rules/apple-apps.md) |

Deeper reference, by need: [PLIST_FORMAT.md](PLIST_FORMAT.md), [VARIABLES.md](VARIABLES.md), [CONTROL_FLOW.md](CONTROL_FLOW.md), [FILTERS.md](FILTERS.md), [PARAMETER_TYPES.md](PARAMETER_TYPES.md), [EXAMPLES.md](EXAMPLES.md), [DATE_TIME.md](DATE_TIME.md), [HEALTHKIT.md](HEALTHKIT.md), [ICONS_AND_COLORS.md](ICONS_AND_COLORS.md), [URL_SCHEMES.md](URL_SCHEMES.md), [JAVASCRIPT_WEBPAGE.md](JAVASCRIPT_WEBPAGE.md), [AUTOMATION_TRIGGERS.md](AUTOMATION_TRIGGERS.md).

## Evidence for actions and parameters

Each new identifier comes from the packaged `data/toolkit-v*-tool-ids.json` snapshots, [ACTIONS.md](ACTIONS.md), [APPINTENTS.md](APPINTENTS.md) or [THIRD_PARTY_ACTIONS.md](THIRD_PARTY_ACTIONS.md). Common slips: Text is `gettext`, Translate is `text.translate`, Send Email is `sendemail`, scripts are `runapplescript` / `runshellscript` / `runsshscript` / `runjavascriptforautomation` / `runjavascriptonwebpage`, podcast details are `properties.podcast` / `properties.podcastshow`. Shortcut input is an `ExtensionInput` attachment, never an `is.workflow.actions.input` action. An identifier found in none of these sources is not used: offer the user the nearest documented action. A third-party action whose app you cannot confirm is installed: ask the user before drafting.

Main keys of common actions (more in [ACTIONS.md](ACTIONS.md) and the golden XMLs):

| Action | Identifier | Keys |
|---|---|---|
| Comment | `comment` | `WFCommentActionText` |
| Text | `gettext` | `WFTextActionText` |
| Number | `number` | `WFNumberActionNumber` |
| URL | `url` | `WFURLActionURL` |
| List, Dictionary | `list`, `dictionary` | `WFItems` |
| Ask for Input | `ask` | `WFAskActionPrompt`, `WFInputType` |
| Show Result | `showresult` | `Text` |
| Alert | `alert` | `WFAlertActionTitle`, `WFAlertActionMessage` |
| Notification | `notification` | `WFNotificationActionTitle`, `WFNotificationActionBody` |
| Set / Get Variable | `setvariable`, `getvariable` | `WFVariableName` + `WFInput`; `WFVariable` |
| Get Contents of URL | `downloadurl` | `WFURL`, `WFHTTPMethod` |
| Open URL | `openurl` | `WFInput` |
| Use Model | `askllm` | `WFLLMPrompt`, `WFLLMModel`, `WFGenerativeResultType` |

Identifiers here drop the `is.workflow.actions.` prefix.

For an action's parameters, use in order: the rule files and reference docs, a matching golden XML, then the grounding helper (it reads bundled JSON only):

```bash
python3 "$CLAUDE_PLUGIN_ROOT/skills/shortcuts-playground/scripts/lookup_action_grounding.py" --identifier "<identifier>" --target-macos 27 --json
```

Curated Shortpy grounding counts as schema evidence. When the helper returns only a `toolkit-parameter-summary`, build from those ToolKit parameter keys, and put every setting you could not verify (key, value chosen, what to look at in the editor) on the **on-device checklist** in your report. Prefer a documented first-party action when one does the same job.

**Targets.** Validation defaults to the host's macOS (`auto`) and the `macos` platform. Pass `--target-macos 27` only for shortcuts that need target-gated macOS v78 identifiers or OS 27-only parameters such as `WFAllowWebSearch` / `FollowUp` on Use Model, `interpretAsMarkdown`, `WFAvoidTolls`, and Safari Tab Group `contents`; on a 26 target, pick a supported fallback and note it in a Comment. `--target-platform ios` is for iPhone/iPad shortcuts. OS 27 targets also reject unknown top-level keys on first-party `com.apple.*` actions.

## Rules for every shortcut

**Root plist.** `WFWorkflowActions` (array), `WFWorkflowClientVersion` `2700.0.4`, `WFWorkflowHasOutputFallback` false, `WFWorkflowIcon` (glyph + color), `WFWorkflowImportQuestions` (empty array), `WFWorkflowInputContentItemClasses`, `WFWorkflowMinimumClientVersion` `900` (integer), `WFWorkflowMinimumClientVersionString` `"900"`, `WFWorkflowName`, `WFWorkflowOutputContentItemClasses`, `WFWorkflowTypes`. Input classes are non-empty only when the shortcut reads Shortcut Input. Full structure: [PLIST_FORMAT.md](PLIST_FORMAT.md).

**Actions and wiring.**
- Each action is a dict with `WFWorkflowActionIdentifier` and `WFWorkflowActionParameters`; any action whose output is used later carries a `UUID` (a missing one shows as "Unknown").
- An output is referenced as `{OutputName, OutputUUID, Type: ActionOutput}`; named variables as `{Type: Variable, VariableName}`.
- Text fields with variables are `WFTextTokenString`: `string` holds `￼` (U+FFFC) at each variable's position and `attachmentsByRange` maps `{position, length}` (for example `{0, 1}`) to it. Keys and placeholders match one-to-one and stay inside the string.
- Fields the user reads (Alert title/message, Notification title/body, Show Result `Text`, Text `WFTextActionText`) are `WFTextTokenString` even for a single variable. Pure data inputs (`WFInput` of Set Variable, Math, Count; `WFVariable`) may be `WFTextTokenAttachment`.
- Set every required input explicitly (`WFInput` and its per-action equivalents), wired to an output. Omit keys you have no value for; an empty placeholder imports as a broken field. A field the user must fill on device (an accessory, a contact) may stay empty with a Comment saying so.
- The `Type=Variable` wrapper around an ActionOutput belongs to If inputs only; other inputs reference the output directly.
- Set Variable always has a `WFInput`; a constant goes through a Text or Number action first.
- Every Text, Number, URL, Math, Count and Format Date output is used, or the action is removed.
- Insert variables straight into the consuming field; add Get Variable only when its output is used at once.
- Variable names have spaces (`PDF Pages`).

**Comments.**
- Action 0: a Comment saying what the shortcut does. Action 1: a Comment with exactly this text, `{User Prompt}` being the user's words verbatim except where [rules/known-gaps.md](rules/known-gaps.md) says otherwise:
  ```
  Shortcuts generated by Shortcuts Playground. May contain mistakes. Always check the shortcut's actions first.

  This shortcut was created via the following user prompt:

  > {User Prompt}
  ```
- Before every If, Repeat and menu start, a Comment with a short bulleted wiring list (`-` or `•`), such as `- Date uses the answer from Ask for Input`.
- At least 3 Comments for 8+ actions, 4 for 16+, 5 for 24+; past ~20 actions, section headers like `--- FETCH TASKS ---`.
- Comment text is plain Shortcuts wording (action names, `Input`, `Repeat Item`): no UUIDs, no `WF*` keys.

**Scope.** Build everything the user asked for; when it looks too large, propose a reduced version and wait. Prefer modern first-party actions that work on iOS and macOS. Add services, import questions or dependencies only on request.

**Escape hatches.** A Comment containing `ALLOW_VCARD`, `ALLOW_TOKEN_FILE`, `ALLOW_MANUAL_UNIT_CONVERSION` or `ALLOW_DATETIME_FORMAT` lifts that check, used only when the user asked for the behaviour.

## Where you look

Your sources are the plugin directory (`$CLAUDE_PLUGIN_ROOT`) and the one draft or source XML you are working on. Schema questions are answered from those sources and the on-device checklist. Off limits, for searching and reading: `~/Library` (including `Shortcuts.sqlite` and ToolKit databases), iCloud and cloud-storage folders, `/Applications`, `/System`, `~/.claude`, the rest of `~/Documents`, other files in the output directory, and signed `.shortcut` files (AEA1-encrypted). No Python that imports `sqlite3` or `objc`. Write only inside `OUTPUT_DIR`; the plugin's own files and the user's repos stay untouched.

## Report

1. Signed `.shortcut` path and archive XML path.
2. One sentence on what it does.
3. Caveats: API keys, permissions, prerequisites.
4. The **on-device checklist**: each setting to confirm in the Shortcuts editor, or "none".
