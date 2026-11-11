"""Validate local publication integrity; not an external semantic fact checker."""
import json
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
D=json.loads(Path('data/evidence.json').read_text())
class Check(HTMLParser):
    def __init__(self): super().__init__(); self.rows=[]; self.row=None; self.body=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='tbody': self.body=True
        if tag=='tr' and self.body: self.row=[]
        if tag in ('a','link'):
            url=a.get('href','')
            if url.startswith('https://'):
                if self.row is not None: self.row.append(url)
            elif url and not url.startswith('#'): assert Path(url.split('#')[0]).is_file(),url
    def handle_endtag(self,tag):
        if tag=='tr' and self.row is not None: self.rows.append(self.row); self.row=None
        if tag=='tbody': self.body=False
allowed={s['url'] for s in D['sources'].values()}
count=0
for p in D['pages']:
    for r in p['rows']:
        assert r['source'] in D['sources']
        assert len(r['cells'])==len(p['columns'])
        assert r['status'] in ('Verified','Analysis','Unverified','Needs review')
        if '' in r['cells']: assert r['status']!='Verified'
        if r['status']=='Unverified' and p['id']!='review': assert r['cells'][1]=='', (p['id'],r)
        count+=1
for file in Path('.').glob('*.html'):
    c=Check(); c.feed(file.read_text())
    for row in c.rows[1:]: assert any(link in allowed for link in row),(file,row)
    for forbidden in ['googletagmanager.com','localhost','127.0.0.1','<iframe','<script']:
        assert forbidden not in file.read_text().lower(),(file,forbidden)
assert all(urlparse(s['url']).scheme=='https' for s in D['sources'].values())
allowed_hosts={'www.census.gov','www.bls.gov','investors.jackinthebox.com','osfm.fire.ca.gov','www.conservation.ca.gov','msc.fema.gov','www.cde.ca.gov','www.dir.ca.gov','zimas.lacity.org','www.irs.gov','assessor.lacounty.gov','finance.lacity.gov','pubs.usgs.gov','www.fire.ca.gov','fred.stlouisfed.org','www.ftb.ca.gov','www.lavote.gov','www.caschooldashboard.org','sustain.scag.ca.gov','lacounty.gov','thesource.metro.net','dof.ca.gov','dq.cde.ca.gov'}
assert all(urlparse(s['url']).netloc in allowed_hosts for s in D['sources'].values())
print(f'PASS: {count} evidence rows; {len(list(Path(".").glob("*.html")))} pages; source links, local links, blank fields, prohibited embed checks.')
