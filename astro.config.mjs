import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

// Canonical origin used for canonical/hreflang/sitemap/JSON-LD/llms.txt.
// Override with SITE_URL (e.g. the pages.dev host) until the custom domain resolves.
const SITE_URL = (process.env.SITE_URL || 'https://ukcleaningplatform.co.uk').replace(/\/$/, '');

// Pages that must not be submitted to search engines.
const SITEMAP_EXCLUDE = ['/404', '/reviews'];

// https://astro.build/config
export default defineConfig({
  site: SITE_URL,
  // Cloudflare Pages 308-redirects `/x` to `/x/` for directory-style output.
  // `file` output (`/x.html`) is served at `/x` with a 200, matching canonicals.
  trailingSlash: 'never',
  build: { format: 'file' },
  integrations: [
    tailwind(),
    sitemap({
      filter: (page) => {
        const path = new URL(page).pathname.replace(/\/$/, '');
        return !SITEMAP_EXCLUDE.includes(path);
      },
      // Strip any trailing slash so sitemap URLs equal canonical URLs.
      serialize: (item) => {
        const url = new URL(item.url);
        if (url.pathname !== '/') url.pathname = url.pathname.replace(/\/$/, '');
        item.url = url.href;
        return item;
      },
    }),
  ],
  output: 'static',
});
