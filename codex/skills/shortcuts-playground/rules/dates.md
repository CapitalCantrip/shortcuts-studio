# Rules: dates and times

Read when the shortcut formats, adjusts, compares or asks for a date. Format recipes (ISO 8601, UNIX time, RFC 2822, TR35 symbols): [DATE_TIME.md](../DATE_TIME.md).

## Format Date (`is.workflow.actions.format.date`)

- `WFDate` (not `WFInput`) holds the source date, as a `WFTextTokenString` placeholder wired to a Date output.
- Custom pattern: `WFDateFormatStyle = Custom` and the pattern itself in `WFDateFormat` (for example `yyyy-MM-dd`, `MMMM d, yyyy`, `yyyy-MM-dd'T'HH:mm:ssXXXXX`). This is ToolKit v78's shape, where `WFDateFormat` is the *Format String* field, and the shape of the golden samples. The runtime reads the pattern from `WFDateFormat`.
- Without `WFDateFormatStyle = Custom` the editor shows Short.
- API parameters take date-only patterns (`yyyy-MM-dd`); hard-coded `00:00:00` / `23:59:59` are out. A date-time pattern for a Start/End Date needs the user's request and a Comment containing `ALLOW_DATETIME_FORMAT`.
- Keep the raw Date in a variable for later math; format into strings last.
- Daily-forecast `Sunrise Time` / `Sunset Time` are lists: **Get Item from List** (First Item for sunrise, Last Item for sunset) before Format Date.

## Adjust Date (`is.workflow.actions.adjustdate`)

`WFDate` (optionally mirrored in `WFInput`) plus a non-empty `WFDuration`; add `WFAdjustOperation` for an explicit Add/Subtract. Offset-picker-only payloads import as `Add 0 seconds` on iOS.

## Get Time Between Dates (`is.workflow.actions.gettimebetweendates`)

`WFInput` plus exactly one non-empty operand (`WFTimeUntilFromDate` preferred for date-vs-date, or `WFDate`, or `WFTimeUntilCustomDate`), both as `WFTextTokenString` placeholders. To compare with now, add a **Date** action set to Current Date and reference it; no `CurrentDate` token directly in this action. Omit unused date keys; omit `WFTimeUntilUnit` only to use the default unit.

## Asking for dates

A date picker in **Ask for Input** defaults to **Date and Time** unless the user wants date only.

## Find Calendar Events

Date filters use date operators. "Next event after now": `Start Date is today` (`Operator 1002`, empty `Values`) plus `Start Date is after Current Date` (`Operator 2`, `Values.Date` = a `CurrentDate` token). `Operator 3` imports as a red invalid condition.
