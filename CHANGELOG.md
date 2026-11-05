# Changelog

Notable changes to Beijer Dictionary (called Beijerterm until October 2026) —
the website (this repo) and the underlying terminology database and search
API. Newest first.

## 2026-11-05

**Site: a cleaner, clearer look**
- **The "Bd" mark, a little deeper.** The green circle keeps its letters,
  but its gradient ends in a less neon green, so the white "d" (which sits
  on that end) no longer fades in a browser tab. A mirrored-"bd" mark on a
  rounded square was on the site for a few hours; the circle came back, as
  one of a family with Supervertaler's "Sv" and MemDesk's "Md".
- **The front page says what the site is.** A headline ("Technical
  terminology you can trace to its source") and a line on what's in it;
  under the search, the key numbers (sources, entries, multilingual
  concepts, sentences of EU legislation) and three cards for the
  Dictionary, EU legislation in context and the Articles; and "Try:"
  example searches. Once you search, the results take their place near the
  top of the screen, and they come back when the box is emptied. Search
  links (?q=…, as SuperLookup uses) open straight on the results.
- **One search bar.** The languages, the box and a Search button sit in one
  bar. The search still runs as you type; the button or Enter runs it at
  once and, on a phone, puts the keyboard away.
- **Search options behind one button, on every screen.** The eleven
  checkboxes that filled a line under the box are now behind an Options
  button, grouped into Search in, Match and Only entries with. The button
  sums up what is on ("terms only", "terms + definitions, exact match"),
  in green when an option from an earlier visit is still on.
- **One green.** Links, buttons, the active tab and labels now share one
  bottle green instead of blue links and two greens (a lighter green in
  dark mode).
- **Readable source names.** Result chips say "Microsoft", "IATE" or
  "Joost de Vree" instead of codes in capitals ("MICROSOFT-TERMINOLOGY"),
  with the full title in the tooltip; the Sources page shows the same
  names. Subjects are in normal case ("Building and public works").
- **Headwords in a serif.** Headwords on results and article titles are set
  in Source Serif, like a printed dictionary; everything else stays in
  Inter.
- **Tidier header and footer.** The dark-mode button is a line icon, the
  "MB" button is gone (the footer links to beijer.uk), and the footer links
  are plain text rather than buttons. Each results tab shows its number in
  a small pill.

**Site and search API**
- **EU legislation in six languages.** The EU legislation tab now works
  between any two of English, Dutch, French, German, Italian and Spanish
  (Dutch → French, German → English, Spanish → Italian, …), not just English
  and Dutch: about 3.5 million different sentence pairs for each two of
  them. Garbled characters from the source are repaired along the way (about
  400,000 sentences showed "愦灭※" for an ellipsis or "愦灭;quot;" for a
  quotation mark), and sentences misaligned in the source sink to the end
  of the list.
- **Articles described as they are.** The Articles page and About page now
  call them dictionary articles: one term each, with its translations,
  often with examples, sources and notes, rather than "longer notes on how to
  tell tricky terms apart".
- **One heading per subject on the Articles page.** Five subjects that were
  tagged under two names now have one each: railways, sport, tax, human
  resources (was also "HR") and health and safety (was also "occupational
  safety").
- **EU legislation on the Sources page.** DGT-TM, the European Commission's
  translation memory behind the EU legislation tab, is now listed with the
  dictionary sources: 4,513,639 sentences from 42,701 documents in six
  languages, with its publisher, reuse terms and a link to the official
  page. It has no source chip, since it never appears on a dictionary
  result, and the source count on the search page now includes it (34).
  On a phone, multilingual sources no longer read "150 concepts entries".
- **Readable tables in articles.** The 72 articles with a table (mostly
  example sentences: Dutch | English | Source) now show it with space between
  the columns, each heading over its own column and a line between rows.
  Before, a row ran together like one long sentence. On a phone, a wide table
  scrolls sideways in its own box.
- **Dictionary and EU legislation tabs.** For English → Dutch and Dutch →
  English searches, the results now have two tabs, each with its number of
  hits: **Dictionary** and **EU legislation**, so the EU sentences no longer
  sit at the bottom of a long list. The site remembers which tab you last
  chose. When the dictionary finds nothing but EU legislation does, the
  empty Dictionary tab offers a link to the EU sentences. Other language
  pairs have no tabs.
- **Articles in columns.** The Articles page lists the articles in as many
  columns as fit (three on a desktop, more in Wide mode, one on a phone),
  each with its language in front, so the page is about half as long.
  Titles that are whole sentences (several patent phrases) are shortened in
  the list; the tooltip and the article itself show them in full.
- **Faster page loads.** The entry count and the list of language pairs
  shown when the page opens are now worked out once per publish instead of
  on every visit, which used to read all 1.3 million entries twice
  (about 0.6 s per page load, and 97% of the dictionary database's reads).

## 2026-11-04

**Site and search API**
- **EU legislation in context.** Searching English → Dutch or Dutch →
  English now also shows, under the results, sentences from EU
  legislation that contain the words as an exact phrase, each beside its
  official translation and linked to the document on EUR-Lex (both
  languages side by side). Shortest sentences first, 20 at a time, with
  "Show more". The sentences come from DGT-TM, the European Commission's
  translation memory of EU legislation (2021 release, via OPUS): about 3.6
  million English–Dutch pairs from some 42,000 documents, up to 2020. They
  live in a separate database from the dictionary, so a dictionary publish
  never re-uploads them.

## 2026-10-23

**Site**
- **Sharp link previews.** A link to any page pasted into WhatsApp,
  LinkedIn, Slack, iMessage or X now shows a proper preview card (the Bd
  mark, large, on the site's stone background) instead of a blurry,
  stretched copy of the browser-tab icon. The first version had the name
  and tagline under the mark, which turned to mush in WhatsApp's small
  preview: the middle of the picture shrunk to about 115 pixels.
  `scripts/make-icons.py` now makes the card along with the icons.

## 2026-10-20

**Site**
- The search box says what to type ("Type a Dutch term…", or "Type a term
  in any language…") instead of repeating the language pair shown right
  below it, and the empty page no longer asks you to type three times.
- The **Articles** page has a filter box: type a term or a subject and the
  list narrows as you type, across titles, headwords and alternative
  spellings, ignoring accents and capitals.
- **The menu is now in the header.** Search, Articles, Sources and About sit
  next to the Beijer Dictionary name, in the same place on every page
  (they used to move down the page on Articles and Sources, and disappear
  on articles and How it works). On a phone they form a second row under
  the name, so the name stays on one line. **About** replaces the "?"
  button, and the footer now links to Articles too.
- The Wide/Narrow button is now an icon, like the buttons beside it: arrows
  pointing outwards widen the page, arrows pointing inwards narrow it again.
  (As text it named what it would switch to, so in wide mode it said
  "Narrow", which read like the current setting.)
- **More room for results on a phone.** The search options fold away behind
  a "Search options" button, which says how many options you've changed
  (they're remembered on each device, so this shows when one is still on).
  With less space around the lead line, the first result now starts about
  200 pixels higher on an iPhone-sized screen.
- On a phone or tablet the **Sources** list shows each source as a card —
  title, short name, then author, year, languages, entries and licence on
  one line — instead of a table that scrolled sideways and cut off the
  authors. The column headings become a row of "Sort by" buttons.
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
