# -*- coding: utf-8 -*-
"""Правка 01/04, шаг второй: кнопка реально встаёт по низу.

`grid-row:1 / -1` считает строки явной сетки, а строк в шаблоне не было —
линия −1 совпадала с первой, и кнопка сидела в одной строке с заголовком.
Поэтому текст заворачиваем в колонку, а плашка становится сеткой
из двух ячеек: слева текст, справа кнопка, обе прижаты к низу."""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import apply, P

OLD = """.pg-cta.is-row{display:grid;grid-template-columns:minmax(0,1fr) auto;
  align-items:center;gap:16px 48px;background:var(--white);
  border:1px solid var(--line)}"""
NEW = """.pg-cta.is-row{display:grid;grid-template-columns:minmax(0,1fr) auto;
  align-items:end;gap:16px 48px;background:var(--white);
  border:1px solid var(--line)}
/* текст — одна колонка сетки, чтобы кнопка равнялась по низу всей плашки,
   а не по строке заголовка */
.pg-cta.is-row .pg-cta-txt{grid-column:1;display:flex;flex-direction:column;
  gap:16px;min-width:0}"""
apply('01/04 сетка плашки', OLD, NEW)

apply('01/04 кнопка по низу',
      '.pg-cta.is-row .acts{grid-column:2;grid-row:1 / -1;align-self:end}',
      '.pg-cta.is-row .acts{grid-column:2;align-self:end}')

# разметка: заворачиваем заголовки и абзацы в .pg-cta-txt
BLK = re.compile(r'(<div class="pg-cta is-row[^"]*">)(.*?)(<div class="acts">)', re.S)
FILES = ['services/wp-marketing-services-consulting.html',
         'services/wp-marketing-services-seo-geo.html',
         'services/wp-marketing-services.html']
total = 0
for f in FILES:
    s = open(P(f), encoding='utf-8').read()
    def wrap(m):
        global total
        if 'pg-cta-txt' in m.group(2):
            return m.group(0)
        total += 1
        return m.group(1) + '<div class="pg-cta-txt">' + m.group(2) + '</div>' + m.group(3)
    s2 = BLK.sub(wrap, s)
    if s2 != s:
        open(P(f), 'w', encoding='utf-8').write(s2)
print('01/04 обёрнуто текстовых блоков:', total)
