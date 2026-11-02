# Rules: If, menus, loops and numbers

Read when the shortcut uses If, Choose from Menu, Choose from List, a Repeat, or Math. Full templates: [CONTROL_FLOW.md](../CONTROL_FLOW.md).

## Every control-flow block

- Start, middle and end actions share one `GroupingIdentifier`; `WFControlFlowMode` is an integer: `0` start, `1` middle (Otherwise, menu case), `2` end. Every block is closed.
- The action right before each start is a Comment with a bulleted wiring list (SKILL.md, Comment rules).

## If

- `WFInput` is always set, as `{ Type: "Variable", Variable: { Value: <ActionOutput or Variable>, WFSerializationType: "WFTextTokenAttachment" } }`. Wrapping an ActionOutput this way is Apple's own shape; a Set Variable hop is not needed. A bare `WFTextTokenAttachment` imports as a blank chip on iOS.
- `WFCondition` is an integer code. Literal field per code, beside `WFInput`:

  | Code | UI label | Extra field |
  |------|----------|-------------|
  | `0` | is less than | `WFNumberValue` |
  | `1` | is less than or equal to | `WFNumberValue` |
  | `2` | is greater than | `WFNumberValue` |
  | `3` | is greater than or equal to | `WFNumberValue` |
  | `4` | is (text) | `WFConditionalActionString` |
  | `5` | is not (text) | `WFConditionalActionString` |
  | `8` | begins with | `WFConditionalActionString` |
  | `9` | ends with | `WFConditionalActionString` |
  | `99` | contains | `WFConditionalActionString` |
  | `999` | does not contain | `WFConditionalActionString` |
  | `100` | has any value | none |
  | `101` | does not have any value | none |
  | `1003` | is between | `WFNumberValue` (lower) + `WFAnotherNumber` (upper, attachment) |

  There is no numeric equals: use `4` on text, or an All-of-two If with `3` (≥ N) and `1` (≤ N). `4` and `99` are not interchangeable.
- Multi-condition If (Any/All) uses `WFConditions` with `WFContentPredicateTableTemplate`; `WFActionParameterFilterPrefix` `0` = Any, `1` = All; each row carries its own `WFCondition`, `WFInput` and literal field. One If uses either `WFConditions` or top-level `WFCondition`, never both.
- macOS 27 Otherwise If: mode `1` with condition fields. Plain Otherwise: mode `1`, no condition fields. End If: mode `2`.
- Text from **Get Dictionary Value** goes through a Text action (and, for string compares, a Set Variable) before the If compares it; direct compares often show blank.
- List `contains` on macOS 27: compare against the final **List** / **Add to List** output, or set the finished list once into a fresh variable name. A variable reassigned several times imports with a blank comparison value.
- If string conditionals still fight the validator, use **Match Text** → **Count** → numeric If (`Count > 0`).
- Clipboard-or-ask: one If with code `100` on the Clipboard, not Count → If.
- A Text action inside a branch is consumed by the next action (Set Variable, Show Result, Alert…).
- Add an Otherwise when the false case needs handling; a **Nothing** action marks a branch that intentionally returns no result.

## Menus and choices

- Choose from Menu: one case per entry in `WFMenuItems`, titles identical in both places.
- Yes/No confirmations use Choose from Menu or Choose from List. Show Alert returns no choice.
- Choose from List: multi-select toggles are booleans; **Select All Initially** only with **Select Multiple**. On OS 26.4+ it takes dictionaries and named text directly.
- Guard empty lists with Count → If before Choose from List or Repeat with Each.

## Repeats

- Repeat Item, Repeat Index (and `Repeat Item 2`… in nested loops) are `Type=Variable` with `VariableName`; an ActionOutput pointing at the repeat's end shows as Repeat Results.
- Repeat Results is read only after the loop ends.
- Running totals: put the current value in a temp variable, **Math** it into the master total, then Set Variable the master total.
- Build lists by initializing the list, then **Add to Variable** inside the loop (Send Message content is the exception, see [text-and-data.md](text-and-data.md)); for **Add Item to List** use `WFInsertPosition` `Beginning`, `End` or `Index`, with a 1-based `WFItemIndex` only for `Index`.
- **Count** sets `WFInput` and `Input` to the same variable so the editor shows it.

## Math

`is.workflow.actions.math`:
- Addition: omit `WFMathOperation`.
- Subtraction `-`, multiplication `×` (U+00D7), division `÷` (U+00F7). ASCII `*` and `/` render as `+` in the editor with no error.
- Scientific ops (modulus, power…): `WFMathOperation` = `…` (U+2026), real op in `WFScientificMathOperation`, operand in `WFScientificMathOperand`.
- Literal `WFMathOperand` is a plain string such as `"10"`.
- Cents to dollars: divide by 100 (`÷`), then round.
- Unit conversions use **Create Measurement** + **Convert Measurement** (`WFInput` = the Measurement). Manual math only for unsupported units, with a Comment containing `ALLOW_MANUAL_UNIT_CONVERSION` saying why.
