import type { APIRoute } from 'astro';
import { getArticles } from '../lib/articles';

/**
 * llms.txt — machine-readable site index for AI agents
 * (https://llmstxt.org/). Generated at build time.
 *
 * The searchable termbase itself is served client-side from the Wordbook
 * API and is NOT crawlable as pages, so this file points agents at the
 * curated sample in /llms-terms.txt (a committed static file regenerated
 * by scripts/generate-llms-terms.py) and at the live search for real
 * lookups. The numbers in its description come from the API's /meta at
 * build time, like the Sources page; if the API can't be reached, the
 * description is written without them.
 */
const apiBase = (
	import.meta.env.PUBLIC_WORDBOOK_API ||
	(import.meta.env.DEV ? 'http://127.0.0.1:8787' : '')
).replace(/\/$/, '');

async function fetchCounts() {
	if (!apiBase) return null;
	try {
		const res = await fetch(apiBase + '/meta');
		if (!res.ok) return null;
		const { counts } = await res.json();
		return counts?.entries && counts?.concepts && counts?.sources ? counts : null;
	} catch {
		return null;
	}
}

export const GET: APIRoute = async ({ site }) => {
	const base = (site?.href ?? 'https://beijerdictionary.com/').replace(/\/$/, '');
	const [articles, counts] = await Promise.all([getArticles(), fetchCounts()]);
	const n = (x: number) => x.toLocaleString('en');

	const lines = [
		'# Beijer Dictionary',
		'',
		"> Michael Beijer's multilingual terminology site for technical translators,",
		...(counts
			? [
					`> Dutch–English at heart: ${n(counts.entries)} term pairs and ${n(counts.concepts)}`,
					`> multilingual concepts from ${counts.sources} glossaries, termbases and EU`,
					'> vocabularies, in English, Dutch, German, French, Italian and Spanish,',
				]
			: [
					'> Dutch–English at heart: term pairs and multilingual concepts from',
					'> glossaries, termbases and EU vocabularies, in English, Dutch, German,',
					'> French, Italian and Spanish,',
				]),
		'> built over 30+ years of patent and technical translation. Searches between',
		'> any two of those six languages also show sentences from EU legislation',
		'> beside their official translations.',
		'',
		'The termbase is searched live at the site (client-side, backed by an API);',
		'individual term pages are not static, so crawling the site yields only the',
		'shell. For terminology content, use the curated sample below or the search',
		`at ${base}/. A link such as ${base}/?q=tegels&from=nl&to=en opens a search.`,
		'',
		'## Terminology',
		'',
		`- [Curated terminology sample](${base}/llms-terms.txt): about 1,000 term pairs from Michael's own dictionary, plus a catalogue of every source with its counts`,
		'',
		'## Pages',
		'',
		`- [Home / search](${base}/): live terminology search`,
		`- [About](${base}/about/): what Beijer Dictionary is and who makes it`,
		`- [Sources](${base}/sources/): the glossaries and termbases indexed, with publication metadata`,
		`- [Articles](${base}/articles/): terminology articles`,
		...articles.map(
			(a) => `- [${a.title}](${base}/articles/${a.slug}/): terminology article on "${a.headword}"`
		),
		'',
		'## Optional',
		'',
		'- [beijer.uk](https://beijer.uk/llms.txt): Michael Beijer\'s personal site',
		'- [Supervertaler docs](https://docs.supervertaler.com/llms.txt): AI-readable docs for the Supervertaler translation tools',
		'',
	];

	return new Response(lines.join('\n'), {
		headers: { 'Content-Type': 'text/plain; charset=utf-8' },
	});
};
