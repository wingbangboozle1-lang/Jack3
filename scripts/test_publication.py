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

    def test_advisor_brief_has_page_scoped_print_layout(self):
        brief = (PUBLIC / 'advisor-brief.html').read_text(encoding='utf-8')
        css = (PUBLIC / 'assets/style.css').read_text(encoding='utf-8')
        self.assertIn('<body class="advisor-brief">', brief)
        self.assertIn('Current position: preserve both options', brief)
        self.assertIn('The public record does not contain the executed lease', brief)
        self.assertIn('browser\'s print command', brief)
        self.assertIn('@page advisorbrief{size:letter landscape', css)
        self.assertIn('body.advisor-brief .sidebar', css)
        self.assertIn('advisor-brief.html', {p['file'] for p in CANONICAL['pages']})

    def test_no_sale_or_renewal_winner_before_verified_inputs(self):
        summary = (PUBLIC / 'executive-summary.html').read_text(encoding='utf-8')
        self.assertIn('do not choose sale or renewal on regional averages alone', summary)
        self.assertIn('Sell before expiry</td>', summary)
        self.assertNotIn('Sell before expiry (base case)', summary)
        self.assertNotIn('Primary track', summary)
        self.assertIn('Run both tracks in parallel (recommended sequence)', summary)

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
        # Inline, network-free JavaScript and text inputs are allowed only on the
        # disclosed interactive pages (SG-01B calculator + SG-12A register filter).
        js_pages = {'calculator.html', 'master.html'}
        for name, doc in self.docs.items():
            with self.subTest(page=name):
                allowed = {'script', 'input', 'button'} if name in js_pages else set()
                self.assertFalse(doc.tags & ({'script', 'iframe', 'form', 'input', 'object', 'embed'} - allowed))
                self.assertEqual(doc.events, [])
                self.assertEqual(doc.remote_resources, [])

    def test_calculator_is_inline_and_network_free(self):
        text = (PUBLIC / 'calculator.html').read_text(encoding='utf-8')
        low = text.lower()
        self.assertIn('<script>', low)
        for token in ('<script src', 'fetch(', 'xmlhttprequest', 'sendbeacon',
                      'localstorage', 'sessionstorage', 'document.cookie', 'import(', 'http://'):
            self.assertNotIn(token, low)
        self.assertIn('runs entirely in this browser', low)

    def test_master_register_filter_is_inline_and_local(self):
        text = (PUBLIC / 'master.html').read_text(encoding='utf-8')
        low = text.lower()
        self.assertIn('id="mq"', low)
        self.assertIn('<script>', low)
        for token in ('<script src', 'fetch(', 'xmlhttprequest', 'sendbeacon', 'http://'):
            self.assertNotIn(token, low)

    def test_no_script_on_any_other_published_page(self):
        for name, doc in self.docs.items():
            if name in ('calculator.html', 'master.html'):
                continue
            with self.subTest(page=name):
                self.assertNotIn('script', doc.tags)

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


class ParserRegressionTests(unittest.TestCase):
    def test_collection_tags_are_recorded(self):
        doc = Document('<script></script><form><input></form><iframe></iframe><object></object><embed>')
        self.assertEqual(doc.tags & {'script', 'form', 'input', 'iframe', 'object', 'embed'},
                         {'script', 'form', 'input', 'iframe', 'object', 'embed'})

    def test_inline_and_remote_resources_are_detected(self):
        doc = Document('<img src="https://example.com/pixel" onload="track()">')
        self.assertEqual(doc.events, ['onload'])
        self.assertEqual(doc.remote_resources, ['https://example.com/pixel'])


if __name__ == '__main__':
    unittest.main()
