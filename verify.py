"""Run with python3 verify.py. Standard-library checks, no dependencies."""
import json,re,subprocess
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
root=Path(__file__).resolve().parent
class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.links=[];self.assets=[];self.texts={};self.active=None;self.details=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a':self.links.append(a.get('href',''))
        if tag=='img':
            assert a.get('alt'),'Image missing alt text'
            self.assets.append(a['src'])
        if tag=='link':self.assets.append(a['href'])
        if tag=='details':self.details+=1
        if tag=='p' and a.get('id','').startswith('text-'):
            self.active=a['id'];self.texts[self.active]=''
    def handle_data(self,data):
        if self.active:self.texts[self.active]+=data
    def handle_endtag(self,tag):
        if tag=='p':self.active=None
s=(root/'index.html').read_text();p=Page();p.feed(s)
c=json.loads((root/'content.json').read_text());blocks=[t for pg in c['pages'] for sec in pg['sections'] for t in sec['texts']]
assert c['total_nodes']==205 and c['unique_nodes']==159
assert len(blocks)==159 and len(p.texts)==159
assert all(p.texts[t['id']]==t['text'] for t in blocks),'Verbatim source coverage failed'
assert len(set(' '.join(t['text'].split()) for t in blocks))==159
assert all(n==1 for n in Counter(p.ids).values()),'Duplicate HTML ID'
for href in p.links:
    assert href,'Empty link'
    if href.startswith('#') and href!='#':assert href[1:] in p.ids,href
    elif not href.startswith('#'):assert href in ['https://t.me/mos_aleksa','https://www.instagram.com/mos.numerology'],href
for asset in p.assets:assert (root/asset).is_file() and (root/asset).stat().st_size>0,asset
assert p.details==5
for price in ['400','700','1300','2500','4800','6900','1672','2351']:assert price in s
for term in ['3–5-7 днів','сума бронювання не повертається','50% — бронювання','100% оплата','Нумерологія не є науковим методом діагностики']:assert term in s,term
script=re.search(r'<script>(.*?)</script>',s,re.S).group(1)
r=subprocess.run(['node','--check','-'],input=script,text=True,capture_output=True)
assert r.returncode==0,r.stderr
print('PASS: 159/159 unique source blocks verbatim from 205 source nodes')
print(f'PASS: {len(p.links)} links, all fragment targets valid, 2 allowed external destinations')
print(f'PASS: {len(p.assets)} local asset references exist, images have alt text')
print('PASS: 5 accessible native accordions, 8 distinct required prices, payment/refund/turnaround terms')
print('PASS: author-attributed health disclaimer and inline JavaScript syntax')
