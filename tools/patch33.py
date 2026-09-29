# -*- coding: utf-8 -*-
"""Перечисление в блоке материала — в одну колонку.

В две колонки длинные формулировки ломались на разной высоте и читались
как таблица. Список идёт сплошным столбиком, пункт за пунктом."""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import apply, P, pages

apply('перечисление материала в один столбик',
      """.pg-mg-cols{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));
  gap:8px 24px;margin:8px 0 0}""",
      """.pg-mg-cols{display:grid;grid-template-columns:1fr;
  gap:8px;margin:8px 0 0}""")

# правило для узких экранов теперь дублирует основное
n = 0
for f in pages():
    s = open(f, encoding='utf-8').read()
    s2 = s.replace('\n  .pg-mg-cols{grid-template-columns:1fr}', '')
    if s2 != s:
        open(f, 'w', encoding='utf-8').write(s2); n += 1
print('ok   %-3d убрано дублирующее правило для узких экранов' % n)
