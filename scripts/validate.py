"""Validate local publication integrity; not an external semantic fact checker."""
import json
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse

D = json.loads(Path("data/evidence.json").read_text(encoding="utf-8"))


class Check(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.row = None
        self.in_tbody = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "tbody":
            self.in_tbody = True
        elif tag == "tr" and self.in_tbody:
            self.row = []
        if tag in ("a", "link"):
            url = a.get("href", "")
            if url.startswith("https://"):
                if self.row is not None:
                    self.row.append(url)
            elif url and not url.startswith("#"):
                assert Path(url.split("#")[0]).is_file(), url

    def handle_endtag(self, tag):
        if tag == "tr" and self.row is not None:
            self.rows.append(self.row)
            self.row = None
        elif tag == "tbody":
            self.in_tbody = False


allowed = {s["url"] for s in D["sources"].values()}
count = 0
for p in D["pages"]:
    tables = [{"columns": p["columns"], "rows": p["rows"]}] + p.get("extra_tables", [])
    for tbl in tables:
        for r in tbl["rows"]:
            assert r["source"] in D["sources"], r
            assert len(r["cells"]) == len(tbl["columns"]), (p["id"], r)
            assert r["status"] in ("Verified", "Analysis", "Unverified", "Needs review"), r
            if "" in r["cells"]:
                assert r["status"] != "Verified", r
            count += 1

for file in sorted(Path(".").glob("*.html")):
    text = file.read_text(encoding="utf-8")
    c = Check()
    c.feed(text)
    for row in c.rows:
        assert any(link in allowed for link in row), (file, row)
    for forbidden in ["googletagmanager.com", "localhost", "127.0.0.1", "<iframe", "<script"]:
        assert forbidden not in text.lower(), (file, forbidden)

assert all(urlparse(s["url"]).scheme == "https" for s in D["sources"].values())
print(
    f"PASS: {count} evidence rows; {len(list(Path('.').glob('*.html')))} pages; "
    "source links, local links, blank fields, prohibited embed checks."
)
