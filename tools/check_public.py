#!/usr/bin/env python3
"""Integrity checks for the actual public artifact (stdlib only, no network).

Runs against `_pages_artifact`, the exact directory GitHub Pages publishes, so a
page that is broken only in the published set cannot pass. Every rule below is a
claim this project makes on its own pages; the checker exists so the claim is
tested rather than asserted.

CHECKS
  1  every page in the artifact is in the allow-list (no stray or research file)
  2  every local link/asset inside the artifact resolves
  3  every external link is https and on an official / primary domain
  4  every *body* table row links to a registered source URL
  5  an "Unverified" row never carries a value in its value column
  6  the artifact contains no personal data (see PERSONAL_PATTERNS)
  7  the artifact contains no tracking, embed or form machinery
  8  every source registered in data/evidence.json is referenced somewhere
  9  every open question and answered question links a registered source

Exit code 0 = all checks pass. Any failure prints a ::error:: line (GitHub
Actions annotation) and exits 1.
"""
from __future__ import annotations

import html as htmllib
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / '_pages_artifact'
DATA = json.loads((ROOT / 'data/evidence.json').read_text())

EXPECTED = {
    'index.html', 'economy.html', 'demographics.html', 'tenant.html', 'risk.html',
    'place.html', 'schools.html', 'decisions.html', 'taxes.html', 'model.html',
    'review.html', 'questions.html', 'sources.html',
    'assets/style.css',
}

ALLOWED_HOSTS = {
    'www.bls.gov', 'www.census.gov', 'fred.stlouisfed.org', 'www.dir.ca.gov',
    'www.ftb.ca.gov', 'www.irs.gov', 'assessor.lacounty.gov', 'www.lavote.gov',
    'finance.lacity.gov', 'lacounty.gov', 'dof.ca.gov', 'www.cde.ca.gov',
    'dq.cde.ca.gov', 'www.caschooldashboard.org', 'sustain.scag.ca.gov',
    'www.conservation.ca.gov', 'msc.fema.gov', 'osfm.fire.ca.gov',
    'www.fire.ca.gov', 'pubs.usgs.gov', 'zimas.lacity.org', 'thesource.metro.net',
    'investors.jackinthebox.com',
}

PROHIBITED = (
    '<script', '<iframe', '<form', 'googletagmanager', 'google-analytics',
    'doubleclick', 'facebook.net', 'hotjar', 'segment.io', 'localhost',
    '127.0.0.1', 'mailto:',
)

# Personal-information patterns. Conservative: a hit is a failure to justify.
PERSONAL_PATTERNS = (
    (re.compile(r'[\w.+-]+@[\w-]+\.[\w.]+'), 'email address'),
    (re.compile(r'\(\d{3}\)\s*\d{3}-\d{4}'), 'telephone number'),
    (re.compile(r'\b\d{4}[ -]\d{2}[ -]\d{4}\b'), 'SSN-like identifier'),
    (re.compile(r'\b\d{3}-\d{3}-\d{3}\b'), 'parcel/APN-like identifier'),
    (re.compile(r'\bAIN\b|\bAPN\b'), 'parcel identifier label'),
)


class Rows(HTMLParser):
    """Collect table headers, body rows and their link hrefs (per table)."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.body = False
        self.head = False
        self.row = None
        self.header: list[str] = []
        self.rows: list[list[str]] = []
        self.cell: list[str] | None = None
        self.in_th = False
        self.th: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'thead':
            self.head = True
        if tag == 'tbody':
            self.body = True
        if tag == 'tr' and self.body:
            self.row = []
        if tag == 'th' and self.head:
            self.in_th = True
            self.th = []
        if tag == 'td' and self.row is not None:
            self.cell = []
        if tag == 'a' and self.row is not None:
            self.row.append(a.get('href', ''))

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if tag == 'td' and self.cell is not None:
            self.row.append(''.join(self.cell))
            self.cell = None
        if tag == 'th' and self.in_th:
            self.header.append(''.join(self.th).strip())
            self.in_th = False
        if tag == 'tr' and self.row is not None:
            self.rows.append(self.row)
            self.row = None
        if tag == 'thead':
            self.head = False
        if tag == 'tbody':
            self.body = False


def main() -> int:
    failures: list[str] = []
    if not ART.is_dir():
        print('::error::artifact directory missing - run scripts/stage_pages.py first')
        return 1

    # 1. exact file set
    actual = {str(p.relative_to(ART)) for p in ART.rglob('*') if p.is_file()}
    if actual != EXPECTED:
        failures.append(f'CHECK 1 file set mismatch: extra={sorted(actual - EXPECTED)} '
                        f'missing={sorted(EXPECTED - actual)}')

    registered = {s['url'] for s in DATA['sources'].values()}
    pages = sorted(ART.glob('*.html'))
    internal = external = rows_checked = 0

    for page in pages:
        text = page.read_text()

        # 2/3. links
        for m in re.finditer(r'(?:href|src)\s*=\s*"([^"]*)"', text):
            link = m.group(1)
            if not link:
                failures.append(f'{page.name}: empty href')
                continue
            if link.startswith(('#', 'javascript:')):
                continue
            if link.startswith('http://'):
                failures.append(f'{page.name}: insecure external link {link}')
                continue
            if link.startswith('https://'):
                external += 1
                host = urlparse(link).netloc
                if host not in ALLOWED_HOSTS:
                    failures.append(f'{page.name}: link to non-official host {host}')
                continue
            internal += 1
            target = (page.parent / unquote(urlparse(link).path)).resolve()
            if not (target.is_relative_to(ART.resolve()) and target.is_file()):
                failures.append(f'{page.name}: broken internal link {link}')

        # 7. prohibited machinery
        low = text.lower()
        for bad in PROHIBITED:
            if bad in low:
                failures.append(f'{page.name}: prohibited content {bad!r}')

        # 6. personal data
        for pattern, label in PERSONAL_PATTERNS:
            hit = pattern.search(text)
            if hit:
                failures.append(f'{page.name}: possible {label}: {hit.group(0)!r}')

        # 4/5. body rows
        parser = Rows()
        parser.feed(text)
        try:
            value_idx = parser.header.index('Value')
        except ValueError:
            value_idx = None
        for row in parser.rows:
            links = [c for c in row if isinstance(c, str) and c.startswith('https://')]
            cells = [c for c in row if isinstance(c, str) and not c.startswith('https://')]
            if not links:
                failures.append(f'{page.name}: body row without a source link: {cells[:2]}')
                continue
            if not any(link in registered for link in links):
                failures.append(f'{page.name}: row link not in the registered source list: {links[0]}')
            rows_checked += 1
            # in a table that has a "Value" column, an Unverified row must leave it blank
            if value_idx is not None and 'Unverified' in ''.join(cells):
                if value_idx < len(cells):
                    value = cells[value_idx].strip()
                    if value:
                        failures.append(
                            f'{page.name}: Unverified row carries a value: '
                            f'{cells[0]!r} -> {value!r}')

    # 8. every registered source is used at least once in the artifact
    body = htmllib.unescape(' '.join(p.read_text() for p in pages))
    for key, src in DATA['sources'].items():
        if src['url'] not in body:
            failures.append(f'source {key!r} is registered but never referenced in the artifact')
        if urlparse(src['url']).scheme != 'https':
            failures.append(f'source {key!r} is not https')

    # 9. question register provenance
    sys.path.insert(0, str(ROOT / 'data'))
    import questions  # noqa: E402
    for q in questions.ROWS:
        if q[5] not in ('Missing - private', 'Partially answered', 'Unverified official', 'Answered'):
            failures.append(f'{q[0]}: unrecognised status {q[5]!r}')
        if q[6] not in DATA['sources']:
            failures.append(f'{q[0]}: unregistered source key {q[6]!r}')
    for a in questions.ANSWERED:
        if a[4] not in DATA['sources']:
            failures.append(f'{a[0]}: unregistered source key {a[4]!r}')

    if failures:
        for f in failures:
            print(f'::error title=Public artifact check::{f}')
        print(f'\nFAIL: {len(failures)} problem(s)')
        return 1

    print(f'PASS: {len(pages)} pages, {rows_checked} body rows, {internal} internal and '
          f'{external} external links; hosts, provenance, blank-value, PII and embed rules all hold.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
