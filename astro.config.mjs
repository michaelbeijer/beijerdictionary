// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Static output (default) → dist/ → Cloudflare Pages.
// `site` is required for @astrojs/sitemap to emit absolute URLs; the integration
// generates sitemap-index.xml + sitemap-0.xml at build time (referenced by
// public/robots.txt).
export default defineConfig({
	site: 'https://beijerdictionary.com',
	integrations: [sitemap()],
});
