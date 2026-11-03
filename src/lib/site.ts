import dataset from '../data/seo_pages.json';

/** Canonical origin, from `site` in astro.config.mjs (no trailing slash). */
export const SITE_URL = (import.meta.env.SITE || 'https://ukcleaningplatform.co.uk').replace(/\/$/, '');

/** Lead-capture endpoint already used by /quote (Cloudflare Worker form hub). */
export const LEAD_ENDPOINT =
  'https://roamglade-form-hub.dwx168200.workers.dev/api/form?service=cleaning&list_id=10&inbox_id=wSE3K4odsBvsv6gYzeLTh9et';

export type Lang = 'en' | 'zh-cn' | 'zh-tw';
export const ALL_LANGS: Lang[] = ['en', 'zh-cn', 'zh-tw'];

export const toSlug = (name: string) => name.toLowerCase().replace(/ /g, '-');

/** Absolute URL for a site path, never with a trailing slash (except the root). */
export function absUrl(path: string): string {
  const clean = path === '/' ? '/' : path.replace(/\/+$/, '');
  return `${SITE_URL}${clean}`;
}

/** Prefix a language-neutral path (`/oven-cleaning`) with the language segment. */
export function langPath(lang: Lang, path: string): string {
  if (lang === 'en') return path || '/';
  return path === '/' || path === '' ? `/${lang}` : `/${lang}${path}`;
}

/** City slugs that have a generated page, so links never point at missing pages. */
export const CITY_SLUGS = new Set(dataset.map((item) => toSlug(item.city.name)));
