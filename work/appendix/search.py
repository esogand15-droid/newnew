#!/usr/bin/env python3
"""Search helper for the corrupted-OCR book text.

Usage:
  python3 work/appendix/search.py "query" [more queries...]
Prints page number + context for each hit. Query is matched against a
normalized copy of the text (line-joins collapsed, all spaces removed).
"""
import re, sys, unicodedata
from pathlib import Path

TXT = Path(__file__).with_name('book-text.txt').read_text(encoding='utf-8')
pages = re.split(r'<<<PDFPAGE (\d+)>>>', TXT)
# pages[0] is preamble; then pairs (num, text)
PAGES = {}
for i in range(1, len(pages) - 1, 2):
    PAGES[int(pages[i])] = pages[i + 1]


def norm(s):
    s = s.replace('\u200c', ' ').replace('\u200f', ' ').replace('\u200e', ' ')
    s = re.sub(r'\s+', '', s)
    return s


NORMPAGES = {p: norm(t) for p, t in PAGES.items()}


def search(q):
    nq = norm(q)
    hits = []
    for p in sorted(NORMPAGES):
        t = NORMPAGES[p]
        start = 0
        while True:
            i = t.find(nq, start)
            if i < 0:
                break
            hits.append((p, max(0, i - 90), t[i - 90:i + 160]))
            start = i + 1
    return hits


if __name__ == '__main__':
    for q in sys.argv[1:]:
        h = search(q)
        print(f'\n########## «{q}»  →  {len(h)} hit(s) ##########')
        for p, _, ctx in h[:12]:
            print(f'  [p{p}] ...{ctx}...')
        if len(h) > 12:
            print(f'  ... and {len(h)-12} more')
