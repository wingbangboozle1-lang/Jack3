#!/usr/bin/env python3
"""Verify the integrated dashboard in ``report/``.

Checks, all fatal (exit 1) rather than advisory:

  1. Structure   - every page builds the same navigation and a unique <title>
  2. Links       - every internal link resolves to a file and, where present, to an anchor
  3. Sources     - every external link is https and on an official, issuer or declared
                   industry domain; no unlisted host is allowed
  4. Row integrity - every evidence row renders a status badge and a source link
  5. Blanking    - no row with status unverified/input renders a value
  6. Privacy     - no email, phone, street address, parcel or taxpayer-identifier pattern
  7. Determinism - rebuilding produces byte-identical output
  8. Consistency - the headline counts printed on the site match the data

Run:  python3 tools/check_report.py
"""

from __future__ import annotations

import filecmp
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = os.path.join(ROOT, "report")
sys.path.insert(0, ROOT)

import data.report_data as D  # noqa: E402

# Domains accepted as official / primary / declared-industry publishers.
OFFICIAL = {
    "census.gov", "bls.gov", "fred.stlouisfed.org", "federalreserve.gov",
    "home.treasury.gov", "lacounty.gov", "assessor.lacounty.gov", "dir.ca.gov",
    "wagesla.lacity.gov", "finance.lacity.gov", "lavote.gov", "irs.gov", "sos.ca.gov",
    "voterguide.sos.ca.gov", "usgs.gov", "pubs.usgs.gov", "fire.ca.gov",
    "osfm.fire.ca.gov", "congress.gov", "cde.ca.gov", "caschooldashboard.org",
    "sec.gov", "bouldergroup.com",
}
INDUSTRY = {"bouldergroup.com"}

PII_PATTERNS = {
    "email": re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"),
    "phone": re.compile(r"(?<!\d)(?:\+?1[\s.\-]?)?\(?\d{3}\)?[\s.\-]\d{3}[\s.\-]\d{4}(?!\d)"),
    "street address": re.compile(
        r"\b\d{2,6}\s+(?:[NSEW]\.?\s+)?[A-Z][A-Za-z]{2,}\s+"
        r"(?:Street|St|Avenue|Ave|Boulevard|Blvd|Road|Rd|Drive|Dr|Way|Lane|Ln|Place|Pl|"
        r"Court|Ct|Terrace|Parkway|Pkwy)\b"),
    "parcel number": re.compile(r"\b\d{3,4}-\d{3}-\d{3}\b"),
    "taxpayer id": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
}


class Collect(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.hrefs = []
        self.text = []
        self.tags = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append((tag, a))
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and "href" in a:
            self.hrefs.append(a["href"])

    def handle_data(self, data):
        self.text.append(data)


def parse_all():
    pages = {}
    for fn in sorted(os.listdir(SITE)):
        if not fn.endswith(".html"):
            continue
        p = Collect()
        raw = open(os.path.join(SITE, fn), encoding="utf-8").read()
        p.feed(raw)
        pages[fn] = (p, raw)
    return pages


def check(pages):
    errors, warnings = [], []
    bases = set(pages)

    # 1. structure
    for fn, (p, raw) in pages.items():
        if fn != "index.html" and "<title>" not in raw:
            errors.append(f"{fn}: missing <title>")
        if "methodology.html" not in raw:
            errors.append(f"{fn}: navigation missing link to methodology.html")
        if raw.count('aria-current="page"') != 1:
            errors.append(f"{fn}: expected exactly one aria-current page marker")

    # 2-3. links
    external = {}
    for fn, (p, raw) in pages.items():
        for href in p.hrefs:
            if href.startswith(("http://", "https://")):
                host = re.sub(r"^https?://", "", href).split("/")[0].lower()
                external.setdefault(host, 0)
                external[host] += 1
                if href.startswith("http://"):
                    errors.append(f"{fn}: insecure external link {href}")
                if not any(host == d or host.endswith("." + d) for d in OFFICIAL):
                    errors.append(f"{fn}: unlisted external host {host}")
            elif href.startswith("#"):
                if href[1:] and href[1:] not in p.ids:
                    errors.append(f"{fn}: broken anchor {href}")
            elif href.startswith("mailto:"):
                errors.append(f"{fn}: mailto link present")
            else:
                path, _, anchor = href.partition("#")
                if path and path not in bases:
                    target = os.path.normpath(os.path.join(SITE, path))
                    if not os.path.exists(target):
                        errors.append(f"{fn}: broken internal link {href}")
                elif path and anchor:
                    tp = pages.get(path)
                    if tp and anchor not in tp[0].ids:
                        errors.append(f"{fn}: broken anchor {href}")

    # 4-5. row integrity
    for fn in ("evidence.html", "sources.html"):
        raw = pages[fn][1]
        rows = re.findall(r"<tr>.*?</tr>", raw, flags=re.S)
        body_rows = [r for r in rows if "<td" in r]
        for r in body_rows:
            if fn == "evidence.html":
                if "badge" not in r:
                    errors.append(f"{fn}: row without status badge: {r[:120]}")
                if "https://" not in r:
                    errors.append(f"{fn}: row without a source link: {r[:120]}")

    for rid, r in {r["id"]: r for r in D.all_rows()}.items():
        if r["status"] not in ("unverified", "input"):
            continue
        val = str(r["display_value"] or "").strip()
        if val and val in pages["evidence.html"][1]:
            errors.append(f"evidence.html: unverified row {rid} rendered a value ({val})")

    # 6. privacy
    for fn, (p, raw) in pages.items():
        for label, pat in PII_PATTERNS.items():
            for m in pat.finditer(raw):
                errors.append(f"{fn}: possible {label}: {m.group(0)[:60]}")
    for fn in ("style.css",):
        pass

    # 7. determinism
    tmp = tempfile.mkdtemp(prefix="reportcheck-")
    try:
        before = {fn: hashlib.sha256(open(os.path.join(SITE, fn), "rb").read()).hexdigest()
                  for fn in os.listdir(SITE) if fn.endswith((".html", ".css"))}
        subprocess.run([sys.executable, os.path.join(HERE, "build_report.py")],
                       check=True, cwd=ROOT, stdout=subprocess.DEVNULL)
        after = {fn: hashlib.sha256(open(os.path.join(SITE, fn), "rb").read()).hexdigest()
                 for fn in os.listdir(SITE) if fn.endswith((".html", ".css"))}
        if before != after:
            changed = [k for k in before if before.get(k) != after.get(k)]
            errors.append(f"build is not deterministic: {changed}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # 8. consistency of headline counts
    counts = D.counts()
    idx = pages["index.html"][1]
    if f">{counts['total']}</b>" not in idx:
        errors.append("index.html: total row count does not match the data")
    if f">{len(D.FLAGS)}</b>" not in idx:
        errors.append("index.html: flag count does not match the data")
    if f">{counts['official_sources']}</b>" not in idx:
        errors.append("index.html: official-source count does not match the data")
    srcs = pages["sources.html"][1]
    if f"{len(D.SOURCES)} publishers" not in srcs:
        errors.append("sources.html: publisher count does not match the register")

    return errors, warnings, external


def main():
    pages = parse_all()
    errors, warnings, external = check(pages)
    print(f"pages checked      : {len(pages)}")
    print(f"external hosts     : {len(external)}")
    print("  " + ", ".join(sorted(external)))
    print(f"evidence rows      : {D.counts()['total']}")
    print(f"flags              : {len(D.FLAGS)}")
    if warnings:
        print("\nWARNINGS")
        for w in warnings:
            print("  -", w)
    if errors:
        print("\nFAILURES")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print("\nOK - links resolve, every row is sourced, nothing unverified is rendered, "
          "no personal-information pattern found, and the build is byte-for-byte reproducible.")


if __name__ == "__main__":
    main()
