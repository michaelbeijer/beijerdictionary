# Beijerdictionary

The public, canonical site for **Beijerdictionary** — a curated, searchable
multilingual terminology database for technical translators
(Dutch ↔ English and more), at **beijerdictionary.com**.

Until October 2026 the site was called Beijerterm, at beijerterm.com, which now
redirects here. The repo, the Cloudflare Worker and code names keep the old
name on purpose; only what visitors see was renamed.

This repo is **software only**. The terminology data is private: it lives in
the separate private `wordbook` repo (the curation pipeline + SQLite master
store) and in a Cloudflare D1 database. This site calls a Cloudflare Worker
search API and only ever receives **per-query result snippets** — never the
bulk dataset.

```
beijerdictionary.com (this site, Cloudflare Pages)
      │  GET /meta, /search   (fetch)
      ▼
  Worker "wordbook-search"   (in the beijer.uk repo's worker/ dir)
      ▼
  D1 "wordbook"              (loaded from the private wordbook repo)
```

beijer.uk hosts a lighter hand-off search box that links here; this is the
canonical home (see `rel=canonical`). Supervertaler's Superlookup calls the
same Worker API.

## Local development

```bash
npm install
npm run dev        # http://localhost:4321
```

In dev the front-end targets a local Worker on `http://127.0.0.1:8787`
(run `wrangler dev` in the beijer.uk `worker/` dir, with a local D1 loaded).
Without it, the page shows "Search API not configured" — it never ships data.

## Deploy (Cloudflare Pages)

beijerdictionary.com is already proxied through Cloudflare, so:

1. **Cloudflare dashboard → Workers & Pages → Create → Pages → Connect to Git**,
   pick this repo (`michaelbeijer/beijerterm`).
2. Build settings:
   - Framework preset: **Astro**
   - Build command: `npm run build`
   - Output directory: `dist`
3. **Environment variables** → add `PUBLIC_WORDBOOK_API` =
   `https://wordbook-search.<subdomain>.workers.dev` (the deployed Worker URL).
   If unset, the page shows "Search API not configured" and ships no data.
4. **Custom domains** → add `beijerdictionary.com` (and `www.beijerdictionary.com`).
   This replaces the old MediaWiki origin — decommission it once the new site
   is verified live.

`public/_redirects` 301s the old indexed `/home` URL onto the clean root `/`,
preserving its search equity.

## Updating content

The site is static; the searchable data is refreshed independently by
reloading Cloudflare D1 from the private `wordbook` repo
(`wordbook build-d1` → `wrangler d1 execute`). No rebuild of this site is
needed when the data changes.
