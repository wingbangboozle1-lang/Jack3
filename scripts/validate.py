#!/usr/bin/env python3
"""Validate the canonical published site. Dependency-free (stdlib only).

Enforced:
  1. Every evidence row has a status, a source key and an official https URL.
  2. Unverified (Blank) rows have an empty value.
  3. Every <tbody> <tr> in every published HTML file contains an official source link.
  4. Every external link is https and on an approved official host.
  5. Every internal link and fragment resolves inside the published artifact.
  6. Every page carries the shared navigation, and no page links to a missing file.
  7. No scripts, iframes, forms, tracking vendors, localhost or http:// links — with one
     documented exception: calculator.html may embed a single INLINE script. That script
     must be src-less and must contain none of: network APIs (fetch, XMLHttpRequest,
     WebSocket, EventSource, sendBeacon, import(), http/https references), storage APIs
     (localStorage, sessionStorage, indexedDB, document.cookie), dynamic code execution
     (eval, new Function), navigation (location), postMessage, or a src/action attribute.
     Every other published file keeps the strict rule. This gate is what makes the private
     calculator private: inputs cannot leave the page.
  8. Privacy gate: no emails, phone numbers, street addresses, parcel numbers,
     taxpayer identifiers, account handles or tenant officer names in published files.
  9. Determinism: rebuilding does not change any published file.
"""
from __future__ import annotations

import hashlib
import html.parser
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parent.parent
D = json.loads((ROOT / "data/canonical.json").read_text(encoding="utf-8"))
SOURCES = D["sources"]
PAGES = D["pages"]
OFFICIAL_URLS = {s["url"] for s in SOURCES.values()}
OFFICIAL_HOSTS = {urlparse(u).netloc for u in OFFICIAL_URLS}
PUBLISHED = sorted(ROOT.glob("*.html")) + [ROOT / "assets/style.css"]
PUBLISHED_NAMES = {str(p.relative_to(ROOT)) for p in PUBLISHED} | {p.name for p in PUBLISHED}

PII = {
    "email": re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"),
    "phone": re.compile(r"(?<![\d.])(?:\+?1[\s.\-]?)?\(?\d{3}\)?[\s.\-]\d{3}[\s.\-]\d{4}(?![\d.])"),
    "street": re.compile(r"\b\d{1,6}\s+[A-Z][A-Za-z.'\- ]{1,40}\s+(?:Street|St|Avenue|Ave|Boulevard|Blvd|Drive|Dr|Road|Rd|Lane|Ln|Way|Place|Pl|Court|Ct|Parkway|Pkwy)\b"),
    "apn": re.compile(r"\b(?:APN|assessor'?s? parcel (?:number|id))\b\s*[:=]\s*[A-Z0-9\-]{4,}", re.I),
    "ssn": re.compile(r"(?<!\d)\d{3}-\d{2}-\d{4}(?!\d)"),
    "account-handle": re.compile(r"wingbangboozle1", re.I),
    "officer-name": re.compile(r"Lance Tucker|Mark King|Rachel Webb|Andres Chait", re.I),
}
FORBIDDEN = ("<script", "<iframe", "<form", "googletagmanager", "google-analytics",
             "localhost", "127.0.0.1", "http://", "onclick=", "onerror=")
# The one page allowed an inline script, with its own stricter token checks below.
OFFLINE_SCRIPT_PAGE = "calculator.html"
FORBIDDEN_WITH_SCRIPT_ALLOWED = ("<iframe", "<form", "googletagmanager", "google-analytics",
                                 "localhost", "127.0.0.1", "http://", "onclick=", "onerror=")
# Anything on this list inside a script block would let inputs, code or page state leave
# the browser, execute dynamically, or load an external asset. The private calculator
# must fail the build if any of them appears.
SCRIPT_FORBIDDEN = ("fetch", "xmlhttprequest", "websocket", "eventsource", "sendbeacon",
                    "import(", "https://", "http://", "localstorage", "sessionstorage",
                    "indexeddb", "document.cookie", "eval(", "new function", "location",
                    "postmessage", "navigator.", "src=", "action=", "<iframe", "<form")
PRIVACY_NOTICE_MARKER = "stays in this browser tab"


class PageParser(html.parser.HTMLParser):
    def __init__(self, name: str):
        super().__init__(convert_charrefs=True)
        self.name = name
        self.in_tbody = False
        self.rows: list[list[str]] = []
        self.row: list[str] | None = None
        self.external: list[str] = []
        self.internal: list[str] = []
        self.ids: set[str] = set()
        self.links: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "tbody":
            self.in_tbody = True
        if tag == "tr" and self.in_tbody:
            self.row = []
        for attr in ("href", "src"):
            v = a.get(attr, "")
            if not v:
                continue
            if self.row is not None and attr == "href":
                self.row.append(v)
            if v.startswith("https://"):
                self.external.append(v)
            elif v.startswith("#"):
                self.internal.append(v)
            elif not v.startswith(("mailto:", "tel:", "http://")):
                self.links.append(v.split("#", 1)[0])
                if "#" in v:
                    self.internal.append("#" + v.split("#", 1)[1])
            elif v.startswith("http://"):
                self.external.append(v)
        if tag == "tr" and not self.in_tbody:
            self.row = None

    def handle_endtag(self, tag):
        if tag == "tr" and self.row is not None:
            self.rows.append(self.row)
            self.row = None
        if tag == "tbody":
            self.in_tbody = False


def script_blocks(text: str) -> list[str]:
    """Return the contents of every <script> block; any script with a src attr fails here."""
    blocks: list[str] = []
    for m in re.finditer(r"<script\b([^>]*)>(.*?)</script>", text, re.I | re.S):
        if (m.group(1) or "").strip():
            raise ValueError("script tag carries attributes (src would load external code)")
        blocks.append(m.group(2))
    return blocks


def main() -> int:
    errors: list[str] = []
    # ---- dataset integrity
    statuses = Counter(r["status"] for r in D["rows"])
    for i, r in enumerate(D["rows"], 1):
        if r["source"] not in SOURCES:
            errors.append(f"row {i}: unknown source {r['source']}")
        if r["status"] not in ("Verified", "Derived", "Analysis", "Blank"):
            errors.append(f"row {i}: bad status {r['status']}")
        if r["status"] == "Blank" and r["value"] != "":
            errors.append(f"row {i}: unverified value is not blank")
        if r["status"] != "Blank" and r["value"] == "":
            errors.append(f"row {i}: non-blank row has an empty value")
    for k, s in SOURCES.items():
        if urlparse(s["url"]).scheme != "https":
            errors.append(f"source {k}: not https")

    # ---- published file integrity
    all_ids: dict[str, set[str]] = {}
    nav_targets = {p["file"] for p in PAGES}
    for p in PUBLISHED:
        text = p.read_text(encoding="utf-8")
        low = text.lower()
        is_offline_page = p.name == OFFLINE_SCRIPT_PAGE
        for token in (FORBIDDEN_WITH_SCRIPT_ALLOWED if is_offline_page else FORBIDDEN):
            if token in low:
                errors.append(f"{p.name}: forbidden token {token!r}")
        if is_offline_page:
            try:
                blocks = script_blocks(text)
            except ValueError as exc:
                errors.append(f"{p.name}: offline-script gate: {exc}")
                blocks = []
            if not blocks:
                errors.append(f"{p.name}: offline-script gate: expected one inline calculator script")
            for i, block in enumerate(blocks, 1):
                bl = block.lower()
                for token in SCRIPT_FORBIDDEN:
                    if token in bl:
                        errors.append(f"{p.name}: offline-script gate: script block {i} contains {token!r}")
            if PRIVACY_NOTICE_MARKER not in low:
                errors.append(f"{p.name}: offline-script gate: privacy notice text missing")
        for label, pat in PII.items():
            for m in pat.finditer(text):
                errors.append(f"{p.name}: PII {label}: {m.group(0)[:60]!r}")
        if p.suffix != ".html":
            continue
        parser = PageParser(p.name)
        parser.feed(text)
        all_ids[p.name] = parser.ids
        for row in parser.rows:
            if not any(u in OFFICIAL_URLS for u in row):
                errors.append(f"{p.name}: table row without official source link: {row[:3]}")
        for u in parser.external:
            parsed = urlparse(u)
            if parsed.scheme != "https" or parsed.netloc not in OFFICIAL_HOSTS:
                errors.append(f"{p.name}: unapproved external link {u}")
        for target in parser.links:
            if target and unquote(target) not in PUBLISHED_NAMES:
                errors.append(f"{p.name}: broken internal link {target}")
        for pid, title, _f, _g in [(x["id"], x["title"], x["file"], x["group"]) for x in PAGES]:
            if f'href="{pid}.html"' not in text:
                errors.append(f"{p.name}: shared navigation missing {pid}.html")
        for anchor in parser.internal:
            frag = anchor[1:]
            if frag and frag not in parser.ids:
                errors.append(f"{p.name}: unresolved fragment #{frag}")

    # ---- determinism
    before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in PUBLISHED}
    subprocess.run([sys.executable, str(ROOT / "scripts/build_canonical.py")],
                   cwd=str(ROOT), check=True, capture_output=True)
    for p in PUBLISHED:
        if hashlib.sha256(p.read_bytes()).hexdigest() != before[p.name]:
            errors.append(f"{p.name}: non-deterministic rebuild changed the file")

    if errors:
        print(f"FAIL — {len(errors)} problem(s):")
        for e in errors[:60]:
            print("  -", e)
        return 1
    print(f"PASS: {len(D['rows'])} evidence rows ({statuses['Verified']} verified, "
          f"{statuses['Derived']} derived, {statuses['Analysis']} analysis, {statuses['Blank']} blank); "
          f"{len(PUBLISHED)} published files; {len(OFFICIAL_HOSTS)} official hosts; "
          f"row provenance, links, PII and deterministic rebuild all clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
