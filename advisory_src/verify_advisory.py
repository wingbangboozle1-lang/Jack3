"""Strict automated verifier for `/advisory/` and `/advisory_src/`.

Session: e04af39b (arena/e04af39b-jack3)
"""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ADV_DIR = ROOT / "advisory"

ALLOWED_OFFICIAL_DOMAINS = {
    "www.census.gov",
    "www.bls.gov",
    "www.cde.ca.gov",
    "dq.cde.ca.gov",
    "www.caschooldashboard.org",
    "www.dir.ca.gov",
    "wagesla.lacity.gov",
    "www.federalreserve.gov",
    "home.treasury.gov",
    "www.sec.gov",
    "investors.jackinthebox.com",
    "finance.lacity.gov",
    "www.lavote.gov",
    "assessor.lacounty.gov",
    "www.boe.ca.gov",
    "www.irs.gov",
    "www.ftb.ca.gov",
    "www.usgs.gov",
    "www.conservation.ca.gov",
    "osfm.fire.ca.gov",
    "file.lacounty.gov",
    "www.congress.gov",
    "www.insurance.ca.gov",
    "msc.fema.gov",
    "planning.lacity.gov",
    "www.metro.net",
    "zimas.lacity.org",
    "dot.ca.gov",
    "ewdd.lacity.gov",
    "scag.ca.gov",
    "dof.ca.gov",
}

FORBIDDEN_SUBSTRINGS = [
    "<script",
    "<iframe",
    "localhost",
    "127.0.0.1",
    "googletagmanager.com",
    "9357" + " Spectrum",
]

PII_PATTERNS = [
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),  # email
    re.compile(r"\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b"),                 # US phone
    re.compile(r"\b\d{4}-\d{3}-\d{3}\b"),                           # LA County AIN/APN format
    re.compile("wingbang" + "boozle", re.IGNORECASE),               # repo handle check
]


class PageAuditParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_tbody = False
        self.in_tr = False
        self.in_td = False
        self.td_class = ""
        self.td_text_parts: list[str] = []
        self.tr_links: list[str] = []
        self.tr_text_parts: list[str] = []
        self.tr_has_blank_cell = False
        self.tbody_rows: list[tuple[list[str], str, bool]] = []
        self.all_hrefs: list[str] = []
        self.blank_cell_nonempty_errors: int = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        ad = dict(attrs)
        if tag == "tbody":
            self.in_tbody = True
        elif tag == "tr" and self.in_tbody:
            self.in_tr = True
            self.tr_links = []
            self.tr_text_parts = []
            self.tr_has_blank_cell = False
        elif tag == "td" and self.in_tr:
            self.in_td = True
            self.td_class = ad.get("class") or ""
            self.td_text_parts = []
            if "blank-cell" in self.td_class:
                self.tr_has_blank_cell = True
        elif tag in ("a", "link"):
            href = ad.get("href")
            if href:
                self.all_hrefs.append(href)
                if self.in_tr and tag == "a":
                    self.tr_links.append(href)

    def handle_data(self, data: str) -> None:
        if self.in_tr:
            self.tr_text_parts.append(data)
        if self.in_td:
            self.td_text_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "td" and self.in_td:
            if "blank-cell" in self.td_class and "".join(self.td_text_parts).strip() != "":
                self.blank_cell_nonempty_errors += 1
            self.in_td = False
        elif tag == "tr" and self.in_tr:
            self.tbody_rows.append((self.tr_links[:], " ".join(self.tr_text_parts), self.tr_has_blank_cell))
            self.in_tr = False
        elif tag == "tbody":
            self.in_tbody = False


def main() -> int:
    errors: list[str] = []
    html_files = sorted(ADV_DIR.glob("*.html"))
    if len(html_files) != 12:
        errors.append(f"Expected 12 HTML files in {ADV_DIR}, found {len(html_files)}")

    css_file = ADV_DIR / "assets" / "style.css"
    if not css_file.is_file():
        errors.append("Missing advisory/assets/style.css")

    total_rows = 0
    total_blank_rows = 0

    for f in list(ADV_DIR.rglob("*")):
        if not f.is_file():
            continue
        raw = f.read_text(encoding="utf-8")
        if raw.startswith("---"):
            errors.append(f"{f.relative_to(ROOT)}: starts with YAML front matter '---' (breaks Jekyll byte-exact check)")
        for bad in FORBIDDEN_SUBSTRINGS:
            if bad.lower() in raw.lower():
                errors.append(f"{f.relative_to(ROOT)}: contains forbidden substring {bad!r}")
        for pat in PII_PATTERNS:
            m = pat.search(raw)
            if m:
                errors.append(f"{f.relative_to(ROOT)}: matched PII pattern {m.group(0)!r}")

    for hf in html_files:
        p = PageAuditParser()
        p.feed(hf.read_text(encoding="utf-8"))
        if p.blank_cell_nonempty_errors:
            errors.append(f"{hf.name}: blank-cell had non-empty text ({p.blank_cell_nonempty_errors})")
        if not p.tbody_rows:
            errors.append(f"{hf.name}: contains 0 tbody rows")

        for idx, (links, row_txt, is_blank) in enumerate(p.tbody_rows, 1):
            total_rows += 1
            ext_links = [u for u in links if u.startswith("https://")]
            if not ext_links:
                errors.append(f"{hf.name} row #{idx}: missing official https:// source link")
            for u in ext_links:
                host = urlparse(u).netloc
                if host not in ALLOWED_OFFICIAL_DOMAINS:
                    errors.append(f"{hf.name} row #{idx}: non-allowlisted domain {host!r} ({u})")
            if is_blank:
                total_blank_rows += 1
                if ("Unverified" not in row_txt) and ("Needs review" not in row_txt):
                    errors.append(f"{hf.name} row #{idx}: blank cell is not marked Unverified / Needs review")

        for href in p.all_hrefs:
            if href.startswith("http://"):
                errors.append(f"{hf.name}: insecure http:// link {href}")
            elif href.startswith("https://"):
                host = urlparse(href).netloc
                if host not in ALLOWED_OFFICIAL_DOMAINS:
                    errors.append(f"{hf.name}: external href domain not allowlisted {host!r}")
            elif not href.startswith("#"):
                clean = href.split("#", 1)[0].split("?", 1)[0]
                target = (hf.parent / clean).resolve()
                if not target.exists():
                    errors.append(f"{hf.name}: broken relative link {href!r} -> {target}")

    # Also check markdown docs in advisory_src for PII
    for mf in HERE.glob("*.md"):
        txt = mf.read_text(encoding="utf-8")
        for pat in PII_PATTERNS:
            m = pat.search(txt)
            if m:
                errors.append(f"{mf.relative_to(ROOT)}: matched PII pattern {m.group(0)!r}")

    if errors:
        print("ADVISORY VERIFICATION FAILED:")
        for e in errors:
            print(" -", e)
        return 1

    print(
        f"ADVISORY VERIFICATION PASSED: {len(html_files)} HTML pages, "
        f"{total_rows} verified/analyzed table rows (100% official https:// linked), "
        f"{total_blank_rows} unconfirmed blank cells properly flagged, 0 PII, 0 <script>."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
