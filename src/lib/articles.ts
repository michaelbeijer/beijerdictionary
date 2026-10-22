// Build-time fetch of the Beijerterm terminology-article feed from beijer.ink.
//
// Articles are hand-written in beijer.ink and published via its token-gated
// feed (GET /api/publish/beijerterm?token=). This module fetches that feed at
// BUILD time only — the token is a non-public env var, never shipped to the
// browser. Every page that needs articles imports getArticles(); ESM module
// state means the feed is fetched once per build and reused.
//
// If the feed can't be read or comes back empty, the build uses the saved copy
// in src/data/articles.json instead: the feed as it stood on 22 Oct 2026, taken
// from the live site when beijer.ink went offline. A build that can't reach
// beijer.ink therefore still ships every article, rather than none.
//
// Build env vars (both optional now that the saved copy exists):
//   BEIJERTERM_EXPORT_TOKEN  — must equal the beijer.ink server's token
//   BEIJER_INK_URL           — optional, defaults to https://beijer.ink

import savedFeed from '../data/articles.json';

export interface BeijertermArticle {
	slug: string;
	title: string;
	headword: string;
	aliases: string[];
	lang: string;
	domain: string;
	order: number;
	html: string;
	updatedAt: string;
}

// Compact per-article record shipped to the browser for client-side search
// (no full body — bodies live on their own /article/<slug> pages).
export interface ArticleIndexItem {
	slug: string;
	title: string;
	headword: string;
	aliases: string[];
	lang: string;
	domain: string;
	excerpt: string;
}

// Build-time env. Prefer import.meta.env (loaded from .env files for local dev),
// fall back to process.env (how Cloudflare Pages provides build environment
// variables). Non-public, so never inlined into the client bundle.
function readEnv(key: string): string {
	const im = (import.meta as any).env?.[key];
	if (im) return String(im);
	if (typeof process !== 'undefined' && process.env && process.env[key]) {
		return String(process.env[key]);
	}
	return '';
}

const FEED_BASE = (readEnv('BEIJER_INK_URL') || 'https://beijer.ink').replace(/\/$/, '');
const TOKEN = readEnv('BEIJERTERM_EXPORT_TOKEN');

const SAVED = savedFeed as BeijertermArticle[];

let cache: BeijertermArticle[] | null = null;

export async function getArticles(): Promise<BeijertermArticle[]> {
	if (cache) return cache;
	const live = await fetchFeed();
	if (live.length) {
		cache = live;
	} else {
		console.warn(`[articles] building from the saved copy (${SAVED.length} articles).`);
		cache = SAVED;
	}
	return cache;
}

// The live feed, or [] when there is no token or beijer.ink can't be read.
async function fetchFeed(): Promise<BeijertermArticle[]> {
	if (!TOKEN) return [];
	try {
		const res = await fetch(
			`${FEED_BASE}/api/publish/beijerterm?token=${encodeURIComponent(TOKEN)}`
		);
		if (!res.ok) {
			console.warn(`[articles] feed returned ${res.status}.`);
			return [];
		}
		const data = await res.json();
		return Array.isArray(data) ? (data as BeijertermArticle[]) : [];
	} catch (e) {
		console.warn('[articles] feed fetch failed.', e);
		return [];
	}
}

// Plain-text teaser from an article's HTML body, for the search-result card
// and the page's meta description.
export function excerpt(html: string, max = 160): string {
	const text = (html || '')
		.replace(/<[^>]+>/g, ' ')
		.replace(/&[a-z]+;/gi, ' ')
		.replace(/\s+/g, ' ')
		.trim();
	if (text.length <= max) return text;
	return text.slice(0, max).replace(/\s+\S*$/, '') + '…';
}

// beijer.ink derives a note's title from its first block, but the block stays
// in the body — so rendering title-as-H1 plus the body repeats the heading.
// Drop the leading block when its text matches the title (mirrors how
// autofingers de-duplicates). The H1 (article.title) is the single heading;
// everything after it is the body.
export function stripLeadingTitle(html: string, title: string): string {
	if (!html || !title) return html || '';
	const m = html.match(/^\s*<(h[1-6]|p)\b[^>]*>([\s\S]*?)<\/\1>\s*/i);
	if (!m) return html;
	const text = m[2]
		.replace(/<[^>]+>/g, '')
		.replace(/&[a-z]+;/gi, ' ')
		.replace(/\s+/g, ' ')
		.trim();
	if (text.toLowerCase() === title.trim().toLowerCase()) {
		return html.slice(m[0].length);
	}
	return html;
}

export function toIndexItem(a: BeijertermArticle): ArticleIndexItem {
	return {
		slug: a.slug,
		title: a.title,
		headword: a.headword,
		aliases: a.aliases || [],
		lang: a.lang,
		domain: a.domain,
		excerpt: excerpt(stripLeadingTitle(a.html, a.title)),
	};
}
