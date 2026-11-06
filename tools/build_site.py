#!/usr/bin/env python3
"""Build the static GitHub Pages site for the SP-01 study.

Outputs to the repository root so GitHub Pages (branch: main, path: /) serves it directly.
After writing, runs a link audit over every generated page and fails loudly on any
internal href that does not resolve to a real file.
"""

import html
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
DATA = os.path.join(ROOT, "data")

sys.path.insert(0, HERE)
import content as C  # noqa: E402


def load(name):
    with open(os.path.join(DATA, name)) as f:
        return json.load(f)


SOURCES = load("sources.json")
DATASETS = load("datasets.json")
MODEL = load("model_output.json")
FLAGS = load("flags.json")

SRC = {s["id"]: s for s in SOURCES["sources"]}

# --------------------------------------------------------------------------- formatting

def money(x, dp=0):
    if x is None:
        return "—"
    return f"${x:,.{dp}f}"


def pct(x, dp=2):
    if x is None:
        return "—"
    return f"{x*100:.{dp}f}%"


def num(x):
    if x is None:
        return "—"
    if isinstance(x, float):
        return f"{x:,.2f}"
    return f"{x:,}"


def esc(s):
    return html.escape(str(s), quote=True)


def src_link(sid, extra=""):
    if not sid:
        return '<span class="badge badge-unv">no source</span>'
    s = SRC.get(sid)
    if not s:
        return f'<span class="badge badge-unv">{esc(sid)}?</span>'
    tier = s["tier"]
    cls = "badge-src" if tier == "official-primary" else ("badge-sec" if tier == "official-secondary" else "badge-unv")
    label = "primary" if tier == "official-primary" else ("secondary" if tier == "official-secondary" else "third-party")
    return (f'<a class="badge {cls}" href="{esc(s["url"])}" target="_blank" rel="noopener" '
            f'title="{esc(s["publisher"])} — {esc(s["as_of"])}">{sid} · {label}</a>{extra}')


STATUS_CLS = {
    "verified": "ok",
    "verified-secondary": "sec",
    "unverified": "unv",
}

# --------------------------------------------------------------------------- layout

NAV = [
    ("index.html", "Overview"),
    ("decision.html", "Decision"),
    ("economy.html", "Economy"),
    ("demographics.html", "Demographics"),
    ("schools.html", "Schools"),
    ("housing.html", "Housing"),
    ("tenant.html", "Tenant credit"),
    ("macro.html", "Macro & tax"),
    ("risk.html", "Risk & black swans"),
    ("projection.html", "Projection model"),
    ("sources.html", "Sources"),
    ("flagged.html", "Flagged for review"),
]


def page(slug, title, subtitle, body, active=None):
    nav = []
    for href, label in NAV:
        cls = ' class="active"' if href == (active or slug) else ""
        nav.append(f'<a href="{href}"{cls}>{label}</a>')
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · SP-01</title>
<meta name="description" content="Decision support for SP-01, a single-tenant Jack in the Box net-lease asset in central Los Angeles. Official sources only.">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="topbar">
  <div class="wrap topbar-in">
    <a class="brand" href="index.html">
      <span class="brand-mark">SP<span>&#8209;01</span></span>
      <span class="brand-txt">Decision file<small>Jack in the Box · NNN · central Los Angeles</small></span>
    </a>
    <nav class="nav" aria-label="Sections">{''.join(nav)}</nav>
  </div>
</header>
<main id="main" class="wrap">
  <div class="page-head">
    <h1>{title}</h1>
    <p class="sub">{subtitle}</p>
  </div>
  {body}
</main>
<footer class="foot">
  <div class="wrap">
    <p><strong>Privacy notice.</strong> This site contains no street address, parcel number, owner name,
    tenant-unit identity, rent figure, lease date or personal financial data. The asset is referred to as
    SP-01 throughout. All analysis is at county, city or metro granularity.</p>
    <p><strong>Not advice.</strong> This is an analytical file prepared from public sources, not an appraisal,
    a legal opinion or a tax opinion. Values marked <em>assumption</em> are modelling choices, not observations.
    Verify every figure at the source link before acting.</p>
    <p class="tiny">Compiled 2026-11-06 · {len(SOURCES['sources'])} source records ·
    {len(DATASETS['sections'])} data sections · <a href="flagged.html">13 items flagged for review</a></p>
  </div>
</footer>
</body>
</html>
"""


def table(headers, rows, cls=""):
    th = "".join(f"<th>{h}</th>" for h in headers)
    tr = "".join(rows)
    return f'<div class="tablewrap"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


# --------------------------------------------------------------------------- sections

def dataset_section(sec):
    rows = []
    for r in sec["rows"]:
        st = r["status"]
        cls = STATUS_CLS.get(st, "unv")
        val = r["value"]
        if val is None:
            shown = '<span class="blank">— blank —</span>'
        elif isinstance(val, (int, float)) and not isinstance(val, bool):
            shown = num(val)
        else:
            shown = esc(val)
        unit = esc(r.get("unit", ""))
        flag = r.get("flag")
        flaghtml = f' <a class="flagchip" href="flagged.html#{flag}">{flag}</a>' if flag else ""
        note = esc(r.get("note", "") or "")
        rows.append(
            f'<tr class="st-{cls}">'
            f'<td class="c-metric">{esc(r["metric"])}</td>'
            f'<td class="c-val">{shown} <span class="unit">{unit}</span>{flaghtml}</td>'
            f'<td class="c-per">{esc(r.get("period","") or "—")}</td>'
            f'<td class="c-src">{src_link(r.get("source"))}</td>'
            f'<td class="c-note">{note}</td>'
            f"</tr>"
        )
    head = f"""
    <div class="sec-head">
      <h2>{esc(sec['title'])}</h2>
      <p class="why">{sec['why']}</p>
    </div>"""
    return head + table(
        ["Metric", "Value", "Period", "Source", "Note"],
        rows,
        "data",
    )


# --------------------------------------------------------------------------- pages

def build_overview():
    findings = ""
    for f in C.KEY_FINDINGS:
        flag = f'<a class="flagchip" href="flagged.html#{f["flag"]}">{f["flag"]}</a>' if f["flag"] else ""
        findings += f"""
        <article class="finding">
          <div class="fnum">{f['n']}</div>
          <div>
            <h3>{f['title']} {flag}</h3>
            <p>{f['body']}</p>
          </div>
        </article>"""

    stats = [
        ("Lease expiry window", "2030&ndash;2035", "Supplied by the owner. Exact date unknown (F-01)."),
        ("County unemployment", "4.8%", "Sep 2026, below CA 5.1% and its own 5.6% a year earlier."),
        ("County population since 2020", "&minus;3.2%", "9,694,934 at July 2025 against 10,014,009 at the 2020 Census."),
        ("Tenant same-store sales", "&minus;1.1%", "Q3 fiscal 2026, improved from &minus;7.1% a year earlier."),
        ("Measure ULA cliff", "4.0% / 5.5%", "Applies to the whole price above $5.4M and $10.9M."),
        ("Structures lost, Jan 2025 fires", "16,263", "Palisades 6,845 plus Eaton 9,418, in one week."),
    ]
    stathtml = "".join(
        f'<div class="stat"><div class="sv">{v}</div><div class="sl">{l}</div><div class="sn">{n}</div></div>'
        for l, v, n in stats
    )

    body = f"""
    <section class="verdict">
      <div class="vlabel">Recommendation</div>
      <h2 class="vh">{C.VERDICT['headline']}</h2>
      <p class="vtext">{C.VERDICT['one_line']}</p>
      <p><a class="btn" href="decision.html">Read the full decision analysis &rarr;</a>
         <a class="btn ghost" href="projection.html">See the model output &rarr;</a></p>
    </section>

    <section>
      <h2 class="kicker">The six numbers that frame the decision</h2>
      <div class="stats">{stathtml}</div>
    </section>

    <section>
      <h2 class="kicker">What the research found</h2>
      <div class="findings">{findings}</div>
    </section>

    <section class="callout">
      <h2>How to read this site</h2>
      <p>Every table row carries a <span class="badge badge-src">Sxx · primary</span> badge linking to the
      government or filer document it came from. Green rows are verified. Amber rows are verified but read
      through a reproduction. Red rows are <strong>unverified</strong>: the value is left blank and the row
      appears on the <a href="flagged.html">Flagged for Review</a> page with the URL to check by hand.
      Nothing is estimated into a verified slot.</p>
      <p>Figures labelled <em>assumption</em> on the <a href="projection.html">Projection</a> page are
      modelling choices, deliberately separated from observations. The sensitivity table shows which of
      them actually move the answer &mdash; so you can see exactly how much of the conclusion rests on
      judgement rather than evidence.</p>
    </section>
    """
    return page("index.html", "SP-01 &mdash; Decision file",
                "Should the owner sell before the lease expires, or renew? A documented answer from official "
                "sources, with every figure traceable and every gap disclosed.", body)


def build_decision():
    matrix = ""
    for r in C.RISK_BY_DECISION:
        sev = {"high": "sev-high", "medium": "sev-med", "low": "sev-low"}.get(r["severity"], "")
        matrix += f"""
        <article class="riskcard {sev}">
          <h3>{r['decision']}</h3>
          <dl>
            <dt>Upside</dt><dd>{r['upside']}</dd>
            <dt>Downside</dt><dd>{r['downside']}</dd>
            <dt>Assessment</dt><dd><strong>{r['verdict']}</strong></dd>
          </dl>
        </article>"""

    steps = ""
    for s in C.RECOMMENDATION_STEPS:
        steps += f"""
        <article class="step">
          <div class="stepno">{s['step']}</div>
          <div><h3>{s['title']}</h3><p>{s['body']}</p></div>
        </article>"""

    # calm comparison table, V2
    calm = [r for r in MODEL["deterministic_calm"] if r["value_band"] == "V2"]
    rows = []
    for r in calm:
        rows.append(
            f'<tr><td><strong>{esc(r["strategy"])}</strong></td><td>{esc(r["name"])}</td>'
            f'<td class="c-val">{r["exit_year"]}</td>'
            f'<td class="c-val">{pct(r["cagr"])}</td>'
            f'<td class="c-val">{money(r["exit_proceeds"])}</td>'
            f'<td class="c-val">{money(r["terminal_wealth"])}</td></tr>'
        )
    calm_tbl = table(["", "Strategy", "Exit year", "CAGR", "Net proceeds at exit", "Terminal after-tax wealth"],
                     rows, "data")

    # risk-adjusted MC
    mc = [r for r in MODEL["strategies"] if r["value_band"] == "V2"]
    rows = []
    for r in mc:
        ce = r["certainty_equivalent"]
        rows.append(
            f'<tr><td><strong>{esc(r["strategy"])}</strong></td><td>{esc(r["name"])}</td>'
            f'<td class="c-val">{pct(r["cagr"]["p50"])}</td>'
            f'<td class="c-val">{money(r["terminal_wealth"]["p50"])}</td>'
            f'<td class="c-val">{money(r["terminal_wealth"]["cvar5"])}</td>'
            f'<td class="c-val">{money(ce["gamma_2"])}</td>'
            f'<td class="c-val">{money(ce["gamma_4"])}</td></tr>'
        )
    mc_tbl = table(["", "Strategy", "Median CAGR", "Median terminal wealth",
                    "5% CVaR", "Certainty equiv. (&gamma;=2)", "Certainty equiv. (&gamma;=4)"],
                   rows, "data")

    body = f"""
    <section class="callout strong">
      <h2>{C.VERDICT['headline']}</h2>
      <p>{C.VERDICT['one_line']}</p>
    </section>

    <section>
      <h2>Recommended sequence</h2>
      <p class="lede">These six steps are ordered. Each one is conditional on the outcome of the one before it,
      and the first two should happen immediately regardless of what is decided about the exit.</p>
      <div class="steps">{steps}</div>
    </section>

    <section>
      <h2>Risk attached to each decision available to you</h2>
      <p class="lede">Five courses of action are actually open. Each is assessed on what it protects and what it
      costs, in both directions.</p>
      <div class="riskgrid">{matrix}</div>
    </section>

    <section>
      <h2>Comparison on a calm path</h2>
      <p class="lede">No recessions, no shocks, cap rates held at the modelled base. Values are for the
      $6.5&nbsp;million property-value band, after all taxes, Los Angeles transfer tax and Measure ULA.
      Interim cash is reinvested at 6.5% (A19) and taxed on liquidation.</p>
      {calm_tbl}
      <p class="note">Read the first line carefully: selling now for cash produces <strong>{money([r for r in calm if r["strategy"]=="S1"][0]["exit_proceeds"])}</strong>
      of net proceeds on a $6,500,000 asset. That is a 25.7% haircut taken entirely in transaction costs and tax.
      The same-day &#167;1031 exchange of the same asset produces
      <strong>{money([r for r in calm if r["strategy"]=="S6"][0]["exit_proceeds"])}</strong>. The market did not
      change between those two lines. Only the structure did.</p>
    </section>

    <section>
      <h2>Comparison under uncertainty</h2>
      <p class="lede">6,000 simulated macro paths per strategy, each drawing recessions, black-swan events,
      rent-growth deviations and cap-rate shifts. Certainty equivalents are the guaranteed amount a risk-averse
      owner would accept in place of the gamble; higher numbers are better.</p>
      {mc_tbl}
      <p class="note">The ranking flips with risk tolerance, and that flip is the whole finding.
      At low risk aversion the long hold wins on the median. At high risk aversion the
      <em>renew-then-exchange</em> route wins, because it keeps most of the median while truncating the tail.
      The one result that never changes: <strong>a cash sale is never the right answer</strong>.</p>
    </section>

    <section>
      <h2>Why the cash sale cannot win</h2>
      <p class="lede">The gap is almost entirely tax. Take the $6.5 million band, a 40% adjusted basis (A10) and a
      33.4% blended rate on gain (A11).</p>
      <ol class="numbered">
        <li><strong>Transfer tax.</strong> Below the threshold, county plus city is 0.56% &mdash; about $36,400 on
        $6.5 million. Above $5.4 million, Measure ULA adds 4% of the <em>entire</em> price: $260,000. Total
        $296,400, an effective 4.56%.</li>
        <li><strong>Selling costs.</strong> Brokerage, title, escrow and legal at 4.0% (A09): $260,000.</li>
        <li><strong>Capital gains.</strong> Net of the above, the gain over a $2.6 million basis is about
        $3.34 million, taxed at 33.4%: roughly $1.12 million.</li>
        <li><strong>Total friction.</strong> About $1.67 million, or 25.7% of asset value, before a dollar is
        reinvested. A &#167;1031 exchange defers item 3 entirely.</li>
        <li><strong>The compounding cost.</strong> That deferred tax then compounds for the whole hold period.
        That is why the terminal-wealth gap is far larger than the tax bill.</li>
      </ol>
      <p>None of this argues for holding forever. It argues that <strong>the exit decision and the structure
      decision are separate</strong>, and the structure decision is worth more.</p>
    </section>

    <section class="callout">
      <h2>What would change this recommendation</h2>
      <ul class="tight">
        <li><strong>The tenant refuses to renew.</strong> Then the recommendation becomes step 4: exchange out
        before term erodes, not after. In the model, exchanging into a renewal and then out in 2032 rather than holding
        to expiry preserves about $4.5 million of terminal wealth on a $6.5 million asset.</li>
        <li><strong>The property is already worth more than $10.9 million.</strong> Then the upper ULA cliff
        applies at 5.5% and the case for exchanging rather than selling gets stronger, not weaker.</li>
        <li><strong>The owner has a very low basis and needs liquidity.</strong> Even then, a &#167;1031 into a
        diversified trust achieves liquidity through a later sale of units at a tighter tax cost than a direct
        asset sale. The sensitivity table shows the answer is not sensitive to basis within the tested range.</li>
        <li><strong>The owner will not diversify.</strong> Then renewing concentrates the entire estate into one
        box in one county that is losing population and just absorbed the largest urban fire loss in its
        history. The case for an early exchange gets materially stronger.</li>
      </ul>
    </section>
    """
    return page("decision.html", "The decision",
                "Five courses of action, the recommended sequence, and the tax arithmetic that separates them.",
                body)


def build_dataset_page(slug, title, subtitle, section_ids):
    body = ""
    for sid in section_ids:
        sec = next((s for s in DATASETS["sections"] if s["id"] == sid), None)
        if sec:
            body += f'<section class="dataset">{dataset_section(sec)}</section>'
    body += """
    <section class="callout">
      <h2>Reading the badges</h2>
      <p><span class="badge badge-src">Sxx · primary</span> a government or filer document read on its own
      domain. <span class="badge badge-sec">Sxx · secondary</span> an official statement read through a
      reproduction, with the caveat recorded on the source. <span class="badge badge-unv">no source</span>
      the value could not be confirmed and has been left blank. Green rows verified, amber rows verified
      secondary, red rows unverified.</p>
    </section>"""
    return page(slug, title, subtitle, body)


def build_projection():
    # observed inputs table
    obs_rows = []
    for o in MODEL["observed_inputs"]:
        v = o["value"]
        if isinstance(v, float) and abs(v) < 5:
            shown = pct(v)
        elif isinstance(v, float):
            shown = num(v)
        else:
            shown = num(v)
        obs_rows.append(
            f'<tr><td>{esc(o["name"].replace("_"," "))}</td>'
            f'<td class="c-val">{shown}</td><td class="c-per">{esc(o["as_of"])}</td>'
            f'<td class="c-src">{src_link(o["source"])}</td></tr>'
        )
    obs_tbl = table(["Input", "Value", "As of", "Source"], obs_rows, "data")

    # assumptions
    ar = []
    for a in MODEL["assumptions"]:
        v = a["value"]
        shown = f"{v:,.4f}" if isinstance(v, float) and abs(v) < 10 else num(v)
        rng = a.get("range")
        rngs = f"{rng[0]:,.4f} – {rng[1]:,.4f}" if rng else "—"
        if rng and any(abs(x) >= 10 for x in rng):
            rngs = f"{rng[0]:,.0f} – {rng[1]:,.0f}"
        ar.append(
            f'<tr><td><strong>{esc(a["id"])}</strong></td><td>{esc(a["name"])}</td>'
            f'<td class="c-val">{shown}</td><td class="c-val">{rngs}</td>'
            f'<td class="c-note">{esc(a["basis"])}</td>'
            f'<td class="c-val"><span class="mat mat-{a["materiality"].split("-")[0].lower()}">{esc(a["materiality"])}</span></td></tr>'
        )
    assump_tbl = table(["ID", "Assumption", "Base", "Range", "Basis", "Materiality"], ar, "data")

    # stress grid
    cases = {}
    for r in MODEL["stress_grid"]:
        cases.setdefault(r["case"], {"name": r["case_name"], "v": {}})
        cases[r["case"]]["v"][r["strategy"]] = r["terminal_wealth"]
    srows = []
    for cid, cd in cases.items():
        best = max(cd["v"], key=cd["v"].get)
        cells = ""
        for sid in ["S1", "S3", "S4", "S6"]:
            val = cd["v"].get(sid)
            mark = ' class="win"' if sid == best else ""
            cells += f'<td class="c-val"{mark}>{money(val)}</td>'
        srows.append(f'<tr><td><strong>{esc(cid)}</strong></td><td>{esc(cd["name"])}</td>{cells}</tr>')
    stress_tbl = table(["Case", "Scenario", "S1 sell now", "S3 sell 2032", "S4 renew+hold", "S6 &#167;1031 now"],
                       srows, "data")

    # exit scan
    erows = []
    for r in MODEL["exit_year_scan"]:
        erows.append(
            f'<tr><td class="c-val">{r["exit_year"]}</td><td class="c-val">{r["years_held"]}</td>'
            f'<td class="c-val">{pct(r["cagr"])}</td>'
            f'<td class="c-val">{money(r["exit_proceeds"])}</td>'
            f'<td class="c-val">{money(r["exit_gross"])}</td>'
            f'<td class="c-val">{money(r["terminal_wealth"])}</td>'
            f'<td class="c-val">{pct(r["cumulative_shock_exposure"],1)}</td></tr>'
        )
    exit_tbl = table(["Exit year", "Years held", "CAGR", "Net proceeds", "Gross value",
                      "Terminal wealth", "Cumulative shock exposure"], erows, "data")

    # sensitivity
    sen = []
    base_s4 = next((s["S4_median"] for s in MODEL["sensitivity"]), None)
    for s in MODEL["sensitivity"]:
        swing = s["swing"]
        sen.append(
            f'<tr><td><strong>{esc(s["assumption_id"])}</strong></td><td>{esc(s["label"])}</td>'
            f'<td class="c-val">{money(s["S4_median_low"])}</td>'
            f'<td class="c-val">{money(s["S4_median"])}</td>'
            f'<td class="c-val">{money(s["S4_median_high"])}</td>'
            f'<td class="c-val">{money(swing)}</td></tr>'
        )
    sen_tbl = table(["ID", "Assumption", "Terminal wealth at low", "at base", "at high", "Swing"],
                    sen, "data")

    # ULA cliff
    ur = []
    for c in MODEL["ula_cliff"]:
        ur.append(
            f'<tr><td class="c-val">{money(c["price"])}</td>'
            f'<td class="c-val">{money(c["county"])}</td>'
            f'<td class="c-val">{money(c["city"])}</td>'
            f'<td class="c-val">{money(c["ula"])}</td>'
            f'<td class="c-val"><strong>{money(c["total"])}</strong></td>'
            f'<td class="c-val">{pct(c["effective_rate"],3)}</td></tr>'
        )
    ula_tbl = table(["Sale price", "County tax", "City tax", "Measure ULA", "Total", "Effective rate"],
                    ur, "data")

    body = f"""
    <section class="callout">
      <h2>The projection system</h2>
      <p>A seeded Monte Carlo engine written in the Python standard library. It separates three things that
      are normally blended together and thereby hidden: <strong>observations</strong> (official data, cited),
      <strong>assumptions</strong> (modelling judgement, labelled and ranged), and <strong>outputs</strong>
      (computed, reproducible). Re-running <code>python3 tools/model.py</code> reproduces every figure below
      exactly, because the random seed is fixed.</p>
      <p>The model is deliberately <strong>scale-invariant</strong>: current rent is expressed as a going-in
      cap rate on value, so nothing depends on knowing the property's price, rent or basis. Three value bands
      are run because they straddle the two Measure ULA thresholds.</p>
    </section>

    <section>
      <h2>1. Observations used as inputs</h2>
      <p class="lede">These are the only numbers taken from the world. Each is cited.</p>
      {obs_tbl}
    </section>

    <section>
      <h2>2. Assumptions &mdash; the modelling judgement, made visible</h2>
      <p class="lede">Every one of these is a choice, not a fact. They are listed with a range so the reader
      can see how much of the answer is judgement. The sensitivity table in section 5 shows which of them
      actually matter.</p>
      {assump_tbl}
    </section>

    <section>
      <h2>3. Stress grid &mdash; business as usual against named shocks</h2>
      <p class="lede">Each column is a strategy; each row a scenario. $6.5 million base case. The highlighted
      cell is the best outcome in that row. This is where the black-swan question is answered concretely.</p>
      {stress_tbl}
      <p class="note">The pattern is the argument. Renewing wins in five of seven scenarios and loses when
      the county's cost of capital dislocates or rent growth turns permanently negative. The &#167;1031 exchange
      executed now never wins outright but never loses badly either &mdash; it is the minimum-regret choice.</p>
    </section>

    <section>
      <h2>4. Exit timing &mdash; does <em>when</em> you sell matter?</h2>
      <p class="lede">A single-asset sale scan holding all else equal on a calm path, $6.5 million.</p>
      {exit_tbl}
      <p class="note">On a calm path, waiting always pays &mdash; the landlord keeps earning, and rent grows at
      2.75% against cost inflation of nothing. That is precisely why the calm path is misleading. The last
      column is what waiting actually costs: cumulative probability of at least one shock, rising from 0% at
      an immediate sale to 16.6% by 2035. The model's whole purpose is to price that column, and it is why the
      recommendation pairs a renewal with a <em>planned</em> exchange date rather than an open-ended hold.</p>
    </section>

    <section>
      <h2>5. Sensitivity &mdash; what actually moves the answer</h2>
      <p class="lede">Each assumption varied to the ends of its stated range, everything else held at base.
      Median terminal wealth of the renew-and-hold strategy at $6.5 million.</p>
      {sen_tbl}
      <p class="note">The cap rate, the tax rate and market rent growth are roughly equal in influence and
      dominate everything else. Note what is <em>not</em> here: the black-swan probability alone swings
      the result by about $3.0 million, which is large but second-order compared with tax structure.
      The renewal probability swings it by only about $0.4 million, because a vacated site retains its land
      value. That is a genuinely reassuring result for a landlord worried about the tenant.</p>
    </section>

    <section>
      <h2>6. The Measure ULA cliff, computed</h2>
      <p class="lede">Measure ULA is not a marginal tax. Once the price crosses a threshold the rate applies to
      the whole consideration. This is the single most avoidable cost in the file.</p>
      {ula_tbl}
      <p class="note">Crossing $5.4 million costs an extra <strong>$216,000</strong> instantly: a $5,399,999
      sale nets more than a $5,400,001 sale. Crossing $10.9 million costs an extra <strong>$163,500</strong>
      instantly. Both thresholds are indexed to Chained CPI and will be higher by 2030, so any negotiation
      near them must re-verify the current figure on the <a href="{esc(SRC['S17']['url'])}" target="_blank" rel="noopener">City of Los Angeles Office of Finance</a> page.</p>
    </section>

    <section>
      <h2>7. What the model cannot see</h2>
      <ul class="tight">
        <li>Contract rent, basis and lease terms (F-01, F-06) &mdash; exposed as scenario parameters instead.</li>
        <li>Whether the tenant has already decided to close this unit (F-01).</li>
        <li>Parcel-level hazard: fire hazard severity zone, flood zone, seismic construction type (F-01, F-03).</li>
        <li>Trade-area population, traffic counts and zoning &mdash; the true demand and residual-value drivers.</li>
        <li>The existence of an actual comparable sale. Neither a broker opinion nor an appraisal was available.</li>
      </ul>
      <p>Each of these is a row in the data tables with a blank value, not an estimate.</p>
    </section>
    """
    return page("projection.html", "Projection model",
                "A seeded Monte Carlo built from cited observations, exposed assumptions and reproducible output.",
                body)


def build_risk():
    cards = ""
    for b in C.BLACK_SWANS:
        cards += f"""
        <article class="swan">
          <h3>{b['name']}</h3>
          <p class="ev"><strong>Evidence.</strong> {b['evidence']}</p>
          <p><strong>How it transmits to this asset.</strong> {b['transmission']}</p>
          <p class="md"><strong>Modelled as.</strong> {b['modelled']}</p>
          <p class="mit"><strong>What to check or do.</strong> {b['mitigation']}</p>
        </article>"""

    haz = next(s for s in DATASETS["sections"] if s["id"] == "hazard")
    haz_table = dataset_section(haz)

    body = f"""
    <section class="callout">
      <h2>Two kinds of risk, treated separately</h2>
      <p><strong>Business as usual</strong> covers recessions, rent drift, cap-rate movement and tenant
      behaviour. It is modelled stochastically across 6,000 paths. <strong>Black swans</strong> are modelled
      as discrete named cases with an explicit annual probability (A13, 2.0%) and severity (A14, 35% of value)
      rather than buried in a standard deviation. Both are reported.</p>
    </section>

    <section>
      <h2>The black-swan register</h2>
      <p class="lede">Six event classes that could materially damage this asset or the local economy that
      supports it. Each is grounded in a verified event or a verified regulatory fact.</p>
      <div class="swans">{cards}</div>
    </section>

    <section class="dataset">
      <h2>Hazard data as verified</h2>
      {haz_table}
    </section>

    <section class="callout">
      <h2>The asymmetry that matters most</h2>
      <p>For an owner who intends to keep working capital intact, the relevant question is not the median
      outcome but the survival outcome. On a $6.5 million asset the mean of the worst 5% of outcomes is
      <strong>{money([r for r in MODEL['strategies'] if r['value_band']=='V2' and r['strategy']=='S4'][0]['terminal_wealth']['cvar5'])}</strong>
      for renew-and-hold, against
      <strong>{money([r for r in MODEL['strategies'] if r['value_band']=='V2' and r['strategy']=='S6'][0]['terminal_wealth']['cvar5'])}</strong>
      for an immediate &#167;1031 exchange and
      <strong>{money([r for r in MODEL['strategies'] if r['value_band']=='V2' and r['strategy']=='S1'][0]['terminal_wealth']['cvar5'])}</strong>
      for a cash sale. The cash sale has the highest <em>floor</em> but the lowest ceiling by a wide margin,
      because the tax is paid with certainty and the growth is forgone with certainty. That is why the
      exchange structures dominate once risk aversion is taken seriously: they sit between the two extremes
      on every measure.</p>
    </section>
    """
    return page("risk.html", "Risk &amp; black swans",
                "Six event classes, grounded in verified events, and how each transmits into this asset's value.",
                body)


def build_sources():
    rows = []
    for s in SOURCES["sources"]:
        tier = s["tier"]
        cls = {"official-primary": "ok", "official-secondary": "sec", "third-party": "unv",
               "unverified": "unv"}.get(tier, "unv")
        verifies = s.get("verifies") or []
        vlist = "<ul class='vlist'>" + "".join(f"<li>{esc(v)}</li>" for v in verifies) + "</ul>" if verifies else \
                "<em>no rows verified</em>"
        rejected = ""
        if s.get("rejected_claim"):
            rejected = (f'<div class="rejected"><strong>Claim not accepted:</strong> {esc(s["rejected_claim"])}'
                        f'<br><strong>Why:</strong> {esc(s.get("reason_rejected",""))}</div>')
        caveat = f'<div class="caveat"><strong>Caveat:</strong> {esc(s["caveat"])}</div>' if s.get("caveat") else ""
        rows.append(f"""
        <tr class="st-{cls}">
          <td><strong>{esc(s['id'])}</strong><br><span class="tier">{esc(tier)}</span></td>
          <td>
            <div class="srctitle">{esc(s['publisher'])}</div>
            <div class="srcname">{esc(s['title'])}</div>
            <a class="srcurl" href="{esc(s['url'])}" target="_blank" rel="noopener">{esc(s['url'])}</a>
            <div class="srcas">as of {esc(s['as_of'])}</div>
            {rejected}{caveat}
            <details><summary>What this source verifies ({len(verifies)})</summary>{vlist}</details>
          </td>
        </tr>""")

    legend = """
    <div class="legend">
      <div><span class="badge badge-src">primary</span> Government or filer document, read on its own domain.</div>
      <div><span class="badge badge-sec">secondary</span> Official statement read through a reproduction; caveat recorded.</div>
      <div><span class="badge badge-unv">third-party</span> Not accepted as verification. Listed for transparency only.</div>
    </div>"""

    body = f"""
    <section class="callout">
      <h2>{len(SOURCES['sources'])} source records</h2>
      <p>{SOURCES['meta']['rule']}</p>
      <p>{esc(SOURCES['meta']['access_note'])}</p>
      {legend}
    </section>
    <section>
      <div class="tablewrap"><table class="sources"><tbody>{''.join(rows)}</tbody></table></div>
    </section>
    <section>
      <h2>Source mix</h2>
      <ul class="tight">
        <li><strong>{sum(1 for s in SOURCES['sources'] if s['tier']=='official-primary')}</strong> primary government or filer documents.</li>
        <li><strong>{sum(1 for s in SOURCES['sources'] if s['tier']=='official-secondary')}</strong> official statements read through a reproduction.</li>
        <li><strong>{sum(1 for s in SOURCES['sources'] if s['tier']=='third-party')}</strong> third-party claims, all rejected as verification and listed for transparency.</li>
      </ul>
    </section>
    """
    return page("sources.html", "Sources",
                "Every document used, what it verified, and what was deliberately rejected.", body)


def build_flagged():
    cards = ""
    for f in FLAGS["items"]:
        sev = f["severity"]
        cls = {"high": "sev-high", "medium": "sev-med", "low": "sev-low", "informational": "sev-info"}.get(sev, "")
        check = (f'<p class="check"><a class="btn ghost" href="{esc(f["check"])}" target="_blank" rel="noopener">'
                 f'Check this at the source &rarr;</a></p>') if f.get("check") else \
                '<p class="check muted">No single source URL resolves this item; it requires information not in the public record.</p>'
        cards += f"""
        <article class="flagcard {cls}" id="{esc(f['id'])}">
          <div class="flaghead">
            <span class="flagid">{esc(f['id'])}</span>
            <span class="flagsev">{esc(sev)}</span>
            <span class="flagcat">{esc(f['category'])}</span>
          </div>
          <h3>{esc(f['title'])}</h3>
          <p><strong>What was found.</strong> {esc(f['detail'])}</p>
          <p><strong>Impact.</strong> {esc(f['impact'])}</p>
          <p><strong>What was done.</strong> {esc(f['action_taken'])}</p>
          <p><strong>Does this affect the recommendation?</strong> {esc(f['affects_conclusion'])}</p>
          {check}
        </article>"""

    body = f"""
    <section class="callout warn">
      <h2>{FLAGS['meta']['counts']['total']} items are flagged</h2>
      <p>{esc(FLAGS['meta']['policy'])}</p>
      <div class="flagcounts">
        <div><span class="big">{FLAGS['meta']['counts']['unverified']}</span> unverified</div>
        <div><span class="big">{FLAGS['meta']['counts']['irregularity']}</span> irregularities</div>
        <div><span class="big">{FLAGS['meta']['counts']['conflict']}</span> source conflict</div>
        <div><span class="big">{FLAGS['meta']['counts']['deliberate_omission']}</span> deliberate omission</div>
      </div>
      <p><strong>None of these blocks the recommendation.</strong> Every one is disclosed so that you can
      review it and ask for a change. Where a figure could not be confirmed it is blank in the tables,
      never estimated.</p>
    </section>
    <section>
      <div class="flags">{cards}</div>
    </section>
    """
    return page("flagged.html", "Flagged for review",
                "Everything that could not be verified, every source irregularity, and every conflict — with the "
                "link to check each one by hand.", body)


def build_methodology():
    notes = "".join(f'<article class="method"><h3>{n["title"]}</h3><p>{n["body"]}</p></article>'
                    for n in C.METHODOLOGY_NOTES)
    priv = "".join(f'<article class="method"><h3>{p["title"]}</h3><p>{p["body"]}</p></article>'
                   for p in C.PRIVACY_POINTS)
    body = f"""
    <section>
      <h2>Method</h2>
      <p class="lede">How the verification standard works, why the model is built the way it is, and what
      the numbers actually mean.</p>
      {notes}
    </section>
    <section>
      <h2>Privacy protocol</h2>
      <p class="lede">Personal information is the highest-priority constraint in this file. Here is exactly
      how it was handled.</p>
      {priv}
    </section>
    <section>
      <h2>Data inventory</h2>
      <p class="lede">Every section of the stored dataset, with how many rows are verified, verified
      secondary and unverified.</p>
      {inventory_table()}
    </section>
    """
    return page("index.html", "Method &amp; privacy", "", body)


def inventory_table():
    rows = []
    for sec in DATASETS["sections"]:
        v = sum(1 for r in sec["rows"] if r["status"] == "verified")
        s = sum(1 for r in sec["rows"] if r["status"] == "verified-secondary")
        u = sum(1 for r in sec["rows"] if r["status"] == "unverified")
        rows.append(f'<tr><td>{esc(sec["title"])}</td><td class="c-val">{v}</td>'
                    f'<td class="c-val">{s}</td><td class="c-val">{u}</td>'
                    f'<td class="c-val">{len(sec["rows"])}</td></tr>')
    return table(["Section", "Verified", "Verified (secondary)", "Unverified", "Total"], rows, "data")


# --------------------------------------------------------------------------- css

CSS = """
:root{
  --ink:#12161c; --ink2:#3c4553; --ink3:#6b7683; --line:#e2e6eb; --line2:#eef1f5;
  --bg:#ffffff; --bg2:#f7f9fb; --bg3:#eff3f7;
  --acc:#0f5132; --acc2:#166a43; --accl:#e6f2ec;
  --warn:#8a5a00; --warnl:#fdf5e3; --warnb:#e8c877;
  --bad:#8c1d18; --badl:#fdeceb; --badb:#e8a9a4;
  --blue:#12456f; --bluel:#e8f0f7;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 var(--sans);font-feature-settings:"kern" 1}
.wrap{max-width:1180px;margin:0 auto;padding:0 22px}
.skip{position:absolute;left:-9999px}
.skip:focus{left:8px;top:8px;background:#fff;padding:8px 14px;z-index:99;border:2px solid var(--acc)}
a{color:var(--blue)}
a:hover{color:var(--acc2)}
code{font-family:var(--mono);font-size:.88em;background:var(--bg3);padding:1px 5px;border-radius:4px}

/* top bar */
.topbar{position:sticky;top:0;z-index:40;background:rgba(255,255,255,.94);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.topbar-in{display:flex;align-items:center;gap:22px;height:62px}
.brand{display:flex;align-items:center;gap:11px;text-decoration:none;color:var(--ink);flex:0 0 auto}
.brand-mark{font:700 15px/1 var(--sans);letter-spacing:.06em;background:var(--ink);color:#fff;padding:8px 9px;border-radius:7px}
.brand-mark span{color:#8ec9a8}
.brand-txt{display:flex;flex-direction:column;font-weight:700;font-size:14px;line-height:1.25}
.brand-txt small{font-weight:400;color:var(--ink3);font-size:11.5px;letter-spacing:.01em}
.nav{display:flex;gap:2px;overflow-x:auto;scrollbar-width:none;margin-left:auto}
.nav::-webkit-scrollbar{display:none}
.nav a{padding:7px 11px;border-radius:7px;font-size:13.5px;font-weight:500;color:var(--ink2);text-decoration:none;white-space:nowrap}
.nav a:hover{background:var(--bg3);color:var(--ink)}
.nav a.active{background:var(--acc);color:#fff}

/* page head */
.page-head{padding:34px 0 6px;max-width:860px}
.page-head h1{margin:0 0 10px;font-size:31px;line-height:1.2;letter-spacing:-.015em;font-weight:700}
.page-head .sub{margin:0;color:var(--ink2);font-size:16.5px;line-height:1.55}

main{padding-bottom:64px}
section{margin:34px 0}
h2{font-size:20px;line-height:1.3;margin:0 0 10px;letter-spacing:-.01em}
h2.kicker{font-size:13px;text-transform:uppercase;letter-spacing:.09em;color:var(--ink3);font-weight:600;margin-bottom:14px}
h3{font-size:16px;margin:0 0 7px;line-height:1.35}
p{margin:0 0 12px}
.lede{color:var(--ink2);font-size:15.5px;max-width:88ch}
.note{color:var(--ink2);font-size:14px;background:var(--bg2);border-left:3px solid var(--line);padding:11px 14px;border-radius:0 6px 6px 0;margin-top:14px}

/* verdict */
.verdict{background:linear-gradient(160deg,#0d3f27,#0f5132 55%,#14603c);color:#fff;border-radius:14px;padding:30px 32px;margin-top:26px}
.verdict .vlabel{font-size:11.5px;text-transform:uppercase;letter-spacing:.13em;opacity:.72;font-weight:600;margin-bottom:11px}
.verdict h2.vh{margin:0 0 13px;font-size:25px;line-height:1.28;color:#fff;font-weight:650;max-width:26ch}
.verdict .vtext{color:#cfe6da;font-size:15.5px;margin-bottom:19px;max-width:78ch}
.verdict .btn{background:#fff;color:#0f5132;border-color:#fff}
.verdict .btn:hover{background:#e8f4ee}
.verdict .btn.ghost{background:transparent;color:#eaf5ef;border-color:rgba(255,255,255,.42)}
.verdict .btn.ghost:hover{background:rgba(255,255,255,.12)}

.btn{display:inline-block;padding:9px 17px;border-radius:8px;font-size:14px;font-weight:600;text-decoration:none;background:var(--acc);color:#fff;border:1px solid var(--acc)}
.btn:hover{background:var(--acc2);color:#fff}
.btn.ghost{background:transparent;color:var(--acc);border-color:var(--line)}
.btn.ghost:hover{background:var(--bg3);color:var(--acc2)}

/* stats */
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(178px,1fr));gap:12px}
.stat{background:var(--bg2);border:1px solid var(--line2);border-radius:10px;padding:15px 16px}
.stat .sv{font-size:23px;font-weight:700;letter-spacing:-.02em;line-height:1.15;color:var(--ink)}
.stat .sl{font-size:12.5px;color:var(--ink3);margin:5px 0 7px;font-weight:600;text-transform:uppercase;letter-spacing:.045em}
.stat .sn{font-size:13px;color:var(--ink2);line-height:1.45}

/* findings */
.findings{display:grid;gap:2px}
.finding{display:grid;grid-template-columns:38px 1fr;gap:15px;padding:19px 0;border-top:1px solid var(--line2)}
.finding:first-child{border-top:0}
.fnum{width:30px;height:30px;border-radius:50%;background:var(--accl);color:var(--acc);font-weight:700;font-size:13.5px;display:flex;align-items:center;justify-content:center}
.finding h3{font-size:16px;margin-bottom:6px}
.finding p{color:var(--ink2);font-size:15px;margin:0;max-width:88ch}

/* callout */
.callout{background:var(--bg2);border:1px solid var(--line2);border-radius:12px;padding:22px 24px}
.callout.strong{background:var(--accl);border-color:#c6e2d3}
.callout.strong h2{color:var(--acc)}
.callout.warn{background:var(--warnl);border-color:var(--warnb)}
.callout.warn h2{color:var(--warn)}
.callout p:last-child{margin-bottom:0}

/* tables */
.tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:#fff}
table{border-collapse:collapse;width:100%;font-size:13.6px}
th{text-align:left;padding:10px 12px;background:var(--bg3);font-size:11.5px;text-transform:uppercase;letter-spacing:.06em;color:var(--ink3);font-weight:650;border-bottom:1px solid var(--line);white-space:nowrap;position:sticky;top:0}
td{padding:9px 12px;border-bottom:1px solid var(--line2);vertical-align:top;line-height:1.45}
tr:last-child td{border-bottom:0}
tbody tr:hover{background:#fbfcfd}
td.c-metric{min-width:200px;font-weight:500}
td.c-val{white-space:nowrap;font-variant-numeric:tabular-nums;font-weight:600}
td.c-per{white-space:nowrap;color:var(--ink3);font-size:12.5px}
td.c-src{white-space:nowrap}
td.c-note{color:var(--ink2);font-size:12.8px;min-width:230px;max-width:430px}
.unit{font-weight:400;color:var(--ink3);font-size:11.5px}
tr.st-ok td.c-metric{border-left:3px solid #2e7d54}
tr.st-sec td.c-metric{border-left:3px solid var(--warnb)}
tr.st-unv{background:var(--badl)}
tr.st-unv td.c-metric{border-left:3px solid var(--badb)}
tr.st-unv td{color:var(--bad)}
.blank{font-family:var(--mono);font-size:12px;color:var(--bad);font-weight:600}

/* badges */
.badge{display:inline-block;padding:2px 7px;border-radius:5px;font-size:11px;font-weight:650;text-decoration:none;white-space:nowrap;letter-spacing:.01em;border:1px solid transparent}
.badge-src{background:var(--accl);color:var(--acc);border-color:#c6e2d3}
.badge-src:hover{background:#d3ebde;color:var(--acc)}
.badge-sec{background:var(--warnl);color:var(--warn);border-color:var(--warnb)}
.badge-sec:hover{background:#faecc9;color:var(--warn)}
.badge-unv{background:var(--badl);color:var(--bad);border-color:var(--badb)}
.flagchip{display:inline-block;background:var(--badl);color:var(--bad);border:1px solid var(--badb);padding:1px 6px;border-radius:4px;font-size:10.5px;font-weight:700;text-decoration:none;font-family:var(--mono)}
.flagchip:hover{background:var(--bad);color:#fff}
.mat{font-size:11px;font-weight:700;padding:2px 6px;border-radius:4px;background:var(--bg3);color:var(--ink2)}
.mat-very{background:var(--badl);color:var(--bad)}
.mat-high{background:var(--warnl);color:var(--warn)}
.mat-medium{background:var(--bluel);color:var(--blue)}
.mat-low{background:var(--accl);color:var(--acc)}

/* risk cards */
.riskgrid{display:grid;gap:14px}
.riskcard{border:1px solid var(--line);border-left:4px solid var(--ink3);border-radius:10px;padding:18px 20px;background:#fff}
.riskcard.sev-high{border-left-color:var(--bad)}
.riskcard.sev-med{border-left-color:var(--warnb)}
.riskcard.sev-low{border-left-color:#2e7d54}
.riskcard h3{margin-bottom:11px;font-size:16.5px}
.riskcard dl{margin:0;display:grid;grid-template-columns:96px 1fr;gap:8px 14px;font-size:14.5px}
.riskcard dt{font-weight:650;color:var(--ink3);font-size:12px;text-transform:uppercase;letter-spacing:.05em;padding-top:2px}
.riskcard dd{margin:0;color:var(--ink2)}

/* steps */
.steps{display:grid;gap:2px}
.step{display:grid;grid-template-columns:44px 1fr;gap:16px;padding:20px 0;border-top:1px solid var(--line2)}
.step:first-child{border-top:0}
.stepno{width:34px;height:34px;border-radius:9px;background:var(--acc);color:#fff;font-weight:700;font-size:15px;display:flex;align-items:center;justify-content:center}
.step h3{font-size:16.5px}
.step p{margin:0;color:var(--ink2);font-size:15px;max-width:88ch}

/* swans */
.swans{display:grid;gap:14px}
.swan{border:1px solid var(--line);border-radius:10px;padding:19px 21px;background:#fff;border-top:3px solid var(--bad)}
.swan .ev{background:var(--bg2);padding:10px 13px;border-radius:6px;font-size:14px}
.swan .md{background:var(--bluel);padding:10px 13px;border-radius:6px;font-size:14px}
.swan .mit{background:var(--accl);padding:10px 13px;border-radius:6px;font-size:14px;margin-bottom:0}
.swan p{font-size:14.5px;color:var(--ink2)}

/* sources */
table.sources td:first-child{width:120px;white-space:nowrap}
.tier{font-size:10.5px;color:var(--ink3);font-family:var(--mono)}
.srctitle{font-weight:650;font-size:14px}
.srcname{color:var(--ink2);font-size:13.5px;margin:2px 0 4px}
.srcurl{font-family:var(--mono);font-size:11.5px;word-break:break-all;line-height:1.4}
.srcas{font-size:11.5px;color:var(--ink3);margin-top:3px}
.vlist{margin:6px 0 0;padding-left:18px;font-size:12.8px;color:var(--ink2)}
.vlist li{margin-bottom:3px}
details summary{cursor:pointer;font-size:12.5px;color:var(--blue);margin-top:6px;font-weight:550}
.rejected{background:var(--badl);border:1px solid var(--badb);border-radius:6px;padding:9px 12px;font-size:12.8px;margin-top:8px;color:var(--bad)}
.caveat{background:var(--warnl);border:1px solid var(--warnb);border-radius:6px;padding:9px 12px;font-size:12.8px;margin-top:8px;color:var(--warn)}
.legend{display:grid;gap:6px;margin-top:14px;font-size:13.5px;color:var(--ink2)}
.legend div{display:flex;align-items:center;gap:9px}

/* flags */
.flags{display:grid;gap:14px}
.flagcard{border:1px solid var(--line);border-left:4px solid var(--ink3);border-radius:10px;padding:18px 21px;background:#fff}
.flagcard.sev-high{border-left-color:var(--bad)}
.flagcard.sev-med{border-left-color:var(--warnb)}
.flagcard.sev-low{border-left-color:#9aa6b2}
.flagcard.sev-info{border-left-color:var(--blue)}
.flaghead{display:flex;gap:9px;align-items:center;margin-bottom:9px;flex-wrap:wrap}
.flagid{font-family:var(--mono);font-weight:700;font-size:13px;background:var(--ink);color:#fff;padding:2px 8px;border-radius:5px}
.flagsev{font-size:11px;text-transform:uppercase;letter-spacing:.07em;font-weight:700;color:var(--ink3)}
.flagcat{font-size:11.5px;color:var(--ink3);background:var(--bg3);padding:2px 8px;border-radius:4px}
.flagcard p{font-size:14px;color:var(--ink2);margin-bottom:9px}
.flagcard p:last-child{margin-bottom:0}
.flagcounts{display:flex;gap:26px;flex-wrap:wrap;margin:14px 0}
.flagcounts .big{display:block;font-size:26px;font-weight:700;color:var(--warn);line-height:1.1}
.flagcounts div{font-size:12.5px;color:var(--ink2);text-transform:uppercase;letter-spacing:.05em;font-weight:600}
.check .btn{font-size:13px;padding:7px 13px}
.muted{color:var(--ink3);font-size:12.5px}

/* misc */
.tight{margin:0;padding-left:20px;color:var(--ink2);font-size:15px}
.tight li{margin-bottom:8px}
.numbered{margin:0;padding-left:22px;color:var(--ink2);font-size:15px}
.numbered li{margin-bottom:11px}
.method{border-left:3px solid var(--line);padding:2px 0 2px 17px;margin-bottom:20px}
.method h3{font-size:15.5px}
.method p{color:var(--ink2);font-size:15px;margin:0;max-width:88ch}
td.win,td .win{background:var(--accl)!important;font-weight:700;color:var(--acc)}
.dataset h2{font-size:19px}
.sec-head{margin-bottom:14px}
.why{color:var(--ink2);font-size:15px;max-width:88ch;margin:0}

/* footer */
.foot{border-top:1px solid var(--line);background:var(--bg2);padding:26px 0;margin-top:20px}
.foot p{font-size:13px;color:var(--ink2);max-width:96ch}
.foot .tiny{font-size:12px;color:var(--ink3);margin-bottom:0}

@media(max-width:820px){
  .topbar-in{height:auto;flex-direction:column;align-items:stretch;gap:8px;padding:10px 0}
  .nav{margin-left:0}
  .page-head h1{font-size:25px}
  .verdict h2.vh{font-size:21px;max-width:none}
  .riskcard dl{grid-template-columns:1fr;gap:2px}
  .riskcard dt{margin-top:8px}
  td.c-note{min-width:200px}
}
"""


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True) if os.path.dirname(full) else None
    with open(full, "w") as f:
        f.write(text)


def link_audit():
    """Fail the build if any generated page links to a file that does not exist."""
    pages = [p for p, _ in NAV] + ["method.html"]
    problems = []
    for p in pages:
        full = os.path.join(ROOT, p)
        if not os.path.exists(full):
            problems.append(f"MISSING PAGE: {p}")
            continue
        text = open(full).read()
        for href in re.findall(r'href="([^"]+)"', text):
            if href.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target = href.split("#")[0]
            if not target:
                continue
            cand = os.path.join(ROOT, target)
            if not os.path.exists(cand):
                problems.append(f"{p} -> broken relative link: {href}")
        for anchor in re.findall(r'href="#([A-Za-z0-9_-]+)"', text):
            if f'id="{anchor}"' not in text:
                problems.append(f"{p} -> in-page anchor has no target: #{anchor}")
    # external http links must be well formed
    for p in pages:
        full = os.path.join(ROOT, p)
        if not os.path.exists(full):
            continue
        for href in re.findall(r'href="(https?://[^"]+)"', open(full).read()):
            if " " in href:
                problems.append(f"{p} -> malformed external link: {href}")
    return problems


def main():
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    write("assets/style.css", CSS)

    write("index.html", build_overview())
    write("decision.html", build_decision())
    write("economy.html", build_dataset_page(
        "economy.html", "Economy",
        "Labour market, industry mix and consumer spending — verified at county and city level.",
        ["labor", "business"]))
    write("demographics.html", build_dataset_page(
        "demographics.html", "Demographics",
        "Population, income, education and the official projection series.",
        ["demographics"]))
    write("schools.html", build_dataset_page(
        "schools.html", "Schools",
        "Public school enrollment and attainment, and what the official projection implies for family formation.",
        ["education"]))
    write("housing.html", build_dataset_page(
        "housing.html", "Housing &amp; property",
        "The land-value floor that protects the downside if the tenant leaves.",
        ["housing"]))
    write("tenant.html", build_dataset_page(
        "tenant.html", "Tenant credit",
        "Jack in the Box Inc. as an unsecured counterparty for the lease term, built from SEC filings only.",
        ["tenant"]))
    write("macro.html", build_dataset_page(
        "macro.html", "Macro &amp; tax",
        "Interest rates, inflation, property tax, transfer tax and regulatory load.",
        ["macro", "tax"]))
    write("risk.html", build_risk())
    write("projection.html", build_projection())
    write("sources.html", build_sources())
    write("flagged.html", build_flagged())
    write("method.html", build_methodology())

    # method is linked from the footer of flagged/decision? keep nav uncluttered but reachable:
    # inject a visible link to method.html on the flagged page
    fp = os.path.join(ROOT, "flagged.html")
    t = open(fp).read()
    t = t.replace('<section>\n      <div class="flags">',
                  '<section><h2>Method and privacy protocol</h2>'
                  '<p class="lede">How the verification standard works and how personal information was '
                  'handled: <a href="method.html">read the method and privacy protocol &rarr;</a></p></section>'
                  '<section>\n      <div class="flags">', 1)
    write("flagged.html", t)

    problems = link_audit()
    if problems:
        print("LINK AUDIT FAILED:")
        for p in problems:
            print("  -", p)
        sys.exit(1)

    pages = [p for p, _ in NAV] + ["method.html"]
    total = sum(len(open(os.path.join(ROOT, p)).read()) for p in pages)
    print(f"built {len(pages)} pages ({total:,} bytes) — link audit clean")


if __name__ == "__main__":
    main()
