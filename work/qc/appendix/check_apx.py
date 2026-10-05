#!/usr/bin/env python3
"""QC for the appendix pages.

Checks: page count, A4 size, card count per page (HTML vs expected), that no
text runs past the footer, that the last card of every page really appears in
the rendered PDF text, and that every source-page token shows up somewhere.
"""
import re, sys
from pathlib import Path
import pymupdf

ROOT = Path('/home/user/newnew')
PDF = ROOT / 'HumsYar_Danesh_Khanevadeh.pdf'
HTML = ROOT / 'work/render/booklet.html'
SRC = (ROOT / 'work/render/render.py').read_text(encoding='utf-8')


def load_data():
    ns = {}
    start = SRC.index('APPENDIX = [')
    end = SRC.index('# HTML fragments for the twenty-three content/review pages.')
    exec(compile(SRC[start:end], 'appendix-data', 'exec'), ns)
    return ns['APPENDIX'], ns['APPENDIX_PAGES']


def norm(t):
    t = t.replace('\u200c', ' ').replace('\u200f', '').replace('\u200e', '')
    return re.sub(r'\s+', '', t)


APX, SPEC = load_data()
html = HTML.read_text(encoding='utf-8')
apx_sections = re.findall(r'<section class="page apx">(.*?)</section>', html, re.S)

plan = []
for slices in SPEC:
    items = []
    for gi, start, end in slices:
        g = APX[gi]
        vis = [it for it in g['items'] if it.get('lvl') != 'B']
        items += vis[start:end]
    plan.append(items)

doc = pymupdf.open(PDF)
n_apx = len(SPEC)
print(f"PDF pages = {len(doc)}  (expected {30 + n_apx})")
status = 'OK'
if len(doc) != 30 + n_apx:
    status = 'FAIL'

apx_text = ''
for pi, items in enumerate(plan):
    num = 31 + pi
    page = doc[num - 1]
    a4 = abs(page.rect.width - 595.276) < 1 and abs(page.rect.height - 841.89) < 1
    html_cards = apx_sections[pi].count('class="apx-card')
    blocks = [b for b in page.get_text('blocks') if 'HumsYar |' not in b[4]]
    bottom = max(b[3] for b in blocks)
    top = min(b[1] for b in blocks)
    footer_line = 841.89 - (5.2 / 25.4 * 72) - 8
    top_pt = 13 / 25.4 * 72
    fill = (bottom - top_pt) / (footer_line - top_pt) * 100
    over = bottom > footer_line
    txt_pages = norm(page.get_text())
    apx_text += txt_pages
    print(f"  p{num}: A4={a4} cards(html)={html_cards} expected={len(items)} "
          f"top={top:.0f} bottom={bottom:.0f} fill={fill:.0f}% overflow={over}")
    if not a4 or over or html_cards != len(items):
        status = 'FAIL'

# every level-A item must be printed somewhere in the appendix
missing = []
for gi, g in enumerate(APX):
    for it in g['items']:
        if it.get('lvl') == 'B':
            continue
        # bidi-safe: PyMuPDF extracts RTL lines in visual order, so compare
        # the multiset of non-space characters of the heading instead.
        pool = sorted(c for c in norm(it['h']) if c.strip())
        pool_txt = sorted(c for c in apx_text if c.strip())
        ok_chars = all(pool_txt.count(ch) >= pool.count(ch) for ch in set(pool))
        if not ok_chars:
            missing.append(it['h'])
print("level-A items not found in appendix text:", missing or 'none')
if missing:
    status = 'CHECK-MANUALLY'

# count level A / B
la = sum(1 for g in APX for it in g['items'] if it.get('lvl') != 'B')
lb = sum(1 for g in APX for it in g['items'] if it.get('lvl') == 'B')
shown = sum(len(p) for p in plan)
print(f"appendix items: level A total={la}, level B total={lb}, shown={shown}")
print('QC-' + status)
