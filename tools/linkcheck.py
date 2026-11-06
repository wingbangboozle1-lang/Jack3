#!/usr/bin/env python3
"""Link and anchor checker for the built static site.

Fails (exit 1) on: missing local files, missing fragment anchors, empty hrefs.
Warns on: external links (not fetched; reported as a count so they can be spot-checked).
"""
import os
import re
import sys
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "analysis"))
ATTR = re.compile(r'(?:href|src)\s*=\s*"([^"]*)"')
ID = re.compile(r'id\s*=\s*"([^"]*)"')

pages = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))
ids = {}
for p in pages:
    with open(os.path.join(ROOT, p)) as fh:
        ids[p] = set(ID.findall(fh.read()))

errors = []
external = Counter()
internal = 0

for p in pages:
    with open(os.path.join(ROOT, p)) as fh:
        text = fh.read()
    for link in ATTR.findall(text):
        if not link or link.startswith("#") and link == "#":
            errors.append((p, link, "empty link"))
            continue
        if link.startswith(("http://", "https://", "mailto:")):
            external[link.split("/")[2]] += 1
            continue
        if link.startswith("#"):
            if link[1:] not in ids[p]:
                errors.append((p, link, "missing anchor in same page"))
            internal += 1
            continue
        path, _, frag = link.partition("#")
        target = os.path.normpath(os.path.join(ROOT, path))
        if not os.path.exists(target):
            errors.append((p, link, "missing file"))
            continue
        internal += 1
        if frag:
            base = os.path.basename(target)
            if base in ids and frag not in ids[base]:
                errors.append((p, link, "missing anchor in target"))

print(f"pages checked      : {len(pages)}")
print(f"internal links     : {internal}")
print(f"external links     : {sum(external.values())} to {len(external)} hosts")
for host, n in external.most_common():
    print(f"   {n:3d}  {host}")

if errors:
    print("\nFAILURES")
    for p, link, why in errors:
        print(f"  {p}: {link}  -> {why}")
    sys.exit(1)

print("\nOK — no broken internal links or anchors.")
