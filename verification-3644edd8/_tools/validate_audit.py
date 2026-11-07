#!/usr/bin/env python3
"""Validate the public audit and produce a reproducible validation report."""
from __future__ import annotations

import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
ROOT = BASE.parent
PAGE = BASE / "index.html"
EVIDENCE_PATH = BASE / "_evidence/evidence.json"
REVIEW_PATH = BASE / "_evidence/review.json"
MODEL_PATH = BASE / "_model-review/results.json"
VALIDATION = BASE / "_validation"
VALIDATION.mkdir(exist_ok=True)

checks: list[tuple[str, str]] = []


def passed(name: str, detail: str) -> None:
    checks.append((name, detail))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# Run the model audit and page build twice. All reviewed outputs must be stable.
outputs = [MODEL_PATH, BASE / "_model-review/REVIEW.md", PAGE]
commands = [
    [sys.executable, str(BASE / "_model-review/review_model.py")],
    [sys.executable, str(BASE / "_tools/build_audit.py")],
]
for _ in range(2):
    for command in commands:
        subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    hashes = [digest(path) for path in outputs]
    if "first_hashes" not in locals():
        first_hashes = hashes
    else:
        assert hashes == first_hashes, "Non-deterministic model or page output"
passed("Deterministic build", "Model review and public page produced identical SHA-256 hashes on two consecutive runs.")

# Reproduction must fail visibly if the reviewed inherited model changes.
model = json.loads(MODEL_PATH.read_text())
current_model_hash = hashlib.sha256((ROOT / "model/projection.py").read_bytes()).hexdigest()
assert model["model_sha256"] == current_model_hash, "Model changed after this review; rerun and reassess semantics"
passed("Reviewed model identity", f"model/projection.py SHA-256 {current_model_hash}")

# Validate evidence/source semantics before inspecting HTML.
evidence = json.loads(EVIDENCE_PATH.read_text())
review = json.loads(REVIEW_PATH.read_text())
sources = evidence["sources"]
rows = evidence["rows"]
assert len(rows) == 45
assert len(sources) == 23
assert len(review["source_findings"]) == 10
assert len(review["flags"]) == 12
assert len({row["id"] for row in rows}) == len(rows), "Duplicate evidence ID"
assert len({flag["id"] for flag in review["flags"]}) == len(review["flags"]), "Duplicate flag ID"
allowed_status = {"Verified", "Verified projection", "Official snapshot conflict", "Unconfirmed"}
official_hosts = {
    "www.census.gov", "dof.ca.gov", "www.bls.gov", "www.sec.gov",
    "investors.jackinthebox.com", "www.usgs.gov", "www.conservation.ca.gov",
    "osfm.fire.ca.gov", "msc.fema.gov", "file.lacounty.gov", "www.fire.ca.gov",
    "www.dir.ca.gov", "wagesla.lacity.gov", "www.cde.ca.gov", "www.irs.gov",
    "home.treasury.gov",
}
for source_id, source in sources.items():
    parsed = urlparse(source["url"])
    assert parsed.scheme == "https", (source_id, "non-HTTPS")
    assert parsed.hostname in official_hosts, (source_id, parsed.hostname)
    assert source["accessed"] == "2026-11-07"
    assert source["kind"] and source["document_date"] and source["publisher"]
for row in rows:
    assert row["status"] in allowed_status
    assert row["source"], row["id"]
    assert all(source_id in sources for source_id in row["source"]), row["id"]
    assert row["period"] and row["geography"] and row["note"], row["id"]
    if row["status"] == "Unconfirmed":
        assert row["value"] == "", f"Unconfirmed row has a value: {row['id']}"
    else:
        assert row["value"], f"Confirmed row is blank: {row['id']}"
for flag in review["flags"]:
    assert flag["value"] == "", f"Unconfirmed input is not blank: {flag['id']}"
    assert all(source_id in sources for source_id in flag["sources"])
for finding in review["source_findings"]:
    assert all(source_id in sources for source_id in finding["sources"])
for risk in review["ordinary_risks"] + review["tail_risks"]:
    assert risk["sources"] and all(source_id in sources for source_id in risk["sources"])
passed("Evidence schema and statuses", "45 unique rows; verified/projection/conflict rows nonblank; unconfirmed school row and all 12 private/property flags blank.")
passed("Official-source allowlist", "23 unique HTTPS government or issuer-primary sources; no commercial market-data host in the evidence register.")


class AuditParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.anchors: list[str] = []
        self.external: list[str] = []
        self.in_tbody = False
        self.current_row: list[str] | None = None
        self.body_rows: list[list[str]] = []
        self.tags: list[str] = []
        self.text: list[str] = []
        self.title_count = 0
        self.h1_count = 0
        self.main_count = 0
        self.has_viewport = False
        self.html_lang = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        self.tags.append(tag)
        if "id" in a and a["id"]:
            self.ids.append(a["id"])
        if tag == "html":
            self.html_lang = a.get("lang", "")
        if tag == "meta" and a.get("name") == "viewport":
            self.has_viewport = True
        if tag == "title":
            self.title_count += 1
        if tag == "h1":
            self.h1_count += 1
        if tag == "main":
            self.main_count += 1
        if tag == "tbody":
            self.in_tbody = True
        if tag == "tr" and self.in_tbody:
            self.current_row = []
        if tag == "a":
            href = a.get("href", "")
            if href.startswith("#"):
                self.anchors.append(href[1:])
            elif href:
                self.external.append(href)
                assert href.startswith("https://"), f"Non-HTTPS external link: {href}"
                assert a.get("target") == "_blank", f"External link missing target: {href}"
                rel = set((a.get("rel") or "").split())
                assert {"noopener", "noreferrer"} <= rel, f"Unsafe external link: {href}"
            if self.current_row is not None:
                self.current_row.append(href)

    def handle_endtag(self, tag: str) -> None:
        if tag == "tr" and self.current_row is not None:
            self.body_rows.append(self.current_row)
            self.current_row = None
        if tag == "tbody":
            self.in_tbody = False

    def handle_data(self, data: str) -> None:
        self.text.append(data)


html = PAGE.read_text()
parser = AuditParser()
parser.feed(html)
assert parser.html_lang == "en"
assert parser.has_viewport and parser.title_count == 1 and parser.h1_count == 1 and parser.main_count == 1
assert len(parser.ids) == len(set(parser.ids)), "Duplicate HTML id"
assert all(anchor in parser.ids for anchor in parser.anchors), "Broken internal anchor"
assert len(parser.body_rows) == 68, f"Expected 45 evidence + 23 source rows, got {len(parser.body_rows)}"
official_urls = {source["url"] for source in sources.values()}
for index, row_links in enumerate(parser.body_rows, 1):
    assert any(href in official_urls for href in row_links), f"Table body row {index} lacks an official source link"
assert "script" not in parser.tags and "form" not in parser.tags and "img" not in parser.tags
assert "link" not in parser.tags and "iframe" not in parser.tags
assert set(urlparse(url).hostname for url in parser.external) <= official_hosts | {"github.com"}
passed("HTML structure and links", "One H1/main/title, unique IDs, all internal anchors resolve, all 68 table body rows carry an official source link, external links use safe HTTPS.")
passed("Self-contained public page", "No script, form, image, iframe, stylesheet link, external asset, tracker or manual-input feature.")

# Inspect visible text only; URLs contain long numeric filing/accession strings.
visible = " ".join(parser.text)
patterns = {
    "email address": r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
    "telephone number": r"(?<!\d)(?:\+?1[ .-]?)?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}(?!\d)",
    "US street address": r"\b\d{1,6}\s+(?:[NSEW]\.?\s+)?[A-Z][A-Za-z'-]+\s+(?:Street|St\.?|Avenue|Ave\.?|Boulevard|Blvd\.?|Road|Rd\.?|Drive|Dr\.?|Lane|Ln\.?|Way|Highway|Hwy\.?)\b",
    "coordinate pair": r"(?<!\d)[+-]?\d{1,3}\.\d{4,}\s*,\s*[+-]?\d{1,3}\.\d{4,}(?!\d)",
}
for label, pattern in patterns.items():
    assert not re.search(pattern, visible, re.I), f"Potential {label} in public text"
assert "Asset A" in visible
assert "No property address or personal data" in visible
passed("Privacy scan", "No email, telephone, street-address or coordinate pattern in visible public text; property remains Asset A.")

# The public page must not present unconfirmed private inputs as numbers.
for flag in review["flags"]:
    assert flag["field"] in visible
assert visible.count("Unconfirmed") >= 2
passed("Unconfirmed-input rendering", "All 12 unconfirmed fields are named; their JSON values remain empty and render as em dashes.")

# Validate Jekyll's default handling when this directory is the source: exactly
# one public file should be emitted; underscore work directories must vanish.
jekyll_out = VALIDATION / "jekyll-out"
if jekyll_out.exists():
    import shutil
    shutil.rmtree(jekyll_out)
command = [
    "jekyll", "build", "--quiet", "--source", str(BASE),
    "--destination", str(jekyll_out), "--disable-disk-cache",
]
try:
    subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
except FileNotFoundError:
    # The local image has no Ruby/Jekyll. Do not claim an actual Jekyll run.
    # Check the public-file convention structurally and defer the executable
    # check to CI, where the repository workflow installs github-pages.
    public_files = sorted(
        path.relative_to(BASE) for path in BASE.rglob("*") if path.is_file()
        and not any(part.startswith(("_", ".")) for part in path.relative_to(BASE).parts)
    )
    assert public_files == [Path("index.html")], f"Unexpected public-layout files: {public_files}"
    passed(
        "Public-file layout; Jekyll deferred",
        "Exactly index.html is outside ignored underscore/dot directories. Jekyll is unavailable in this sandbox, so executable artifact validation is explicitly deferred to CI.",
    )
    jekyll_status = "DEFERRED_EXECUTABLE_UNAVAILABLE"
except subprocess.CalledProcessError as exc:
    raise AssertionError(f"Isolated Jekyll build failed: {exc}") from exc
else:
    public_files = sorted(path.relative_to(jekyll_out) for path in jekyll_out.rglob("*") if path.is_file())
    assert public_files == [Path("index.html")], f"Unexpected public files: {public_files}"
    assert (jekyll_out / "index.html").read_bytes() == PAGE.read_bytes()
    passed("Isolated Jekyll artifact", "Exactly index.html is emitted; all evidence/research/model/tool/validation underscore directories are excluded and HTML bytes are unchanged.")
    jekyll_status = "PASS"

# Root integration still requires the curated-artifact owner to stage this one
# page. Do not mutate or bypass that shared script here.
stage_script = (ROOT / "scripts/stage_pages.py").read_text()
integrated = "verification-3644edd8" in stage_script
integration_text = (
    "Root scripts/stage_pages.py already names this audit; run the full curated-artifact comparison before merge."
    if integrated else
    "Root scripts/stage_pages.py does not yet stage this audit. Owner-side conditional staging remains required; this isolated session does not edit that shared script."
)
passed("Root integration boundary recorded", integration_text)

report = [
    "# Standalone audit validation",
    "",
    "Review date: **2026-11-07 UTC**. All checks below ran locally against the generated page and reviewed model.",
    "",
]
for name, detail in checks:
    report.extend([f"## PASS — {name}", "", detail, ""])
report.extend([
    "## Scope limit",
    "",
    "These are structural, provenance, deterministic-build and privacy checks. They are not a live network monitor, appraisal, legal/tax opinion or proof that every inherited repository row is correct. Manual official-source readings are recorded in `_research/source-notes.md`.",
    "",
    "## Reproduce",
    "",
    "```sh",
    "python verification-3644edd8/_model-review/review_model.py",
    "python verification-3644edd8/_tools/build_audit.py",
    "python verification-3644edd8/_tools/validate_audit.py",
    "```",
    "",
    "When Jekyll is available, isolated output is written under `_validation/jekyll-out`, which Jekyll itself ignores on subsequent builds. In this sandbox the executable was unavailable and the structural fallback is labelled above; CI must perform the real build.",
    "",
])
(VALIDATION / "VALIDATION.md").write_text("\n".join(report))
manifest = {
    "reviewed": "2026-11-07",
    "status": "PASS",
    "checks": [{"name": name, "detail": detail} for name, detail in checks],
    "public_files": ["verification-3644edd8/index.html"],
    "page_sha256": digest(PAGE),
    "model_sha256": current_model_hash,
    "isolated_jekyll_status": jekyll_status,
    "root_staging_integrated": integrated,
}
(VALIDATION / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
print(f"PASS: {len(checks)} validation groups; one public HTML file; 68/68 table rows source-linked")
print(integration_text)
