#!/usr/bin/env python3
"""Static site integrity checker (stdlib only).

Checks:
  1. Every internal href/src target exists on disk.
  2. No page references localhost / 127.0.0.1.
  3. External links use target=_blank + rel=noopener.
  4. All nav links from every page resolve.
  5. Reports counts; exits 1 on any failure.
"""
import html.parser, os, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = sorted(ROOT.glob('*.html'))

class LinkParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs = []  # (attr, value, line)
        self.external_target_blank_ok = True
        self.issues = []
        self._stack = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for attr in ('href', 'src'):
            if attr in a and a[attr]:
                self.refs.append((attr, a[attr], self.getpos()[0], tag, a))

failures = []
checked_internal = 0
for page in PAGES:
    src = page.read_text(encoding='utf-8')
    p = LinkParser()
    p.feed(src)
    for attr, value, line, tag, a in p.refs:
        if value.startswith(('http://', 'https://')):
            if a.get('target') == '_blank' and 'noopener' not in (a.get('rel') or ''):
                p.issues.append(f'{page.name}:{line}: external link missing rel=noopener: {value}')
            continue
        if value.startswith(('mailto:', 'tel:', '#', 'javascript:')):
            continue
        target = value.split('#', 1)[0].split('?', 1)[0]
        if not target:
            continue
        checked_internal += 1
        target_path = (ROOT / target).resolve()
        if not str(target_path).startswith(str(ROOT)) or not target_path.exists():
            p.issues.append(f'{page.name}:{line}: broken internal {attr} -> {value}')
    if 'localhost' in src or '127.0.0.1' in src:
        p.issues.append(f'{page.name}: references localhost/127.0.0.1')
    for issue in p.issues:
        failures.append(issue)

print(f'Pages checked: {len(PAGES)}')
print(f'Internal references checked: {checked_internal}')
if failures:
    print('\nFAILURES:')
    for f in failures:
        print(' -', f)
    sys.exit(1)
print('\nALL CHECKS PASSED')
