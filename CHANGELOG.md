# Changelog

Notable changes to Beijer Dictionary (called Beijerterm until October 2026) —
the website (this repo) and the underlying terminology database and search
API. Newest first.

## 2026-10-20

**Site**
- **The menu is now in the header.** Search, Articles, Sources and About sit
  next to the Beijer Dictionary name, in the same place on every page
  (they used to move down the page on Articles and Sources, and disappear
  on articles and How it works). On a phone they form a second row under
  the name, so the name stays on one line. **About** replaces the "?"
  button, and the footer now links to Articles too.
- **More room for results on a phone.** The search options fold away behind
  a "Search options" button, which says how many options you've changed
  (they're remembered on each device, so this shows when one is still on).
  With less space around the lead line, the first result now starts about
  200 pixels higher on an iPhone-sized screen.
- The **Sources** list is now in alphabetical order of title (it was sorted
  by each source's short name, which often starts with a different word).
  Each source also shows the short name its chips carry on search results
  (e.g. BGL), so a chip you see on a result is easy to find in the list.
  Click a column heading to sort by author, year, entries or licence.
- When a search result combines several sources, a faint dotted line now
  separates each source's translations, so it's clear at a glance which
  source chip belongs to which terms.
- The source list has its own **Sources** tab again (beijerdictionary.com/sources),
  next to Search and Articles, so the search page is just the search. The
  "32 sources" count under the search box links to it, and the source chips on
  search results still open a source's details in place.
- The search box no longer says "(press /)", which read like an instruction to
  type a slash; the shortcut is in the box's tooltip. It also says "any
  language" instead of "Any", and follows the To language when you change it.
- **New light mode.** Light mode now uses beijer.uk's warm stone and ink
  instead of white, with slightly larger text, and is what new visitors see.
  The moon button still switches to dark mode, and the choice is remembered on
  each device.
- The MB button (top right) opens beijer.uk in a new tab.
- On a phone, article pages no longer scroll sideways because of long links,
  and the search options are easier to read in Dark.

**Sources added**
- Nuffic Glossary (Dutch–English), with its English-only terms.
- NICHE terminology list (Nuffic; English–French).
- Blood Pressure Monitoring Glossary (English, Dutch, German, French, Spanish,
  Italian).

**Under the hood**
- Importing a new dictionary no longer creates duplicate copies of
  hand-edited entries, and hand-edited entries keep their ids through imports.

## 2026-10-17

**Site**
- In search results, definitions and notes are now labelled ("Definition",
  "Note", in the logo's green), so it's clear where an entry's definition ends
  and its notes begin.

**Under the hood**
- Hand edits reach the live search in seconds: the admin app's new "Publish my
  edits" sends only what was edited, instead of re-uploading the whole
  database.
- Entries can be looked up, edited and published from a Claude chat, through a
  local MCP server.

## 2026-10-14

**Beijer Dictionary**
- Beijerterm is now **Beijer Dictionary**, at **BeijerDictionary.com**. Old
  beijerterm.com links redirect to the new address.
- Michael's own Dutch–English technical dictionary, one of the sources, has
  taken the same name.

**Site**
- New green "Bd" logo, also used as the browser tab icon.
- Every page shares one header: the Beijer Dictionary wordmark on the left,
  square buttons on the right ("?" for How it works, the light/dark switch,
  "MB" for beijer.uk). On phones it stays on one line.
- The sources table fits the page; on a phone it scrolls sideways in its own
  box instead of widening the whole page.

**Fixes**
- Clicking a source chip on a search result opens the source's info box
  again. Since August it opened invisibly and left the page frozen until Esc
  or a refresh.

**Under the hood**
- The database now holds 28 sources and about 1.9 million entries.

## 2026-08-07

**Site**
- The full source list is on the front page, under the search box, and hides
  while search results are showing. It replaces the separate Sources page;
  old /sources links redirect to it.
- A source chip on a result opens that source's info box on the same page.

**Search**
- Each definition appears under the translation it defines, so it is clear
  which meaning it belongs to. Definitions from single-language glossaries,
  with no translation to attach to, get their own labelled block.
- Common words with many translations no longer lose some of them.
- The language direction now affects ranking, so changing it re-runs the
  search.
- Long runs of translations wrap inside the card instead of running off its
  edge.

**Sources added**
- TU Delft terminologielijst (Dutch–English).

## 2026-07-17

**Articles**
- Terminology articles: each has its own page under /articles/, an
  **Articles** tab lists them by subject, and a matching article appears as a
  card at the top of search results.

**For AI tools**
- /llms.txt describes the site for AI assistants and points to
  /llms-terms.txt: the full source list plus a sample of about 1,000 entries
  from Michael's own dictionary and 100 from the openly licensed ERA Railway
  collection. Sources with restricted licences are named but not republished.

**Sources added**
- VVT Terminologielijst 2024 (vertical transport): translations and
  definitions.

## 2026-06-22

**Search results**
- Translations are grouped by meaning: a word with several senses gets one
  numbered line per sense, with a short definition of that sense where there
  is one.
- When several sources share a word, each translation line carries its own
  source and subject area, so you can see where every translation came from.
- Each definition is tied to the source it came from and its own reference
  link.
- Entries can link to an outside reference (e.g. EUR-Lex), shown as a 🔗 chip.
- Source chips have a light fill and sit clear of the subject text.

**Sources added**
- Microsoft Terminology Collection (Dutch–English).
- Terminologie Financieel Management (F. van Amerongen; Dutch–English).
- Statistics Glossary (Piotr Bienkowski; Dutch–English).
- ERA Railway Terminology Collection, with EUR-Lex reference links.
- Textile Glossary (Dutch, English, German, French).

**Site**
- A sitemap is now generated, so search engines can find every page.

## 2026-06-03

**Search**
- Field-scoped search: by default only **terms** are matched; opt in to search
  **definitions** and/or **notes** ("Search in:" toggles).
- New options: **exact match**, **whole word**, **case-sensitive**,
  **accent-sensitive**.
- "**Only entries with:**" filters — abbreviation, definition or notes.
- **Any** option in the language selectors (search to/from any language).
- Matched search words are now **highlighted** in results.
- Exact matches rank first (e.g. "AFF" beats "afferent").
- Monolingual (single-language) glossaries are now searchable.

**Sources added**
- EU Legislation Glossary (Dutch–English + English-only), with definitions.
- Dutch–English construction terms (joostdevree.nl).
- US construction abbreviations (American English).
- Latin→Dutch glossary of conservation-relevant plant species.
- IATE, the EU's terminology database: the Dutch–English termbase, plus
  Dutch–English abbreviations and acronyms and a Dutch-only acronym list.

**Site**
- Sources page refreshes its list automatically after a data update.
- "How it works" page updated; GitHub link and back-to-top button added.

**Under the hood**
- Notes are now searchable; the database grew to ~16 sources / ~934k entries,
  with ~138k definitions.
- Standardised per-source provenance metadata; paren-aware synonym splitting;
  merge-synonym preprocessing.
