# Changelog

Notable changes to Beijer Dictionary (called Beijerterm until October 2026) —
the website (this repo) and the underlying terminology database and search
API. Newest first.

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
