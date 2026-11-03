#!/usr/bin/env python3
"""Audit a built Astro `dist/` directory for technical SEO problems.

Usage: python3 scripts/audit_dist.py [dist_dir] [--site https://example.com]

Checks every HTML page for: exactly one <title>/canonical/description,
canonical == the page's own clean URL, duplicate titles/descriptions,
JSON-LD that parses, fabricated-looking schema fields, hreflang targets that
exist, and internal links that do not resolve to a built page or file.
Exits non-zero when a hard error is found.
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

args = [a for a in sys.argv[1:] if not a.startswith('--')]
DIST = os.path.abspath(args[0] if args else 'dist')
SITE = 'https://ukcleaningplatform.co.uk'
if '--site' in sys.argv:
    SITE = sys.argv[sys.argv.index('--site') + 1].rstrip('/')


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.titles, self.canonicals, self.descs, self.hreflangs = [], [], [], []
        self.links, self.jsonld, self.h1 = [], [], 0
        self.robots = []
        self._in_title = self._in_ld = False
        self._buf = ''
        self._in_head = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'head':
            self._in_head = True
        if tag == 'title':
            self._in_title, self._buf = True, ''
            self.titles.append(('head' if self._in_head else 'body', None))
        elif tag == 'link' and a.get('rel') == 'canonical':
            self.canonicals.append(a.get('href'))
        elif tag == 'link' and a.get('rel') == 'alternate' and a.get('hreflang'):
            self.hreflangs.append((a['hreflang'], a.get('href')))
        elif tag == 'meta' and a.get('name') == 'description':
            self.descs.append(a.get('content') or '')
        elif tag == 'meta' and a.get('name') == 'robots':
            self.robots.append(a.get('content') or '')
        elif tag == 'a' and a.get('href'):
            self.links.append(a['href'])
        elif tag == 'form' and a.get('action'):
            self.links.append(a['action'])
        elif tag == 'script' and a.get('type') == 'application/ld+json':
            self._in_ld, self._buf = True, ''
        elif tag == 'h1':
            self.h1 += 1

    def handle_endtag(self, tag):
        if tag == 'head':
            self._in_head = False
        if tag == 'title' and self._in_title:
            self._in_title = False
            where, _ = self.titles[-1]
            self.titles[-1] = (where, self._buf.strip())
        if tag == 'script' and self._in_ld:
            self._in_ld = False
            self.jsonld.append(self._buf)

    def handle_data(self, data):
        if self._in_title or self._in_ld:
            self._buf += data


def page_url(rel):
    """Map a dist-relative file path to the clean public URL path."""
    p = '/' + rel.replace(os.sep, '/')
    if p.endswith('/index.html'):
        p = p[: -len('index.html')]
    elif p.endswith('.html'):
        p = p[: -len('.html')]
    if p != '/' and p.endswith('/'):
        p = p[:-1]
    return p


files, pages = set(), {}
for root, _, names in os.walk(DIST):
    for n in names:
        rel = os.path.relpath(os.path.join(root, n), DIST)
        files.add('/' + rel.replace(os.sep, '/'))
        if n.endswith('.html'):
            pages[page_url(rel)] = rel

errors, warnings = defaultdict(list), defaultdict(list)
title_map, desc_map = defaultdict(list), defaultdict(list)
dead = Counter()
dead_examples = {}
sizes = []
FAKE_KEYS = ('aggregateRating', 'review', 'telephone', 'address')


def resolves(path):
    path = path.split('#')[0].split('?')[0]
    if path in ('', '/'):
        return '/' in pages
    if path in files:
        return True
    clean = path.rstrip('/')
    return clean in pages


def walk_ld(node, found):
    if isinstance(node, dict):
        for k, v in node.items():
            if k in FAKE_KEYS:
                found.add(k)
            walk_ld(v, found)
    elif isinstance(node, list):
        for v in node:
            walk_ld(v, found)


for url, rel in sorted(pages.items()):
    if url == '/404':
        continue
    html = open(os.path.join(DIST, rel), encoding='utf-8').read()
    sizes.append((len(html.encode()), url))
    p = PageParser()
    p.feed(html)
    if len(p.titles) != 1:
        errors['title_count'].append(f'{url} ({len(p.titles)})')
    elif p.titles[0][0] != 'head':
        errors['title_in_body'].append(url)
    if len(p.canonicals) != 1:
        errors['canonical_count'].append(f'{url} ({len(p.canonicals)})')
    elif p.canonicals[0] != SITE + (url if url != '/' else '/'):
        errors['canonical_mismatch'].append(f'{url} -> {p.canonicals[0]}')
    if len(p.descs) != 1:
        errors['description_count'].append(f'{url} ({len(p.descs)})')
    if p.h1 != 1:
        warnings['h1_count'].append(f'{url} ({p.h1})')
    for t in p.titles:
        title_map[t[1]].append(url)
    for d in p.descs:
        desc_map[d].append(url)
        if len(d) > 170:
            warnings['description_too_long'].append(f'{url} ({len(d)})')
    for lang, href in p.hreflangs:
        u = urlparse(href or '')
        if href and href.startswith(SITE) and not resolves(u.path):
            errors['hreflang_dead'].append(f'{url} [{lang}] -> {u.path}')
    for raw in p.jsonld:
        try:
            data = json.loads(raw)
        except Exception as e:  # noqa: BLE001
            errors['jsonld_invalid'].append(f'{url}: {e}')
            continue
        found = set()
        walk_ld(data, found)
        for k in found:
            warnings[f'schema_has_{k}'].append(url)
    for href in p.links:
        if href.startswith(('mailto:', 'tel:', 'javascript:', '#', 'weixin:')):
            continue
        absu = urljoin(SITE + url + ('/' if url == '/' else ''), href)
        u = urlparse(absu)
        if f'{u.scheme}://{u.netloc}' != SITE:
            continue
        if u.path.endswith('/') and u.path != '/':
            warnings['trailing_slash_link'].append(f'{url} -> {u.path}')
        if not resolves(u.path):
            dead[u.path] += 1
            dead_examples.setdefault(u.path, url)

for t, us in title_map.items():
    if len(us) > 1:
        errors['duplicate_title'].append(f'{t!r} x{len(us)} e.g. {us[:3]}')
for d, us in desc_map.items():
    if len(us) > 1:
        warnings['duplicate_description'].append(f'{d[:80]!r} x{len(us)} e.g. {us[:3]}')
for path, n in dead.most_common():
    errors['dead_internal_link'].append(f'{path} (x{n}, e.g. on {dead_examples[path]})')

print(f'Pages audited: {len(sizes)} (dist: {DIST})')
sizes.sort(reverse=True)
print('Largest pages:', ', '.join(f'{u} {s // 1024}KB' for s, u in sizes[:3]))
print(f'Distinct dead internal paths: {len(dead)}; total dead link occurrences: {sum(dead.values())}')
for label, bucket in (('ERROR', errors), ('WARN', warnings)):
    for k, v in sorted(bucket.items()):
        print(f'[{label}] {k}: {len(v)}')
        for line in (v if os.environ.get("FULL") else v[:5]):
            print('    ', line)
sys.exit(1 if errors else 0)
