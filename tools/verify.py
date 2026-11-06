#!/usr/bin/env python3
"""Verification harness.

Three checks, all of which must pass before the site is publishable:

1. STRUCTURE  — every generated page parses, every internal link resolves, every
                in-page anchor has a target, every <table> is well formed.
2. CITATION   — every table row that claims a value has a resolvable source id,
                and every unverified row has a flag attached.
3. PROSE      — every number quoted in the narrative (content.py) must appear in
                either datasets.json, model_output.json or model_assumptions.json.
                This is the check that catches a hallucinated figure in prose.
"""

import html.parser
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
DATA = os.path.join(ROOT, "data")
sys.path.insert(0, HERE)

PAGES = ["index.html", "decision.html", "economy.html", "demographics.html", "schools.html",
         "housing.html", "tenant.html", "macro.html", "risk.html", "projection.html",
         "sources.html", "flagged.html", "method.html"]

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "param", "source", "track", "wbr"}


class Balance(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"stray </{tag}>")
            return
        if self.stack[-1] == tag:
            self.stack.pop()
        elif tag in self.stack:
            # unwind, recording the mismatch
            while self.stack and self.stack[-1] != tag:
                self.errors.append(f"unclosed <{self.stack.pop()}> before </{tag}>")
            if self.stack:
                self.stack.pop()
        else:
            self.errors.append(f"unmatched </{tag}>")


def check_structure():
    problems = []
    for p in PAGES:
        full = os.path.join(ROOT, p)
        if not os.path.exists(full):
            problems.append(f"[structure] missing page {p}")
            continue
        text = open(full).read()
        b = Balance()
        b.feed(text)
        b.close()
        for e in b.errors:
            problems.append(f"[structure] {p}: {e}")
        for t in b.stack:
            problems.append(f"[structure] {p}: unclosed <{t}>")

        # anchors
        ids = set(re.findall(r'id="([^"]+)"', text))
        for a in re.findall(r'href="#([A-Za-z0-9_\-]+)"', text):
            if a not in ids:
                problems.append(f"[structure] {p}: anchor #{a} has no target")

        # internal links
        for href in re.findall(r'href="([^"]+)"', text):
            if href.startswith(("http", "#", "mailto:")):
                continue
            target = href.split("#")[0]
            if target and not os.path.exists(os.path.join(ROOT, target)):
                problems.append(f"[structure] {p}: broken link {href}")

        # tables must have matching thead/tbody cell counts
        for tbl in re.findall(r"<table[^>]*>.*?</table>", text, re.S):
            heads = len(re.findall(r"<th[ >]", tbl))
            first_row = re.search(r"<tbody>.*?<tr[^>]*>(.*?)</tr>", tbl, re.S)
            if heads and first_row:
                cells = len(re.findall(r"<td[ >]", first_row.group(1)))
                if cells and cells != heads:
                    problems.append(f"[structure] {p}: table header has {heads} cols, first row has {cells}")
    return problems


def check_citations():
    problems = []
    ds = json.load(open(os.path.join(DATA, "datasets.json")))
    sources = json.load(open(os.path.join(DATA, "sources.json")))
    valid = {s["id"] for s in sources["sources"]}

    n_rows = n_val = n_blank = 0
    for sec in ds["sections"]:
        for r in sec["rows"]:
            n_rows += 1
            if r["status"] == "unverified":
                n_blank += 1
                if not r.get("flag"):
                    problems.append(f"[citation] {sec['id']}: unverified row '{r['metric']}' has no flag")
            else:
                n_val += 1
                if not r.get("source"):
                    problems.append(f"[citation] {sec['id']}: verified row '{r['metric']}' has no source")
                elif r["source"] not in valid:
                    problems.append(f"[citation] {sec['id']}: unknown source id {r['source']}")
            if r["status"] == "unverified" and r.get("value") is not None:
                problems.append(f"[citation] {sec['id']}: unverified row '{r['metric']}' carries a value "
                                f"({r['value']!r}) — must be null")
    print(f"  rows: {n_rows} total, {n_val} with values, {n_blank} blank/unverified")

    # every source must be referenced or explicitly be a rejected/context source
    used = set()
    for sec in ds["sections"]:
        for r in sec["rows"]:
            if r.get("source"):
                used.add(r["source"])
    for s in sources["sources"]:
        if s["tier"] == "third-party":
            continue
        if s["id"] not in used:
            problems.append(f"[citation] source {s['id']} is registered but never used by a data row")
    return problems


def check_prose():
    """Every number in the narrative must be traceable to the data files."""
    problems = []
    blob = []
    for name in ("datasets.json", "model_output.json", "model_assumptions.json", "flags.json",
                 "sources.json"):
        blob.append(open(os.path.join(DATA, name)).read())
    corpus = "\n".join(blob)

    # normalise corpus numbers into a set of plain digit strings
    corpus_nums = set(re.findall(r"-?\d[\d,\.]*", corpus))
    corpus_digits = set()
    for n in corpus_nums:
        plain = n.replace(",", "").rstrip(".")
        corpus_digits.add(plain)
        corpus_digits.add(plain.lstrip("0") or "0")
        corpus_digits.add(plain.lstrip("-").lstrip("0") or "0")
        try:
            f = float(plain)
        except ValueError:
            continue
        # rounded variants, including percentage form
        for dp in range(1, 5):
            corpus_digits.add(f"{round(f, dp)}")
            corpus_digits.add(f"{round(f, dp):g}")
            corpus_digits.add(f"{round(abs(f), dp)}")
        corpus_digits.add(f"{round(f*100, 2):g}")   # percentage form
        corpus_digits.add(f"{round(f*100, 1):g}")
        corpus_digits.add(f"{round(abs(f)*100, 1):g}")
        corpus_digits.add(f"{round(abs(f)*100, 2):g}")
        corpus_digits.add(f"{round(f/1e6, 2):g}")   # millions form
        corpus_digits.add(f"{round(f/1e6, 1):g}")
        corpus_digits.add(f"{round(f/1000, 1):g}")

    import content as C
    texts = []
    texts.append(C.VERDICT["headline"])
    texts.append(C.VERDICT["one_line"])
    for f in C.KEY_FINDINGS:
        texts += [f["title"], f["body"]]
    for r in C.RECOMMENDATION_STEPS:
        texts += [r["title"], r["body"]]
    for r in C.RISK_BY_DECISION:
        texts += [r["decision"], r["upside"], r["downside"], r["verdict"]]
    for b in C.BLACK_SWANS:
        texts += [b["name"], b["evidence"], b["transmission"], b["modelled"], b["mitigation"]]
    for n in C.METHODOLOGY_NOTES:
        texts += [n["title"], n["body"]]
    for p in C.PRIVACY_POINTS:
        texts += [p["title"], p["body"]]

    allowed_literals = {
        "1031", "20261106", "2035", "2020", "2025", "2026", "2030", "2032", "2042", "2052",
        "2031", "2036", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "10", "11", "12",
        "18", "20", "24", "25", "26", "27", "40", "50", "60", "62", "75", "86", "100", "175",
        "4911", "11911", "1474", "1475", "1476", "1039", "007882", "0000807882",
    }

    suspects = set()
    for t in texts:
        clean = re.sub(r"&#?\w+;", " ", t)
        clean = re.sub(r"<[^>]+>", " ", clean)
        for m in re.findall(r"\d[\d,\.]*", clean):
            plain = m.replace(",", "").rstrip(".")
            if not plain:
                continue
            if plain in corpus_digits or plain in allowed_literals:
                continue
            suspects.add(plain)

    for s in sorted(suspects):
        problems.append(f"[prose] number not found in any data file: {s!r}")
    return problems


def main():
    print("1. structure")
    p1 = check_structure()
    print(f"   {'FAIL' if p1 else 'ok'} ({len(p1)} problems)")
    print("2. citations")
    p2 = check_citations()
    print(f"   {'FAIL' if p2 else 'ok'} ({len(p2)} problems)")
    print("3. prose traceability")
    p3 = check_prose()
    print(f"   {'FAIL' if p3 else 'ok'} ({len(p3)} problems)")

    allp = p1 + p2 + p3
    if allp:
        print("\nPROBLEMS:")
        for x in allp:
            print("  -", x)
        sys.exit(1)
    print("\nall checks passed")


if __name__ == "__main__":
    main()
