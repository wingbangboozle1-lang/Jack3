#!/usr/bin/env python3
"""Build the single public audit page from reviewed JSON and model results."""
from __future__ import annotations

from collections import Counter
from html import escape
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
ROOT = BASE.parent
EVIDENCE = json.loads((BASE / "_evidence/evidence.json").read_text())
REVIEW = json.loads((BASE / "_evidence/review.json").read_text())
MODEL = json.loads((BASE / "_model-review/results.json").read_text())
SOURCES = EVIDENCE["sources"]
OUT = BASE / "index.html"

LABELS = {
    "census_county": "Census — county",
    "census_city": "Census — city",
    "dof_p2a": "DOF P-2A workbook",
    "dof_series": "DOF series notes",
    "bls_summary": "BLS LA summary",
    "bls_metro": "BLS metro table",
    "sec_10k": "SEC FY2025 10-K",
    "sec_10q": "SEC Q3 FY2026 10-Q",
    "ir_q3": "Issuer Q3 release",
    "ir_closure": "Issuer closure release",
    "usgs_quake": "USGS regional forecast",
    "cgs_eq": "CGS EQ Zapp",
    "calfire_fhsz": "CAL FIRE hazard zones",
    "fema_msc": "FEMA Map Service Center",
    "county_fire": "County fire fact sheet",
    "calfire_palisades": "CAL FIRE incident",
    "dir_fast": "DIR fast-food FAQ",
    "dir_general": "DIR general wage FAQ",
    "la_wages": "LA wage standards",
    "cde_dashboard": "CDE Dashboard route",
    "irs_1031": "IRS §1031 overview",
    "irs_8824": "IRS Form 8824 instructions",
    "treasury_2026": "Treasury 2026 table",
}


def link(source_id: str) -> str:
    source = SOURCES[source_id]
    return (
        f'<a href="{escape(source["url"], quote=True)}" target="_blank" '
        f'rel="noopener noreferrer">{escape(LABELS[source_id])} <span aria-hidden="true">↗</span></a>'
    )


def refs(ids: list[str]) -> str:
    if not ids:
        return '<p class="refs muted">Evidence type: analyst interpretation / model review; no official site-specific observation claimed.</p>'
    return '<p class="refs"><span>Official context:</span> ' + ' · '.join(link(i) for i in ids) + '</p>'


def status_class(status: str) -> str:
    return {
        "Verified": "verified",
        "Verified projection": "projection",
        "Official snapshot conflict": "conflict",
        "Unconfirmed": "unconfirmed",
    }[status]


def blank(value: str) -> str:
    return escape(value) if value else '<span class="blank" aria-label="Unconfirmed — no value">—</span>'


parts: list[str] = []
add = parts.append
add('<!doctype html>')
add('<html lang="en">')
add('<head>')
add('<meta charset="utf-8">')
add('<meta name="viewport" content="width=device-width,initial-scale=1">')
add('<meta name="description" content="Independent official-source and model-semantic audit for an anonymized central Los Angeles net-lease asset.">')
add('<meta name="robots" content="index,follow">')
add('<title>Independent source & model audit — Asset A</title>')
add('''<style>
:root{--ink:#152b35;--muted:#52656d;--paper:#f4f7f6;--card:#fff;--line:#d8e2df;--teal:#086b65;--teal-soft:#e4f3ef;--navy:#173f50;--amber:#9a5700;--amber-soft:#fff2dc;--red:#a23a32;--red-soft:#fff0ed;--green:#27654d;--green-soft:#e9f4ed;--shadow:0 8px 24px rgba(21,43,53,.06)}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:76px}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.58 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}a{color:var(--teal);text-underline-offset:3px}a:hover{text-decoration-thickness:2px}.skip{position:absolute;left:-9999px;top:8px;background:#fff;padding:10px 16px;z-index:20}.skip:focus{left:8px}.wrap{width:min(1180px,calc(100% - 36px));margin:auto}.top{background:var(--navy);color:#fff;padding:54px 0 38px}.eyebrow{text-transform:uppercase;letter-spacing:.13em;font-size:.76rem;font-weight:750;color:#a9ded6;margin:0 0 12px}.top h1{font-size:clamp(2rem,5vw,3.65rem);line-height:1.06;letter-spacing:-.035em;max-width:900px;margin:0 0 18px}.top .lede{font-size:1.08rem;max-width:850px;color:#e0eeed;margin:0}.chips{display:flex;gap:8px;flex-wrap:wrap;margin-top:22px}.chip{font-size:.78rem;font-weight:700;padding:5px 10px;border-radius:99px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2)}nav{position:sticky;top:0;z-index:10;background:rgba(255,255,255,.97);border-bottom:1px solid var(--line);backdrop-filter:blur(8px)}nav .wrap{display:flex;gap:20px;overflow:auto;padding-top:13px;padding-bottom:13px}nav a{white-space:nowrap;text-decoration:none;font-size:.85rem;font-weight:700;color:var(--navy)}main{padding:32px 0 64px}.notice{border-left:5px solid var(--amber);background:var(--amber-soft);padding:16px 19px;border-radius:4px;margin:0 0 30px}.notice strong{color:#754000}.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:22px 0 36px}.metric{background:var(--card);border:1px solid var(--line);padding:18px;border-radius:10px;box-shadow:var(--shadow)}.metric b{display:block;font-size:1.8rem;line-height:1.1;color:var(--navy)}.metric span{font-size:.82rem;color:var(--muted)}section{margin:46px 0}section>h2{font-size:1.75rem;line-height:1.2;letter-spacing:-.02em;margin:0 0 10px;color:var(--navy)}.section-intro{color:var(--muted);max-width:900px;margin:0 0 22px}.decision{background:#fff;border:1px solid #bad6cf;border-top:5px solid var(--teal);padding:26px;border-radius:10px;box-shadow:var(--shadow)}.decision h3{font-size:1.35rem;line-height:1.35;margin:0 0 12px;color:#075a55}.decision .why{margin:0;color:#334d55}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.path,.finding,.check,.risk,.flag,.scenario{background:#fff;border:1px solid var(--line);border-radius:9px;padding:19px}.path h4,.finding h3,.risk h3{margin:0 0 8px;line-height:1.35}.path p,.finding p,.risk p{margin:8px 0 0}.path{margin-top:16px}.severity{display:inline-block;text-transform:uppercase;letter-spacing:.08em;font-size:.68rem;font-weight:800;padding:3px 8px;border-radius:4px;margin-bottom:10px}.critical{background:var(--red-soft);color:var(--red)}.high{background:#fff0e1;color:#8d4800}.medium{background:#edf1f5;color:#3e5e72}.resolved{background:var(--green-soft);color:var(--green)}.finding{border-left:4px solid #bdc9c9}.finding:has(.critical){border-left-color:var(--red)}.finding:has(.high){border-left-color:var(--amber)}.finding:has(.resolved){border-left-color:var(--green)}.refs{font-size:.8rem;line-height:1.6;margin:13px 0 0!important;color:var(--muted)}.refs span{color:var(--muted)}.muted{color:var(--muted)}.model-warning{padding:15px 18px;background:#edf3f5;border:1px solid #cad9de;border-radius:8px;margin:18px 0}.model-warning strong{color:var(--navy)}.scenario-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:14px 0}.scenario{padding:16px}.scenario h4{margin:0 0 7px;color:var(--navy)}.scenario .big{font-size:1.35rem;font-weight:800;line-height:1.3}.scenario p{font-size:.86rem;margin:7px 0 0}.model-subtitle{font-size:1.08rem;margin:28px 0 6px;color:var(--navy)}details{background:#fff;border:1px solid var(--line);border-radius:8px;margin:10px 0;overflow:hidden}summary{cursor:pointer;padding:14px 17px;font-weight:750;color:var(--navy)}details .details-body{padding:0 17px 16px}details.checks .details-body{padding-top:0}.check-list{display:grid;gap:10px}.check{padding:15px}.check h4{margin:0 0 5px}.check p{margin:6px 0}.check-id{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;color:var(--teal);font-size:.8rem}.table-wrap{overflow:auto;border:1px solid var(--line);border-radius:8px;background:#fff}table{width:100%;border-collapse:collapse;font-size:.83rem;line-height:1.45}th{position:sticky;top:0;background:#eaf1f0;color:#294750;text-align:left;padding:11px 10px;vertical-align:bottom;white-space:nowrap}td{padding:11px 10px;border-top:1px solid #e4ebe9;vertical-align:top;min-width:110px}td:first-child{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;min-width:76px;color:#385760}td.value{font-weight:700;min-width:170px}td.note{min-width:240px;color:#465e66}td.sources{min-width:145px}td.sources a{display:block;margin-bottom:4px}.status{display:inline-block;border-radius:4px;padding:3px 7px;font-size:.7rem;font-weight:750;white-space:normal}.verified{background:var(--green-soft);color:var(--green)}.projection{background:#e9eef9;color:#36578b}.conflict{background:var(--amber-soft);color:var(--amber)}.unconfirmed{background:#eef0f1;color:#5a676c}.blank{font-size:1.25rem;color:#68797e}.evidence-group{margin:15px 0}.evidence-group summary{display:flex;justify-content:space-between;gap:10px}.count{font-weight:500;color:var(--muted);font-size:.8rem}.flag{display:grid;grid-template-columns:75px 1fr;gap:0 14px}.flag .flag-id{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;color:var(--teal);font-weight:750}.flag h3{font-size:1rem;margin:0}.flag .value{font-size:1.5rem;line-height:1.2;margin:7px 0}.flag p{margin:5px 0}.flag .refs{grid-column:2}.risk h3{color:var(--navy)}.risk .interpretation{border-top:1px solid var(--line);padding-top:10px}.method{background:#fff;border:1px solid var(--line);border-radius:9px;padding:20px 25px}.method li{margin:8px 0}.privacy{margin-top:18px;padding:18px;background:var(--teal-soft);border-radius:8px}.source-note{font-size:.85rem;color:var(--muted)}footer{border-top:1px solid var(--line);padding:25px 0 45px;color:var(--muted);font-size:.82rem}.code{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:.78rem;word-break:break-all}@media(max-width:820px){.metrics{grid-template-columns:repeat(2,1fr)}.scenario-grid{grid-template-columns:1fr}.grid{grid-template-columns:1fr}.top{padding-top:38px}.wrap{width:min(100% - 24px,1180px)}section{margin:36px 0}}@media(max-width:480px){.metrics{grid-template-columns:1fr 1fr;gap:8px}.metric{padding:13px}.metric b{font-size:1.45rem}.decision{padding:18px}.flag{grid-template-columns:55px 1fr}.top h1{font-size:2rem}}@media print{nav{display:none}.top{background:#fff;color:var(--ink);padding:20px 0}.top .lede,.eyebrow{color:var(--ink)}.chip{color:var(--ink);border-color:var(--line)}body{background:#fff;font-size:11px}.wrap{width:100%}section{break-inside:auto;margin:24px 0}.finding,.path,.risk,.flag,.scenario,.metric{box-shadow:none;break-inside:avoid}details{break-inside:auto}details:not([open]) .details-body{display:block}summary{list-style:none}a{color:inherit;text-decoration:none}.table-wrap{overflow:visible}th{position:static}td.note{min-width:0}footer{padding-bottom:0}}
</style>''')
add('</head>')
add('<body>')
add('<a class="skip" href="#main">Skip to audit</a>')
add('<header class="top"><div class="wrap">')
add('<p class="eyebrow">Independent verification · Asset A · anonymized</p>')
add('<h1>Official-source &amp;<br>model-semantic audit</h1>')
add('<p class="lede">A targeted review of the decision-critical evidence for the reported central Los Angeles single-tenant net-lease asset. Public facts are separated from projections, model sensitivities, unresolved inputs and analyst judgment.</p>')
add('<div class="chips"><span class="chip">Reviewed 7 November 2026 · UTC</span><span class="chip">No property address or personal data</span><span class="chip">Not an appraisal or personalized advice</span></div>')
add('</div></header>')
add('<nav aria-label="Audit sections"><div class="wrap"><a href="#decision">Decision</a><a href="#corrections">Corrections</a><a href="#model">Model tests</a><a href="#evidence">Evidence</a><a href="#flags">Unconfirmed</a><a href="#risks">Risks</a><a href="#sources">Sources &amp; method</a></div></nav>')
add('<main id="main" class="wrap">')
add('<aside class="notice"><strong>Evidence boundary:</strong> this audit does not certify every inherited repository layer. It independently verifies every row published in <em>this audit’s</em> evidence register and flags material errors found in the reviewed inherited model/narratives. “Verified” means the linked source was read; it never means the property outcome is certain.</aside>')

status_counts = Counter(row["status"] for row in EVIDENCE["rows"])
add('<div class="metrics" aria-label="Audit coverage">')
for number, label in (
    (len(EVIDENCE["rows"]), "source-linked evidence rows"),
    (len(SOURCES), "official / issuer-primary sources"),
    (len(REVIEW["source_findings"]), "source & narrative findings"),
    (len(REVIEW["flags"]), "inputs deliberately left blank"),
):
    add(f'<div class="metric"><b>{number}</b><span>{escape(label)}</span></div>')
add('</div>')

add('<section id="decision"><h2>Decision — conditional, not categorical</h2>')
add('<p class="section-intro">The defensible output is a decision process and explicit evidence gaps, not a fabricated property-specific prediction.</p>')
decision = REVIEW["decision"]
add(f'<div class="decision"><h3>{escape(decision["headline"])}</h3><p class="why">{escape(decision["why"])}</p>')
add('</div><div class="grid">')
for path in decision["paths"]:
    add(f'<article class="path"><h4>{escape(path["name"])}</h4><p>{escape(path["condition"])}</p>{refs(path["sources"])}</article>')
add('</div></section>')

add('<section id="corrections"><h2>Material source &amp; narrative findings</h2>')
add('<p class="section-intro">These findings are independent observations from the reviewed sources and inherited narratives. “Critical” means capable of changing the decision, not that the subject tenant will default or close.</p><div class="grid">')
for finding in REVIEW["source_findings"]:
    add(f'<article class="finding"><span class="severity {finding["severity"]}">{escape(finding["id"])} · {escape(finding["severity"])}</span><h3>{escape(finding["title"])}</h3><p>{escape(finding["body"])}</p>{refs(finding["sources"])}</article>')
add('</div></section>')

add('<section id="model"><h2>Independent model tests</h2>')
add('<p class="section-intro">The inherited Python model was executed read-only. All currency is normalized to <strong>R</strong>, one year of current annual rent. These are mechanical sensitivity outputs under declared assumptions, not official forecasts, appraised values or after-tax proceeds.</p>')
add('<div class="model-warning"><strong>Passing audit checks ≠ a valid appraisal.</strong> Nine assertions reproduce this review’s observations. They confirm the arithmetic and isolate semantic defects; they do not validate cap rates, probabilities, costs, terminal values, or the owner’s wealth outcome. <a href="https://github.com/wingbangboozle1-lang/Jack3/blob/main/verification-3644edd8/_model-review/review_model.py" target="_blank" rel="noopener noreferrer">Reproduction code on GitHub ↗</a></div>')

add('<h3 class="model-subtitle">Same-horizon correction to R-05</h3><div class="scenario-grid">')
for row in MODEL["same_horizon_comparisons"]:
    add(f'<article class="scenario"><h4>{escape(row["expiry"].split(" (")[0])} · hold then re-let</h4><div class="big">{row["base_R"]:.4f} R → {row["pessimistic_R"]:.4f} R</div><p>Base → pessimistic, same strategy and expiry. Model-derived.</p></article>')
add('</div>')

add('<h3 class="model-subtitle">One isolated change materially moves S3’s 2035 rank</h3><p>Counterfactual: remove only S3’s extra tenant-survival multiplier; retain every other input and the existing catastrophe adjustment. This is not a corrected model or a recommendation.</p><div class="scenario-grid">')
for row in MODEL["counterfactual"]["rows"]:
    if row["expiry"] != "2035 (9 years out)":
        continue
    add(f'<article class="scenario"><h4>{escape(row["scenario"].title())}</h4><div class="big">Rank {row["published_rank"]} → {row["counterfactual_rank"]}</div><p>{row["published_adjusted_R"]:.4f} R → {row["counterfactual_R"]:.4f} R after removing only that multiplier. Model-derived.</p></article>')
add('</div>')

add('<h3 class="model-subtitle">Sale-cap one-way sensitivity; all other inputs at base</h3><div class="scenario-grid">')
for row in MODEL["cap_sensitivity"]:
    add(f'<article class="scenario"><h4>Today cap: {row["today_cap_rate_pct"]:.2f}%</h4><div class="big">S1 {row["sell_now_R"]:.4f} R</div><p>S5 extend-then-sell: {row["extend_then_sell_R"]:.4f} R. Higher mechanical PV: {row["higher_mechanical_pv"]}. Model-derived.</p></article>')
add('</div>')

add('<details class="checks"><summary>Open all nine model observations</summary><div class="details-body check-list">')
for check in MODEL["checks"]:
    add(f'<article class="check"><h4><span class="check-id">{escape(check["id"])} · {escape(check["status"])}</span><br>{escape(check["title"])}</h4><p>{escape(check["finding"])}</p></article>')
add('</div></details>')
add(f'<p class="source-note">Reviewed model: <span class="code">model/projection.py</span>; SHA-256 <span class="code">{escape(MODEL["model_sha256"])}</span>. The counterfactual changes review state only; it does not edit the inherited model.</p>')
add('</section>')

add('<section id="evidence"><h2>Verified evidence register</h2>')
add(f'<p class="section-intro">{status_counts["Verified"]} directly verified observations, {status_counts["Verified projection"]} official projections, {status_counts["Official snapshot conflict"]} source-specific conflict rows and {status_counts["Unconfirmed"]} explicit blank. Open a category to inspect every value, period, geography, official source and interpretation.</p>')

groups: dict[str, list[dict]] = {}
for row in EVIDENCE["rows"]:
    groups.setdefault(row["category"], []).append(row)
preferred_order = ["Tenant & lease", "Population & income", "Official projections", "Employment", "Prices", "Catastrophe context", "Operating costs & tax", "Schools"]
for index, category in enumerate(preferred_order):
    rows = groups[category]
    opened = " open" if index < 2 else ""
    add(f'<details class="evidence-group"{opened}><summary><span>{escape(category)}</span><span class="count">{len(rows)} rows</span></summary><div class="details-body"><div class="table-wrap"><table><thead><tr><th scope="col">ID</th><th scope="col">Indicator</th><th scope="col">Value</th><th scope="col">Period / geography</th><th scope="col">Status</th><th scope="col">Official source</th><th scope="col">Boundary / interpretation</th></tr></thead><tbody>')
    for row in rows:
        source_html = "".join(link(source_id) for source_id in row["source"])
        add('<tr>'
            f'<td>{escape(row["id"])}</td>'
            f'<td>{escape(row["indicator"])}</td>'
            f'<td class="value">{blank(row["value"])}</td>'
            f'<td>{escape(row["period"])}<br><span class="muted">{escape(row["geography"])}</span></td>'
            f'<td><span class="status {status_class(row["status"])}">{escape(row["status"])}</span></td>'
            f'<td class="sources">{source_html}</td>'
            f'<td class="note">{escape(row["note"])}</td>'
            '</tr>')
    add('</tbody></table></div></div></details>')
add('<p class="source-note">Verified rows reflect their stated period and may be revised. They are not all “current” merely because they were accessed on the review date. Official projections are forecasts. Official conflict rows deliberately retain different source snapshots.</p>')
add('</section>')

add('<section id="flags"><h2>Unconfirmed input register</h2>')
add('<p class="section-intro">Every value below is intentionally blank (<span class="blank">—</span>). No zero, rate, date, probability or school/catchment is inferred. These items require private records or address-specific professional diligence; they are not invitations to publish personal or property identifiers.</p><div class="grid">')
for flag in REVIEW["flags"]:
    add(f'<article class="flag"><div class="flag-id">{escape(flag["id"])}</div><div><h3>{escape(flag["field"])}</h3><div class="value blank" aria-label="Unconfirmed — no value">—</div><p>{escape(flag["why"])}</p></div>{refs(flag["sources"])}</article>')
add('</div></section>')

add('<section id="risks"><h2>Risk interpretation</h2>')
add('<p class="section-intro">No unverified probability score is assigned. The following links separate observed context from analyst interpretation; none is an Asset A outcome forecast.</p>')
add('<h3 class="model-subtitle">Ordinary risks</h3><div class="grid">')
for risk in REVIEW["ordinary_risks"]:
    add(f'<article class="risk"><h3>{escape(risk["title"])}</h3><p>{escape(risk["evidence"])}</p><p class="interpretation"><strong>Interpretation:</strong> {escape(risk["interpretation"])}</p>{refs(risk["sources"])}</article>')
add('</div><h3 class="model-subtitle">Rare / catastrophe risks</h3><div class="grid">')
for risk in REVIEW["tail_risks"]:
    add(f'<article class="risk"><h3>{escape(risk["title"])}</h3><p>{escape(risk["evidence"])}</p><p class="interpretation"><strong>Interpretation:</strong> {escape(risk["interpretation"])}</p>{refs(risk["sources"])}</article>')
add('</div></section>')

add('<section id="sources"><h2>Official sources &amp; method</h2>')
add('<p class="section-intro">Only government, official institutional and issuer-primary sources support the evidence register. Commercial cap-rate reports, blogs and crowd-sourced property pages are not used as verified evidence. Links were checked during this review; availability can change later.</p>')
add('<div class="table-wrap"><table><thead><tr><th scope="col">ID</th><th scope="col">Publisher / document</th><th scope="col">Document period</th><th scope="col">Accessed</th><th scope="col">Official link</th></tr></thead><tbody>')
for source_id, source in SOURCES.items():
    add('<tr>'
        f'<td>{escape(source_id)}</td>'
        f'<td><strong>{escape(source["publisher"])}</strong><br>{escape(source["title"])}<br><span class="muted">{escape(source["kind"])}</span></td>'
        f'<td>{escape(source["document_date"])}</td>'
        f'<td>{escape(source["accessed"])}</td>'
        f'<td class="sources">{link(source_id)}</td>'
        '</tr>')
add('</tbody></table></div>')
add('<h3 class="model-subtitle">Review method</h3><ol class="method">')
for item in REVIEW["methodology"]:
    add(f'<li>{escape(item)}</li>')
add('</ol>')
add(f'<div class="privacy"><strong>Privacy &amp; publication boundary.</strong> {escape(EVIDENCE["meta"]["privacy"])} School data are used only as a public service context, not to target a household or infer a property premium. Private lease, tax, debt and financial-capacity analysis must remain off this public page.</div>')
add('</section>')
add('</main>')
add('<footer><div class="wrap"><strong>Independent audit · Asset A · reviewed 2026-11-07 UTC.</strong><br>Evidence labels are source-specific, not guarantees. Analyst conclusions are conditional and model-derived values are not official data. No external assets, analytics, forms or trackers are used.</div></footer>')
add('</body></html>')

OUT.write_text("\n".join(parts) + "\n")
print(f"Built {OUT}: {len(EVIDENCE['rows'])} evidence rows, {len(SOURCES)} official sources")
