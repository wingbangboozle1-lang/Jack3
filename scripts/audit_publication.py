"""Idempotent, dependency-free evidence-boundary notices for all public HTML."""
from pathlib import Path
import re
import os

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- publication-audit:start -->'
END = '<!-- publication-audit:end -->'

def apply():
    count = 0
    for path in ROOT.rglob('*.html'):
        if any(p.startswith('.') or p in {'node_modules', 'private', 'pii', 'scratch'} for p in path.relative_to(ROOT).parts):
            continue
        text = path.read_text()
        text = re.sub(re.escape(START) + r'.*?' + re.escape(END), '', text, flags=re.S)
        target = os.path.relpath(ROOT / 'audit/index.html', path.parent).replace(os.sep, '/')
        banner = (START + '<section aria-label="Publication audit" style="position:relative;z-index:20;'
                  'background:#fff4cf;color:#322600;padding:14px 20px;border-bottom:2px solid #aa7a12;'
                  'font:15px/1.6 system-ui,sans-serif">'
                  '<strong>Evidence boundary · 7 November 2026.</strong> '
                  'No verified property valuation or personalized sell/renew ranking is available. '
                  'Companion model outputs and risk scores are illustrative assumptions, not official forecasts. '
                  f'<a style="color:#443000;text-decoration:underline" href="{target}">'
                  'Executive audit &amp; Flagged for Review</a>.</section>' + END)
        text, n = re.subn(r'(<body\b[^>]*>)', lambda m: m[0] + banner, text, count=1, flags=re.I)
        if n:
            path.write_text(text)
            count += 1
    return count

if __name__ == '__main__':
    print(f'Publication notices applied to {apply()} pages')

def check():
    from html.parser import HTMLParser
    from urllib.parse import urlsplit, unquote
    class Page(HTMLParser):
        def __init__(self):
            super().__init__()
            self.links = []
            self.ids = set()
        def handle_starttag(self, tag, attrs):
            a = dict(attrs)
            if 'id' in a:
                self.ids.add(a['id'])
            if tag in ('a', 'link', 'script', 'img'):
                self.links.append(a.get('href', a.get('src', '')))
    pages = {}
    for path in ROOT.rglob('*.html'):
        if any(p.startswith('.') for p in path.relative_to(ROOT).parts):
            continue
        text = path.read_text()
        assert text.count(START) == 1, (path, 'missing/duplicate audit notice')
        page = Page()
        page.feed(text)
        pages[path.resolve()] = page
    for path, page in pages.items():
        for url in page.links:
            u = urlsplit(url)
            if not url or u.scheme or u.netloc:
                continue
            target = (path.parent / unquote(u.path)).resolve() if u.path else path
            if target.is_dir():
                target /= 'index.html'
            assert target.exists(), (path, url)
            if u.fragment and target in pages:
                assert unquote(u.fragment) in pages[target].ids, (path, url, 'anchor')
    print(f'PASS: {len(pages)} public pages; notices, local references and anchors')

if __name__ == '__main__':
    check()
