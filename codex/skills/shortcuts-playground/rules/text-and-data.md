# Rules: text, lists, dictionaries and messages

Read when the shortcut transforms text, builds lists or dictionaries, or sends a message.

## Input keys per text action

Wrong keys import fine but show an empty input in the editor.

| Action | Identifier | Source text key |
|--------|------------|-----------------|
| Replace Text | `is.workflow.actions.text.replace` | `WFInput`, as a `WFTextTokenString` placeholder (or wrapped variable), never a bare attachment |
| Match Text | `is.workflow.actions.text.match` | `text` |
| Change Case | `is.workflow.actions.text.changecase` | `text` |
| Split Text | `is.workflow.actions.text.split` | `text`; with `WFTextSeparator = Custom` also `WFTextCustomSeparator` (a single space is valid) |
| Get URLs from Input | `is.workflow.actions.detect.link` | `WFInput` as a `WFTextTokenString` placeholder |
| Translate Text | `is.workflow.actions.text.translate` | `WFInputText`; `WFSelectedFromLanguage` and `WFSelectedLanguage` take display names (`Spanish`, `Chinese (Simplified)`), not ISO codes |
| Base64 Encode/Decode | `is.workflow.actions.base64encode` | `WFInput`, always explicit |

- Replace Text that deletes a match: omit `WFReplaceTextReplace` (an explicit empty string also works).
- Regex extraction: **Match Text** → **Get Group**, then Replace/Split/Combine to normalize.
- **Get Rich Text from Markdown** / **Get Markdown from Rich Text** when moving between plain and rich-text apps.

## Composing text

- One Text action interleaves literals and variables, with a placeholder per variable (`Track – Artist` has two).
- After editing template text, recount every `attachmentsByRange` offset.

## Lists and dictionaries

- Dictionary actions use `WFDictionaryFieldValue` wrappers with the right `WFItemType` for strings, nested dictionaries and booleans.
- **Set Dictionary Value** sets `WFDictionary` to the target dictionary.
- JSON that arrives as text goes through **Detect Dictionary** before **Get Dictionary Value**.
- Present built lists with **Combine Text** or **Choose from List**. vCard/VCF formatting only when the user asks for contact cards, with a Comment containing `ALLOW_VCARD`.

## Send Message

- Content is a named variable built by at least two **Add to Variable** (`is.workflow.actions.appendvariable`) actions, with no initializing Set Variable. Mixed content: append the media, then the text. One content type: append the source, then an empty Text action's output.
- Pass it as `WFSendMessageContent`, a `WFTextTokenString` with a placeholder. `WFSendMessageAttachments` stays unset.

```text
Find Photos -> Add to Variable "Message Items"
Text "" -> Add to Variable "Message Items"
Send Message content -> WFTextTokenString placeholder for "Message Items"
```

## Send Email

`is.workflow.actions.sendemail` (never `sendmail`); attachments in `WFSendEmailActionInputAttachments` as a `WFTextTokenString` placeholder.
