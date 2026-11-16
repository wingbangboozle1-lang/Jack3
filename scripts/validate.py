#!/usr/bin/env python3
"""Validate the canonical published site. Dependency-free (stdlib only).

Enforced:
  1. Every evidence row has a status, a source key and an official https URL.
  2. Unverified (Blank) rows have an empty value.
  3. Every <tbody> <tr> in every published HTML file contains an official source link.
  4. Every external link is https and on an approved official host.
  5. Every internal link and fragment resolves inside the published artifact.
  6. Every page carries the shared navigation, and no page links to a missing file.
  7. No tracking, remote scripts, forms, localhost or http:// links. Exactly one self-contained inline calculator script is allowed on private-calculator.html; its CSP and source are checked for network/storage APIs.
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
FORBIDDEN = ("<iframe", "<form", "googletagmanager", "google-analytics",
             "localhost", "127.0.0.1", "http://", "onclick=", "onerror=")
PRIVATE_CALCULATOR = "private-calculator.html"
NETWORK_APIS = tuple(re.compile(pattern, re.I) for pattern in (
    r"\bfetch\s*\(", r"\bXMLHttpRequest\b", r"\bWebSocket\b",
    r"\bEventSource\b", r"\bsendBeacon\b", r"\blocalStorage\b",
    r"\bsessionStorage\b", r"\bindexedDB\b", r"document\s*\.\s*cookie",
    r"\bserviceWorker\b", r"\bWorker\s*\("
))


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
        self.tags: set[str] = set()
        self.scripts: list[str] = []
        self.script_srcs: list[str] = []
        self.resource_srcs: list[str] = []
        self.inputs: list[dict[str, str | None]] = []
        self.meta_csp: list[str] = []
        self.event_handlers: list[str] = []
        self._script_parts: list[str] | None = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.add(tag)
        self.event_handlers.extend(k for k in a if k.lower().startswith("on"))
        if tag == "input":
            self.inputs.append(a)
        if tag == "meta" and a.get("http-equiv", "").lower() == "content-security-policy":
            self.meta_csp.append(a.get("content", ""))
        if tag == "script":
            self._script_parts = []
            if a.get("src"):
                self.script_srcs.append(a["src"])
        if a.get("src"):
            self.resource_srcs.append(a["src"])
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

    def handle_data(self, data):
        if self._script_parts is not None:
            self._script_parts.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._script_parts is not None:
            self.scripts.append("".join(self._script_parts))
            self._script_parts = None
        if tag == "tr" and self.row is not None:
            self.rows.append(self.row)
            self.row = None
        if tag == "tbody":
            self.in_tbody = False


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
        for token in FORBIDDEN:
            if token in low:
                errors.append(f"{p.name}: forbidden token {token!r}")
        for label, pat in PII.items():
            for m in pat.finditer(text):
                errors.append(f"{p.name}: PII {label}: {m.group(0)[:60]!r}")
        if p.suffix != ".html":
            continue
        parser = PageParser(p.name)
        parser.feed(text)
        all_ids[p.name] = parser.ids
        if p.name == PRIVATE_CALCULATOR:
            required_ids = {
                "horizon-years", "discount-rate", "sale-gross", "sale-costs", "sale-transfer",
                "sale-debt", "sale-tax", "sale-other", "hold-annual-net", "hold-terminal-net",
                "renew-annual-net", "renew-terminal-net",
            }
            input_ids = {a.get("id") for a in parser.inputs}
            if len(parser.scripts) != 1 or parser.script_srcs:
                errors.append(f"{p.name}: expected exactly one inline script and no external scripts")
            if input_ids != required_ids or len(parser.inputs) != len(required_ids):
                errors.append(f"{p.name}: calculator fields differ from the reviewed blank-input set")
            if any("value" in a or "name" in a or a.get("autocomplete") != "off" for a in parser.inputs):
                errors.append(f"{p.name}: calculator inputs must be unnamed, blank by default, and autocomplete-off")
            if parser.resource_srcs:
                errors.append(f"{p.name}: self-contained calculator has an external resource: {parser.resource_srcs}")
            if parser.event_handlers:
                errors.append(f"{p.name}: inline event handler is not allowed")
            policy = " ".join(parser.meta_csp).lower()
            required_directives = ("default-src 'none'", "style-src 'unsafe-inline'", "script-src 'unsafe-inline'",
                                   "connect-src 'none'", "img-src 'none'", "object-src 'none'",
                                   "form-action 'none'", "base-uri 'none'")
            for directive in required_directives:
                if directive not in policy:
                    errors.append(f"{p.name}: missing restrictive CSP directive {directive}")
            script = parser.scripts[0] if parser.scripts else ""
            for pattern in NETWORK_APIS:
                if pattern.search(script):
                    errors.append(f"{p.name}: prohibited network/storage API {pattern.pattern}")
            source_js = (ROOT / "scripts/private_calculator.js").read_text(encoding="utf-8").strip()
            if script.strip() != source_js:
                errors.append(f"{p.name}: embedded calculator differs from its reviewed source")
        elif parser.scripts or parser.inputs:
            errors.append(f"{p.name}: scripts and user inputs are restricted to {PRIVATE_CALCULATOR}")
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
