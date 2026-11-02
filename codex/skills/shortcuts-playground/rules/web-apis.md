# Rules: web APIs and JSON

Read when the shortcut calls a web API, builds a request body, or parses JSON.

## Research

- For an unfamiliar API, read its latest official docs before drafting: auth, endpoint, parameters, payload shape. Match endpoint strings exactly (underscore vs hyphen matters).
- Use the API's own upload method for files. Add third-party services, CDNs, hidden dependencies or extra import questions only when the user asks for them.
- Notion: upload images with the `file_uploads` endpoints and the `file_upload` block type; use `external` image blocks only when the user supplies a URL. Filter on the `title` property unless the user names a different title property (for example `Name`).
- Todoist updates: `/rest/v2/tasks/` carries the task ID placeholder.

## Credentials

- Store API tokens in a Text action, with a Comment before it linking to the service's API-key page.
- Credentials in shell snippets, examples, logs and transcripts are placeholders or env vars, never real values.
- Tokens come from a Text action. Loading one from a file needs the user's request plus a Comment containing `ALLOW_TOKEN_FILE` saying why.
- Authorization headers: `Basic {base64(user:pass)}` or `Bearer {token}`, as the API requires.

## Building the request

- Static URL: set it directly in **Get Contents of URL** (`WFURL`). URL with variables or query parameters: build it in a **URL** or **Text** action with placeholders and pass that in.
- `WFURL` is a `WFTextTokenString` with placeholders even when the whole URL is one variable.
- Before output, scan every API string: no `//` beyond the protocol, no empty JSON fields where a variable belongs (`equals:""`, `id:""`, `url:""`, `filename:""`), a placeholder right after the slash of a path parameter (`/tasks/{id}`), and the **Ask for Input** variable inside any query parameter that takes user input.
- JSON body (`WFHTTPBodyType = JSON`): use `WFJSONValues` for flat key/value payloads so the editor keeps the body.
- Arrays of objects or deep nesting (or `WFJSONValues` rendering as `Number 0` or empty rows): build the JSON in a Text action, set it as `WFRequestVariable`, set body type **File**, keep `Content-Type: application/json`. Every JSON Text is a request's `WFRequestVariable`, or it is removed.
- Form uploads (`WFHTTPBodyType = Form`): a file field (`WFItemType = 5`) wraps the file in `WFTokenAttachmentParameterState` with an inner `WFTextTokenAttachment`. Set `WFRequestVariable` only when the body type is File.
- Dictionary arrays (`WFItemType = 2`) use `WFArrayParameterState` with a list of items (`WFItemType` + `WFValue`).
- With **Get Name** for an upload, append the extension (for example `.png`) in the payload, and set **Get Web Page Title** to Off so it returns the file name.

## JSON text templates

- Insert Dictionary or List outputs into JSON Text only after turning them into JSON text; Shortcuts stringifies raw ones as newline-separated pseudo-JSON that **Detect Dictionary** rejects.
- Sanitize freeform text before putting it inside `"content":""`: backslashes, double quotes, newlines and tabs.
- Appending to a JSON array with **Replace Text** on `\]$`: the replacement ends with `]`.
- Multi-turn continuation payloads: append assistant text from a plain text variable (for example `Response Text`) and keep `messages_json` valid JSON.

## Reading the response

- Keep `ShowHeaders` off unless needed; with it on, the output shape changes.
- Run **Detect Dictionary** on **Contents of URL**, then **Get Dictionary Value** with dot notation and 1-based indexes (`results.tracks.items`, `artists.1.name`).
- Guard optional parents: extract `error`, check it with **If Has Any Value**, read `message` inside that branch. Never read `error.message` straight off a raw response.
- JSON booleans arrive as numbers `1`/`0`: compare numerically (`is greater than 0`) or normalize through a Text action and compare to `"1"` with `is`.
- JSON `null` arrives as empty: test with Has Any Value, never against the string `"null"`.
- Every extracted field is used later, or the extraction is removed.
