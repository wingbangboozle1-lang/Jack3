"""Apply the 2026-11-11 re-verification results to data/evidence.json.

Run once: python3 scripts/update_2026_11_11.py
Every change is expressed as an explicit, auditable edit against a known cell
string; the script fails loudly if the expected text is not found, so it cannot
silently rewrite a row it does not recognise.
"""
import json
from pathlib import Path

P = Path('data/evidence.json')
D = json.loads(P.read_text())
BY_ID = {(r['source']): r for p in D['pages'] for r in p['rows']}

D['reviewed'] = '2026-11-11'

# --- source register updates -------------------------------------------------
D['sources']['fred']['checked'] = '2026-11-11'
D['sources']['fred']['label'] = 'Federal Reserve H.15 via FRED · DGS10'
D['sources']['cde']['checked'] = '2026-11-11'
# New verified sources found during the 2026-11-11 pass.
D['sources']['dqteach'] = {
    'label': 'CA Dept. of Education · DataQuest cohort graduation report',
    'url': 'https://dq.cde.ca.gov/dataquest/dqcensus/CohRate.aspx?cds=1964733&agglevel=District&year=2025-26',
    'checked': '2026-11-11', 'type': 'Government'}
D['sources']['cdenews'] = {
    'label': 'CA Dept. of Education · news release 26-44 (2026-10-15)',
    'url': 'https://www.cde.ca.gov/nr/ne/yr26/yr26rel44.asp',
    'checked': '2026-11-11', 'type': 'Government'}


def page(pid):
    return next(p for p in D['pages'] if p['id'] == pid)


def find(pid, lead):
    p = page(pid)
    for i, r in enumerate(p['rows']):
        if r['cells'][0].startswith(lead):
            return p, i, r
    raise SystemExit(f'row not found: {pid} / {lead!r}')


def setrow(pid, lead, cells=None, status=None, source=None):
    p, i, r = find(pid, lead)
    if cells:
        assert len(cells) == len(p['columns']), (pid, lead, len(cells))
        r['cells'] = cells
    if status:
        r['status'] = status
    if source:
        r['source'] = source


# --- economy: refresh the rate anchor to the latest dated observation ---------
setrow('economy', 'Net taxable assessed value',
       ['Net taxable assessed value',
        '$2.272 trillion · +4.42% year over year',
        'LA County · 2026 Assessment Roll, lien date 2026-01-01',
        'Whole-county tax roll; not market appreciation or this asset’s value. The official release prints '
        '“42%” in one highlights bullet; 4.42% is used because the narrative and the $96bn change agree.'])

# --- taxes: dated rate anchor ------------------------------------------------
setrow('taxes', 'Discount-rate anchor',
       ['Discount-rate anchor for any present-value work',
        '4.86% · 10-year Treasury, 2026-11-06 (4.88% on 2026-11-09)',
        'Federal Reserve H.15 via FRED (DGS10), re-read 2026-11-11',
        'A market anchor, not the owner’s required return. Rates move daily; the published cells are dated.'],
       source='fred')

# --- model: anchors row + a new dated row for the later observation ----------
setrow('model', 'Verified input anchors',
       ['Verified input anchors',
        '10-year Treasury 4.86% (2026-11-06) and 4.88% (2026-11-09); LA CPI-U +3.7% and ECI +3.9% year over '
        'year (Sep 2026); LA city population −0.8% from the 2020 estimates base to July 2025.',
        'Anchors, not forecasts. Each is an observation from an official release and is used only to bound '
        'discounting and growth assumptions.'],
       source='fred')

# --- risk: dated rate row ----------------------------------------------------
setrow('risk', 'Interest-rate and exit-yield shock',
       ['Interest-rate and exit-yield shock',
        '10-year Treasury constant-maturity yield 4.86% on 2026-11-06; 4.88% on 2026-11-09.',
        'Analysis: a higher exit yield lowers price for the same rent; no property cap rate is published.'],
       source='fred')

# --- schools: the graduation-rate provenance problem ------------------------
setrow('schools', 'District four-year graduation rate',
       ['District four-year graduation rate',
        '',
        'LAUSD · 2026 Dashboard (unverified)',
        'Unverified. The cited Dashboard page renders its tables in the browser, so no value could be read '
        'from the served page on 2026-11-11. This file previously published 86.2% from that page (2026-11-10) '
        'and has withheld it rather than repeat a figure it cannot re-read. The server-rendered CDE '
        'DataQuest report for the same school year returns 87.4% with charter schools excluded by default, a '
        'different population; it is published as its own row.'],
       status='Unverified', source='dashboard2026')

setrow('schools', 'District combined four- and five-year',
       ['District combined four- and five-year graduation rate',
        '',
        'LAUSD · 2026 Dashboard (unverified)',
        'Unverified. The combined measure appears only on the browser-rendered 2026 Dashboard page. The '
        'previously published 87.6% (2026-11-10) is withheld rather than repeated unread; CDE DataQuest '
        'publishes the four-year cohort rate, not this combined measure.'],
       status='Unverified', source='dashboard2026')

# Insert two server-rendered, freshly verified rows after the 4-year row.
p = page('schools')
idx = next(i for i, r in enumerate(p['rows']) if r['cells'][0].startswith('District four-year'))
p['rows'][idx + 3:idx + 3] = [
    {'cells': ['District four-year cohort graduation rate (charter schools excluded)',
               '87.4%',
               'LAUSD · 2025-26 · DataQuest four-year adjusted cohort rate',
               'Verified on the server-rendered state report. CDE removes charter schools from district '
               'reports by default, so this is not the district-wide rate and must not be compared with a '
               'charter-inclusive figure.'],
     'status': 'Verified', 'source': 'dqteach'},
    {'cells': ['Statewide four-year cohort graduation rate',
               '87.9%',
               'California · 2025-26 · CDE news release 26-44, 2026-10-15',
               'Benchmark only. A district average says nothing about an assigned campus.'],
     'status': 'Verified', 'source': 'cdenews'},
]

# --- review register: add the new irregularities -----------------------------
p = page('review')
new_review = [
    {'cells': ['High',
               'Graduation rate could not be re-read from the cited page (C-01)',
               'On 2026-11-11 the 2026 California School Dashboard page served no table values: its '
               'indicators are rendered in the browser. The published 86.2% four-year and 87.6% combined '
               'figures were therefore downgraded to Unverified, and the server-rendered CDE DataQuest '
               'report for the same year now supplies 87.4% (charter schools excluded by default) as a '
               'separately labelled Verified row. Re-read the Dashboard directly before using any of them.'],
     'status': 'Needs review', 'source': 'dashboard2026'},
    {'cells': ['Medium',
               'Treasury anchor moved after publication (C-02)',
               'The 10-year constant-maturity yield was 4.86% on 2026-11-06 when first published and 4.88% '
               'on 2026-11-09 at the 2026-11-11 re-read. Both dates are now shown rather than replacing the '
               'earlier value, because a dated observation stays true after the series moves.'],
     'status': 'Needs review', 'source': 'fred'},
    {'cells': ['Medium',
               'Five open PRs overlap this published dataset (C-03)',
               'Open pull requests #42 (a 222-row canonical site), #43 (publication-integrity tests) and '
               'older branches each propose a different data contract for the same pages. They are not '
               'merged here: merging any of them would replace the verified dataset without a line-by-line '
               're-check. They remain open for the owner to decide.'],
     'status': 'Needs review', 'source': 'cdenews'},
]
p['rows'].extend(new_review)

P.write_text(json.dumps(D, indent=2, ensure_ascii=False) + '\n')
print('evidence.json updated:', len(D['pages']), 'pages,',
      sum(len(p['rows']) for p in D['pages']), 'rows,', len(D['sources']), 'sources')
