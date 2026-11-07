# Rules: files, photos, images and documents

Read when the shortcut picks, renames, saves or shares files, or works with photos, images, video or PDFs.

## Picking and saving

- User picks a file: **Select File** (`is.workflow.actions.file.select`); Document Picker Open/Save for explicit Files UI flows.
- Videos: **Select Photos** configured for videos; both Photos and Files requested → Choose from Menu with both pickers.
- **Set Name** (`is.workflow.actions.setitemname`) makes a renamed copy: `WFInput` = source item, `WFName` = target name (for example `Test.txt`); output **Renamed Item** feeds **Save File** (`is.workflow.actions.documentpicker.save`) or **Share**.
- **Rename File** (`is.workflow.actions.file.rename`, `WFFile` + `WFNewFilename`) renames the original in place. Rename-save-delete flows: keep the pick as **Original File**, Set Name on it, save/share **Renamed Item**, delete **Original File** afterwards only if asked.
- Preview with **Quick Look** before Save/Share when useful; PDFs: Make PDF → Preview Document → Save/Share.
- PDF pages: **Split PDF Into Pages**, then Count.
- Prefer cross-platform actions: Get Details of File for a path rather than macOS-only Get Parent Folder.

## Images

- **Convert Image** (`is.workflow.actions.image.convert`): explicit `WFInput`.
- **Extract Text from Image** (`is.workflow.actions.extracttextfromimage`): exactly one non-empty image key; `imageFile` on OS 27+, `WFImage` for older exports, `WFInput` only to follow an existing pattern.
- **Delete Photos** (`is.workflow.actions.deletephotos`) takes `photos`, not `WFInput`.
- Find Photos filters: [FILTERS.md](../FILTERS.md).
- Bottom-aligning in **Combine Images** (horizontal mode top-aligns): flip each image upside-down, combine, flip the result back. **Flip Image** is mirrored across platforms: upside-down is `Vertical` on iOS/iPadOS and `Horizontal` on macOS. Wrap each flip in an If on `Device Model is Mac` (Mac → Horizontal, otherwise Vertical).
