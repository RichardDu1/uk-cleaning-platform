import dataset from '../data/seo_pages.json';

/** Canonical origin, from `site` in astro.config.mjs (no trailing slash). */
export const SITE_URL = (import.meta.env.SITE || 'https://ukcleaningplatform.co.uk').replace(/\/$/, '');

/** Highland Travel group form system: JSON POST, CORS open, source site recorded from Origin. */
export const FORM_ENDPOINT = 'https://form.highland-travel.com';

/** Shown when a form submission fails (the site-wide WeChat ID). */
export const FALLBACK_WECHAT = 'ukclean_london';

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
