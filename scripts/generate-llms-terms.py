#!/usr/bin/env python3
"""Generate public/llms-terms.txt – Beijer Dictionary's curated terminology sample
for AI agents.

Reads the local Wordbook database (D:\\SynologyDrive\\Dev\\beijerterm-database\\data\\
wordbook.db – NOT available in CI, which is why the output is committed)
and the live search API's /meta, and writes a copyright-clean subset:

  * a catalogue of ALL sources with their counts, taken from /meta so the
    numbers are the ones the site shows (the master store counts the pairs
    behind multilingual sources too, which the site shows as concepts);
    titles and counts are facts – no third-party content is republished;
  * ~1,000 entries sampled from the "Beijer Dictionary – Dutch–English Technical
    Dictionary" source ONLY (Michael's own work, his copyright),
    stratified across subject domains.

Until 2026-11-06 it also promised ~100 entries from the ERA Railway
Terminology Collection, but ERA is English terms with definitions, so the
pair sample always came out empty; it was dropped.

Sources tagged `restricted` or `unknown` are listed by name only.
Rerun after a new source or a large import, with the search API's address
(the site's PUBLIC_WORDBOOK_API) in the environment:

    PUBLIC_WORDBOOK_API=https://wordbook-search.<subdomain>.workers.dev \
        python scripts/generate-llms-terms.py
"""

import json
import os
import sqlite3
import sys
import urllib.request
from pathlib import Path

DB = r"D:\SynologyDrive\Dev\beijerterm-database\data\wordbook.db"
OUT = Path(__file__).resolve().parent.parent / "public" / "llms-terms.txt"

LANG_NAMES = {"en": "English", "nl": "Dutch", "de": "German", "fr": "French",
              "it": "Italian", "es": "Spanish", "la": "Latin"}

BEIJERTERM_SAMPLE = 1000
MIN_LEN, MAX_LEN = 3, 60


def sample_source(con, source_id, budget):
    """Deterministic, domain-stratified sample of clean entries."""
    domains = [r[0] for r in con.execute(
        "select domain from raw_entries where source_id=? "
        "group by domain order by count(*) desc limit 12", (source_id,))]
    per_domain = max(20, budget // max(len(domains), 1))
    seen, out = set(), []
    for dom in domains:
        if len(out) >= budget:
            break
        cond = "re.domain is null" if dom is None else "re.domain = ?"
        args = (source_id,) if dom is None else (source_id, dom)
        rows = con.execute(
            f"""select distinct e.term_a, e.term_b, re.domain
                from entries e
                join entry_sources es on es.entry_id = e.id
                join raw_entries re on re.id = es.raw_entry_id
                where re.source_id = ? and {cond}
                  and length(e.term_a) between {MIN_LEN} and {MAX_LEN}
                  and length(e.term_b) between {MIN_LEN} and {MAX_LEN}
                  and e.term_a not like '-%%'
                  and e.term_a not like '%%(none)%%'
                  and e.term_b not like '%%(none)%%'
                order by e.id""", args).fetchall()
        step = max(len(rows) // per_domain, 1)
        for row in rows[::step][:per_domain]:
            key = (row[0].lower(), row[1].lower())
            if key in seen:
                continue
            seen.add(key)
            out.append(row)
    return out[:budget]


def fetch_meta():
    api = os.environ.get("PUBLIC_WORDBOOK_API", "").rstrip("/")
    if not api:
        sys.exit("Set PUBLIC_WORDBOOK_API to the search API's address "
                 "(the same one the site is built with).")
    req = urllib.request.Request(
        api + "/meta", headers={"Accept": "application/json",
                                "User-Agent": "generate-llms-terms"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def langs(s):
    return ", ".join(LANG_NAMES.get(c, c) for c in s.get("languages") or [])


def main():
    meta = fetch_meta()
    counts = meta["counts"]
    by_slug = {s["slug"]: s for s in meta["sources"]}
    pairs = sorted((s for s in meta["sources"] if s.get("entry_count")),
                   key=lambda s: -s["entry_count"])
    concepts = sorted((s for s in meta["sources"] if s.get("concept_count")),
                      key=lambda s: -s["concept_count"])
    corpora = meta.get("corpora") or []

    con = sqlite3.connect(Path(DB).as_uri() + "?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    bt = by_slug["beijer-dictionary"]
    bt_id = con.execute("select id from sources where slug = 'beijer-dictionary'"
                        ).fetchone()[0]
    sample = sample_source(con, bt_id, BEIJERTERM_SAMPLE)
    # A query that quietly matches nothing (as the ERA sample once did) must
    # not produce a file that promises a sample and holds none.
    if len(sample) < BEIJERTERM_SAMPLE // 2:
        sys.exit(f"Only {len(sample)} sample entries found; nothing written.")

    lines = [
        "# Beijer Dictionary – curated terminology sample",
        "",
        "> Beijer Dictionary (https://beijerdictionary.com) is Michael Beijer's",
        "> multilingual terminology site for technical translators, Dutch–English",
        f"> at heart: {counts['entries']:,} term pairs and {counts['concepts']:,}"
        " multilingual concepts",
        f"> from {counts['sources']} glossaries, termbases and thesauri,"
        " built over 30+ years",
        "> of patent and technical translation.",
        "",
        "This file contains a REPRESENTATIVE SAMPLE, not the full database:",
        f"{len(sample):,} entries from Michael's own Beijer Dictionary. The other",
        "sources are catalogued below by name only – their content is not",
        "republished here, for copyright reasons. For real",
        "lookups, use the search at https://beijerdictionary.com/ (a link such as",
        "https://beijerdictionary.com/?q=tegels&from=nl&to=en opens a search).",
        "",
        "## Source catalogue",
        "",
        "### Term-pair sources (entry counts)",
        "",
    ]
    for s in pairs:
        lines.append(f"- {s['title']} — {s['entry_count']:,} entries ({langs(s)})")

    lines += [
        "",
        "### Multilingual sources (one concept per row, with its terms in each language)",
        "",
    ]
    for s in concepts:
        lines.append(f"- {s['title']} — {s['concept_count']:,} concepts, "
                     f"{s['term_count']:,} terms ({langs(s)})")

    if corpora:
        lines += [
            "",
            "### EU legislation in context (sentences, not dictionary entries)",
            "",
        ]
        for c in corpora:
            lines.append(f"- {c['title']} — {c['sentence_count']:,} sentences "
                         f"({langs(c)})")

    lines += [
        "",
        f"## Sample: Beijer Dictionary – Dutch–English Technical Dictionary "
        f"({bt['entry_count']:,} entries total)",
        "",
        "© Michael Beijer. Format: Dutch term = English term (domain).",
        "",
    ]
    for term_a, term_b, dom in sample:
        suffix = f" ({dom})" if dom else ""
        lines.append(f"{term_a} = {term_b}{suffix}")

    lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"wrote {OUT} ({OUT.stat().st_size:,} bytes, "
          f"{len(lines):,} lines)")


if __name__ == "__main__":
    main()
