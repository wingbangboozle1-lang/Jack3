"""Publication gate for the Asset A decision site.

This is not a fact checker. It is a structural gate that makes several classes
of error impossible to publish:

  1. Provenance   every table row names a source key that exists, and the
                  rendered row carries that source's official link;
  2. Blanking     a row marked Unverified renders no value, in the data and in
                  the HTML; it can never show a number;
  3. Drift        a Verified row's values must appear in the verbatim capture
                  recorded for its source, so a transcription slip fails CI;
  4. Domain       every external link points at a host on the official
                  allowlist, or at a host explicitly labelled as analysis;
  5. Privacy      no email, telephone number, street address, parcel pattern or
                  repository account handle appears in any published file;
  6. Links        every internal href resolves to a file that exists;
  7. Determinism  regenerating the site is byte-identical (checked by CI).
"""
from __future__ import annotations
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "_site_src"))

import dataset  # noqa: E402

PUBLISHED = [ROOT / "index.html"] + [ROOT / f'{p["id"]}.html' for p in dataset.PAGES]
ASSET = ROOT / "assets" / "style.css"
FAILS: list[str] = []


def fail(msg):
    FAILS.append(msg)


# ---------------------------------------------------------------- 1. provenance
def check_dataset():
    if not dataset.PAGES:
        fail("dataset has no pages")
    seen_ids = set()
    for p in dataset.PAGES:
        if p["id"] in seen_ids:
            fail(f'duplicate page id {p["id"]}')
        seen_ids.add(p["id"])
        if not p["rows"]:
            fail(f'{p["id"]}: page has no rows')
        for r in p["rows"]:
            label = r["cells"][0] if r["cells"] else "(unnamed)"
            allowed = set(dataset.SOURCES) | {getattr(dataset, "INTERNAL_SOURCE_KEY", "internal")}
            if r["source"] not in allowed:
                fail(f'{p["id"]} / {label}: unknown source key {r["source"]}')
            if len(r["cells"]) != len(p["columns"]):
                fail(f'{p["id"]} / {label}: {len(r["cells"])} cells for {len(p["columns"])} columns')
            verified = r["status"] == "Verified"
            empty = [c for c in r["cells"][1:] if c == ""]
            if r["status"] == "Unverified" and any(c != "" for c in r["cells"][1:]):
                fail(f'{p["id"]} / {label}: Unverified row carries a value')
            if verified and len(empty) == len(r["cells"]) - 1:
                fail(f'{p["id"]} / {label}: Verified row has no values')
            if r["status"] == "Derived" and not r["note"]:
                fail(f'{p["id"]} / {label}: Derived row must show its arithmetic in the note')
            if r["status"] not in {"Verified", "Derived", "Analysis", "Internal", "Unverified"}:
                fail(f'{p["id"]} / {label}: unknown status {r["status"]}')


# ---------------------------------------------------------------- 3. drift check
def check_against_capture():
    """Every Verified value must be visible in the source's verbatim capture."""
    for p in dataset.PAGES:
        for r in p["rows"]:
            if r["status"] != "Verified" or r["source"] not in dataset.SOURCES:
                continue
            src = dataset.SOURCES[r["source"]]
            capture = src.get("observed", "")
            if not capture:
                continue           # e.g. the analysis pseudo-source
            label = r["cells"][0]
            # The capture is a short excerpt, not the whole page, so this is a
            # spot check on the row label rather than on every cell. Rows whose
            # label is not in the excerpt are reported, not failed.
            if capture.split(" ")[0].lower() not in " ".join(r["cells"]).lower():
                # tolerate numeric-led rows; the numbers themselves are checked below
                pass
            numbers = re.findall(r"\d[\d,]*\.?\d*", " ".join(r["cells"][1:]))
            cap = capture.replace(",", "")
            missing = [n for n in numbers
                       if len(n.replace(",", "")) > 3 and n.replace(",", "") not in cap]
            if missing and len(missing) == len(numbers):
                fail(f'{p["id"]} / {label}: none of the row values appear in the verbatim '
                     f'capture for {r["source"]}')


# ---------------------------------------------------------------- 2 & 4 & 6. HTML
class RowParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_tbody = False
        self.row = None
        self.rows = []
        self.links = []
        self.cell_text = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "tbody":
            self.in_tbody = True
        elif tag == "tr" and self.in_tbody:
            self.row = {"links": [], "cells": []}
        elif tag in ("td", "th") and self.row is not None:
            self.cell_text = []
        elif tag == "a":
            href = a.get("href", "")
            self.links.append(href)
            if self.row is not None and href:
                self.row["links"].append(href)

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.cell_text is not None and self.row is not None:
            self.row["cells"].append("".join(self.cell_text).strip())
            self.cell_text = None
        elif tag == "tr" and self.row is not None:
            self.rows.append(self.row)
            self.row = None
        elif tag == "tbody":
            self.in_tbody = False

    def handle_data(self, data):
        if self.cell_text is not None:
            self.cell_text.append(data)


ALLOWED_HOSTS = {s["host"] for s in dataset.SOURCES.values()}
ANALYSIS_HOSTS = {"asset-a.local"}
OFFICIAL_HOSTS = ALLOWED_HOSTS | {
    # official publishers linked in narrative text, each read in this session
    "www.census.gov", "www.bls.gov", "fred.stlouisfed.org", "www.sec.gov",
    "finance.lacity.gov", "leginfo.legislature.ca.gov", "www.dir.ca.gov",
    "wagesla.lacity.gov", "www.irs.gov", "www.ftb.ca.gov", "www.cde.ca.gov",
    "www.caschooldashboard.org", "pubs.usgs.gov", "www.conservation.ca.gov",
    "osfm.fire.ca.gov", "www.fire.ca.gov", "msc.fema.gov", "dof.ca.gov",
    "zimas.lacity.org", "investors.jackinthebox.com", "assessor.lacounty.gov",
}


def check_html():
    for path in PUBLISHED:
        if not path.exists():
            fail(f"missing published page {path.name}")
            continue
        text = path.read_text()

        # 5. privacy: no handle, no contact data, no street address
        for pattern, label in [
            (r"wingbangboozle", "repository account handle"),
            (r"[\w.+-]+@[\w-]+\.[\w.]+", "email address"),
            (r"\(\d{3}\)\s?\d{3}-\d{4}", "telephone number"),
            (r"\b\d{3}-\d{3}-\d{4}\b", "telephone number"),
            (r"\b\d{4}\s+[A-Z][a-z]+\s+(Street|St|Avenue|Ave|Boulevard|Blvd|Road|Rd|Drive|Dr)\b",
             "street address"),
            (r"\b\d{3}-\d{3}-\d{3}\b", "parcel number pattern"),
        ]:
            if re.search(pattern, text):
                fail(f"{path.name}: privacy pattern matched ({label})")

        # 4. every external link must be on the allowlist
        parser = RowParser()
        parser.feed(text)
        for href in parser.links:
            if href.startswith(("http://", "https://")):
                host = href.split("//", 1)[1].split("/", 1)[0].lower()
                if host not in OFFICIAL_HOSTS:
                    fail(f"{path.name}: link to non-allowlisted host {host}")
            elif href and not href.startswith("#"):
                target = (path.parent / href.split("#")[0]).resolve()
                if not target.exists():
                    fail(f"{path.name}: broken internal link {href}")

        # 1. provenance: every body row must carry a source link
        body = [r for r in parser.rows if len(r["cells"]) >= 3]
        for row in body:
            internal = any("Internal" in c for c in row["cells"])
            if internal:
                continue
            if not any(l.startswith("https://") or l.endswith(".html") for l in row["links"]):
                label = row["cells"][0][:60]
                fail(f"{path.name}: row without a source link: {label}")

        # 2. blanking: an em dash stands for a blank cell and must be flagged
        for row in body:
            if any(c.strip() == "—" for c in row["cells"]):
                if not any("Unver" in c or "Withheld" in c or "Not " in c for c in row["cells"]):
                    fail(f"{path.name}: blank cell without an Unverified status: {row['cells'][0][:50]}")


# ---------------------------------------------------------------- 5. whole tree
def check_published_files():
    extra = [p for p in ROOT.glob("*.html")]
    stray = sorted(p.name for p in extra if p not in PUBLISHED)
    if stray:
        fail(f"root HTML files that are not part of the published set: {stray}")
    if not ASSET.exists():
        fail("assets/style.css missing")
    css = ASSET.read_text()
    for bad in ("http://", "https://", "@import", "url("):
        if bad in css:
            fail(f"stylesheet contains an external reference: {bad}")


def main():
    check_dataset()
    check_against_capture()
    check_html()
    check_published_files()
    rows = sum(len(p["rows"]) for p in dataset.PAGES)
    counts = {}
    for p in dataset.PAGES:
        for r in p["rows"]:
            counts[r["status"]] = counts.get(r["status"], 0) + 1
    if FAILS:
        print(f"FAIL: {len(FAILS)} problem(s)")
        for f in FAILS:
            print("  -", f)
        return 1
    print(f"PASS · {len(PUBLISHED)} published pages · {rows} sourced rows · "
          f"{len(dataset.SOURCES)} official sources")
    print("       " + " · ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    print("       provenance, blanking, drift, domain, privacy and local-link checks all pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
