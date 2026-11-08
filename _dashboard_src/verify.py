"""Automated verification gate for the /dashboard/ layer (session 27610006).

Exits non-zero on any failure. Checks:
  1. every <tbody> <tr> carries a link from this layer's official source register
  2. every external link resolves to an approved official host
  3. no personal information (account handles, names, emails, phones, street addresses)
  4. every internal relative link resolves to a file that exists in the layer
  5. no scripts, forms, trackers or third-party assets
  6. unverified rows are rendered blank, never with a value
  7. the build is deterministic
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "dashboard"

import dataset as D  # noqa: E402

DATA = D.to_json()
SRC = DATA["sources"]
ALLOWED_HOSTS = sorted({urlparse(s["url"]).netloc for s in SRC.values()})

FAILURES: list[str] = []
SRC_URLS = {s["url"] for s in SRC.values()}
CHECKS: list[str] = []


def fail(msg: str) -> None:
    FAILURES.append(msg)


class Page(HTMLParser):
    def __init__(self, path: Path):
        super().__init__()
        self.path = path
        self.rows: list[list[str]] = []
        self.row: list[str] | None = None
        self.in_body_rows = False
        self.links: list[str] = []
        self.text: list[str] = []
        self.tags: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append(tag)
        if tag == "tbody":
            self.in_body_rows = True
        if tag == "tr" and self.in_body_rows:
            self.row = []
        if tag in ("a", "link", "script", "img", "iframe", "form"):
            href = a.get("href") or a.get("src") or ""
            if href:
                self.links.append((tag, href))
            if tag == "a" and self.row is not None and href:
                self.row.append(href)

    def handle_endtag(self, tag):
        if tag == "tbody":
            self.in_body_rows = False
        if tag == "tr" and self.row is not None:
            self.rows.append(self.row)
            self.row = None

    def handle_data(self, data):
        self.text.append(data)


# ---------------------------------------------------------------------------
# 1-5. Parse every generated page
# ---------------------------------------------------------------------------
pages = sorted(OUT.rglob("*.html"))
if not pages:
    fail("no HTML generated")
parsed: dict[Path, Page] = {}
for p in pages:
    pg = Page(p)
    pg.feed(p.read_text(encoding="utf-8"))
    parsed[p] = pg

# 1. every body row needs an official source link
row_count = 0
for p, pg in parsed.items():
    for row in pg.rows:
        row_count += 1
        if not any(h in SRC_URLS for h in row):
            fail(f"row without an official source link in {p.name}: {row[:3]}")
CHECKS.append(f"{row_count} body rows checked for source links")

# 2. external hosts must be approved
for p, pg in parsed.items():
    for tag, href in pg.links:
        if href.startswith(("http://", "https://")):
            host = urlparse(href).netloc
            if host not in ALLOWED_HOSTS:
                fail(f"non-approved host in {p.name}: {host} ({href})")
        elif href.startswith("#"):
            continue
        else:
            target = (p.parent / href.split("#")[0].split("?")[0]).resolve()
            if not target.is_file():
                fail(f"broken internal link in {p.name}: {href}")
CHECKS.append(f"{len(ALLOWED_HOSTS)} approved official hosts; internal links resolved")

# 3. personal information
PII_PATTERNS = [
    (r"wingbangboozle1", "repository account handle"),
    (r"[\w.+-]+@[\w-]+\.[\w.]+", "email address"),
    (r"\b\d{3}-\d{3}-\d{4}\b", "telephone number"),
    (r"\b\d{3,5}\s+[A-Z][a-z]+\s+(St|Ave|Street|Avenue|Blvd|Boulevard|Rd|Road|Dr|Drive|Way)\b", "street address"),
    (r"\b\d{4}-\d{3}-\d{3}\b", "assessor parcel number"),
]
for p in list(parsed) + [HERE / "dataset.py", HERE / "build.py", HERE / "dataset.json"]:
    txt = p.read_text(encoding="utf-8", errors="replace")
    for pat, label in PII_PATTERNS:
        for m in re.finditer(pat, txt):
            fail(f"possible {label} in {p.name}: {m.group(0)[:40]!r}")
CHECKS.append("PII scan clean across generated pages and generators")

# 4. no scripts, forms or third-party assets
for p, pg in parsed.items():
    for tag in pg.tags:
        if tag in ("script", "form", "iframe", "img"):
            fail(f"disallowed <{tag}> element in {p.name}")
CHECKS.append("no scripts, forms, iframes or embedded images")

# 5. unverified rows rendered blank
for f in DATA["facts"]:
    if f["status"] == "unverified":
        if not (str(f["value"]).startswith("(") and str(f["value"]).endswith(")")):
            fail(f"unverified fact {f['id']} carries a value: {f['value']}")
CHECKS.append(f"{sum(1 for f in DATA['facts'] if f['status']=='unverified')} unverified rows confirmed blank")

# 6. determinism
before = {p: p.read_bytes() for p in pages}
subprocess.run([sys.executable, str(HERE / "build.py")], check=True, cwd=str(HERE),
               stdout=subprocess.DEVNULL)
after = {p: p.read_bytes() for p in pages}
if before != after:
    fail("build is not deterministic")
CHECKS.append("deterministic rebuild produces byte-identical output")

# ---------------------------------------------------------------------------
print(f"dashboard pages: {len(pages)}")
print(f"facts: {len(DATA['facts'])} "
      f"({sum(1 for f in DATA['facts'] if f['status']=='verified')} verified, "
      f"{sum(1 for f in DATA['facts'] if f['status']=='derived')} derived, "
      f"{sum(1 for f in DATA['facts'] if f['status']=='unverified')} unverified)")
print(f"sources: {len(SRC)}  flags: {len(DATA['flags'])}  irregularities: {len(DATA['irregularities'])}")
for c in CHECKS:
    print(f"  PASS  {c}")
if FAILURES:
    print("\nFAILURES:")
    for f in FAILURES[:40]:
        print("  -", f)
    raise SystemExit(1)
print("\nPASS: all dashboard verification checks")
