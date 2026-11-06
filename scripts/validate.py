"""Validate local publication integrity; not an external semantic fact checker."""
import json
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
D=json.loads(Path('data/evidence.json').read_text())
class Check(HTMLParser):
    def __init__(self): super().__init__(); self.rows=[]; self.row=None
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='tr': self.row=[]
        if tag in ('a','link'):
            url=a.get('href','')
            if url.startswith('https://'):
                if self.row is not None: self.row.append(url)
            elif url and not url.startswith('#'): assert Path(url.split('#')[0]).is_file(),url
    def handle_endtag(self,tag):
        if tag=='tr': self.rows.append(self.row); self.row=None
allowed={s['url'] for s in D['sources'].values()}
count=0
for p in D['pages']:
    for r in p['rows']:
        assert r['source'] in D['sources']
        assert len(r['cells'])==len(p['columns'])
        assert r['status'] in ('Verified','Analysis','Unverified','Needs review')
        if '' in r['cells']: assert r['status']!='Verified'
        count+=1
for file in Path('.').glob('*.html'):
    c=Check(); c.feed(file.read_text())
    for row in c.rows[1:]: assert any(link in allowed for link in row),(file,row)
    for forbidden in ['googletagmanager.com','localhost','127.0.0.1','<iframe','<script']:
        assert forbidden not in file.read_text().lower(),(file,forbidden)
assert all(urlparse(s['url']).scheme=='https' for s in D['sources'].values())
print(f'PASS: {count} evidence rows; {len(list(Path(".").glob("*.html")))} pages; source links, local links, blank fields, prohibited embed checks.')
