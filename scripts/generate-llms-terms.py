#!/usr/bin/env python3
"""Generate public/llms-terms.txt – Beijerdictionary's curated terminology sample
for AI agents.

Reads the local Wordbook database (D:\\SynologyDrive\\Dev\\beijerterm-database\\data\\
wordbook.db – NOT available in CI, which is why the output is committed)
and writes a copyright-clean subset:

  * a catalogue of ALL sources with entry counts (titles and counts are
    facts – no third-party content is republished);
  * ~1,000 entries sampled from the "Beijer Dictionary – Dutch–English Technical
    Dictionary" source ONLY (Michael's own work, his copyright),
    stratified across subject domains;
  * ~100 entries from the ERA Railway Terminology Collection (tagged
    `permissive`; © European Union Agency for Railways, reused with
    attribution).

Sources tagged `restricted` or `unknown` are listed by name only.
Rerun after major termbase updates:  python scripts/generate-llms-terms.py
"""

import sqlite3
from pathlib import Path

DB = r"D:\SynologyDrive\Dev\beijerterm-database\data\wordbook.db"
OUT = Path(__file__).resolve().parent.parent / "public" / "llms-terms.txt"

BEIJERTERM_SAMPLE = 1000
ERA_SAMPLE = 100
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


def main():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row

    total = con.execute("select count(*) from entries").fetchone()[0]
    sources = con.execute(
        """select s.id, s.title, s.licence, count(distinct es.entry_id) n
           from sources s
           join raw_entries re on re.source_id = s.id
           join entry_sources es on es.raw_entry_id = re.id
           group by s.id order by n desc""").fetchall()

    bt = next(s for s in sources if (s["title"] or "").startswith("Beijer Dictionary"))
    era = next(s for s in sources if "ERA Railway" in (s["title"] or ""))

    lines = [
        "# Beijerdictionary – curated terminology sample",
        "",
        "> Beijerdictionary (https://beijerdictionary.com) is Michael Beijer's Dutch–English",
        "> terminology site: a searchable database of "
        f"{total:,} term pairs from {len(sources)} sources,",
        "> built over 30+ years of patent and technical translation.",
        "",
        "This file contains a REPRESENTATIVE SAMPLE, not the full database:",
        f"~{BEIJERTERM_SAMPLE} entries from Michael's own Beijer Dictionary and",
        f"~{ERA_SAMPLE} from the permissively licensed ERA Railway Terminology",
        "Collection. Other indexed sources are catalogued below by name only –",
        "their content is not republished here for copyright reasons. For real",
        "lookups, use the search at https://beijerdictionary.com/.",
        "",
        "## Source catalogue (entry counts)",
        "",
    ]
    for s in sources:
        lines.append(f"- {s['title']} — {s['n']:,} entries")

    lines += [
        "",
        f"## Sample: Beijer Dictionary – Dutch–English Technical Dictionary "
        f"({bt['n']:,} entries total)",
        "",
        "© Michael Beijer. Format: Dutch term = English term (domain).",
        "",
    ]
    for term_a, term_b, dom in sample_source(con, bt["id"], BEIJERTERM_SAMPLE):
        suffix = f" ({dom})" if dom else ""
        lines.append(f"{term_a} = {term_b}{suffix}")

    lines += [
        "",
        f"## Sample: ERA Railway Terminology Collection ({era['n']:,} entries total)",
        "",
        "© European Union Agency for Railways, reused with attribution.",
        "",
    ]
    for term_a, term_b, dom in sample_source(con, era["id"], ERA_SAMPLE):
        lines.append(f"{term_a} = {term_b}")

    lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"wrote {OUT} ({OUT.stat().st_size:,} bytes, "
          f"{len(lines):,} lines)")


if __name__ == "__main__":
    main()
