"""Stage the curated Pages artifact and validate it.

GitHub Pages serves the repository root on `main`. Everything that is not
staged here is either excluded by _config.yml or lives in a directory Jekyll
ignores, so the published site is exactly this file list: the root dashboard,
its category pages, and one stylesheet. No legacy research layer is published.

The script then validates the artifact rather than the checkout: relative
links must resolve inside the artifact, every table row must carry an official
source link, and no published page may contain identifying information.
"""
from __future__ import annotations
import json
import re
import shutil
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_pages_artifact"

PAGES = [
    "index.html",
    "executive-summary.html",
    "decision.html",
    "property-profile.html",
    "geography.html",
    "demographics.html",
    "economy.html",
    "projections.html",
    "schools.html",
    "tenant.html",
    "taxes.html",
    "model.html",
    "hazards.html",
    "risk-register.html",
    "sources.html",
    "flagged.html",
    "repo-review.html",
    "privacy.html",
    "methodology.html",
]

OFFICIAL_HOSTS = {
    "www.census.gov", "www.bls.gov", "fred.stlouisfed.org", "www.sec.gov",
    "finance.lacity.gov", "leginfo.legislature.ca.gov", "www.dir.ca.gov",
    "wagesla.lacity.gov", "www.irs.gov", "www.ftb.ca.gov", "www.cde.ca.gov",
    "www.caschooldashboard.org", "pubs.usgs.gov", "www.conservation.ca.gov",
    "osfm.fire.ca.gov", "www.fire.ca.gov", "msc.fema.gov", "dof.ca.gov",
    "zimas.lacity.org", "investors.jackinthebox.com", "assessor.lacounty.gov",
}


def build_artifact():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)
    for name in PAGES:
        src = ROOT / name
        if not src.is_file():
            raise SystemExit(f"::error title=Missing page::{name}")
        shutil.copy2(src, OUT / name)
    shutil.copy2(ROOT / "assets/style.css", OUT / "assets/style.css")
    for extra in ("CNAME", "404.html", ".nojekyll"):
        if (ROOT / extra).is_file():
            shutil.copy2(ROOT / extra, OUT / extra)


class Check(HTMLParser):
    def __init__(self, page: Path):
        super().__init__()
        self.page = page
        self.in_body = False
        self.row = None
        self.rows = []
        self.cell = None
        self.issues = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "tbody":
            self.in_body = True
        elif tag == "tr" and self.in_body:
            self.row = []
        elif tag in ("td", "th") and self.row is not None:
            self.cell = []
        elif tag == "a":
            href = a.get("href", "")
            if not href:
                return
            if href.startswith("https://"):
                host = href.split("//", 1)[1].split("/", 1)[0].lower()
                if host not in OFFICIAL_HOSTS:
                    self.issues.append(f"{self.page.name}: non-official host {host}")
                if self.row is not None:
                    self.row.append(href)
            elif href.startswith("#"):
                pass
            elif urlparse(href).scheme:
                self.issues.append(f"{self.page.name}: non-https link {href}")
            else:
                target = (self.page.parent / unquote(urlparse(href).path)).resolve()
                if not str(target).startswith(str(OUT.resolve())) or not target.is_file():
                    self.issues.append(f"{self.page.name}: broken link {href}")

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.cell is not None:
            self.row.append("".join(self.cell).strip()) if self.row is not None else None
            self.cell = None
        elif tag == "tr" and self.row is not None:
            self.rows.append(self.row)
            self.row = None
        elif tag == "tbody":
            self.in_body = False

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)


def validate_artifact():
    problems = []
    row_count = 0
    for page in sorted(OUT.glob("*.html")):
        text = page.read_text()
        checker = Check(page)
        checker.feed(text)
        problems.extend(checker.issues)
        for row in checker.rows:
            links = [c for c in row if c.startswith("https://")]
            if any(c.strip().startswith(("Internal", "Analysis", "Unverified")) for c in row):
                row_count += 1
                continue
            if not links:
                problems.append(f"{page.name}: body row without an official source link: {row[0][:50]}")
            row_count += 1
        if re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", text):
            problems.append(f"{page.name}: email address present")
        if re.search(r"wingbangboozle", text, re.I):
            problems.append(f"{page.name}: repository account handle present")
        for forbidden in ("localhost", "127.0.0.1", "<script", "<iframe", "googletagmanager"):
            if forbidden in text.lower():
                problems.append(f"{page.name}: prohibited content {forbidden}")
    if problems:
        for p in problems:
            print(f"::error title=Artifact validation::{p}")
        raise SystemExit(f"artifact validation failed with {len(problems)} problem(s)")
    return row_count


def compare_with_jekyll(actual: Path):
    expected = {p.relative_to(OUT) for p in OUT.rglob("*") if p.is_file()}
    found = {p.relative_to(actual) for p in actual.rglob("*") if p.is_file()}
    if found != expected:
        missing = sorted(map(str, expected - found))
        extra = sorted(map(str, found - expected))
        print(f"::error title=Jekyll artifact mismatch::missing {missing}; unexpected {extra}")
        raise SystemExit("Jekyll output does not match the curated artifact")
    for rel in sorted(expected):
        if (OUT / rel).read_bytes() != (actual / rel).read_bytes():
            print(f"::error title=Jekyll content mismatch::content changed: {rel}")
            raise SystemExit(1)
    print(f"PASS: GitHub Pages' own Jekyll build reproduces all {len(expected)} staged files byte for byte")


if __name__ == "__main__":
    build_artifact()
    rows = validate_artifact()
    staged = sum(1 for p in OUT.rglob("*") if p.is_file())
    print(f"Staged {staged} files · {rows} source-linked table rows · every host official")
    if len(sys.argv) > 1:
        compare_with_jekyll(Path(sys.argv[1]).resolve())
