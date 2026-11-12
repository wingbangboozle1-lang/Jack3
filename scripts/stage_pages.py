#!/usr/bin/env python3
"""Build the exact GitHub Pages artifact for the canonical site.

The legacy Pages build publishes the repository root through Jekyll.  This script
stages the intended public files, validates that every table body row carries an
official source link and that every internal link resolves inside the artifact, and
(optionally) compares the artifact byte-for-byte with an actual Jekyll build.

    python3 scripts/stage_pages.py                 # stage + validate
    python3 scripts/stage_pages.py _jekyll_test   # also compare with Jekyll output
"""
from __future__ import annotations

import html.parser
import json
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_pages_artifact"
D = json.loads((ROOT / "data/canonical.json").read_text(encoding="utf-8"))
OFFICIAL_URLS = {s["url"] for s in D["sources"].values()}

def strip_front_matter(text: str) -> str:
    """Jekyll removes YAML front matter from output; the staged artifact must match."""
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---\n", 4)
    if end < 0:
        return text
    return text[end + len("\n---\n"):]


if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
for page in sorted(ROOT.glob("*.html")):
    (OUT / page.name).write_text(
        strip_front_matter(page.read_text(encoding="utf-8")), encoding="utf-8")
(OUT / "assets").mkdir()
shutil.copy2(ROOT / "assets/style.css", OUT / "assets/style.css")


class ArtifactCheck(html.parser.HTMLParser):
    def __init__(self, page: Path):
        super().__init__(convert_charrefs=True)
        self.page = page
        self.in_tbody = False
        self.row: list[str] | None = None
        self.bad: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "tbody":
            self.in_tbody = True
        if tag == "tr" and self.in_tbody:
            self.row = []
        href = a.get("href", "") or a.get("src", "")
        if not href:
            return
        if href.startswith("https://"):
            if self.row is not None:
                self.row.append(href)
        elif href.startswith("#"):
            return
        elif href.startswith(("mailto:", "tel:", "http://")):
            if href.startswith("http://"):
                self.bad.append(f"non-https link {href}")
            return
        else:
            target = (self.page.parent / unquote(urlparse(href).path)).resolve()
            if not target.is_relative_to(OUT.resolve()) or not target.is_file():
                self.bad.append(f"broken internal link {href}")

    def handle_endtag(self, tag):
        if tag == "tr" and self.row is not None:
            if not any(u in OFFICIAL_URLS for u in self.row):
                self.bad.append(f"table row without official source link: {self.row[:3]}")
            self.row = None
        if tag == "tbody":
            self.in_tbody = False


errors: list[str] = []
files = sorted(p for p in OUT.rglob("*") if p.is_file())
for page in [p for p in files if p.suffix == ".html"]:
    check = ArtifactCheck(page)
    check.feed(page.read_text(encoding="utf-8"))
    errors.extend(f"{page.name}: {b}" for b in check.bad)
print(f"Staged {len(files)} files in {OUT.name}: "
      f"{len([p for p in files if p.suffix == '.html'])} HTML pages + assets/style.css")
if errors:
    for e in errors[:40]:
        print("  FAIL:", e)
    raise SystemExit(1)
print("PASS: staged artifact — every table row source-linked, every internal link resolves")

if len(sys.argv) > 1:
    actual = Path(sys.argv[1]).resolve()
    expected = {p.relative_to(OUT) for p in files}
    expected_html = {p for p in expected if p.suffix == ".html"}
    found = {p.relative_to(actual) for p in actual.rglob("*") if p.is_file()}
    # A private document or script can leak as a non-HTML file too. Fail closed
    # on all unreviewed output, not just additional HTML pages.
    if found != expected:
        msg = (f"unexpected Jekyll files: {sorted(map(str, found - expected))}; "
               f"missing: {sorted(map(str, expected - found))}")
        print("::error title=Jekyll artifact mismatch::" + msg)
        raise SystemExit(msg)
    for rel in expected:
        if rel not in found:
            print(f"::error title=Jekyll artifact missing::missing file: {rel}")
            raise SystemExit(1)
        if (OUT / rel).read_bytes() != (actual / rel).read_bytes():
            print(f"::error title=Jekyll content mismatch::content changed: {rel}")
            raise SystemExit(1)
    print("PASS: actual Jekyll output matches the curated artifact byte-for-byte "
          f"({len(expected_html)} HTML pages, exact file inventory)")
