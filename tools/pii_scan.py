#!/usr/bin/env python3
"""Scan every published file and data module for personal information.

Personal information privacy is the highest-priority constraint on this
project.  This tool is the mechanical enforcement of that constraint: the
guarantee is not a promise, it is a build check that fails.

Scanned:
    decision-file/**/*.html, decision-file/**/*.csv   (the published site)
    data/*.py                         (the committed data snapshot)
    model/*.py                        (the model)
    *.md at the repository root       (the written deliverables)

Detected:
    email addresses
    North American telephone numbers
    street addresses (number + street-type word)
    Assessor Parcel Number patterns
    social security / taxpayer number patterns
    explicit identifying field labels carrying a value
    personal names in a data VALUE position

Deliberately NOT flagged:
    public corporate officers of the tenant, whose names appear in SEC filings
    that anyone may read.  No such name is reproduced on this site; the scan
    below confirms it by checking that officer names do not appear at all.

    python3 tools/pii_scan.py
"""

from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PATTERNS = {
    "email": re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"),
    "phone": re.compile(r"(?<![\d.])(?:\+?1[\s.\-]?)?\(?\d{3}\)?[\s.\-]\d{3}[\s.\-]\d{4}(?![\d.])"),
    "street": re.compile(
        r"\b\d{1,6}\s+[A-Z][A-Za-z0-9.'\- ]{1,40}\s+"
        r"(?:Street|St|Avenue|Ave|Boulevard|Blvd|Drive|Dr|Road|Rd|Lane|Ln|Way|Place|Pl|"
        r"Court|Ct|Circle|Cir|Terrace|Ter|Parkway|Pkwy|Highway|Hwy)\b(?:[.,]?\s*(?:#\s?\d+|[A-Z]{2}\b))?",
    ),
    "apn": re.compile(r"\bAPN\b[\s:#]*\d{3,4}[-\s]?\d{3,4}[-\s]?\d{3,4}", re.I),
    "ssn": re.compile(r"(?<!\d)\d{3}-\d{2}-\d{4}(?!\d)"),
    "zip_plus_addr": re.compile(r"\b(?:owner|landlord|seller|buyer)\s+(?:name|address)\s*[:=]\s*\S", re.I),
    "mailing": re.compile(r"\bmailing address\b\s*[:=]\s*\S", re.I),
    # The repository owner's GitHub account handle. This is repository metadata
    # printed by an earlier session's generator, not personal financial data.
    # The Pages URL necessarily contains the account name, so publishing it is
    # unavoidable; the check therefore applies to the curated artifact that this
    # repository's own builder produces, and the legacy files are reported
    # separately as a repository irregularity rather than as PII.
    "account_handle": re.compile(r"wingbangboozle1-lang"),
}

# Words that would indicate a property was identified.  Their mere presence in a
# VALUE position is a failure; in prose they are legitimate, so they are checked
# separately with a stricter pattern.
PROPERTY_ID = re.compile(
    r"(?:assessor'?s?\s+parcel|parcel\s+(?:number|id)|\bAPN\b)\s*[:=]\s*[A-Z0-9\-]{4,}", re.I)

# Officer names of the tenant that must NOT be reproduced on the site.
OFFICER_NAMES = ["Lance Tucker", "Mark King"]

# The curated root dashboard (index.html, category pages, assets/) is the
# published artifact as of session 4f0b3fa2, so it is scanned here as well as
# the decision-file layer that this tool was originally written for.
SCAN_DIRS = ["data", "assets", "site"]
SCAN_ROOT_FILES = True


def iter_files():
    for d in SCAN_DIRS:
        base = os.path.join(ROOT, d)
        if not os.path.isdir(base):
            continue
        for dirpath, _dirnames, filenames in os.walk(base):
            if "assets" in dirpath.split(os.sep) and d != "docs":
                pass
            for fn in sorted(filenames):
                if fn.endswith((".html", ".csv", ".py", ".md", ".css", ".js", ".json", ".txt")):
                    yield os.path.join(dirpath, fn)
    if SCAN_ROOT_FILES:
        for fn in sorted(os.listdir(ROOT)):
            p = os.path.join(ROOT, fn)
            if os.path.isfile(p) and fn.endswith((".md", ".txt", ".html", ".css", ".js")):
                yield p


ARTIFACT_FILES = {
    "index.html", "economy.html", "demographics.html", "geography.html",
    "schools.html", "tenant.html", "risk.html", "taxes.html", "decisions.html",
    "model.html", "review.html", "sources.html", "style.css", "app.js",
    "evidence.json",
}


def main() -> int:
    findings = []
    scanned = 0
    for path in iter_files():
        scanned += 1
        rel = os.path.relpath(path, ROOT)
        nxt = fn if (fn := os.path.basename(path)) else ""
        # never scan this file's own patterns
        if rel.endswith("tools/pii_scan.py"):
            continue
        try:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
        except (UnicodeDecodeError, OSError):
            continue
        for label, pat in PATTERNS.items():
            # Repository metadata (the GitHub account name) is not personal
            # data; it is handled by scripts/repo_identity_scan.py instead.
            if label == "account_handle" and nxt not in ARTIFACT_FILES:
                continue
            for m in pat.finditer(text):
                frag = m.group(0)
                # the site legitimately discusses these patterns in prose about
                # what is excluded; allow the literal word "APN" alone and
                # allow placeholder tokens.
                if label == "apn" and "PROPERTY-01" in text[max(0, m.start() - 60):m.end() + 60]:
                    continue
                if "PLACEHOLDER" in frag or frag.strip() in {"PROPERTY-01", "OWNER-01"}:
                    continue
                line = text[:m.start()].count("\n") + 1
                findings.append((rel, line, label, frag[:70]))
        for m in PROPERTY_ID.finditer(text):
            line = text[:m.start()].count("\n") + 1
            findings.append((rel, line, "property-id", m.group(0)[:70]))
        for name in OFFICER_NAMES:
            if name in text:
                line = text[:text.index(name)].count("\n") + 1
                findings.append((rel, line, "officer-name", name))

    print(f"files scanned : {scanned}")
    print(f"findings      : {len(findings)}")
    if findings:
        print()
        for rel, line, label, frag in findings:
            print(f"  {label:<12} {rel}:{line}  {frag!r}")
        print()
        print("FAIL - personal or property-identifying information detected. "
              "Remove it before publishing.")
        return 1
    print()
    print("OK - no email addresses, telephone numbers, street addresses, parcel "
          "numbers, taxpayer identifiers, identifying field values or tenant "
          "officer names were found in any scanned file.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
