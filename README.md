# Beijer Dictionary

The public, canonical site for **Beijer Dictionary** — a curated, searchable
multilingual terminology database for technical translators
(Dutch ↔ English and more), at **BeijerDictionary.com**.

Until October 2026 the site was called Beijerterm, at beijerterm.com, which now
redirects here. The GitHub repo is now `beijerdictionary`; the Cloudflare
Worker, the local folder and code names keep the old name on purpose.

This repo is **software only**. The terminology data is private: it lives in
the separate private `wordbook` repo (the curation pipeline + SQLite master
store) and in a Cloudflare D1 database. This site calls a Cloudflare Worker
search API and only ever receives **per-query result snippets** — never the
bulk dataset.

```
beijerdictionary.com (this site: static Astro build, served by the
      │                "beijerterm" Cloudflare Worker as static assets)
      │  GET /meta, /search   (fetch)
      ▼
  Worker "wordbook-search"   (in the beijer.uk repo's worker/ dir)
      ▼
  D1 "wordbook"              (loaded from the private wordbook repo)
```

beijer.uk hosts a lighter hand-off search box that links here; this is the
canonical home (see `rel=canonical`). Supervertaler's Superlookup calls the
same Worker API.

## The site

Four pages, linked from the menu in the header (`src/layouts/Base.astro`):

- **Search** (`/`, `src/pages/index.astro`): the search box and result
  cards. Results come from the Worker per query; nothing is shipped in bulk.
  `?q=…&from=nl&to=en` runs a search on load (how Superlookup embeds it).
- **Articles** (`/articles/`): hand-written terminology articles, fetched
  from beijer.ink's feed **at build time** (`src/lib/articles.ts`), each with
  its own page. Matching articles also appear at the top of search results.
- **Sources** (`/sources/`, `src/components/SourcesTable.astro`): every
  source with its metadata, built from the Worker's `/meta` at build time and
  refreshed in the browser, so a data reload shows without a rebuild.
- **About** (`/about/`): how the dictionary works.

Notable changes are listed in [CHANGELOG.md](CHANGELOG.md).

## Local development

```bash
npm install
npm run dev        # http://localhost:4321
```

In dev the front-end targets a local Worker on `http://127.0.0.1:8787`
(run `wrangler dev` in the beijer.uk `worker/` dir, with a local D1 loaded).
Without it, the page shows "Search API not configured" — it never ships data.
To work against the live data instead, point it at the deployed Worker:

```bash
PUBLIC_WORDBOOK_API=https://wordbook-search.<subdomain>.workers.dev npm run dev
```

The Articles pages read the beijer.ink feed when `BEIJERTERM_EXPORT_TOKEN`
(the feed token) is set in a git-ignored `.env`. Without it, or when beijer.ink
can't be reached, the build uses the saved copy in `src/data/articles.json`
(the feed as of 22 Oct 2026, when beijer.ink went offline).

## Deploy

Pushing to `main` deploys. The repo is connected to **Cloudflare Workers
Builds**, which runs `npm run build` and `npx wrangler deploy`; `wrangler.toml`
uploads `dist/` as the static assets of the `beijerterm` Worker, which serves
beijerdictionary.com (and www). The build needs these variables in the
Worker's build settings:

- `PUBLIC_WORDBOOK_API` = `https://wordbook-search.<subdomain>.workers.dev`
  (the search Worker). If unset, the page shows "Search API not configured"
  and ships no data.
- `BEIJERTERM_EXPORT_TOKEN`, for the articles (optionally `BEIJER_INK_URL`,
  default `https://beijer.ink`).

`public/_redirects` 301s the old indexed `/home` URL onto the clean root `/`,
preserving its search equity.

## Updating content

The searchable data is refreshed independently of this site, by publishing
to Cloudflare D1 from the private `wordbook` repo (its admin app's *Publish to
live D1*). No rebuild of this site is needed when the data changes. New or
edited articles do need a rebuild, since they're fetched at build time.
