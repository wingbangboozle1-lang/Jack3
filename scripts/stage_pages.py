"""Create an explicit, minimal Pages artifact; do not publish legacy research."""
from pathlib import Path
import shutil

root = Path(__file__).resolve().parent.parent
out = root / '_pages_artifact'
if out.exists():
    shutil.rmtree(out)
out.mkdir()
for name in ('index.html', 'economy.html', 'demographics.html', 'tenant.html', 'risk.html',
             'place.html', 'schools.html', 'decisions.html', 'taxes.html', 'model.html',
             'review.html', 'sources.html'):
    shutil.copy2(root / name, out / name)
(out / 'assets').mkdir()
shutil.copy2(root / 'assets/style.css', out / 'assets/style.css')
if (root / 'dashboard').is_dir():
    shutil.copytree(root / 'dashboard', out / 'dashboard')
print('Staged', len(list(out.rglob('*'))), 'entries in', out)

# Validate the actual artifact, not just the repository checkout. Relative links
# must resolve inside the artifact, and each body row needs a recognized source.
import json
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
sources = {s['url'] for s in json.loads((root / 'data/evidence.json').read_text())['sources'].values()}
if (root / '_dashboard_src/dataset.json').is_file():
    sources |= {s['url'] for s in json.loads((root / '_dashboard_src/dataset.json').read_text())['sources'].values()}
class Check(HTMLParser):
    def __init__(self, page):
        super().__init__(); self.page = page; self.row = None; self.body = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'tbody': self.body = True
        if tag == 'tr' and self.body: self.row = []
        if tag in ('a', 'link'):
            href = a.get('href', '')
            if href.startswith('https://'):
                if self.row is not None: self.row.append(href)
            elif href and not href.startswith('#'):
                assert not urlparse(href).scheme, (self.page, href)
                target = (self.page.parent / unquote(urlparse(href).path)).resolve()
                assert target.is_relative_to(out.resolve()) and target.is_file(), (self.page, href)
    def handle_endtag(self, tag):
        if tag == 'tr' and self.row is not None:
            assert any(x in sources for x in self.row), (self.page, self.row)
            self.row = None
        if tag == 'tbody': self.body = False
for page in sorted(out.rglob('*.html')):
    Check(page).feed(page.read_text())
print('PASS: staged HTML links and source-linked table rows')

# CI also supplies GitHub Pages' own Jekyll output. Reject unexpected or
# missing public files and ensure Jekyll preserved the curated contents.
import sys
if len(sys.argv) > 1:
    actual = Path(sys.argv[1]).resolve()
    expected = {p.relative_to(out) for p in out.rglob('*') if p.is_file()}
    found = {p.relative_to(actual) for p in actual.rglob('*') if p.is_file()}
    if found != expected:
        message = f"unexpected Jekyll files: {sorted(map(str, found-expected))}; missing: {sorted(map(str, expected-found))}"
        print("::error title=Jekyll artifact mismatch::" + message)
        raise SystemExit(message)
    for rel in expected:
        if (out / rel).read_bytes() != (actual / rel).read_bytes():
            print(f"::error title=Jekyll content mismatch::content changed: {rel}")
            raise SystemExit(1)
    print('PASS: actual Jekyll output matches curated artifact')
