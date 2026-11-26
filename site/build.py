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

def _sync_brand_assets(repo, out):
    import shutil, re
    public = repo / "public"
    for filename in ["favicon.svg", "apple-touch-icon.png", "frankie-stocks-lockup.svg", "frankie-stocks-lockup-dark.svg"]:
        shutil.copyfile(public / filename, out / filename)
    for page in out.rglob("*.html"):
        prefix = "../" * (len(page.relative_to(out).parts) - 1)
        content = page.read_text()
        content = re.sub(r'<link[^>]+rel=["\'](?:icon|apple-touch-icon)["\'][^>]*>', '', content)
        links = f'<link rel="icon" type="image/svg+xml" href="{prefix}favicon.svg"><link rel="apple-touch-icon" href="{prefix}apple-touch-icon.png">'
        content = content.replace("</head>", links + "</head>")
        page.write_text(content)

_build_content = build
def build(repo, out):
    _build_content(repo, out)
    _sync_brand_assets(repo, out)


def _add_family_navigation(repo, out):
    import shutil
    series = out / "series"
    series.mkdir(exist_ok=True)
    for icon in (repo / ".github/brand/series").glob("*.svg"):
        shutil.copyfile(icon, series / icon.name)
    for page in out.rglob("*.html"):
        prefix = "../" * (len(page.relative_to(out).parts) - 1)
        nav = '<nav aria-label="Frankie projects" style="display:flex;flex-wrap:wrap;justify-content:center;gap:4px;padding:28px 20px;max-width:100%;border-top:1px solid #8883"><a href="https://songhaifan.github.io/frankie-brain/" title="Frankie Brain" style="display:inline-flex;padding:6px"><img src="{prefix}series/brain.svg" width="28" height="28" alt="Frankie Brain" style="object-fit:contain;border:0;max-width:none"></a><a href="https://songhaifan.github.io/frankie-brain-ios/" title="Frankie Brain · iOS" style="display:inline-flex;padding:6px"><img src="{prefix}series/brain-ios.svg" width="28" height="28" alt="Frankie Brain · iOS" style="object-fit:contain;border:0;max-width:none"></a><a href="https://songhaifan.github.io/frankie-cards/" title="Frankie Cards" style="display:inline-flex;padding:6px"><img src="{prefix}series/cards.svg" width="28" height="28" alt="Frankie Cards" style="object-fit:contain;border:0;max-width:none"></a><a href="https://songhaifan.github.io/frankie-dictionary/" title="Blue Dictionary" style="display:inline-flex;padding:6px"><img src="{prefix}series/dictionary.svg" width="28" height="28" alt="Blue Dictionary" style="object-fit:contain;border:0;max-width:none"></a><a href="https://songhaifan.github.io/frankie-generative-art/" title="Frankie Generative Art Gallery" style="display:inline-flex;padding:6px"><img src="{prefix}series/generative-art.svg" width="28" height="28" alt="Frankie Generative Art Gallery" style="object-fit:contain;border:0;max-width:none"></a><a href="https://songhaifan.github.io/frankie-goal/" title="Frankie Goal" style="display:inline-flex;padding:6px"><img src="{prefix}series/goal.svg" width="28" height="28" alt="Frankie Goal" style="object-fit:contain;border:0;max-width:none"></a><a href="https://songhaifan.github.io/frankie-guitar/" title="Frankie Guitar" style="display:inline-flex;padding:6px"><img src="{prefix}series/guitar.svg" width="28" height="28" alt="Frankie Guitar" style="object-fit:contain;border:0;max-width:none"></a><a href="https://songhaifan.github.io/frankie-list/" title="Frank’s Life List" style="display:inline-flex;padding:6px"><img src="{prefix}series/list.svg" width="28" height="28" alt="Frank’s Life List" style="object-fit:contain;border:0;max-width:none"></a><a href="https://songhaifan.github.io/frankie-mbti/" title="Frankie MBTI" style="display:inline-flex;padding:6px"><img src="{prefix}series/mbti.svg" width="28" height="28" alt="Frankie MBTI" style="object-fit:contain;border:0;max-width:none"></a><a href="https://songhaifan.github.io/frankie-onitama/" title="Frankie Onitama" style="display:inline-flex;padding:6px"><img src="{prefix}series/onitama.svg" width="28" height="28" alt="Frankie Onitama" style="object-fit:contain;border:0;max-width:none"></a><a href="https://songhaifan.github.io/frankie-poker/" title="Frankie Poker" style="display:inline-flex;padding:6px"><img src="{prefix}series/poker.svg" width="28" height="28" alt="Frankie Poker" style="object-fit:contain;border:0;max-width:none"></a><a href="https://songhaifan.github.io/frankie-tarot/" title="Frankie Tarot" style="display:inline-flex;padding:6px"><img src="{prefix}series/tarot.svg" width="28" height="28" alt="Frankie Tarot" style="object-fit:contain;border:0;max-width:none"></a><a href="https://songhaifan.github.io/frankie-tarot-api/" title="Frankie Tarot API" style="display:inline-flex;padding:6px"><img src="{prefix}series/tarot-api.svg" width="28" height="28" alt="Frankie Tarot API" style="object-fit:contain;border:0;max-width:none"></a><a href="https://songhaifan.github.io/frankie-werewolf/" title="Werewolf Local" style="display:inline-flex;padding:6px"><img src="{prefix}series/werewolf.svg" width="28" height="28" alt="Werewolf Local" style="object-fit:contain;border:0;max-width:none"></a></nav>'
        nav = nav.replace("{prefix}", prefix)
        content = page.read_text().replace("</body>", nav + "</body>")
        page.write_text(content)

_build_native_intro = build
def build(repo, out):
    _build_native_intro(repo, out)
    _add_family_navigation(repo, out)

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='_site');a=ap.parse_args();build(Path(__file__).resolve().parents[1],Path(a.out).resolve())
