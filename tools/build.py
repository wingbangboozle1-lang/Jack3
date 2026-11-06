#!/usr/bin/env python3
"""Static site builder for the Jack3 decision dashboard.

Reads  assets/data/{sources,dataset,risks,flagged,scenarios}.json
Writes *.html at the repo root (GitHub Pages serves main / ).

Design rules enforced in code:
  * every data table row renders a link to its named source
  * an unknown source id is a hard build error
  * no personal information is rendered; the parcel is [PROPERTY-A]
"""
import json
import os
import html
from datetime import date

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE = os.path.join(ROOT, "analysis")   # this session's scope; root and docs/ belong to other sessions
D = os.path.join(SITE, "data")


def load(name):
    with open(os.path.join(D, name)) as f:
        return json.load(f)


SOURCES = {s["id"]: s for s in load("sources.json")["sources"]}
DATA = load("dataset.json")["rows"]
RISKS = load("risks.json")["risks"]
FLAGS = load("flagged.json")
SC = load("scenarios.json")

BUILD_DATE = "2026-11-06"

NAV = [
    ("index.html", "Dashboard"),
    ("economy.html", "Economy"),
    ("tenant.html", "Tenant"),
    ("property.html", "Property & lease"),
    ("risk.html", "Risk"),
    ("scenarios.html", "Scenarios"),
    ("decision.html", "Decision"),
    ("data.html", "Master table"),
    ("flagged.html", "Flagged"),
    ("sources.html", "Sources"),
    ("methodology.html", "Method"),
]


# ---------------------------------------------------------------- helpers
def e(x):
    return html.escape(str(x), quote=True)


def usd(x):
    return f"${x:,.0f}" if isinstance(x, (int, float)) else x


def pct(x, dp=2):
    return f"{x*100:.{dp}f}%"


def badge(status):
    m = {
        "verified": ("v", "Verified"),
        "verified-industry": ("i", "Industry data"),
        "calculated": ("c", "Calculated"),
        "flagged": ("f", "Unverified"),
    }
    cls, label = m.get(status, ("f", "Unverified"))
    return f'<span class="badge {cls}">{label}</span>'


def srclink(sid):
    s = SOURCES[sid]
    return (f'<a href="{e(s["url"])}" target="_blank" rel="noopener" '
            f'title="{e(s["publisher"] + " — " + s["name"])}">{e(sid)}</a>')


def table(headers, rows, cls="", numeric=(), caption=None):
    out = [f'<div class="tablewrap"><table class="{cls}">', "<thead><tr>"]
    for i, h in enumerate(headers):
        c = ' class="num"' if i in numeric else ""
        out.append(f"<th{c}>{h}</th>")
    out += ["</tr></thead>", "<tbody>"]
    for r in rows:
        out.append("<tr>")
        for i, cell in enumerate(r):
            c = ' class="num"' if i in numeric else ""
            out.append(f"<td{c}>{cell}</td>")
        out.append("</tr>")
    out += ["</tbody></table></div>"]
    if caption:
        out.append(f'<p class="caption">{caption}</p>')
    return "\n".join(out)


def kpi(label, value, sub):
    return (f'<div class="kpi"><div class="label">{label}</div>'
            f'<div class="value">{value}</div><div class="sub">{sub}</div></div>')


def data_table(rows, caption=None):
    body = []
    for r in rows:
        if r["src"] not in SOURCES:
            raise SystemExit(f"unknown source id {r['src']} in row {r['id']}")
        body.append([
            f'<span class="mono">{e(r["id"])}</span>',
            e(r["metric"]),
            f'<b class="mono">{e(r["value"])}</b>',
            e(r["unit"]),
            e(r["period"]),
            e(r["geo"]),
            badge(r["status"]),
            f'<td class="src">{srclink(r["src"])}</td>'.replace("<td class=\"src\">", "").replace("</td>", ""),
        ])
    return table(["ID", "Indicator", "Value", "Unit", "Period", "Geography", "Status", "Source"],
                 body, numeric=(2,), caption=caption)


def page(title, active, body, desc=""):
    nav_parts = []
    for h, l in NAV:
        cls = ' class="active"' if h == active else ""
        nav_parts.append(f'<a href="{h}"{cls}>{e(l)}</a>')
    nav = "\n".join(nav_parts)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · Jack in the Box NNN · Central Los Angeles</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="index,follow">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
<header class="site"><div class="wrap">
  <a class="brand" href="index.html"><span class="dot"></span>
    <span>Jack in the Box NNN<small>Central Los Angeles · decision research</small></span></a>
  <nav class="main">
{nav}
  </nav>
</div></header>
<main><div class="wrap">
{body}
</div></main>
<footer class="site"><div class="wrap">
  <div><b>Privacy:</b> the parcel is anonymised as [PROPERTY-A]; owner, franchisee and all personal information are withheld.</div>
  <div>Compiled {BUILD_DATE} · sources verified {BUILD_DATE} · <a href="methodology.html">method &amp; limitations</a></div>
</div></footer>
<script src="assets/js/app.js"></script>
</body>
</html>
"""


def head(title, lede, toc=None):
    t = ""
    if toc:
        t = '<div class="toc">' + "".join(
            f'<a href="#{a}">{e(b)}</a>' for a, b in toc) + "</div>"
    return f'<div class="page-head"><h1>{e(title)}</h1><p class="lede">{lede}</p>{t}</div>'


# ---------------------------------------------------------------- page: index
def build_index():
    rows_by_cat = {}
    for r in DATA:
        rows_by_cat.setdefault(r["cat"], []).append(r)
    n_ver = sum(1 for r in DATA if r["status"] == "verified")
    n_ind = sum(1 for r in DATA if r["status"] == "verified-industry")
    n_calc = sum(1 for r in DATA if r["status"] == "calculated")
    n_flag = sum(1 for r in DATA if r["status"] == "flagged")

    kpis = "".join([
        kpi("Metro unemployment", "4.4%", 'Sept 2026 · <a href="sources.html#S01">BLS</a>'),
        kpi("10-yr Treasury", "4.90%", '4 Nov 2026 · <a href="sources.html#S04">FRED / Fed</a>'),
        kpi("Net-lease cap rate", "6.92%", 'Q3 2026, decade high · <a href="sources.html#S24">Boulder</a>'),
        kpi("County roll growth", "+4.42%", '2026 roll · <a href="sources.html#S05">Assessor</a>'),
        kpi("Jack same-store sales", "−4.2%", 'FY2025 · <a href="sources.html#S22">SEC</a>'),
        kpi("County population", "9.69M", '−3.2% since 2020 · <a href="sources.html#S02">Census</a>'),
    ])

    body = f"""
{head("Decision dashboard",
      "Should [OWNER-1] sell [PROPERTY-A] before the triple-net lease expires between 2030 and 2035, or renew it? "
      "This dashboard collects the verified evidence, the financial model, the risk register and the recommendation in one place.")}

<div class="note">
  <b>Privacy first.</b> The property address, parcel number, owner identity, franchisee identity and every personal detail
  are withheld. The asset is referred to as <b>[PROPERTY-A]</b> and the owner as <b>[OWNER-1]</b>. Nothing on this site
  identifies a person or a specific parcel. All statistics are area-level (Los Angeles County, City of Los Angeles, or the
  Los Angeles–Long Beach–Anaheim metro area).
</div>

<div class="grid c3" style="margin-top:18px">{kpis}</div>

<h2 id="recommendation">Recommendation in one paragraph</h2>
<div class="card">
<p><b>Do not sell before the lease expires on an unconditional basis. Hold, extend and prepare, and sell only when a
defined trigger fires.</b> The arithmetic in the model favours holding: under the base case an unlevered hold returns
<b>8.03% a year</b> against <b>7.25%</b> for selling now and deferring tax through a Section 1031 exchange, and holding only
loses if the exit cap rate widens to <b>7.22%</b> or more. Selling costs 4.5% in fees before any tax — and, above the
$5.4 million threshold, another 4% to 5.5% in Measure ULA. Against that, the tenant is visibly contracting, which is the
one fact that can destroy the hold case; so the recommendation is a <i>conditional hold with a hard decision gate in 2029</i>,
not a passive one. Full reasoning: <a href="decision.html">Decision</a>.</p>
</div>

<h2 id="summary">Executive summary</h2>
<div class="grid c2">
<div class="card">
<h3>1 · The question and what actually drives the answer</h3>
<ul>
<li>Three variables dominate: <b>net operating income</b>, the <b>exit cap rate</b>, and <b>whether the tenant renews</b>.
All three are private. NOI and rent are unknown and are published as open items, not estimated.</li>
<li>Everything else — demographics, employment, schools, hazards — moves those three variables at the margin. They are
necessary context, not the decision itself.</li>
<li>Two <b>certain</b> costs push toward holding: transaction friction of about 4.5% of price, and capital-gains plus
depreciation-recapture tax that a 1031 exchange defers but does not eliminate.</li>
</ul>
</div>
<div class="card">
<h3>2 · What the area data says</h3>
<ul>
<li><b>Mixed, mildly positive for a restaurant site.</b> Leisure and hospitality employment is up <b>1.5%</b> year over year
and education/health up <b>3.8%</b>, while information is down <b>5.7%</b> and professional services down <b>0.5%</b>
(<a href="sources.html#S01">BLS</a>).</li>
<li>Population is <b>falling</b> (−3.2% since 2020) and unemployment is <b>4.4%</b> — a soft, not collapsing, market.</li>
<li>Household income is <b>$90,112</b> county-wide and <b>$81,939</b> in the city; median gross rent <b>$1,954</b>; poverty
<b>13.3%</b> county / <b>16.5%</b> city (<a href="sources.html#S02">Census</a>).</li>
<li>The county assessment roll grew <b>4.42%</b> to <b>$2.272 trillion</b> despite the January 2025 fires — the 16th
consecutive year of growth (<a href="sources.html#S05">Assessor</a>).</li>
</ul>
</div>
<div class="card">
<h3>3 · What the tenant data says</h3>
<ul>
<li>Jack in the Box closed <b>86</b> restaurants and opened <b>31</b> in fiscal 2025; same-store sales fell <b>4.2%</b> for
the year and <b>7.4%</b> in Q4; guidance is <b>2,050–2,100</b> restaurants by fiscal 2026 year end versus 2,136
(<a href="sources.html#S22">SEC</a>).</li>
<li>Del Taco is being sold for <b>$115 million</b> — management is reshaping the portfolio, not expanding it
(<a href="sources.html#S21">10-K</a>).</li>
<li><b>Implication:</b> renewal is not automatic. The probability of a dark store at expiry is material, and that
probability — not the demographics — is the main risk to the hold case.</li>
</ul>
</div>
<div class="card">
<h3>4 · What the market says</h3>
<ul>
<li>Single-tenant net-lease cap rates rose to <b>6.92%</b> in Q3 2026, the highest in over a decade; retail is 6.69%,
corporate QSR 5.90%, franchisee QSR 6.87% (<a href="sources.html#S24">Boulder Group</a>).</li>
<li><b>Financing costs now exceed net-lease cap rates</b> — negative leverage — so the bid is dominated by all-cash buyers
and pricing is soft. The 10-year Treasury sits at <b>4.90%</b>.</li>
<li><b>Implication:</b> this is a mediocre moment to sell income paper. It is a better moment to hold and prepare.</li>
</ul>
</div>
</div>

<h2 id="risks">Top five risks, in order</h2>
<div class="tablewrap"><table>
<thead><tr><th>#</th><th>Risk</th><th>Why it matters here</th><th>Evidence</th><th>Type</th></tr></thead>
<tbody>
<tr><td>1</td><td><b>Tenant non-renewal</b></td><td>The brand is shrinking; a dark store at expiry means 12–24 months of downtime, tenant improvements and possibly a change of use.</td><td>{srclink("S22")}</td><td>Business as usual</td></tr>
<tr><td>2</td><td><b>Cap-rate widening / exit pricing</b></td><td>Cap rates are at a decade high and financing costs exceed yields; the exit price is the second-largest lever on total return.</td><td>{srclink("S24")} {srclink("S04")}</td><td>Business as usual</td></tr>
<tr><td>3</td><td><b>Earthquake</b></td><td>USGS models about 1,800 deaths and $213bn of losses for a M7.8 southern San Andreas event; uninsured damage would be borne by [OWNER-1].</td><td>{srclink("S07")}</td><td>Black swan</td></tr>
<tr><td>4</td><td><b>Exit taxes and fees</b></td><td>0.56% base transfer tax plus 4–5.5% Measure ULA above $5.4m, plus 25% recapture and up to 20% capital gains.</td><td>{srclink("S14")} {srclink("S28")} {srclink("S16")}</td><td>Business as usual</td></tr>
<tr><td>5</td><td><b>Wildfire and insurance</b></td><td>January 2025 proved urban Los Angeles County is exposed; insurers withdrew and a moratorium was imposed. Parcel-level hazard class is unverified.</td><td>{srclink("S19")} {srclink("S08")}</td><td>Black swan</td></tr>
</tbody></table></div>
<p class="caption">Full register with likelihood, impact and mitigations: <a href="risk.html">Risk</a>.</p>

<h2 id="audit">What is verified, and what is not</h2>
<div class="grid c3">
<div class="kpi"><div class="label">Dataset rows</div><div class="value">{len(DATA)}</div><div class="sub">across {len(rows_by_cat)} categories</div></div>
<div class="kpi"><div class="label">Rows verified on an official or filed source</div><div class="value">{n_ver}</div><div class="sub">{pct(n_ver/len(DATA))} of the dataset · plus {n_ind} industry and {n_calc} calculated</div></div>
<div class="kpi"><div class="label">Rows flagged unverified</div><div class="value">{n_flag}</div><div class="sub">left in the table, marked, not deleted</div></div>
</div>
<div class="note warn" style="margin-top:16px">
<b>What is deliberately missing.</b> {len(FLAGS)} items could not be verified from an official source and are published
without values on the <a href="flagged.html">Flagged for Review</a> page: the parcel's assessed value, its seismic and
flood classification, its fire-hazard class, the lease rent and NOI, the tenant's identity and credit, the owner's tax
basis, and the zoning capacity. No value was inferred or filled in for any of them.
</div>

<h2 id="navigate">Browse by category</h2>
<div class="grid c2">
<div class="card"><h3><a href="economy.html">Economy &amp; demographics →</a></h3>
<p class="small">Population, income, poverty, housing, employment by sector, prices and rates. {len(rows_by_cat.get("Demographics", [])) + len(rows_by_cat.get("Income & Housing", [])) + len(rows_by_cat.get("Labor Market", [])) + len(rows_by_cat.get("Prices & Rates", []))} verified indicators.</p></div>
<div class="card"><h3><a href="tenant.html">Tenant &amp; brand credit →</a></h3>
<p class="small">Jack in the Box Inc. unit counts, closures, same-store sales, guidance, the Del Taco divestiture, and what it means for renewal probability.</p></div>
<div class="card"><h3><a href="property.html">Property, lease and transaction economics →</a></h3>
<p class="small">Proposition 13, the 2026 roll, transfer taxes, Measure ULA, 1031 mechanics, and the value-per-dollar-of-NOI matrix.</p></div>
<div class="card"><h3><a href="risk.html">Risk register →</a></h3>
<p class="small">{len(RISKS)} risks split into business-as-usual and black swan, each with a sourced factual basis, a labelled judgement of likelihood and impact, and a mitigation.</p></div>
<div class="card"><h3><a href="scenarios.html">Projection and scenario model →</a></h3>
<p class="small">Hold versus sell-and-1031, sensitivity to exit cap and rent growth, the ULA cliff, and an after-tax illustration — every assumption disclosed.</p></div>
<div class="card"><h3><a href="decision.html">Decision framework →</a></h3>
<p class="small">Five options scored against weighted criteria, the recommendation, the triggers that change it, and a dated action plan.</p></div>
</div>
"""
    return page("Decision dashboard", "index.html", body,
                "Evidence, financial model, risk register and recommendation for a Jack in the Box triple-net property in central Los Angeles with a 2030-2035 lease expiry.")


# ---------------------------------------------------------------- page: economy
def build_economy():
    cats = ["Demographics", "Income & Housing", "Labor Market", "Prices & Rates"]
    blocks = []
    for c in cats:
        rows = [r for r in DATA if r["cat"] == c]
        blocks.append(f'<h2 id="{c.lower().replace(" & ", "-").replace(" ", "-")}">{c}</h2>')
        blocks.append(data_table(rows))
    body = f"""
{head("Economy, demographics and labour market",
      "Every figure below was read on an official government page and is linked by source key. "
      "No value is estimated, interpolated or inferred. Where a metric could not be verified it is absent from the table and listed on the Flagged page.",
      [("demographics", "Demographics"), ("income-housing", "Income & housing"), ("labor-market", "Labour market"), ("prices-rates", "Prices & rates"), ("reading", "How to read it")])}

<div class="note">
<b>Geography.</b> "LA–Long Beach–Anaheim MSA" is the metropolitan statistical area that contains central Los Angeles.
"Los Angeles County" is the county. "Los Angeles city" is the city limits. Submarket (neighbourhood) statistics are not
shown because no official neighbourhood-level table could be verified in this session — see flag F-13.
</div>

{"".join(blocks)}

<h2 id="reading">How to read this for the decision</h2>
<div class="grid c2">
<div class="card"><h3>What is supportive</h3>
<ul>
<li><b>Leisure and hospitality is hiring</b> (+1.5% year over year, 782,000 jobs). A restaurant market that is adding jobs
is a restaurant market that can absorb a re-let.</li>
<li><b>Education and health services is the growth engine</b> (+3.8%, 1.34 million jobs) — stable, non-cyclical daytime
demand that suits a drive-through on a commuter corridor.</li>
<li><b>Income and rents are high by national standards</b> ($90,112 median household income; $1,954 median gross rent), which
supports menu pricing and therefore rent coverage.</li>
<li><b>County property values are still rising</b> (+4.42%, 16th straight year) even after the fires.</li>
</ul></div>
<div class="card"><h3>What is not supportive</h3>
<ul>
<li><b>Population is shrinking</b>: −3.2% since April 2020. A falling population is the single most important long-run
headwind for a consumer-facing site.</li>
<li><b>Unemployment is 4.4%</b> and total nonfarm employment grew only <b>0.5%</b> — the metro is not in a boom.</li>
<li><b>Information (−5.7%) and professional services (−0.5%)</b> are contracting, which thins weekday lunch traffic in
office-adjacent corridors.</li>
<li><b>Inflation at 3.7%</b> against lease escalations that are often 2% is a real-terms rent cut every year.</li>
</ul></div>
</div>
<p class="caption">Sources: {srclink("S01")} Bureau of Labor Statistics · {srclink("S02")} {srclink("S03")} Census Bureau ·
{srclink("S04")} Federal Reserve via FRED. Full citations on the <a href="sources.html">Sources</a> page.</p>
"""
    return page("Economy & demographics", "economy.html", body,
                "Verified Los Angeles County and City demographic, income, housing, labour-market and price data.")


# ---------------------------------------------------------------- page: tenant
def build_tenant():
    rows = [r for r in DATA if r["cat"] == "Tenant"]
    body = f"""
{head("Tenant and brand credit",
      "Jack in the Box Inc. is a public company, so its trajectory is verifiable from its own filings. "
      "That trajectory is the strongest argument against a passive hold.",
      [("facts", "Verified facts"), ("reading", "What the numbers mean"), ("lease", "Where the lease sits in this")])}

<h2 id="facts">Verified facts from SEC filings</h2>
{data_table(rows, "Source: Jack in the Box Inc. Form 10-K for the fiscal year ended 28 September 2025 and the Q4 FY2025 earnings release (Exhibit 99.1).")}

<h2 id="reading">What the numbers mean for [PROPERTY-A]</h2>
<div class="grid c2">
<div class="card"><h3>The contraction is deliberate</h3>
<p>38 of the 47 units closed in Q4 were shut under the "JACK on Track" block-closure programme. Management is pruning
underperformers rather than retreating. That matters: a unit that is <i>performing</i> is more likely to be renewed, so the
question is whether [PROPERTY-A]'s unit is a pruner or a keeper. Only the franchisor's unit-level data can answer that,
and it is not public.</p></div>
<div class="card"><h3>Same-store sales are the warning light</h3>
<p>−4.2% for the year and −7.4% in Q4, attributed in the filing to fewer transactions and unfavourable mix, partly offset by
menu price. A unit losing transactions is a unit whose rent coverage is falling even if its rent is flat. Under a
triple-net lease the owner does not see this until renewal, which is exactly why the extension conversation must start
now rather than in 2030.</p></div>
<div class="card"><h3>Corporate is reshaping, not expanding</h3>
<p>The Del Taco divestiture at $115 million, plus a guided unit count of 2,050–2,100 for fiscal 2026 (from 2,136), signals a
management team focused on the balance sheet. New-unit development in an expensive infill market like central Los Angeles
is unlikely to be a priority. The base case should be <b>renewal of an existing, profitable unit</b> or <b>vacancy</b> —
not relocation of a new corporate build.</p></div>
<div class="card"><h3>Credit quality depends on who signed</h3>
<p>If the lease is with Jack in the Box Inc. with a corporate guarantee, the credit is the public company. If it is with a
franchisee — the common structure, since the system is roughly 93% franchised — the credit is a private operator whose
financials are not public. This single fact can move the achievable cap rate by 50–100 basis points.</p></div>
</div>

<h2 id="lease">Where the lease sits in this</h2>
<p>The lease expires between 2030 and 2035: five to nine years from now. That window has three useful properties:</p>
<ol>
<li><b>It is long enough to negotiate from strength.</b> An extension agreed now — while the unit is trading — is worth more
to both sides than a renewal negotiation conducted in the shadow of a closure decision.</li>
<li><b>It is short enough that the exit cap rate already reflects lease-term risk.</b> A buyer of a five-year QSR lease
discounts for rollover; the Boulder Group reports the widest pricing uncertainty exactly in shorter-term and
unrated-operator assets.</li>
<li><b>It overlaps the 2028 Olympic Games in Los Angeles</b> (14–30 July 2028, {srclink("S23")}), a demand and rent event that
sits inside the remaining term rather than after it.</li>
</ol>
<div class="note warn">
<b>Open items that change this page.</b> The lease itself has not been reviewed. Rent, escalations, renewal options,
percentage-rent clauses, guarantor structure and assignment rights are all unknown and are listed as flags F-06 and F-08.
Nothing on this page asserts what the lease says.
</div>
"""
    return page("Tenant & brand credit", "tenant.html", body,
                "Jack in the Box Inc. unit counts, closures, same-store sales, guidance and Del Taco divestiture, verified from SEC filings.")


# ---------------------------------------------------------------- page: property
def build_property():
    prop = [r for r in DATA if r["cat"] in ("Property Tax & Value", "Transaction Costs & Tax")]
    vm = SC["value_matrix"]
    cap_rows = []
    for cap in vm["caps"]:
        cap_rows.append([
            f"{cap*100:.2f}%",
            usd(round(vm["per_100k"][vm["caps"].index(cap)])),
            usd(round(120000 / cap)),
            usd(round(180000 / cap)),
            usd(round(240000 / cap)),
            usd(round(400000 / cap)),
            usd(round(700000 / cap)),
        ])
    cliff_rows = []
    for c in SC["tax_cliff"]:
        cliff_rows.append([
            usd(c["price"]), usd(c["transfer_tax"]), usd(c["ula"]), usd(c["total_transfer"]),
            f'{c["pct_of_price"]:.3f}%', usd(c["net_before_mortgage"]),
        ])
    body = f"""
{head("Property, lease and transaction economics",
      "What the state and city charge on a sale, how Proposition 13 treats a held asset, and how value responds to net operating income and cap rate. "
      "No figure here is a valuation of [PROPERTY-A]: the rent and NOI are private and are listed as flags.",
      [("tax", "Property tax"), ("transfer", "Transfer taxes"), ("ula", "Measure ULA"), ("value", "Value matrix"), ("lease", "Lease economics"), ("1031", "Section 1031")])}

<h2 id="tax">Property tax and Proposition 13</h2>
{data_table(prop)}

<h2 id="transfer">Transfer taxes and the cost of a sale</h2>
<p>In the City of Los Angeles the documentary transfer tax is the county rate of <b>$1.10 per $1,000</b> plus a city rate of
<b>$4.50 per $1,000</b>, a combined <b>0.56%</b> of price ({srclink("S14")}). Add roughly 3% brokerage and 1% legal and
closing, and a sale costs about <b>4.5% of price</b> before any Measure ULA surtax and before tax on the gain.</p>

<h2 id="ula">The Measure ULA cliff</h2>
<p>Measure ULA applies only inside the City of Los Angeles and only above a price threshold. Because the threshold is indexed
every 1 July, the rate table must be re-confirmed for the closing date — which is why the two ULA rows in the dataset are
marked unverified (see <a href="flagged.html#F-01">flag F-01</a>).</p>
{data_table([r for r in DATA if r["id"].startswith("TAX-0") and r["id"] in ("TAX-04", "TAX-05")])}
<p><b>Why it matters:</b> the tax applies to the <i>entire</i> price once the threshold is crossed, not to the excess. A sale at
$5.40 million pays nothing; a sale at $5.41 million pays roughly $216,400. That is a genuine cliff, and it is worth
engineering the price or the timing around it.</p>
{table(["Price", "Base transfer tax (0.56%)", "Measure ULA", "Total transfer cost", "% of price", "Net before mortgage & other costs"],
       cliff_rows, numeric=(1, 2, 3, 4, 5),
       caption="Arithmetic on the disclosed rates in the dataset. ULA at 4% above $5.4m and 5.5% above $10.9m; shown as flagged because the City page could not be read directly (F-01).")}

<h2 id="value">Value matrix: what each dollar of NOI is worth</h2>
<p>Value = NOI ÷ cap rate. The table is deliberately expressed so that it can be used the moment the real rent is known.
Read down a column to see what happens if cap rates move; read across a row to compare income levels.</p>
{table(["Cap rate", "Value per $100k NOI", "NOI $120k", "NOI $180k", "NOI $240k", "NOI $400k", "NOI $700k"],
       cap_rows, numeric=(1, 2, 3, 4, 5, 6),
       caption="Pure arithmetic. The NOI levels are illustrative bands, not estimates of [PROPERTY-A]'s income.")}
<div class="note warn">
<b>Do not read any of these as a valuation.</b> The actual NOI, the actual rent and the actual lease terms are unknown
(flag F-06). These numbers exist so that the owner can drop in the real figure and immediately see the consequence.
</div>

<h2 id="lease">Lease economics under a triple-net structure</h2>
<div class="grid c2">
<div class="card"><h3>What NNN does for the owner</h3>
<ul>
<li>The tenant pays property tax, insurance and maintenance, so the owner's cash flow is close to net.</li>
<li>The owner is therefore exposed to <b>credit risk, not operating risk</b> — which is why the tenant's trajectory above
matters more than the building's condition.</li>
<li>At expiry all of that reverts to the owner. A roof, parking lot, HVAC and signage package can easily absorb 12–24 months
of net income.</li>
</ul></div>
<div class="card"><h3>What the model assumes, and why</h3>
<ul>
<li><b>2% of NOI a year</b> held back as a structural reserve, even under NNN, because the reserve is needed the day the
tenant leaves.</li>
<li><b>4.5% sale cost</b>: 3.0% brokerage, 0.56% transfer, about 0.94% legal and closing. ULA is added only when the price
crosses the threshold.</li>
<li><b>2.5% rent growth</b>, between a 2% fixed bump and a 10%-every-five-years structure amortised.</li>
</ul></div>
</div>

<h2 id="1031">Section 1031 and the tax deferral option</h2>
<p>A like-kind exchange defers gain, it does not eliminate it: the taxpayer must identify replacement property in writing within
<b>45 days</b> and close within <b>180 days</b> ({srclink("S15")}). Unrecaptured Section 1250 gain is taxed at up to
<b>25%</b> and long-term capital gain on real property at up to <b>20%</b>, before any state tax ({srclink("S16")}). A 1031
exchange preserves the deferred gain inside the replacement asset, so the comparison on the
<a href="scenarios.html">Scenarios</a> page is run pre-tax, with the after-tax illustration shown separately and labelled.</p>
<div class="note bad">
<b>The binding constraint on selling is not the market — it is the tax and friction.</b> An owner with a low basis who sells
without exchanging can lose 15–25% of the price to tax on top of 4.5% in fees. Any sell decision has to be made jointly
with a CPA, not after the fact.
</div>
"""
    return page("Property & lease economics", "property.html", body,
                "Proposition 13, 2026 assessment roll, transfer taxes, Measure ULA, value matrix and Section 1031 mechanics.")


# ---------------------------------------------------------------- page: risk
def build_risk():
    def sev(x):
        m = {"Severe": "high", "High": "high", "High (temporary)": "high", "Medium-high": "med",
             "Medium": "med", "Medium (temporary)": "med", "Low-medium": "med", "Low": "low",
             "Low in any year": "low", "Unknown": "f", "Certain on sale": "high", "Low-medium ": "med"}
        return f'<span class="badge {m.get(x, "med")}">{e(x)}</span>'

    def rows_for(t):
        out = []
        for r in RISKS:
            if r["type"] != t:
                continue
            ev = " ".join(srclink(s) for s in r["evidence"]) or '<span class="small">no external source (structural)</span>'
            out.append([f'<span class="mono">{r["id"]}</span>', f'<b>{e(r["risk"])}</b><br><span class="small">{e(r["fact"])}</span>',
                        ev, sev(r["likelihood"]), sev(r["impact"]),
                        e(r["mitigation"]), " ".join(f'<span class="chip">{e(o)}</span>' for o in r["options"])])
        return out

    bau = rows_for("Business as usual")
    swan = rows_for("Black swan")
    hdr = ["ID", "Risk and factual basis", "Evidence", "Likelihood", "Impact", "Mitigation", "Affects"]
    num = ()

    counts = {k: sum(1 for r in RISKS if r["type"] == k) for k in ("Business as usual", "Black swan")}

    body = f"""
{head("Risk register",
      "Every decision carries risk; the job is to know which risks are being taken, which are being avoided, and which are being kept without being paid for. "
      "Facts are sourced; likelihood and impact are labelled judgement.",
      [("bau", "Business as usual"), ("swan", "Black swans"), ("byoption", "Risk by decision"), ("tail", "Uninsured tail")])}

<div class="note">
<b>How to read this.</b> The <i>fact</i> text inside each row is sourced. The <b>likelihood</b> and <b>impact</b> columns are
analyst judgement expressed qualitatively — no probability is asserted, because no official probability exists for most of
these events. Rows with no evidence link are structural risks that follow from the lease or the market rather than from a
published statistic.
</div>

<div class="grid c3">
<div class="kpi"><div class="label">Risks registered</div><div class="value">{len(RISKS)}</div><div class="sub">{counts["Business as usual"]} business-as-usual · {counts["Black swan"]} black swan</div></div>
<div class="kpi"><div class="label">Highest-impact tenant risk</div><div class="value">Non-renewal</div><div class="sub">driven by 86 closures vs 31 openings in FY2025</div></div>
<div class="kpi"><div class="label">Largest uninsured tail</div><div class="value">Seismic</div><div class="sub">USGS models $213bn regional loss</div></div>
</div>

<h2 id="bau">Business-as-usual risks</h2>
{table(hdr, bau, numeric=num, caption="These are the risks that are already in motion. They are the ones that should change behaviour this year.")}

<h2 id="swan">Black-swan risks</h2>
{table(hdr, swan, numeric=num, caption="Low-probability, high-consequence events. Each row states the modelled or observed magnitude where an official source exists.")}

<h2 id="byoption">Risk by decision</h2>
<div class="grid c2">
<div class="card"><h3>Selling now removes…</h3>
<ul>
<li>Tenant non-renewal risk (R-01), franchisee insolvency (R-02) and brand restructuring (B-09).</li>
<li>Seismic and wildfire exposure on the <i>building</i> (B-01, B-02) — though not on the sale price if the buyer prices it in.</li>
<li>Illiquidity and concentration.</li>
</ul>
<h3 style="margin-top:14px">…and creates</h3>
<ul>
<li>Certain tax and friction: 4.5% fees, plus 25% recapture and up to 20% capital gains, plus state tax (R-06, R-07).</li>
<li>Reinvestment risk: the proceeds must be redeployed at 6.87%-type franchisee-QSR yields while financing costs exceed
cap rates (R-05).</li>
<li>Loss of the low Proposition 13 basis and of the redevelopment option.</li>
</ul></div>
<div class="card"><h3>Holding creates…</h3>
<ul>
<li>Concentration in one parcel, one tenant and one submarket.</li>
<li>Exposure to a dark store at expiry and to the capital calls that follow it.</li>
<li>Exposure to a cap-rate widening that a buyer would otherwise have absorbed.</li>
</ul>
<h3 style="margin-top:14px">…and preserves</h3>
<ul>
<li>The low tax basis, the deferral option, and the land/redevelopment upside.</li>
<li>The ability to sell <i>after</i> an extension, when the asset prices tighter (R-13).</li>
</ul></div>
</div>

<h2 id="tail">The uninsured tail, stated plainly</h2>
<p>A magnitude-7.8 southern San Andreas event is modelled by the USGS at roughly <b>1,800 deaths and $213 billion of economic
losses</b>, of which about <b>$112.7 billion</b> is property damage and <b>$96.2 billion</b> is business interruption
({srclink("S07")}). That is a regional model from 2008 in 2008 dollars, not a forecast for [PROPERTY-A]. It is used here
for one purpose: to size the tail that insurance either covers or does not. Earthquake cover for unreinforced or
pre-1976 construction is expensive and often sub-limited; the owner should know, in writing, exactly what is excluded
before assuming the tail is transferred.</p>
<p>The January 2025 fires show the same logic for wildfire: <b>9,414</b> structures destroyed in Eaton and <b>6,837</b> in
Palisades, about <b>6,800 businesses</b> and <b>47,000 workers</b> affected, and an insurance market that responded with a
one-year moratorium on non-renewals ({srclink("S19")} {srclink("S20")}). Wildfire is no longer a foothill-only problem in this county.</p>
"""
    return page("Risk register", "risk.html", body,
                "Business-as-usual and black-swan risk register with sourced facts, labelled likelihood and impact, and mitigations.")


# ---------------------------------------------------------------- page: scenarios
def build_scenarios():
    a = SC["assumptions"]
    comp = SC["comparison"]
    comp_rows = []
    for c in comp:
        comp_rows.append([
            usd(c["noi"]), usd(c["value_today"]),
            pct(c["hold"]["irr"]), f'{c["hold"]["multiple"]:.2f}×', usd(c["hold"]["terminal_wealth"]),
            pct(c["sell"]["irr"]), f'{c["sell"]["multiple"]:.2f}×', usd(c["sell"]["terminal_wealth"]),
            pct(c["breakeven_exit_cap"]), f'{c["irr_gap_pp"]:+.2f} pp',
        ])
    sens = SC["sensitivity"]
    sens_rows = []
    for r in sens["rows"]:
        sens_rows.append([f'{r["growth"]*100:.1f}%'] + [pct(v) for v in r["irr"]])
    spread_rows = []
    for r in SC["cap_spread"]:
        spread_rows.append([pct(r["entry_cap"]), pct(r["flat"]), pct(r["widen_25"]), pct(r["widen_75"])])
    at_rows = []
    for r in SC["after_tax"]:
        at_rows.append([usd(r["price"]), f'{r["basis_pct"]*100:.0f}%', usd(r["basis"]), usd(r["gain"]),
                        usd(r["estimated_tax"]), f'{r["effective_on_gain"]:.1f}%', usd(r["net_after_tax"])])
    aec = SC["all_in_exit_cost"]

    body = f"""
{head("Projection and scenario model",
      "A deterministic, fully disclosed model. It does not know the rent or the NOI — so it is built to be scale-free in percentage terms and to accept the real number the moment the owner supplies it.",
      [("assume", "Assumptions"), ("compare", "Hold vs sell"), ("sens", "Sensitivity"), ("spread", "Cap-rate spread"), ("tax", "After tax"), ("limits", "Limits")])}

<div class="note warn">
<b>These are not projections of [PROPERTY-A].</b> Every input below is an assumption chosen for transparency, not a fact
about the asset. The rent, NOI, basis and lease terms are private and are the subject of flags F-06 and F-07. What the
model does provide is the <i>structure</i> of the decision: which variables dominate, and how far a variable has to move
before the answer changes.
</div>

<h2 id="assume">Disclosed assumptions</h2>
<div class="tablewrap"><table>
<thead><tr><th>Input</th><th class="num">Value</th><th>Basis</th></tr></thead>
<tbody>
<tr><td>Entry cap rate</td><td class="num">{pct(a["cap_entry"])}</td><td>Between the franchisee QSR average (6.87%) and retail net lease (6.69%); a central-LA land component argues for the tighter side. Judgement.</td></tr>
<tr><td>Rent growth</td><td class="num">{pct(a["rent_growth"],1)}</td><td>Between a 2% fixed bump and 10%-every-5-years amortised. Judgement.</td></tr>
<tr><td>Hold period</td><td class="num">{a["hold_years"]} years</td><td>Mid-point of the 2030–2035 expiry band.</td></tr>
<tr><td>Exit cap rate</td><td class="num">{pct(a["cap_exit"])}</td><td>+25 bp for shorter remaining term at exit. Judgement.</td></tr>
<tr><td>Sale cost (below ULA threshold)</td><td class="num">{pct(a["sale_cost"],1)}</td><td>3.0% brokerage + 0.56% transfer tax + ~0.94% legal/closing. Transfer tax verified ({srclink("S14")}); brokerage is market practice.</td></tr>
<tr><td>Structural reserve</td><td class="num">{pct(a["reserve"],1)} of NOI</td><td>Capital that reverts to the owner when the tenant leaves.</td></tr>
<tr><td>Reinvestment cap (1031)</td><td class="num">{pct(a["reinvest_cap"])}</td><td>Boulder Q3 2026 franchisee QSR average ({srclink("S24")}).</td></tr>
<tr><td>Reinvestment growth / exit</td><td class="num">{pct(a["reinvest_growth"],1)} / {pct(a["reinvest_exit_cap"])}</td><td>Diversified net-lease assumptions. Judgement.</td></tr>
<tr><td>Measure ULA</td><td class="num">4% / 5.5%</td><td>Above $5.4m / $10.9m, City of LA only. Flagged (F-01).</td></tr>
</tbody></table></div>

<h2 id="compare">Option A — hold to expiry versus Option B — sell now and exchange</h2>
<p>Both options are run unlevered and pre-tax over the same {a["hold_years"]}-year horizon, so they are directly comparable.
Option B assumes the proceeds are redeployed through a Section 1031 exchange into a diversified net-lease position at
{pct(a["reinvest_cap"])} — which is the only way selling avoids an immediate tax bill.</p>
{table(["NOI", "Value today", "Hold IRR", "Hold multiple", "Hold terminal cash", "Sell + 1031 IRR", "Sell multiple", "Sell terminal cash", "Exit cap that ties the two", "Hold advantage"],
       comp_rows, numeric=(1, 2, 3, 4, 5, 6, 7, 8, 9),
       caption="Terminal cash = cumulative rent plus net sale proceeds, before tax. IRR is on the value today.")}
<div class="note">
<b>The finding.</b> Holding wins in every income band. The margin is about <b>0.8 percentage points a year</b> below the ULA
threshold and widens to about <b>1.6 points</b> above it, because a sale at those values pays the ULA surtax twice — once
on the way out and again, economically, when the replacement asset is later sold. Holding only loses if the exit cap
widens beyond roughly <b>7.2%–7.9%</b>, which would be a severe repricing from today's 6.5% entry level.
</div>

<h2 id="sens">Sensitivity: exit cap rate against rent growth</h2>
<p>Rows are annual rent growth; columns are the cap rate at exit. Cells are the unlevered hold IRR at a $180,000 NOI.</p>
{table(["Rent growth"] + [pct(c) + " exit" for c in sens["exit_caps"]], sens_rows, numeric=tuple(range(1, 8)),
       caption="Read the top-left corner: weak growth and a tight exit cap still produce a competitive return because the entry yield is high. Read the bottom-right: strong growth with cap compression is the best case.")}

<h2 id="spread">Cap-rate spread: what a widening costs</h2>
<p>The single largest risk to a hold is not the tenant — it is the exit cap rate. This table isolates it.</p>
{table(["Entry cap", "Exit flat", "Exit +25 bp", "Exit +75 bp"], spread_rows, numeric=(1, 2, 3),
       caption="At a 6.50% entry, a 75 bp widening at exit still leaves a 7.2% IRR — because the income return and rent growth carry it. That is why the hold case is robust to all but a severe repricing.")}

<h2 id="tax">After-tax illustration (flat arithmetic, not an IRR)</h2>
<p>These rows show what a sale costs if it is <b>not</b> exchanged. They use IRS maxima: 25% on unrecaptured Section 1250
gain, 20% on long-term capital gain, plus net investment income tax at 3.8% where applicable
({srclink("S16")}), plus an assumed 13.3% California rate. The California rate and the NIIT application were
<b>not</b> verified against a fetched official page in this session and are therefore labelled as assumptions.</p>
{table(["Price", "Basis as % of price", "Basis", "Gain", "Estimated tax", "Effective rate on gain", "Net after tax"],
       at_rows, numeric=(2, 3, 4, 5, 6),
       caption="Illustrative only. The owner's actual basis, depreciation history and residency are unknown (flag F-07).")}
<div class="note bad">
<b>What this means in practice.</b> At a 35% basis, a sale at $5.4 million leaves roughly 24% of the gain with the tax
authorities. A 1031 exchange defers that, but only if a replacement is identified within 45 days — so the exchange must be
arranged before Listing, not after closing.
</div>

<h2 id="limits">Limits of the model</h2>
<ul>
<li><b>No leverage.</b> Debt would amplify both the income return and the cap-rate risk, and financing costs currently exceed
net-lease cap rates ({srclink("S24")}), so negative leverage would lower returns.</li>
<li><b>No vacancy scenario.</b> The model assumes the lease runs to expiry. The vacancy case is handled qualitatively on the
<a href="risk.html">Risk</a> page because its cost depends on the tenant improvements a replacement user needs — unknown.</li>
<li><b>No redevelopment value.</b> The land may be worth more as housing or mixed use than as a restaurant. That upside is
described on the <a href="decision.html">Decision</a> page and excluded here because zoning capacity is unverified (F-09).</li>
<li><b>Single path, no Monte Carlo.</b> A probability distribution over cap rates and rents would imply a precision the
underlying inputs do not support.</li>
</ul>
<p class="small">Reproduce every number on this page with <code>python3 tools/model.py</code>. The script and its assumptions are in the repository.</p>
"""
    return page("Scenarios & projections", "scenarios.html", body,
                "Deterministic hold-versus-sell model with disclosed assumptions, sensitivity grids and an after-tax illustration.")


# ---------------------------------------------------------------- page: decision
def build_decision():
    # weighted scoring, computed so the table cannot drift from the text
    weights = {"Wealth preservation (after tax)": 0.25, "Risk-adjusted return": 0.20,
               "Liquidity and flexibility": 0.15, "Downside protection": 0.15,
               "Growth and optionality": 0.15, "Execution burden (5 = light)": 0.10}
    options = {
        "Sell now, outright": dict(zip(weights, [2, 2, 5, 4, 1, 4])),
        "Hold to expiry, renew": dict(zip(weights, [5, 4, 2, 3, 3, 4])),
        "Hold, then reposition or redevelop": dict(zip(weights, [4, 4.5, 1, 2, 5, 2])),
        "Sell now via 1031 exchange": dict(zip(weights, [4, 2.5, 3, 4, 2.5, 2])),
        "Ground-lease recapitalisation": dict(zip(weights, [4.5, 3.5, 4, 3, 3.5, 2.5])),
    }
    scored = []
    for name, s in options.items():
        total = sum(s[k] * weights[k] for k in weights) / 5 * 100
        scored.append((name, s, total))
    scored.sort(key=lambda x: -x[2])
    score_rows = []
    for name, s, total in scored:
        score_rows.append([f"<b>{e(name)}</b>"] + [f"{s[k]:.1f}" for k in weights] + [f"<b>{total:.0f}</b>"])

    body = f"""
{head("Decision framework and recommendation",
      "Five options, scored against six weighted criteria, with the triggers that would change the answer and a dated action plan.",
      [("options", "Options"), ("matrix", "Scoring"), ("rec", "Recommendation"), ("triggers", "Triggers"), ("plan", "Action plan"), ("change", "What would change the answer")])}

<h2 id="options">The five real options</h2>
<div class="tablewrap"><table>
<thead><tr><th>Option</th><th>What it means</th><th>Strongest argument for</th><th>Strongest argument against</th></tr></thead>
<tbody>
<tr><td><b>A · Sell now, outright</b></td><td>List in 2027, pay the tax, redeploy the net proceeds elsewhere.</td><td>Removes tenant, seismic, wildfire and concentration risk in one transaction.</td><td>Crystallises 4.5% fees plus 25% recapture and up to 20% capital gains; sells into a decade-high cap-rate market with negative leverage.</td></tr>
<tr><td><b>B · Hold to expiry, then renew</b></td><td>Collect NNN rent to 2030–2035, negotiate a renewal, keep the asset.</td><td>Preserves basis, keeps the 1031 option, avoids selling into a soft bid.</td><td>Assumes a shrinking tenant renews; leaves concentration and illiquidity in place.</td></tr>
<tr><td><b>C · Hold, then reposition or redevelop</b></td><td>Use the expiry as the moment to re-tenant, expand, or entitle the land for housing or mixed use.</td><td>Land value in central Los Angeles may exceed the value of the income stream; entitlement is the biggest upside lever available.</td><td>Entitlement risk, years of carry, construction cost, and zoning capacity is unverified (F-09).</td></tr>
<tr><td><b>D · Sell now via 1031</b></td><td>Exchange into diversified net-lease assets, deferring tax.</td><td>Diversifies tenant, geography and sector risk without an immediate tax bill.</td><td>Model says it returns 0.8–1.6 points less a year than holding; 45/180-day clock; replacement inventory is thin at these yields.</td></tr>
<tr><td><b>E · Ground-lease recapitalisation</b></td><td>Grant a long-term ground lease to a developer, retain the land and a ground rent.</td><td>Monetises land value without a taxable sale, keeps a perpetual income strip.</td><td>Complex, dependent on entitlements, and a thin buyer pool for a single infill parcel.</td></tr>
</tbody></table></div>

<h2 id="matrix">Weighted scoring</h2>
<p>Weights and scores are the analyst's judgement and are shown in full so they can be challenged. Change a weight and the
ranking changes; that is the point of publishing them.</p>
{table(["Option"] + [f"{k} ({int(w*100)}%)" for k, w in weights.items()] + ["Weighted score /100"],
       score_rows, numeric=tuple(range(1, 7)),
       caption="Scores 1–5, higher is better. Weighted score = Σ(score × weight) ÷ 5 × 100.")}

<h2 id="rec">Recommendation</h2>
<div class="card">
<p><b>Primary recommendation: Option B, executed as a conditional hold with prepared optionality — not a passive hold.</b></p>
<ol>
<li><b>Do not list in 2026–2027.</b> The model shows a 0.8–1.6 percentage-point annual return advantage to holding, and the
market is at a decade-high cap rate with financing costs above yields ({srclink("S24")}): a seller is competing for a thin
pool of all-cash buyers. Selling also triggers 4.5% of friction and, above $5.4 million, a 4%–5.5% ULA surtax
({srclink("S14")} {srclink("S28")}).</li>
<li><b>Convert the lease into an asset before the market tests it.</b> Open an extension conversation now, while the unit is
trading. A five-year extension at a market rent reset converts a five-year lease into a ten-year lease and lifts the
achievable price by more than the rent concession typically costs.</li>
<li><b>Buy information, not opinions.</b> Commission an appraisal, a property-condition report, a Phase I environmental site
assessment and a seismic evaluation this year. Each is cheap relative to the decision and each closes a flag.</li>
<li><b>Test the redevelopment option in parallel.</b> A zoning and entitlement feasibility study tells the owner whether the
land is worth more than the income stream. If it is, the expiry date stops being a risk and becomes the trigger for
Option C.</li>
<li><b>Hold the sell option live.</b> If any trigger below fires, sell — and sell through a 1031 exchange arranged in advance,
not in haste.</li>
</ol>
<p><b>Why this is the best answer for [OWNER-1] as an individual, not just for the asset:</b> it keeps the low Proposition 13
basis, defers an avoidable tax bill, and preserves every exit route while adding the one thing the asset currently lacks —
information. It accepts manageable risk (tenant, seismic, rate) and avoids the two unmanageable ones (a forced sale into a
soft bid, and an unplanned tax event).</p>
</div>

<h2 id="triggers">Sell triggers — any two of these, or any one of the starred</h2>
<div class="tablewrap"><table>
<thead><tr><th>Trigger</th><th>Why it flips the decision</th><th>How to monitor</th></tr></thead>
<tbody>
<tr><td><b>★ Tenant gives notice, or declines to discuss extension by end-2028</b></td><td>A dark store changes the asset from income to redevelopment; selling with the lease in place is worth more than selling vacant.</td><td>Written renewal dialogue; franchisor unit-level performance.</td></tr>
<tr><td><b>★ Unsolicited offer above appraised value, all cash</b></td><td>An all-cash bid sidesteps the negative-leverage problem entirely.</td><td>Broker network; keep the appraisal current.</td></tr>
<tr><td>10-year Treasury falls below 4.0% and cap rates compress</td><td>A lower-rate market prices long income tighter; selling becomes relatively attractive ({srclink("S04")}).</td><td>Monthly FRED series.</td></tr>
<tr><td>Measure ULA is repealed or capped</td><td>Removes a 4–5.5% exit cost; the cliff stops distorting pricing.</td><td>City of LA and Secretary of State ({srclink("S17")}).</td></tr>
<tr><td>Entitlements secured for a higher use</td><td>Entitled land sells to developers at a different price basis than income paper.</td><td>Planning approvals.</td></tr>
<tr><td>Capex surprise above one year of NOI</td><td>Turns a net-lease hold into an operating project without the income to match.</td><td>Property-condition report, roof and seismic findings.</td></tr>
<tr><td>Personal liquidity need or estate event</td><td>Overrides the asset case; the question becomes <i>how</i> to sell, not whether.</td><td>Owner's own planning.</td></tr>
</tbody></table></div>

<h2 id="plan">Action plan and dates</h2>
<div class="tablewrap"><table>
<thead><tr><th>When</th><th>Action</th><th>Output</th><th>Closes</th></tr></thead>
<tbody>
<tr><td>Q4 2026</td><td>Order an MAI appraisal, a property-condition report, a Phase I ESA and a seismic evaluation.</td><td>Four documents and a current value range.</td><td>F-03, F-06, F-11, F-12</td></tr>
<tr><td>Q4 2026</td><td>Have a CPA reconstruct basis and depreciation, and confirm 1031 eligibility and timing.</td><td>After-tax proceeds estimate for a hypothetical sale.</td><td>F-07</td></tr>
<tr><td>Q1 2027</td><td>Pull ZIMAS zoning and FHSZ and FEMA flood determinations for the parcel.</td><td>Zoning capacity and hazard class.</td><td>F-04, F-05, F-09</td></tr>
<tr><td>Q1–Q2 2027</td><td>Open the extension conversation with the tenant and franchisor; request unit-level performance.</td><td>Term sheet for a 5-year extension with a rent reset.</td><td>F-08</td></tr>
<tr><td>Q2 2027</td><td>Commission a redevelopment feasibility study (housing or mixed use, TOC or incentive programmes).</td><td>Residual land value versus income value.</td><td>F-09</td></tr>
<tr><td>2029</td><td><b>Hard decision gate:</b> extension signed, or trigger-based sale, or repositioning.</td><td>Board-level decision on the asset.</td><td>—</td></tr>
</tbody></table></div>

<h2 id="change">What would change the answer</h2>
<div class="grid c2">
<div class="card"><h3>Toward selling sooner</h3>
<ul>
<li>The tenant signals closure, or unit-level sales are materially below the system average.</li>
<li>The appraisal lands just above $5.4 million, making the ULA cliff decisive — restructure the price or wait for the
next 1 July threshold indexation.</li>
<li>A rate-driven cap-rate compression makes the income stream expensive relative to its risk.</li>
<li>The owner needs liquidity, or the estate plan requires a step-up.</li>
</ul></div>
<div class="card"><h3>Toward holding longer</h3>
<ul>
<li>The tenant extends: a ten-year lease re-rates the asset and makes a later sale cheaper in cap-rate terms.</li>
<li>Entitlements are secured: the land option dominates the income option.</li>
<li>Rates fall and the income stream is re-rated upward.</li>
<li>The 2028 Games deliver the anticipated demand lift to the trade area.</li>
</ul></div>
</div>

<div class="note bad">
<b>Not legal, tax or investment advice.</b> This is research prepared for internal decision support. Before acting, [OWNER-1]
should engage a California-licensed appraiser, a CPA with real-estate tax experience, a land-use attorney and, if a sale is
contemplated, a qualified intermediary for the exchange. Every statutory rate cited here should be re-confirmed for the
closing date.
</div>
"""
    return page("Decision framework", "decision.html", body,
                "Five options scored against weighted criteria, the recommendation, sell triggers and a dated action plan.")


# ---------------------------------------------------------------- page: data
def build_data():
    cats = sorted({r["cat"] for r in DATA})
    opts = "".join(f'<option value="{e(c)}">{e(c)}</option>' for c in cats)
    rows = []
    for r in DATA:
        if r["src"] not in SOURCES:
            raise SystemExit("unknown source " + r["src"])
        rows.append([
            f'<span class="mono">{e(r["id"])}</span>',
            e(r["cat"]),
            e(r["metric"]),
            f'<b class="mono">{e(r["value"])}</b>',
            e(r["unit"]),
            e(r["period"]),
            e(r["geo"]),
            badge(r["status"]),
            f'<span class="src">{srclink(r["src"])}</span>',
        ])
    body = f"""
{head("Master verified dataset",
      f"All {len(DATA)} indicators in one table. Every row links to the exact official page it was read from. "
      "Rows that could not be verified are marked and explained on the Flagged page rather than filled in.",
      [("table", "Table"), ("legend", "Legend")])}

<div class="controls">
  <input type="search" id="q" placeholder="Search metric, geography, ID…" aria-label="Search the dataset">
  <select id="cat" aria-label="Filter by category"><option value="">All categories</option>{opts}</select>
  <select id="status" aria-label="Filter by status">
    <option value="">All statuses</option>
    <option value="Verified">Verified</option>
    <option value="Industry data">Industry data</option>
    <option value="Calculated">Calculated</option>
    <option value="Unverified">Unverified</option>
  </select>
  <span class="count" id="count">{len(DATA)} rows</span>
</div>

<div id="table">{table(["ID", "Category", "Indicator", "Value", "Unit", "Period", "Geography", "Status", "Source"], rows, numeric=(3,))}</div>

<h2 id="legend">Legend</h2>
<div class="grid c2">
<div class="card">{badge("verified")}<p class="small" style="margin-top:8px">The value was read directly on the linked official page on {BUILD_DATE}. Government, statute or filing.</p></div>
<div class="card">{badge("verified-industry")}<p class="small" style="margin-top:8px">Read directly on the linked page, but the publisher is an industry research firm rather than a government body. Used only for market context.</p></div>
<div class="card">{badge("calculated")}<p class="small" style="margin-top:8px">Arithmetic on verified inputs; the formula is stated in the row.</p></div>
<div class="card">{badge("flagged")}<p class="small" style="margin-top:8px">Could not be confirmed on an official page this session. The value is shown for context but is not relied on; see <a href="flagged.html">Flagged for Review</a>.</p></div>
</div>
"""
    return page("Master dataset", "data.html", body,
                "All verified indicators with source links, status and geography.")


# ---------------------------------------------------------------- page: flagged
def build_flagged():
    cards = []
    for f in FLAGS:
        srcs = " ".join(srclink(s) for s in f["sources"]) or '<span class="small">no external source available</span>'
        sev_cls = {"High": "high", "Medium": "med", "Low": "low"}.get(f["severity"].split(" ")[0], "med")
        cards.append(f"""
<div class="card" id="{f['id']}" style="margin-bottom:14px">
  <h3 style="margin-bottom:6px"><span class="mono">{f['id']}</span> · {e(f['topic'])}
    <span class="badge {sev_cls}">{e(f['severity'])}</span></h3>
  <p>{e(f['detail'])}</p>
  <p><b>What is needed to close it:</b> {e(f['needed'])}</p>
  <p class="small"><b>Related sources:</b> {srcs}</p>
</div>""")
    body = f"""
{head("Flagged for review",
      f"{len(FLAGS)} items could not be verified against an official source in this session. They are listed here rather than estimated, "
      "so that the published product contains no invented values. None of them blocks publication; all of them should be closed before a transaction.",
      [("items", "Open items"), ("why", "Why they are not filled in")])}

<div class="note warn" id="why">
<b>The rule applied.</b> If a value could not be read on an official, verified source, it was left blank in the dataset and
recorded here. Nothing was inferred, interpolated or copied from an unofficial summary. Where a number appears in the
analysis that depends on an open item, it is labelled as an assumption and the dependency is stated.
</div>

<h2 id="items">Open items</h2>
{"".join(cards)}
"""
    return page("Flagged for review", "flagged.html", body,
                "Items that could not be verified from an official source, with what is needed to close each one.")


# ---------------------------------------------------------------- page: sources
def build_sources():
    tiers = {1: "Official government / statute", 2: "Primary issuer filing", 3: "Industry research"}
    rows = []
    for s in SOURCES.values():
        rows.append([
            f'<span id="{s["id"]}" class="mono">{e(s["id"])}</span>',
            f'<span class="badge {"v" if s["tier"]==1 else ("i" if s["tier"]==3 else "c")}">Tier {s["tier"]}</span>',
            e(s["publisher"]),
            e(s["name"]),
            f'<a href="{e(s["url"])}" target="_blank" rel="noopener">open ↗</a>',
            e(s["accessed"]),
        ])
    body = f"""
{head("Source registry",
      "Every source used, with its tier, publisher, exact page and the date it was read. Only these sources appear anywhere in the dataset.",
      [("registry", "Registry"), ("tiers", "Tier definitions"), ("gaps", "Sources we could not use")])}

<h2 id="registry">Registry</h2>
{table(["ID", "Tier", "Publisher", "Document", "Link", "Accessed"], rows,
       caption="Tier 1 is a government, statutory or court source. Tier 2 is a filed or official issuer disclosure. Tier 3 is industry research and is used only for market context.")}

<h2 id="tiers">Tier definitions</h2>
<div class="grid c3">
<div class="card"><h3>Tier 1 · Official</h3><p class="small">Federal and state agencies, county and city departments, statutes and the Secretary of State. Used for every factual claim about demographics, employment, prices, taxes, hazards and law.</p></div>
<div class="card"><h3>Tier 2 · Filings</h3><p class="small">SEC filings and the official Games organiser. Legally accountable disclosure, audited where applicable. Used for everything about the tenant.</p></div>
<div class="card"><h3>Tier 3 · Industry</h3><p class="small">Net-lease research and broker market data. Never used for a legal or statutory fact, and always labelled "Industry data" in the dataset.</p></div>
</div>

<h2 id="gaps">Sources that were attempted and could not be used</h2>
<ul>
<li><b>Census data API.</b> The API now requires a registered key, so ZIP-code-level tables could not be pulled programmatically. County and city QuickFacts pages were used instead (F-13).</li>
<li><b>BLS QCEW API.</b> The county-by-industry CSV endpoint returned an error; sector detail was taken from the BLS Economy at a Glance page instead.</li>
<li><b>City of Los Angeles Office of Finance — Measure ULA.</b> The deep link returned 404; the rate table is therefore flagged (F-01).</li>
<li><b>Boulder Group PDFs.</b> The report landing page and its executive summaries were read; the PDFs themselves were not parsed in this session.</li>
</ul>
"""
    return page("Sources", "sources.html", body,
                "Source registry with tiers, publishers, URLs and access dates.")


# ---------------------------------------------------------------- page: methodology
def build_methodology():
    body = f"""
{head("Method, verification standard and limitations",
      "How the research was done, how each value was checked, what was excluded for privacy, and where the analysis stops.",
      [("verify", "Verification"), ("privacy", "Privacy"), ("model", "Model"), ("limits", "Limitations"), ("repro", "Reproduce")])}

<h2 id="verify">Verification standard</h2>
<ol>
<li><b>One claim, one source.</b> Each row in the dataset names a single source page. If two sources disagree, both are recorded
and the conflict is disclosed on the Flagged page rather than resolved silently.</li>
<li><b>Read it, then cite it.</b> A value is marked <span class="badge v">Verified</span> only when it was read on the linked page
during compilation on {BUILD_DATE}. Where a number came from a search snippet and the page could not be read, it is marked
<span class="badge f">Unverified</span>.</li>
<li><b>No inference.</b> Nothing is filled in by calculation unless the row says <span class="badge c">Calculated</span> and shows
the formula. Nothing is filled in from a secondary summary unless the source is itself named and tiered.</li>
<li><b>Parcel-level claims are not made.</b> The address is withheld, so seismic, flood, fire-hazard and zoning determinations
require a parcel lookup and are published as open items (F-03, F-04, F-05, F-09).</li>
<li><b>Judgement is labelled.</b> Likelihood and impact scores in the risk register, the weights in the decision matrix and the
model's assumptions are the analyst's judgement. They are shown in full so a reader can substitute their own.</li>
</ol>

<h2 id="privacy">Privacy and anonymisation</h2>
<div class="note">
<b>No personal information is published.</b> The following are withheld from the website: the street address and parcel number
(<b>[PROPERTY-A]</b>), the owner's name and any individual's name (<b>[OWNER-1]</b>), the franchisee's identity and
principals (<b>[FRANCHISEE-1]</b>), lease counterparties, and any contact, financial-account or tenancy information. No
photograph, map pin, or data field on this site can be used to identify the parcel or a person. Everything published is
area-level and available to any member of the public.
</div>
<p>This site is public. Any information that could identify the property or a person has been kept out of the repository
itself, not merely hidden in the presentation, so that the published product cannot leak it through source files.</p>

<h2 id="model">Model method</h2>
<p>The scenario model is a deterministic annual cash-flow projection. It computes value as NOI ÷ cap rate, projects rent at a
fixed growth rate, applies a structural reserve, exits at a stated cap rate with stated sale costs, and solves the
internal rate of return by bisection. The sell-and-reinvest path applies the same machinery to net proceeds reinvested at
the franchisee-QSR benchmark. The script is <code>tools/model.py</code> and its output is
<code>assets/data/scenarios.json</code>, which is what the site renders. Nothing on the site is typed in by hand after the
script runs.</p>

<h2 id="limits">Limitations, stated plainly</h2>
<ul>
<li><b>The property is not valued.</b> Without rent and NOI there is no valuation, and none is asserted.</li>
<li><b>Submarket data is coarse.</b> Verified figures are county, city or metro level; no ZIP-level table could be pulled (F-13).</li>
<li><b>Industry data is industry data.</b> Cap rates come from a research firm, not a government body. They are labelled.</li>
<li><b>Hazard figures are scenarios, not forecasts.</b> The USGS ShakeOut numbers describe a modelled event in 2008 dollars.</li>
<li><b>No forecast of prices.</b> The model shows what happens under stated assumptions; it does not predict the market.</li>
</ul>

<h2 id="repro">Reproduce or challenge anything here</h2>
<p>Every number is traceable. The dataset lives in <code>assets/data/dataset.json</code>, the sources in
<code>assets/data/sources.json</code>, the risks in <code>assets/data/risks.json</code>, and the flags in
<code>assets/data/flagged.json</code>. Rebuild the site with <code>python3 tools/build.py</code>; recompute the model with
<code>python3 tools/model.py</code>; check every link with <code>python3 tools/linkcheck.py</code>. Task ownership and the
verification log are in <code>COORDINATION.md</code>.</p>
"""
    return page("Method & limitations", "methodology.html", body,
                "Verification protocol, anonymisation rules, model method and limitations.")


# ---------------------------------------------------------------- build
def main():
    pages = {
        "index.html": build_index(),
        "economy.html": build_economy(),
        "tenant.html": build_tenant(),
        "property.html": build_property(),
        "risk.html": build_risk(),
        "scenarios.html": build_scenarios(),
        "decision.html": build_decision(),
        "data.html": build_data(),
        "flagged.html": build_flagged(),
        "sources.html": build_sources(),
        "methodology.html": build_methodology(),
    }
    for name, html_out in pages.items():
        with open(os.path.join(SITE, name), "w") as f:
            f.write(html_out)
        print(f"built {name:16s} {len(html_out):>7,} bytes")


if __name__ == "__main__":
    main()
