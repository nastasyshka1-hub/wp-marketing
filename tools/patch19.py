# -*- coding: utf-8 -*-
"""Календарь такта — ровно тот же компонент, что на «Стандартах»:
шапка пн-вс и четыре недели клеток. Такт читается подписью, как
в эталоне у «Ежемесячно» и «Ежеквартально»."""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import apply, P

F = 'services/wp-marketing-services-seo-geo.html'

apply('эталон: сетка пн-вс',
      """.pg-flow-cal{display:flex;flex-direction:column;gap:8px;padding:8px;
  margin:0;background:var(--white);
  border:1px solid var(--line);border-radius:var(--r-m)}
.pg-flow-q,.pg-flow-ms{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));
  gap:8px}""",
      """.pg-flow-cal{display:flex;flex-direction:column;gap:8px;padding:8px;
  margin:0;max-width:328px;background:var(--white);
  border:1px solid var(--line);border-radius:var(--r-m)}
.pg-flow-q,.pg-flow-ms{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));
  gap:8px}""", files=[F])

apply('эталон: комментарий к календарю',
      """/* Календарь года над тактом: карточка той же анатомии, что календари
   на «Стандартах» — обводка, шапка с подписями, клетки 8px. Колонка —
   квартал, строка — месяц внутри квартала; закрашены те месяцы,
   в которые такт повторяется. */""",
      """/* Календарь над тактом — тот же компонент, что на «Стандартах»:
   обводка, шапка пн-вс, четыре недели клеток. Закрашен день, в который
   такт случается; периодичность читается подписью под календарём. */""",
      files=[F])

WD = '<div class="pg-flow-q">' + ''.join(
     '<span>%s</span>' % d for d in ('пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс')) + '</div>'
cells = lambda: ''.join(
    '<i class="pg-flow-m%s" style="--d:%dms"></i>' % (' on' if i == 0 else '', i * 18)
    for i in range(28))

s = open(P(F), encoding='utf-8').read()
found = re.findall(r'<div class="pg-flow-cal" aria-hidden="true">.*?</div></div>', s)
assert len(found) == 3, 'календарей: %d' % len(found)
for old in found:
    s = s.replace(old, '<div class="pg-flow-cal" aria-hidden="true">' + WD +
                  '<div class="pg-flow-ms">' + cells() + '</div></div>', 1)
open(P(F), 'w', encoding='utf-8').write(s)
print('эталон: перестроено календарей: 3')
