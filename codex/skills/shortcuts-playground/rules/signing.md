# Rules: signing and install troubleshooting

Read when `sign-shortcut` fails, or the user reports an import problem.

## What `sign-shortcut` does

1. Copies the unsigned XML to `<output dir>/<YYYY-MM-DD>/<name>-<HHMMSS>.xml` (the archive is always the raw XML).
2. Copies it to `<output dir>/<name>.shortcut` and runs `shortcuts sign --mode <mode>` on it, adding about 19 KB of signature.
3. On a format error from a validator-clean plist, retries once after `plutil -convert binary1` on the `.shortcut` copy.
4. Prints JSON with the archive and signed paths.

## Failures

- `Error: The file doesn't exist.` for a file that exists: copy the XML to a clean `.shortcut` path (for example `cp source.xml /tmp/MyShortcut.shortcut`) and sign that.
- `The file couldn't be opened because it isn't in the correct format.` after the binary retry too: retry from an unrestricted shell and check filesystem permissions before treating the plist as malformed.
- `ERROR: Unrecognized attribute string flag '?'` is noise when the output file exists.
- The `shortcuts` CLI has only `run`, `list`, `view` and `sign`; there is no `import`, `delete` or `rename`.

## Install naming

- The signed filename is the display name: no `_signed` or `_final`. A `_signed` name in the library is a failed install; reinstall from a canonical filename.
- Importing over an existing shortcut of the same name is silently skipped. Tell the user to delete the old one in Shortcuts.app first.
