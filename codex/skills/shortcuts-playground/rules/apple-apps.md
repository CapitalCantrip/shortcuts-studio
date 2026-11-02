# Rules: Apple apps and system features

Read when the shortcut uses Weather, Location, Health, Reminders, Notes, Music, Shortcuts URL schemes, Safari JavaScript or automation triggers.

## Weather and Location

- **Get Detail of Weather Conditions** (`is.workflow.actions.properties.weather.conditions`): `WFInput` is the direct ActionOutput of **Get Current Weather** (`weather.currentconditions`) or **Get Weather Forecast** (`weather.forecast`), not a named variable; `WFContentItemPropertyName` is one of `Date`, `Location`, `Temperature`, `Low`, `High`, `Feels Like`, `Condition`, `Visibility`, `Dewpoint`, `Humidity`, `Pressure`, `Precipitation Amount`, `Precipitation Chance`, `Wind Speed`, `Wind Direction`, `UV Index`, `Sunrise Time`, `Sunset Time`, `Air Quality Index`, `Air Quality Category`, `Air Pollutants`, `Name` (never the placeholder `Detail`).
- Daily `Sunrise Time` / `Sunset Time` are lists; see [dates.md](dates.md).
- `WFLocation`, `WFWeatherCustomLocation` and `WFWeatherLocation` are `WFTextTokenAttachment`s referencing a Get Current Location / Location output (directly or via a variable sourced from one), never empty. `is.workflow.actions.location` always carries a non-empty `WFLocation`.

## Health (iOS/iPadOS only)

Use [HEALTHKIT.md](../HEALTHKIT.md) and `data/healthkit-ios26.2-reference.json` for every Health action. The traps:
- Find Health Samples: the sample kind is a non-removable `Type` row in `WFContentItemFilter` (`Values.Enumeration`, `WFStringSubstitutableState`, picker label such as `Steps`); `WFHealthQuantityType` is obsolete.
- Picker labels: `Sleep`, `Exercise Minutes`, `Active Calories`.
- Sleep `Duration` through Math is seconds: ÷ 3600 for hours. Walking + Running Distance is summed as-is.
- Log Health Sample: `WFQuantitySampleType` + `WFQuantitySampleQuantity` (`WFQuantityFieldValue`).
- Validate Health-writing shortcuts by import/export; run them only when the user asks.

## Reminders

Edit an existing reminder with `is.workflow.actions.setters.reminders`, one action per property (`Mode = Set`, `WFContentItemPropertyName`, matching `WFReminderContentItem<Property>` key), chained through each setter's `Edited Reminder` output. `UpdateReminderAppIntent` is not used. `List` takes a plain string. Date filters in `filter.reminders`: `1002` (is today) with empty `Values`; `1003` (is between) with `Values.Date` + `Values.AnotherDate`. Full schema: [PARAMETER_TYPES.md](../PARAMETER_TYPES.md#reminders--filter--setter-schemas-definitive).

## Notes

- Create-note actions set both a title and a content parameter.
- Markdown on older targets: `com.apple.Notes.CreateNoteFromMarkdownLinkAction` with `markdownContents` (camelCase; `markdown` makes an empty note). On OS 27+, `com.apple.mobilenotes.SharingExtension` has `interpretAsMarkdown`.
- Notes unavailable on the target: Share or Save File, with a Comment explaining the fallback.
- **Find Notes**: `WFContentItemFilter` is `WFContentPredicateTableTemplate` with non-empty templates; Name filters use `Values.String` (`WFTextTokenString`), Folder filters `Values.Enumeration` with `WFLinkDynamicOptionSubstitutableState` around a `WFTextTokenAttachment`.
- **Store Content** (`is.workflow.actions.setstoredcontent`): `WFInput` is a `WFTextTokenString` with one placeholder at `{0, 1}`.

## Music

Search and play with `is.workflow.actions.filter.music` + `is.workflow.actions.playmusic` rather than `PlayMusicTopHitAction`.

## Shortcuts URL schemes

Only the Apple-documented routes in [URL_SCHEMES.md](../URL_SCHEMES.md): `shortcuts://`, `create-shortcut`, `open-shortcut`, `run-shortcut`, `gallery`, `gallery/search`, `x-callback-url/run-shortcut`. URL-encode every query value and callback.

## Run JavaScript on Webpage

Safari share-sheet shortcuts only: `ActionExtension`, input scoped to `WFSafariWebPageContentItem`, call `completion(...)`, return JSON-compatible values, no `alert`/`prompt`/`confirm` or long timers. The user's Allow Running Scripts setting is outside the plist. Details: [JAVASCRIPT_WEBPAGE.md](../JAVASCRIPT_WEBPAGE.md).

## Automation triggers

Portable automation headers come from exported samples: top-level `WFWorkflowTriggers` array, fresh `WFTriggerUUID`s, `--target-macos 27`. Shapes in `data/macos27-workflow-trigger-samples.json` and [AUTOMATION_TRIGGERS.md](../AUTOMATION_TRIGGERS.md); ToolKit trigger metadata alone is not enough to author one, and live Shortcuts database rows are never written.
