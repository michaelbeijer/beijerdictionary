// Build-time fetch of the Beijerterm terminology-article feed from beijer.ink.
//
// Articles are hand-written in beijer.ink and published via its token-gated
// feed (GET /api/publish/beijerterm?token=). This module fetches that feed at
// BUILD time only — the token is a non-public env var, never shipped to the
// browser. Every page that needs articles imports getArticles(); ESM module
// state means the feed is fetched once per build and reused.
//
// Everything degrades to an empty list on any failure, so a build that can't
// reach beijer.ink still succeeds (just with no article pages).
//
// Required build env vars:
//   BEIJERTERM_EXPORT_TOKEN  — must equal the beijer.ink server's token
//   BEIJER_INK_URL           — optional, defaults to https://beijer.ink

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

let cache: BeijertermArticle[] | null = null;

export async function getArticles(): Promise<BeijertermArticle[]> {
	if (cache) return cache;
	if (!TOKEN) {
		cache = [];
		return cache;
	}
	try {
		const res = await fetch(
			`${FEED_BASE}/api/publish/beijerterm?token=${encodeURIComponent(TOKEN)}`
		);
		if (!res.ok) {
			console.warn(`[articles] feed returned ${res.status}; building with no articles.`);
			cache = [];
			return cache;
		}
		const data = await res.json();
		cache = Array.isArray(data) ? (data as BeijertermArticle[]) : [];
	} catch (e) {
		console.warn('[articles] feed fetch failed; building with no articles.', e);
		cache = [];
	}
	return cache;
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
