"""Regression tests of the actual public artifact, not historical companion sites.
Run: python -m unittest discover -s scripts -p 'test_publication.py' -v
These checks test integrity, not accuracy of external source claims.

Inventory contract (repaired 2026-11-11, session b7ead2a1):
  The published artifact is built from data/canonical.json by scripts/build_canonical.py
  and staged by scripts/stage_pages.py. The expected file set is therefore derived from
  the canonical page registry plus one documented alias:
    - every page registered in data/canonical.json (pages[].file) must be staged;
    - flagged.html is a byte-identical alias of review.html ("Flagged for Review"),
      generated on purpose by build_canonical.page_flagged();
    - anything else appearing in the artifact fails the inventory test, so stray or
      private files cannot reach the public site unnoticed.
  Adding a legitimate page means registering it in data/canonical.json in the same
  change; the gate follows the registry automatically.
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

CANONICAL = json.loads((ROOT / 'data/canonical.json').read_text(encoding='utf-8'))
REGISTERED_PAGES = {p['file'] for p in CANONICAL['pages']}
# Deliberate alias of review.html; see module docstring.
ALIASED_PAGES = {'flagged.html'}
# Kept for the shared-navigation assertion below.
ALIASES = ALIASED_PAGES
PAGES = REGISTERED_PAGES | ALIASED_PAGES
STYLESHEET = {'assets/style.css'}
# Status vocabulary of the canonical dataset. A new status must be a deliberate,
# reviewed change to this contract, not an accident.
ALLOWED_STATUSES = {'Verified', 'Blank', 'Analysis', 'Derived'}


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
        cls.docs = {name: Document((PUBLIC / name).read_text()) for name in sorted(PAGES)}

    def test_exact_public_inventory(self):
        actual = {str(p.relative_to(PUBLIC)) for p in PUBLIC.rglob('*') if p.is_file()}
        self.assertEqual(actual, PAGES | STYLESHEET)

    def test_flagged_alias_is_byte_identical_to_review(self):
        # flagged.html is allowed in the artifact only because it is this alias.
        self.assertEqual(
            (PUBLIC / 'flagged.html').read_bytes(),
            (PUBLIC / 'review.html').read_bytes(),
        )

    def test_registered_page_names_are_bare_filenames(self):
        for page in CANONICAL['pages']:
            with self.subTest(page=page.get('file')):
                name = page['file']
                self.assertTrue(name.endswith('.html'))
                self.assertEqual(Path(name).name, name)

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
        # Every staged page must carry the shared nav that reaches every
        # registered page; the flagged.html alias is reached as review.html.
        for name, doc in self.docs.items():
            with self.subTest(page=name):
                targets = {urlsplit(x).path for x in doc.links}
                self.assertTrue((PAGES - ALIASED_PAGES) <= targets)

    def test_unknowns_are_not_verified_or_filled(self):
        """Blank stays blank; every row cites a registered source; status vocabulary fixed."""
        sources = set(CANONICAL['sources'])
        for row in CANONICAL['rows']:
            with self.subTest(category=row.get('category'), indicator=row.get('indicator')):
                self.assertIn(row.get('source'), sources)
                self.assertIn(row.get('status'), ALLOWED_STATUSES)
                if row['status'] == 'Blank':
                    self.assertEqual(row['value'], '')
                if row['status'] == 'Verified':
                    self.assertNotEqual(row['value'].strip(), '')

    def test_legacy_evidence_dataset_rules(self):
        # data/evidence.json still backs scripts/build.py; its rules are unchanged.
        data = json.loads((ROOT / 'data/evidence.json').read_text())
        for page in data['pages']:
            for row in page['rows']:
                with self.subTest(page=page['id'], row=row['cells'][0]):
                    self.assertIn(row['source'], data['sources'])
                    if row['status'] == 'Verified':
                        self.assertNotIn('', row['cells'])
                    if row['status'] == 'Unverified' and page['id'] != 'review':
                        self.assertEqual(row['cells'][1], '')


if __name__ == '__main__':
    unittest.main()
