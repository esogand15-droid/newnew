#!/usr/bin/env python3
"""Print normalized-text context around queries: python3 ctx.py "q1" "q2" ..."""
import re, sys
from pathlib import Path
TXT = Path('book-text.txt').read_text(encoding='utf-8')
parts = re.split(r'<<<PDFPAGE (\d+)>>>', TXT)
P = {int(parts[i]): parts[i+1] for i in range(1, len(parts)-1, 2)}
def norm(s):
    s = s.replace('\u200c',' ').replace('\u200f',' ').replace('\u200e',' ')
    return re.sub(r'\s+','', s)
N = {p: norm(t) for p,t in P.items()}
for q in sys.argv:
    nq = norm(q); print(f"\n########## «{q}»")
    n=0
    for p in sorted(N):
        t = N[p]; i = t.find(nq)
        if i>=0:
            print(f"  [p{p}] ...{t[max(0,i-260):i+420]}...")
            n+=1
            if n>=4: break
    if n==0: print("   NOT FOUND")
