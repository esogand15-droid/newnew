#!/usr/bin/env python3
"""Render a zoomed crop of a source-book page around a searchable anchor.

Usage:
  python3 work/appendix/zoom.py PAGE "anchor" [pad_left] [pad_right] [pad_up] [pad_down] [zoom]
Anchor must exist literally in the page's text layer (numbers, latin words and
most Persian words work; corrupted words may not). Output goes to
work/appendix/crops/p<page>-<slug>.png
"""
import re, sys
from pathlib import Path
import pymupdf

SRC = Path('/home/user/newnew/work/source.pdf')
OUTDIR = Path('/home/user/newnew/work/appendix/crops')
OUTDIR.mkdir(parents=True, exist_ok=True)


def main():
    page_no = int(sys.argv[1])
    anchor = sys.argv[2]
    pad_l = float(sys.argv[3]) if len(sys.argv) > 3 else 8
    pad_r = float(sys.argv[4]) if len(sys.argv) > 4 else 8
    pad_u = float(sys.argv[5]) if len(sys.argv) > 5 else 30
    pad_d = float(sys.argv[6]) if len(sys.argv) > 6 else 30
    zoom = float(sys.argv[7]) if len(sys.argv) > 7 else 4.0
    doc = pymupdf.open(SRC)
    page = doc[page_no - 1]
    rects = page.search_for(anchor)
    if not rects:
        print(f'ANCHOR NOT FOUND on p{page_no}: {anchor!r}')
        # dump lines to help
        for b in page.get_text('blocks')[:30]:
            print(round(b[1]), round(b[3]), repr(b[4][:80]))
        return 1
    r = rects[0]
    clip = pymupdf.Rect(max(0, r.x0 - pad_l), max(0, r.y0 - pad_u),
                        min(page.rect.x1, r.x1 + pad_r), min(page.rect.y1, r.y1 + pad_d))
    pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), clip=clip)
    slug = re.sub(r'[^0-9A-Za-zآ-ی]+', '-', anchor)[:30]
    out = OUTDIR / f'p{page_no}-{slug}.png'
    pix.save(out)
    print(f'{out}  ({pix.width}x{pix.height})  clip={clip}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
