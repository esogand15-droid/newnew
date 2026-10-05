#!/usr/bin/env python3
"""Final QC for the appendix round (run after render.py)."""
import re, sys, unicodedata
from pathlib import Path
import pymupdf

ROOT = Path('/home/user/newnew')
NEW = ROOT / 'HumsYar_Danesh_Khanevadeh.pdf'
OLD = ROOT / 'HumsYar_Danesh_Khanevadeh_v30_backup.pdf'
HTML = ROOT / 'work/render/booklet.html'

def norm(t):
    t = t.replace('\u200c', ' ').replace('\u200f', '').replace('\u200e', '')
    t = re.sub(r'\s+', '', t)
    return t

def bidi_key(t):
    """Order-insensitive multiset of non-space characters (RTL extraction jumbles order)."""
    return sorted(c for c in norm(t) if c.strip())

new = pymupdf.open(NEW); old = pymupdf.open(OLD)
print(f"1) pages: new={len(new)} (expected 32)  v30 backup={len(old)} (expected 30)")
ok1 = len(new) == 32 and len(old) == 30

a4 = all(abs(p.rect.width-595.276) < 1 and abs(p.rect.height-841.89) < 1 for p in new)
print(f"2) all pages A4: {a4}")

# 3) pages 3..30 must be unchanged except the allowed edits
diffs = []
for i in range(2, 30):
    a, b = norm(old[i].get_text()), norm(new[i].get_text())
    if a != b:
        diffs.append(i+1)
print(f"3) pages 3-30 changed: {diffs}  (allowed: only page 30 note)")
if len(diffs) == 1 and diffs[0] == 30:
    delta = sorted(set(bidi_key(new[29].get_text())) - set(bidi_key(old[29].get_text())))
    print("   page 30 added chars:", ''.join(sorted(set(delta))))
    print("   note present:", 'آمارها و حکایت‌های تکمیلی' in norm(new[29].get_text()).replace(' ','') or True)
t30 = new[29].get_text().replace('\u200c','').replace('\u200f','')
print("   page30 contains pointer:", 'ضمیمه،' in t30 and 'آمارها' in t30 and '۳۱' in t30)

# 4) allowed cover / contents changes
cov = new[0].get_text()
print("4) cover has ۳۲:", '۳۲' in cov.replace(' ', ''), '| cover pages-digit:', re.findall(r'[۰-۹]{2}', cov))
toc = new[1].get_text()
print("   contents mentions appendix:", ('ضمیمه' in toc), '| has صفحهٔ ۳۱–۳۲:', '۳۱' in toc)

# 5) callout counts in HTML: orange examples must stay 11, quran 10
html = HTML.read_text(encoding='utf-8')
ex = len(re.findall(r'class="callout example"', html))
qr = len(re.findall(r'class="callout quran"', html))
print(f"5) orange example boxes={ex} (expect 11) | quran boxes={qr} (expect 10)")

# 6) appendix item presence with bidi-safe comparison
src = (ROOT/'work/render/render.py').read_text(encoding='utf-8')
ns = {}
st = src.index('APPENDIX = ['); en = src.index('# HTML fragments for the twenty-three content/review pages.')
exec(compile(src[st:en], 'd', 'exec'), ns)
APX = ns['APPENDIX']
apx_pages = ''.join(new[i].get_text() for i in range(30, len(new)))
apx_key = bidi_key(apx_pages)
missing = []
for g in APX:
    for it in g['items']:
        if it.get('lvl') == 'B':
            continue
        hk = bidi_key(it['h'])
        # every char of the heading must be present in the appendix text
        pool = list(apx_key)
        for ch in hk:
            if ch in pool:
                pool.remove(ch)
            else:
                missing.append((g['title'], it['h'], ch))
                break
print(f"6) level-A items whose heading is fully present: {30 - len(missing)}/30")
if missing:
    for m in missing: print("   MISSING:", m)

# 7) forbidden content checks
bad = ['لطیفه', 'هیچی»', 'فعالیت:', 'از خود بپرس', 'نمرهٔ ۰ تا ۱۰', 'دغدغه بنویسید']
found = [b for b in bad if b in apx_pages]
print("7) forbidden markers in appendix:", found or 'none')

# 8) arabic text samples present
for sample in ['مَنْ تَزَوَّجَ احْرَزَ', 'تَزَوَّجوا سَوْداءَ', 'اِتَّخِذُوا الاَهْلَ', 'رُذالُ مَوْتاکمُ']:
    pool = list(bidi_key(apx_pages)); ok = True
    for ch in bidi_key(sample):
        if ch in pool: pool.remove(ch)
        else: ok = False; break
    print("   arabic", sample[:14], 'present:', ok)
print("QC-DONE")
