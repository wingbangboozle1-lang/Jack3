"""Regression tests of the actual public artifact, not historical companion sites.
Run: python -m unittest discover -s scripts -p 'test_publication.py' -v
These checks test integrity, not accuracy of external source claims.
"""
import json
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import sys
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / '_pages_artifact'
PAGES = {p['file'] for p in json.loads((ROOT / 'data/canonical.json').read_text())['pages']} | {'flagged.html'}
ALIASES = {'flagged.html'}


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = set()
        self.links = []
        self.tags = set()
        self.remote_resources = []
        self.events = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.add(tag)
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        self.events.extend(k for k in attrs if k.lower().startswith('on'))
        for key in ('href', 'src', 'action'):
            if key in attrs:
                self.links.append(attrs[key])
                if tag != 'a' and urlsplit(attrs[key]).netloc:
                    self.remote_resources.append(attrs[key])


class PublicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, 'scripts/stage_pages.py'], cwd=ROOT, check=True)
        cls.docs = {name: Document((PUBLIC / name).read_text()) for name in PAGES}

    def test_exact_public_inventory(self):
        actual = {str(p.relative_to(PUBLIC)) for p in PUBLIC.rglob('*') if p.is_file()}
        self.assertEqual(actual, PAGES | {'assets/style.css'})

    def test_all_local_targets_and_fragments(self):
        for name, doc in self.docs.items():
            for link in doc.links:
                with self.subTest(page=name, link=link):
                    url = urlsplit(link)
                    self.assertNotIn(url.scheme.lower(), {'javascript', 'data', 'mailto', 'tel'})
                    if url.scheme or url.netloc:
                        self.assertEqual(url.scheme, 'https')
                        continue
                    target = (PUBLIC / unquote(url.path or name)).resolve()
                    self.assertTrue(target.is_relative_to(PUBLIC.resolve()))
                    self.assertTrue(target.is_file())
                    if url.fragment:
                        target_doc = self.docs.get(target.name)
                        self.assertIsNotNone(target_doc)
                        self.assertIn(unquote(url.fragment), target_doc.ids)

    def test_no_active_collection_or_remote_resources(self):
        for name, doc in self.docs.items():
            with self.subTest(page=name):
                self.assertFalse(doc.tags & {'script', 'iframe', 'form', 'input', 'object', 'embed'})
                self.assertEqual(doc.events, [])
                self.assertEqual(doc.remote_resources, [])

    def test_all_pages_accessible_from_shared_navigation(self):
        for name, doc in self.docs.items():
            with self.subTest(page=name):
                targets = {urlsplit(x).path for x in doc.links}
                self.assertTrue((PAGES - ALIASES) <= targets)

    def test_unknowns_are_not_verified_or_filled(self):
        data = json.loads((ROOT / 'data/evidence.json').read_text())
        for page in data['pages']:
            for row in page['rows']:
                with self.subTest(page=page['id'], row=row['cells'][0]):
                    self.assertIn(row['source'], data['sources'])
                    if row['status'] == 'Verified':
                        self.assertNotIn('', row['cells'])
                    if row['status'] == 'Unverified' and page['id'] != 'review':
                        self.assertEqual(row['cells'][1], '')

    def test_canonical_register_unknowns_are_blank_not_filled(self):
        # Same rule for the published canonical register (data/canonical.json):
        # every row resolves to a registered official https:// source; Verified
        # rows carry a value; Blank rows carry none (never inferred/filled).
        data = json.loads((ROOT / 'data/canonical.json').read_text())
        sources = data['sources']
        for key, src in sources.items():
            with self.subTest(source=key):
                self.assertTrue(src['url'].startswith('https://'))
        for i, row in enumerate(data['rows']):
            with self.subTest(row=i, indicator=row['indicator']):
                self.assertIn(row['source'], sources)
                if row['status'] == 'Verified':
                    self.assertTrue(str(row['value']).strip())
                if row['status'] == 'Blank':
                    self.assertEqual(row['value'], '')


if __name__ == '__main__':
    unittest.main()
