# Rosetta Support Manual

The Support Manual for the Rosetta system: more technical topics (hardware build,
installation, HAL files, Mesa card, diagnostics, …). It is not the starting place
for the general user — that is the
[User Manual](https://rosetta.colvintools.com/UserManual/).

This manual is for the website only; unlike the User Manual and Gcode Library
(which live in the [Rosetta](https://github.com/RichColvin/Rosetta) repo and are
installed on every Rosetta), it is not copied to the Raspberry Pi.

## What's here

| Path | What it is |
|---|---|
| `Rosetta_Support_Manual/` | The manual: plain HTML pages, `index.html` is the contents page. Open any page in a browser — no web server needed. |
| `Rosetta_Support_Manual/rosetta-docs.css`, `rosetta-docs.js` | The look and the search / picture zoom, the same as the User Manual's except for the **dark grey header** (the User Manual's is navy, so readers can tell at a glance which manual they're in). |
| `Rosetta_Support_Manual/search-index.js` | Made by the build tool — don't edit. |
| `tools/build_manual.py` | Rebuilds the search index and each page's Previous / Next links. |

## Editing

1. Edit the HTML pages in `Rosetta_Support_Manual/` directly. Each page carries its
   own header and footer; links between pages and to pictures are relative; links
   that need the Internet are `https://` links with `class="online"` (shown with ↗).
2. After editing, adding or renaming a page, run:

   ```bash
   python3 tools/build_manual.py
   ```

   Running it again changes nothing. A page gets Previous / Next links only if the
   contents page (`index.html`) links to it.
3. If you change `rosetta-docs.css` or `rosetta-docs.js`, make the same change in the
   Rosetta repo's `Rosetta_User_Manual/` and `Rosetta_Gcode_Library/` copies (apart
   from the header colour, `--header`), so the manuals stay alike.

## History

Converted on 21 November 2026 from the PmWiki Support Manual at
`rosetta.colvintools.com/Support/`. Ten pages from before the Rose Engine Butler →
Rosetta renaming (`REBBackup`, `REBLaunch`, `UpdatingRoseEngineButler`, …), which no
current page linked to, were left out. Pictures were re-compressed (about 5.1 MB →
3.1 MB) only where the result is visually the same.
