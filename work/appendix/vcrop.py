#!/usr/bin/env python3
"""Crop a full-width band of a source page between two y-anchors.
usage: vcrop.py PAGE y1 y2 out [zoom]   (y = points from page top)
"""
import sys, pymupdf
from pathlib import Path
SRC = Path('/home/user/newnew/work/source.pdf')
OUT = Path('/home/user/newnew/work/appendix/vcrops'); OUT.mkdir(exist_ok=True)
p = int(sys.argv[1]); y1=float(sys.argv[2]); y2=float(sys.argv[3]); name=sys.argv[4]
zoom = float(sys.argv[5]) if len(sys.argv)>5 else 2.6
doc = pymupdf.open(SRC); page = doc[p-1]
r = pymupdf.Rect(20, max(0,y1), page.rect.x1-20, min(page.rect.y1, y2))
pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom,zoom), clip=r)
pix.save(OUT/f'{name}.png'); print(OUT/f'{name}.png', pix.width, pix.height, r)
