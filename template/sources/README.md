# sources/

One folder per source: `sources/<source-id>/` with a kebab-case id (e.g. `fr3066128a1`, `kurmus-2020-toxicity`).

Each folder contains:

- `document.pdf` — the original, human-readable (when legally available; otherwise SOURCE.md links to it)
- `text.md` — full text for AI reading. Converted by the AI if its tools allow; **operator-supplied conversions are preferred when available**. If missing, note that in SOURCE.md and continue without stalling.
- `SOURCE.md` — metadata: title, authors, year, type (patent | peer-reviewed | thesis | report | company disclosure | press | failed attempt), where found, URL, legal status if a patent, access notes (paywall etc.), one-line relevance note.

Rule: a source without `text.md` is not a blocker. The registry entry can proceed with `parameter_not_located` marks and be deepened when the text arrives.
