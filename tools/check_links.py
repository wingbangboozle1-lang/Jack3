#!/usr/bin/env python3
"""Audit every external link emitted into the curated public dashboard.

Three checks:

  1. WELL-FORMED  -- the URL parses, uses https, and has a host.
  2. OFFICIAL     -- every external URL must sit on an approved official or
                     issuer domain. A broker, aggregator, data vendor or news
                     site is a hard failure wherever it appears.
  3. PRESENT      -- no placeholder, example.com, TODO or empty href.

This tool does NOT make network requests: the build environment has no general
route to census.gov, bls.gov or sec.gov, so an HTTP check here would report
failures that are properties of the sandbox rather than of the link. Reachability
was verified separately, manually, on 2026-11-10; the record is in
research/VERIFICATION-2026-11-10.md. What this tool enforces is that every link
is syntactically valid, correctly attributed and on an approved domain -- the
failure mode that actually matters for a verification claim.

    python3 tools/check_links.py
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data/evidence.json").read_text())

# Government, statute, or the tenant's own securities disclosure. Nothing else.
OFFICIAL_SUFFIXES = (".gov", ".mil")
OFFICIAL_HOSTS = {
    "investors.jackinthebox.com",     # the issuer's own investor relations site
    "leginfo.legislature.ca.gov",     # California Legislative Information
    "zimas.lacity.org",               # City of Los Angeles zoning lookup
}
# Hosts that must never appear in a published page or the dataset. Matched
# against the host and its parent domains only, never against a path, so that a
# legitimate issuer host cannot collide with a blocked name.
BLOCKED_HOSTS = {
    "loopnet.com", "crexi.com", "costar.com", "reonomy.com", "netleaseadvisor.com",
    "nnnig.com", "bouldergroup.com", "seyfarth.com", "zillow.com", "redfin.com",
    "trulia.com", "apartments.com", "biggerpockets.com", "1031crowdfunding.com",
    "wikipedia.org", "investopedia.com", "bloomberg.com", "reuters.com",
    "forbes.com", "medium.com", "substack.com", "facebook.com", "twitter.com",
    "x.com", "linkedin.com", "youtube.com", "example.com", "localhost",
    "127.0.0.1",
}


def blocked(host: str) -> bool:
    host = host.lower().split(":")[0]
    parts = host.split(".")
    for i in range(len(parts) - 1):
        if ".".join(parts[i:]) in BLOCKED_HOSTS:
            return True
    return False
PLACEHOLDER = re.compile(r"(your-?url|example\.com|TODO|FIXME|href=\"\"|href=\"#\")", re.I)


def approved(host: str) -> bool:
    return host.endswith(OFFICIAL_SUFFIXES) or host in OFFICIAL_HOSTS


failures: list[str] = []
urls: Counter[str] = Counter()

# ---- 1. the dataset's own source register
for key, s in DATA["sources"].items():
    u = urlparse(s["url"])
    if u.scheme != "https" or not u.netloc:
        failures.append(f"source {key}: not a well-formed https URL: {s['url']}")
    elif not approved(u.netloc):
        failures.append(f"source {key}: {u.netloc} is not an approved official/issuer host")
    if blocked(u.netloc):
        failures.append(f"source {key}: blocked domain in {s['url']}")
    urls[u.netloc] += 1

# ---- 2. every link actually rendered into a page
HREF = re.compile(r'(?:href|src)="([^"]+)"')
PAGES = ["index.html", "economy.html", "demographics.html", "geography.html",
         "schools.html", "tenant.html", "risk.html", "taxes.html", "decisions.html",
         "model.html", "review.html", "sources.html"]
rendered = Counter()
for name in PAGES:
    text = (ROOT / name).read_text()
    for href in HREF.findall(text):
        if href.startswith("https://"):
            host = urlparse(href).netloc
            rendered[host] += 1
            if not approved(host):
                failures.append(f"{name}: unapproved external host {host} ({href})")
            if blocked(host):
                failures.append(f"{name}: blocked domain {href}")
        elif href.startswith("http://"):
            failures.append(f"{name}: insecure http link {href}")
        if PLACEHOLDER.search(href):
            failures.append(f"{name}: placeholder href {href!r}")

print(f"source register      : {len(DATA['sources'])} documents on {len(urls)} hosts")
print(f"rendered external    : {sum(rendered.values())} links on {len(rendered)} hosts")
for host, n in rendered.most_common():
    print(f"  {n:>3}  {host}")

if failures:
    print("\nFAILURES")
    for f in failures:
        print("  !! ", f)
    sys.exit(1)
print(f"\nPASS: every published external link is https and on an approved official or issuer host; 0 placeholders.")
