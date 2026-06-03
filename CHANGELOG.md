# Changelog

Notable changes to Beijerterm — the website (this repo) and the underlying
terminology database and search API. Newest first.

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

**Site**
- Sources page refreshes its list automatically after a data update.
- "How it works" page updated; GitHub link and back-to-top button added.

**Under the hood**
- Notes are now searchable; the database grew to ~16 sources / ~934k entries,
  with ~138k definitions.
- Standardised per-source provenance metadata; paren-aware synonym splitting;
  merge-synonym preprocessing.
