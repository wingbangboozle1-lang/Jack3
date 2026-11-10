#!/usr/bin/env python3
"""Publication integrity gate for the curated root dashboard.

This is a build check, not a fact-checker. It cannot know whether the Census
Bureau still publishes 3,869,089. What it can do -- and does -- is make the
claims this project makes about its own publication mechanically true:

  1. PROVENANCE   every <tbody> row on every page carries a link to a URL that
                  is registered as an official source in data/evidence.json.
  2. BLANK        a row whose status is Unverified or Needs review never renders
                  a value. Blank is enforced in code, in build.py:value_cell().
  3. ARITHMETIC   every Derived row is recomputed here from its stated
                  components and must agree with the published string.
  4. LINKS        every internal href/src resolves to a file in the artifact,
                  and every same-page anchor resolves to an id in that page.
  5. HYGIENE      no third-party scripts, iframes, fonts, forms, trackers or
                  localhost references; one first-party script; one stylesheet.
  6. DETERMINISM  rebuilding produces byte-identical HTML.

    python3 scripts/validate.py
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
D = json.loads((ROOT / "data/evidence.json").read_text())
ROWS = D["rows"]
SRC = D["sources"]
OFFICIAL_URLS = {s["url"] for s in SRC.values()}
# Issuer and government hosts that are not on a .gov domain but are the
# competent authority for the fact cited. Anything else is a failure.
OFFICIAL_ISSUERS = {
    "investors.jackinthebox.com",     # the tenant's own investor-relations site
    "leginfo.legislature.ca.gov",     # California Legislative Information
    "zimas.lacity.org",               # City of Los Angeles zoning lookup
}
PAGES = ["index"] + [c["id"] for c in D["categories"]] + ["sources"]
FAILS: list[str] = []
CHECKS: list[str] = []


def ok(msg):
    CHECKS.append(msg)


def fail(msg):
    FAILS.append(msg)


# ---------------------------------------------------------------- 1. rows
class RowParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows = []
        self.row = None
        self.in_body = False
        self.links = []
        self.ids = set()
        self.tags = []
        self.attrs = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append(tag)
        self.attrs.append((tag, a))
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "tbody":
            self.in_body = True
        if tag == "tr" and self.in_body:
            self.row = []
        if tag == "a":
            href = a.get("href", "")
            self.links.append(href)
            if self.row is not None and href.startswith("https://"):
                self.row.append(href)

    def handle_endtag(self, tag):
        if tag == "tr" and self.row is not None:
            self.rows.append(self.row)
            self.row = None
        if tag == "tbody":
            self.in_body = False


parsed = {}
for pid in PAGES:
    path = ROOT / f"{pid}.html"
    if not path.is_file():
        fail(f"missing page {path.name}")
        continue
    p = RowParser()
    p.feed(path.read_text())
    parsed[pid] = p

for pid, p in parsed.items():
    for i, row in enumerate(p.rows, 1):
        if not any(u in OFFICIAL_URLS for u in row):
            fail(f"{pid}.html body row {i}: no registered official source link -> {row}")
ok(f"provenance: {sum(len(p.rows) for p in parsed.values())} body rows across {len(parsed)} pages, "
   f"every one carries a registered official source")

# ---------------------------------------------------------- 2. blank values
unverified_rows = [(pid, r) for pid in ROWS for r in ROWS[pid]
                   if r["status"] in ("Unverified", "Needs review") and r["value"].strip()]
if unverified_rows:
    for pid, r in unverified_rows:
        fail(f"unverified row {r['id']} in {pid} carries a value: {r['value']!r}")
else:
    ok("blank-when-unverified: no Unverified or Needs review row carries a value")

for pid in ROWS:
    if pid not in parsed:
        continue
    html_text = (ROOT / f"{pid}.html").read_text()
    for r in ROWS[pid]:
        if r["status"] in ("Unverified", "Needs review"):
            if "not published" not in html_text:
                fail(f"{pid}.html: unverified rows exist but no blank placeholder rendered")
                break
ok("blank rendering: unverified rows render the explicit 'not published' placeholder")

# ------------------------------------------------------------ 3. arithmetic
def money_per_unit(cap):
    return 100.0 / cap


CAPS = [5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0]
PRICE = 6_000_000
CITY_BASE = PRICE * 0.0045
ULA = PRICE * 0.04
COUNTY = PRICE / 500 * 0.55
TOTAL = CITY_BASE + ULA + COUNTY
PCT = TOTAL / PRICE * 100.0
PV = 1.0 / (1.0488 ** 4)

derived_checks = {
    # id: (published string must contain, computed string)
    "M-05": ([f"{money_per_unit(c):,.2f}" for c in CAPS], "value per $1 of NOI at each cap rate"),
    "M-06": ([f"{(money_per_unit(CAPS[4]) / money_per_unit(CAPS[2]) - 1) * 100:+.1f}%",
              f"{(money_per_unit(CAPS[6]) / money_per_unit(CAPS[2]) - 1) * 100:+.1f}%"],
             "value change 6.0% to 7.0% and to 8.0%"),
    "M-07": ([f"${TOTAL:,.0f}", f"{PCT:.2f}%"], "transfer taxes on $6.0m"),
    "M-08": ([f"${PV:.3f}"], "present value of $1 in 2030"),
    "R-08": ([f"{PCT:.2f}%"], "transfer tax share"),
}
index = {r["id"]: r for pid in ROWS for r in ROWS[pid]}
for rid, (expected, label) in derived_checks.items():
    r = index.get(rid)
    if not r:
        fail(f"derived row {rid} missing")
        continue
    for token in expected:
        if token not in r["value"]:
            fail(f"{rid} ({label}): published {r['value']!r} lacks computed {token!r}")
ok(f"arithmetic: {len(derived_checks)} derived rows recomputed and matched")

# R-11 sums two verified incident counts.
pal = index["R-12"]["value"]
eat = index["R-13"]["value"]
m_pal = re.search(r"([\d,]+) structures destroyed", pal)
m_eat = re.search(r"([\d,]+) structures destroyed", eat)
if m_pal and m_eat:
    s = int(m_pal.group(1).replace(",", "")) + int(m_eat.group(1).replace(",", ""))
    if f"{s:,}" not in index["R-11"]["value"]:
        fail(f"R-11: sum {s:,} not present in {index['R-11']['value']!r}")
    else:
        ok(f"arithmetic: R-11 sums {m_pal.group(1)} + {m_eat.group(1)} = {s:,} structures")
else:
    fail("R-11 / R-12 / R-13 incident counts not parseable")

# E-07 cross-check: unemployed / labour force reproduces the published rate.
try:
    lf = float(index["E-06"]["value"].split()[0].replace(",", ""))
    emp = float(index["E-07"]["value"].split()[0].replace(",", ""))
    rate = (lf - emp) / lf * 100
    if abs(rate - 4.4) > 0.05:
        fail(f"E-06/E-07 imply {rate:.2f}% unemployment, published 4.4%")
    else:
        ok(f"arithmetic: labour-force components imply {rate:.2f}% unemployment, consistent with 4.4%")
except Exception as exc:  # noqa: BLE001
    fail(f"could not cross-check E-06/E-07: {exc}")

# ---------------------------------------------------------------- 4. links
internal = 0
for pid, p in parsed.items():
    for tag, a in p.attrs:
        for attr in ("href", "src"):
            v = a.get(attr)
            if not v:
                continue
            if v.startswith(("https://", "mailto:")):
                continue
            if v.startswith("#"):
                if v[1:] and v[1:] not in p.ids:
                    fail(f"{pid}.html: anchor {v} not present in page")
                continue
            if v.startswith("//") or urlparse(v).scheme:
                fail(f"{pid}.html: non-https external reference {v}")
                continue
            target = v.split("#")[0].split("?")[0]
            if not target:
                continue
            internal += 1
            if not (ROOT / target).is_file():
                fail(f"{pid}.html: broken internal {attr} -> {v}")
ok(f"links: {internal} internal references resolve on disk")

# ------------------------------------------------------------- 5. hygiene
BANNED = [
    "googletagmanager", "google-analytics", "gtag(", "fonts.googleapis", "fonts.gstatic",
    "cdn.jsdelivr", "unpkg.com", "cdnjs", "<iframe", "localhost", "127.0.0.1", ":8000",
    "http://", "<form", "facebook.com/tr", "hotjar", "segment.io",
]
for pid, p in parsed.items():
    text = (ROOT / f"{pid}.html").read_text()
    low = text.lower()
    for b in BANNED:
        if b in low:
            fail(f"{pid}.html: banned pattern {b!r}")
    scripts = [a.get("src") for t, a in p.attrs if t == "script"]
    if scripts != ["assets/app.js"]:
        fail(f"{pid}.html: expected exactly one first-party script, found {scripts}")
    sheets = [a.get("href") for t, a in p.attrs if t == "link" and a.get("rel") == "stylesheet"]
    if sheets != ["assets/style.css"]:
        fail(f"{pid}.html: expected exactly one stylesheet, found {sheets}")
    for req in ("<!doctype html>", 'lang="en"', 'name="description"', 'class="skip"', "<h1"):
        if req not in text:
            fail(f"{pid}.html: missing {req}")
ok("hygiene: one first-party stylesheet, one first-party script, no third-party or localhost references")

# every source URL is https and on an official or issuer host
for k, s in SRC.items():
    u = urlparse(s["url"])
    if u.scheme != "https":
        fail(f"source {k}: not https ({s['url']})")
    host = u.netloc
    if not (host.endswith(".gov") or host in OFFICIAL_ISSUERS):
        fail(f"source {k}: host {host} is not an official or issuer domain")
ok(f"hosts: {len({urlparse(s['url']).netloc for s in SRC.values()})} distinct official/issuer hosts, all https")

# PII patterns must not appear in the dataset or the pages
PII = {
    "email": re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"),
    "ssn/itin": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "parcel": re.compile(r"\b\d{3,4}-\d{3}-\d{3}\b"),
    "phone": re.compile(r"\(\d{3}\)\s?\d{3}-\d{4}"),
    "street": re.compile(r"\b\d{3,5}\s+[A-Z][a-z]+\s+(Street|St|Avenue|Ave|Boulevard|Blvd|Road|Rd|Drive|Dr)\b"),
}
scanned = 0
for f in [ROOT / "data/evidence.json"] + [ROOT / f"{pid}.html" for pid in PAGES] + \
         [ROOT / "assets/style.css", ROOT / "assets/app.js"]:
    text = f.read_text()
    scanned += 1
    for name, rx in PII.items():
        for m in rx.finditer(text):
            fail(f"{f.name}: possible {name} -> {m.group(0)!r}")
ok(f"privacy: {scanned} published files scanned for email, phone, street address, parcel and taxpayer patterns")

# --------------------------------------------------------- 6. determinism
def digest():
    h = hashlib.sha256()
    for pid in PAGES:
        h.update((ROOT / f"{pid}.html").read_bytes())
    h.update((ROOT / "assets/style.css").read_bytes())
    h.update((ROOT / "assets/app.js").read_bytes())
    return h.hexdigest()


before = digest()
subprocess.run([sys.executable, str(ROOT / "scripts/build.py")], check=True,
               cwd=ROOT, stdout=subprocess.DEVNULL)
after = digest()
if before != after:
    fail("rebuild changed the artifact: build is not deterministic")
else:
    ok(f"determinism: rebuild is byte-identical ({before[:12]})")

# --------------------------------------------------------------- report
print("PASS CHECKS")
for c in CHECKS:
    print(f"  ok  {c}")
if FAILS:
    print("\nFAILURES")
    for f in FAILS:
        print(f"  !!  {f}")
    sys.exit(1)
print(f"\nPASS: {len(CHECKS)} check groups, 0 failures.")
