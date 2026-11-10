"""Create and verify the exact GitHub Pages artifact for the curated dashboard.

The repository keeps several research layers produced by earlier sessions as an
audit trail. None of them is published. This script copies **only** the curated
dashboard into `_pages_artifact/`, then verifies the artifact itself rather than
the checkout:

  * every internal href/src resolves to a file inside the artifact
  * every same-page and cross-page anchor resolves to an element id
  * every <tbody> row carries a registered official source URL
  * no page references a host that is not https

If GitHub Pages' own Jekyll output is supplied as an argument, the artifact is
also compared file-by-file against it, so a Jekyll exclusion or plugin cannot
silently drop or alter a published page.

    python3 scripts/stage_pages.py [jekyll_output_dir]
"""
from __future__ import annotations

import json
import shutil
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_pages_artifact"
DATA = json.loads((ROOT / "data/evidence.json").read_text())

PAGES = ["index.html", "economy.html", "demographics.html", "geography.html",
         "schools.html", "tenant.html", "risk.html", "taxes.html", "decisions.html",
         "model.html", "review.html", "sources.html"]
ASSETS = ["assets/style.css", "assets/app.js"]

if OUT.exists():
    shutil.rmtree(OUT)
(OUT / "assets").mkdir(parents=True)
for name in PAGES:
    shutil.copy2(ROOT / name, OUT / name)
for name in ASSETS:
    shutil.copy2(ROOT / name, OUT / name)
# Tell Jekyll not to process the artifact if it is ever served from a branch.
(OUT / ".nojekyll").write_text("")

SOURCES = {s["url"] for s in DATA["sources"].values()}


class Check(HTMLParser):
    def __init__(self, page: Path):
        super().__init__(convert_charrefs=True)
        self.page = page
        self.row = None
        self.body_rows = 0
        self.ids: set[str] = set()
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "tr":
            self.row = []
        for attr in ("href", "src"):
            if a.get(attr):
                self.links.append((attr, a[attr]))
        if tag == "a" and self.row is not None and a.get("href", "").startswith("https://"):
            self.row.append(a["href"])

    def handle_endtag(self, tag):
        if tag == "tr" and self.row is not None:
            if self.row:
                self.body_rows += 1
                if not any(u in SOURCES for u in self.row):
                    raise SystemExit(f"{self.page.name}: body row without registered source -> {self.row}")
            self.row = None


def anchors(path: Path, cache={}):
    if path not in cache:
        p = Check(path)
        p.feed(path.read_text())
        cache[path] = p.ids
    return cache[path]


failures = []
rows_checked = 0
links_checked = 0
for name in PAGES:
    page = OUT / name
    parser = Check(page)
    parser.feed(page.read_text())
    rows_checked += parser.body_rows
    for attr, value in parser.links:
        if value.startswith("https://"):
            continue
        if urlparse(value).scheme:
            failures.append(f"{name}: non-https or non-relative reference {value}")
            continue
        if value.startswith("#"):
            if value[1:] and value[1:] not in parser.ids:
                failures.append(f"{name}: missing same-page anchor {value}")
            continue
        target, _, frag = value.partition("#")
        if not target:
            continue
        links_checked += 1
        resolved = (page.parent / unquote(urlparse(target).path)).resolve()
        if not resolved.is_relative_to(OUT.resolve()):
            failures.append(f"{name}: reference escapes the artifact {value}")
        elif not resolved.is_file():
            failures.append(f"{name}: missing file {value}")
        elif frag and frag not in anchors(resolved):
            failures.append(f"{name}: missing anchor {value}")

if failures:
    print("STAGE FAILURES")
    for f in failures:
        print(f"  !!  {f}")
    raise SystemExit(1)

staged = sorted(p.relative_to(OUT) for p in OUT.rglob("*") if p.is_file())
print(f"Staged {len(staged)} files in {OUT.name}/")
print(f"PASS: {len(PAGES)} pages, {rows_checked} source-linked body rows, {links_checked} internal links resolved")

# ---------------------------------------------------------------- Jekyll
if len(sys.argv) > 1:
    actual = Path(sys.argv[1]).resolve()
    expected = {p.relative_to(OUT) for p in OUT.rglob("*") if p.is_file() and p.name != ".nojekyll"}
    found = {p.relative_to(actual) for p in actual.rglob("*") if p.is_file()}
    if found != expected:
        msg = (f"unexpected Jekyll files: {sorted(map(str, found - expected))}; "
               f"missing: {sorted(map(str, expected - found))}")
        print("::error title=Jekyll artifact mismatch::" + msg)
        raise SystemExit(msg)
    for rel in sorted(expected):
        if (OUT / rel).read_bytes() != (actual / rel).read_bytes():
            print(f"::error title=Jekyll content mismatch::content changed: {rel}")
            raise SystemExit(f"content changed: {rel}")
    print(f"PASS: Jekyll output matches the curated artifact byte for byte ({len(expected)} files)")
