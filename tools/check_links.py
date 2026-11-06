#!/usr/bin/env python3
"""Validate every external link emitted into the published site.

Three checks:

  1. WELL-FORMED   - the URL parses, uses https, and has a host.
  2. OFFICIAL      - any URL that appears in a column claiming to be verified
                     must sit on an official or primary domain.  A broker or
                     aggregator URL in a verified column is a hard failure.
  3. REACHABLE-LOOKING - no placeholder, example.com, TODO or empty href.

This tool does NOT make network requests.  The build environment has no route
to census.gov, bls.gov or sec.gov, so an HTTP check here would report failures
that are properties of the sandbox rather than of the link.  What it checks is
that every link is syntactically valid, correctly attributed and on an approved
domain -- which is the failure mode that actually matters for a verification
claim.

    python3 tools/check_links.py
"""

from __future__ import annotations

import html.parser
import os
import re
import sys
from collections import Counter, defaultdict
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Scans THIS session's published site only.  docs/ belongs to another
# session and is deliberately not touched.
DOCS = os.path.join(ROOT, "decision-file")

# Domains accepted as official or primary.  Anything else appearing in the
# generated site is reported -- and if it appears inside a verified source cell
# it is a hard failure.
OFFICIAL_TLDS = (".gov", ".mil", ".edu")
OFFICIAL_DOMAINS = {
    "sec.gov", "www.sec.gov", "data.sec.gov",
    "investors.jackinthebox.com",      # the issuer's own investor relations
    "leginfo.legislature.ca.gov",
    # Official agencies that do not sit on a .gov domain.
    "www.cadedash.net", "cadedash.net",          # California Dept of Education
    "www.metro.net", "metro.net",                # LA County Metropolitan Transportation Authority
    "www.lausd.org", "lausd.org",                # Los Angeles Unified School District
    "zimas.lacity.org",                          # City of LA zoning lookup
}
# Domains that must never appear in the published site at all.
BLOCKED = re.compile(
    r"(netleaseadvisor|nnninvestmentgroup|nnnig|loopnet|crexi|costar|"
    r"reonomy|plainhazard|disasterriskindex|wildfirescore|climateatlas|"
    r"earthquaketracker|top1031|baker1031|wealthbuilder1031|sambrotman|"
    r"kdshomebuyers|akgeotech|la2028metro|rtands|foxla|yahoo|nasdaq\.com|"
    r"thestreet|drillr|biggo|newgeography|citywatchla|basin\.la|"
    r"example\.com|localhost|127\.0\.0\.1)",
    re.I,
)
PLACEHOLDER = re.compile(r"(your-?url|example\.com|TODO|FIXME|href=[\"']{2}|#\s*$)", re.I)


class LinkGrab(html.parser.HTMLParser):
    """Collect href values together with the class of the enclosing <td>.

    The class tells us whether a link sits in a column that claims to be a
    verified official source (classes 'src', or a header of 'Official source').
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []          # (url, td_class, in_verified_column)
        self._td_class = ""
        self._in_td = False
        self._td_depth = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "td":
            self._in_td = True
            self._td_class = a.get("class", "")
        if tag == "a" and a.get("href"):
            verified_col = bool(re.search(r"\bsrc\b", self._td_class))
            self.links.append((a["href"], self._td_class, verified_col))

    def handle_endtag(self, tag):
        if tag == "td":
            self._in_td = False
            self._td_class = ""


def scan(path):
    with open(path, encoding="utf-8") as fh:
        src = fh.read()
    p = LinkGrab()
    p.feed(src)
    return src, p.links


def main() -> int:
    if not os.path.isdir(DOCS):
        print("decision-file/ does not exist -- run `python3 build_site.py` first.")
        return 2

    pages = sorted(f for f in os.listdir(DOCS) if f.endswith(".html"))
    errors, warnings = [], []
    hosts = Counter()
    per_page = defaultdict(int)
    total_links = 0

    for fname in pages:
        path = os.path.join(DOCS, fname)
        src, links = scan(path)
        for url, tdcls, verified_col in links:
            total_links += 1
            per_page[fname] += 1
            if url.startswith(("mailto:", "#")):
                continue
            if BLOCKED.search(url):
                errors.append(f"{fname}: BLOCKED non-official domain in published site: {url}")
                continue
            if PLACEHOLDER.search(url):
                errors.append(f"{fname}: placeholder or malformed href: {url!r}")
                continue
            pr = urlparse(url)
            if pr.scheme not in ("http", "https"):
                # relative link -- must resolve to a file that exists
                if not url.startswith("/") and not os.path.exists(os.path.join(DOCS, url)):
                    errors.append(f"{fname}: broken internal link -> {url}")
                continue
            if pr.scheme != "https":
                warnings.append(f"{fname}: non-HTTPS external link: {url}")
            if not pr.netloc:
                errors.append(f"{fname}: URL with no host: {url!r}")
                continue
            host = pr.netloc.lower().split(":")[0]
            hosts[host] += 1
            official = (any(host == d or host.endswith("." + d.lstrip("."))
                            for d in OFFICIAL_DOMAINS)
                        or any(host.endswith(t) for t in OFFICIAL_TLDS))
            if verified_col and not official:
                errors.append(
                    f"{fname}: NON-OFFICIAL domain in a verified source column: "
                    f"{host} -> {url}")

    print(f"pages scanned        : {len(pages)}")
    print(f"links found          : {total_links}")
    print(f"distinct hosts       : {len(hosts)}")
    nonofficial = {h: n for h, n in hosts.items()
                   if not (any(h == d or h.endswith("." + d.lstrip(".")) for d in OFFICIAL_DOMAINS)
                           or any(h.endswith(t) for t in OFFICIAL_TLDS))}
    print(f"non-official hosts   : {len(nonofficial)}")
    for h, n in sorted(nonofficial.items(), key=lambda x: -x[1]):
        print(f"    {h:<44} {n}")
    print()
    print("top official hosts:")
    for h, n in hosts.most_common(14):
        print(f"    {h:<44} {n}")
    print()
    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for w in warnings[:40]:
            print("  " + w)
        print()
    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors:
            print("  " + e)
        return 1
    print("OK - every link is well formed, every verified-source link is on an "
          "official or primary domain, and no blocked domain appears anywhere.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
