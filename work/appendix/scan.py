#!/usr/bin/env python3
"""Inventory scanner: pull candidate A/B items out of the corrupted book text.

Usage: python3 work/appendix/scan.py [stats|quotes|names|all]
"""
import re, sys
from pathlib import Path

TXT = Path(__file__).with_name('book-text.txt').read_text(encoding='utf-8')
parts = re.split(r'<<<PDFPAGE (\d+)>>>', TXT)
PAGES = {}
for i in range(1, len(parts) - 1, 2):
    PAGES[int(parts[i])] = parts[i + 1]


def flat(t):
    """Collapse whitespace but keep a marker for line breaks."""
    t = t.replace('\u200c', ' ').replace('\u200f', '').replace('\u200e', '')
    t = re.sub(r'[ \t]+', ' ', t)
    t = re.sub(r'\n+', ' ', t)
    return t


def sentences(t):
    return [s.strip() for s in re.split(r'(?<=[.!؟؛:])\s+', t) if s.strip()]


def show_stats():
    print('\n================ NUMERIC SENTENCES ================')
    for p in sorted(PAGES):
        if p < 9:
            continue
        for s in sentences(flat(PAGES[p])):
            if re.search(r'[0-9]', s):
                print(f'[p{p}] {s[:300]}')


def show_quotes():
    print('\n================ QUOTED / NARRATIVE SENTENCES ================')
    for p in sorted(PAGES):
        if p < 9:
            continue
        for s in sentences(flat(PAGES[p])):
            if '«' in s or '»' in s or 'فرمود' in s or 'روایت' in s or 'حدیث' in s:
                print(f'[p{p}] {s[:320]}')


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if what in ('stats', 'all'):
        show_stats()
    if what in ('quotes', 'all'):
        show_quotes()
