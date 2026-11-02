# Known validator gaps

Runtime-verified false positives the Craig Loop may work around. Anything not listed here is fixed in the shortcut, or reported.

## Date patterns in Comment text read as units

A Comment containing `MM` (as in a quoted `yyyy-MM-dd`) fails with "Unit conversion detected but no measurement.convert action": the unit check reads `MM` as millimetres. Format Date fields themselves are exempt. Workaround: in Comments, including action 1's quoted prompt, write the pattern in words ("year-month-day"), and say in the report that the quoted prompt was reworded. Tracked for a validator fix in #5.
