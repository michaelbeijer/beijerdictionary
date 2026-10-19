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
 * lookups.
 */
export const GET: APIRoute = async ({ site }) => {
	const base = (site?.href ?? 'https://beijerdictionary.com/').replace(/\/$/, '');
	const articles = await getArticles();

	const lines = [
		'# Beijer Dictionary',
		'',
		"> Michael Beijer's Dutch–English terminology site: a searchable database",
		'> of ~1.9 million term pairs from 27 glossaries and termbases, built over',
		'> 30+ years of patent and technical translation.',
		'',
		'The termbase is searched live at the site (client-side, backed by an API);',
		'individual term pages are not static, so crawling the site yields only the',
		'shell. For terminology content, use the curated sample below or the search',
		`at ${base}/.`,
		'',
		'## Terminology',
		'',
		`- [Curated terminology sample](${base}/llms-terms.txt): ~1,100 term pairs from Michael's own dictionary and permissively licensed sources, plus a full source catalogue with entry counts`,
		'',
		'## Pages',
		'',
		`- [Home / search](${base}/): live terminology search`,
		`- [About](${base}/about/): what Beijer Dictionary is and who makes it`,
		`- [Sources](${base}/sources): the glossaries and termbases indexed, with publication metadata`,
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
