#!/usr/bin/env python3
"""Build the independent bilingual Stocks introduction without app/env dependencies."""
import argparse,html,json,re,shutil
from pathlib import Path
H=html.escape

def build(repo,out):
 cfg=json.loads((repo/'site/project.json').read_text());content=json.loads((repo/'site/content.json').read_text());out.mkdir(parents=True,exist_ok=True);(out/'media').mkdir(exist_ok=True)
 for name in ['style.css','demo.js']:shutil.copy(repo/'site'/name,out/name)
 for name in ['dashboard','ranked','settings','edit']:shutil.copy(repo/f'site/assets/{name}-current.png',out/f'media/{name}.png')
 for src,dest in [('docs/readme/banner.png','banner.png'),('docs/readme/assets/frankie.svg','signature.svg')]:shutil.copy(repo/src,out/'media'/dest)
 # Reuse the real app palette, including its dark theme, instead of drifting tokens.
 css=(repo/'src/styles/app.css').read_text();tokens=css[css.index(':root'):css.index('* {')];(out/'tokens.css').write_text(tokens)
 chart=(repo/'src/components/HorizonRow.tsx').read_text();ratios=re.search(r'return (\[0, 0\.236, 0\.382, 0\.618, 1\])',chart)
 if not ratios:raise ValueError('Review band explanation: app thresholds changed')
 data={'prices':[100,104,99,107,106,110],'benchmark':[100,102,103,104,105,106],'ratios':json.loads(ratios.group(1))}
 (out/'.nojekyll').touch()
 for lang,c in content.items():
  zh=lang=='zh';pre='../' if zh else './';dest=out/'zh' if zh else out;dest.mkdir(exist_ok=True)
  rows=lambda xs:''.join('<article><h3>'+H(a)+'</h3><p>'+H(b)+'</p></article>' for a,b in xs)
  gallery=''.join(f'<figure><a href="{pre}media/{name}.png"><img src="{pre}media/{name}.png" alt="{H(cap)}" width="1468" height="1247" loading="lazy"></a><figcaption>{H(cap)}</figcaption></figure>' for name,cap in zip(['dashboard','ranked','settings','edit'],c['captions']))
  d={**data,'return':c['return'],'excess':c['excess'],'points':c['points']};serialized=json.dumps(d,ensure_ascii=False).replace('<','\\u003c')
  page=f'''<!doctype html><html lang="{'zh-CN' if zh else 'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Frank Stocks | {'主题自选与地平线图' if zh else 'Thematic watchlists & horizon charts'}</title><meta name="description" content="{H(c['intro'])}"><link rel="canonical" href="{cfg['pages_url']+('zh/' if zh else '')}"><link rel="alternate" hreflang="en" href="{cfg['pages_url']}"><link rel="alternate" hreflang="zh-CN" href="{cfg['pages_url']}zh/"><link rel="stylesheet" href="{pre}tokens.css"><link rel="stylesheet" href="{pre}style.css"><meta name="theme-color" content="#f4f3f1"><meta property="og:type" content="website"><meta property="og:url" content="{cfg['pages_url']+('zh/' if zh else '')}"><meta property="og:title" content="Frank Stocks"><meta property="og:description" content="{H(c['intro'])}"><meta property="og:image" content="{cfg['pages_url']}media/banner.png"></head><body>
<a class="skip" href="#main">{H(c['skip'])}</a><header class="shell"><a class="brand" href="{pre}">Frank Stocks</a><nav aria-label="{'页面导航' if zh else 'Page navigation'}"><a href="#chart">{H(c['nav'][0])}</a><a href="#use">{H(c['nav'][1])}</a><a href="#screens">{H(c['nav'][2])}</a><a href="#start">{H(c['nav'][3])}</a><a href="{pre}" lang="en" {'aria-current="page"' if not zh else ''}>EN</a><a href="{pre}zh/" lang="zh-CN" {'aria-current="page"' if zh else ''}>中文</a></nav></header>
<main id="main" class="shell"><section class="hero"><div><h1>{'<br>'.join(H(x) for x in c['headline'].splitlines())}</h1><p class="lead">{H(c['intro'])}</p><a class="button" href="{cfg['app_url']}">{H(c['open'])} ↗</a></div><figure><div class="hero-image"><img src="{pre}media/dashboard.png" alt="{H(c['captions'][0])}" width="1468" height="1247" fetchpriority="high"></div><figcaption>{H(c['captions'][0])}</figcaption></figure></section>
<section class="section concept" id="chart"><div><h2>{H(c['concept_title'])}</h2><p class="lead">{H(c['concept'])}</p><p>{H(c['concept_note'])}</p><a class="reference" href="https://idl.uw.edu/papers/horizon">{H(c['reference'])} ↗</a></div><div class="demo"><h3>{H(c['demo_title'])}</h3><p class="small">{H(c['demo_note'])}</p><p class="sample-values">{H(c['sample'])}</p><div class="demo-controls"><label><input id="benchmark" type="checkbox"> {H(c['benchmark'])}</label><label>{H(c['bands'])} <select id="bands"><option value="fibonacci">{H(c['fibonacci'])}</option><option value="normal">{H(c['normal'])}</option></select></label></div><div class="example-strip"><svg id="chart-example" viewBox="0 0 500 70" role="img" aria-label="{'合成数值的四层地平线图示例' if zh else 'Four-band horizon diagram using synthetic values'}"></svg></div><div id="result" aria-live="polite"></div><noscript><p>{'示例：价格变化 10%，基准变化 6%，相差 4 个百分点。' if zh else 'Example: 10% price change minus 6% benchmark change is 4 percentage points.'}</p></noscript></div></section>
<section class="section"><h2>{H(c['features_title'])}</h2><div class="features">{rows(c['features'])}</div></section>
<section class="section" id="use"><h2>{H(c['workflow_title'])}</h2><ol class="steps">{''.join('<li><h3>'+H(a)+'</h3><p>'+H(b)+'</p></li>' for a,b in c['steps'])}</ol></section>
<section class="section" id="screens"><h2>{H(c['screens_title'])}</h2><div class="gallery">{gallery}</div></section>
<section class="section" id="start"><h2>{H(c['data_title'])}</h2><div class="data">{rows(c['data'])}</div><div class="run"><h3>{H(c['run'])}</h3><pre><code>npm ci\nnpm run dev</code></pre><p>{H(c['run_note'])}</p><a href="https://github.com/{cfg['repository']}/blob/main/site/GUIDE.md">{H(c['guide'])} ↗</a></div></section></main>
<footer class="shell"><a href="https://github.com/SonghaiFan"><img src="{pre}media/signature.svg" width="92" height="34" alt="Frankie"></a><span>{H(c['footer'])}</span><a href="https://github.com/{cfg['repository']}">{H(c['source'])} ↗</a></footer><script id="demo-data" type="application/json">{serialized}</script><script src="{pre}demo.js" defer></script></body></html>'''
  (dest/'index.html').write_text(page)
 print(out)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='_site');a=ap.parse_args();build(Path(__file__).resolve().parents[1],Path(a.out).resolve())
