# -*- coding: utf-8 -*-
"""Правки из «правки правок.zip»: 01/04 — кнопка по низу в строчных плашках,
05 — стрелка в меню не прыгает при наведении, 06 — прячем заметку про ПСБ,
02/07 — календари ревью в стиле наших календарей со страницы стандартов."""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import apply, sub, pages, P, NB

# ── 01 + 04 ─────────────────────────────────────────────────────────────
# Кнопка в строчной плашке прижимается к низу текстового блока,
# а не висит по центру: так она попадает на базовую линию последней строки.
apply('01/04 кнопка по низу',
      '.pg-cta.is-row .acts{grid-column:2;grid-row:1 / -1;align-self:center}',
      '.pg-cta.is-row .acts{grid-column:2;grid-row:1 / -1;align-self:end}')

# ── 05 ──────────────────────────────────────────────────────────────────
# Шеврон нарисован уголком квадрата: при повороте на 45° чернила уходят
# вниз от центра рамки на ~3px, при 225° — на столько же вверх. Раньше
# сдвиг был одинаковый (−1px) в обоих состояниях, поэтому стрелка
# подпрыгивала. Теперь сдвиг зеркальный и оптический центр стоит на месте.
apply('05 шеврон вниз',
      "border-bottom:1.5px solid currentColor;transform:translateY(-1px) rotate(45deg);",
      "border-bottom:1.5px solid currentColor;transform:translateY(-3px) rotate(45deg);")
apply('05 шеврон вверх',
      '.has-sub.open>a::after,.has-sub.open>.nav-sec::after{transform:translateY(-1px) rotate(225deg)}',
      '.has-sub.open>a::after,.has-sub.open>.nav-sec::after{transform:translateY(3px) rotate(225deg)}')

# ── 06 ──────────────────────────────────────────────────────────────────
# Заметку про ПСБ прячем, но не удаляем: вернуть — снять комментарий.
NOTE = ('<div class="pg-note"><p>ПСБ' + NB + '— пример третьего направления: '
        'ведём только ссылочный профиль, SEO сайта остаётся на' + NB + 'стороне' + NB + 'клиента</p></div>')
apply('06 прячем заметку про ПСБ', NOTE, '<!-- скрыто по просьбе заказчика: ' + NOTE + ' -->',
      files=['industries/wp-marketing-industries-fintech.html'])

# ── 02 + 07 ─────────────────────────────────────────────────────────────
# Календарь такта переезжает на анатомию наших календарей со «Стандартов»:
# белая карточка с обводкой, шапка с подписями и сетка клеток 8px.
# Год делится на четыре квартала по три месяца: колонка — квартал,
# строка — месяц внутри квартала.
F = 'services/wp-marketing-services-seo-geo.html'

OLD_CSS = """.pg-flow-cal{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));
  gap:8px;margin:0 0 16px;max-width:216px}
.pg-flow-m{display:block;aspect-ratio:1;border-radius:6px;
  background:var(--cold);transform:scale(.6);opacity:0;
  transition:transform .4s cubic-bezier(.16,.86,.26,1) var(--d,0ms),
             opacity .4s ease var(--d,0ms)}
.pg-flow-m.on{background:var(--accent)}
.pg-flow-i.in .pg-flow-m{transform:none;opacity:1}"""

NEW_CSS = """.pg-flow-cal{display:flex;flex-direction:column;gap:8px;padding:8px;
  margin:0 0 16px;max-width:200px;background:var(--white);
  border:1px solid var(--line);border-radius:var(--r-m)}
.pg-flow-q,.pg-flow-ms{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));
  gap:8px}
.pg-flow-q span{font-size:13px;line-height:16px;text-align:center;
  color:var(--ink-soft)}
.pg-flow-m{display:block;aspect-ratio:1;border-radius:8px;
  background:var(--cold);transform:scale(.6);opacity:0;
  transition:transform .4s cubic-bezier(.16,.86,.26,1) var(--d,0ms),
             opacity .4s ease var(--d,0ms)}
.pg-flow-m.on{background:var(--accent)}
.pg-flow-i.in .pg-flow-m{transform:none;opacity:1}"""

apply('02/07 стиль календаря', OLD_CSS, NEW_CSS, files=[F])

# комментарий над блоком — чтобы правка читалась в коде
apply('02/07 комментарий',
      """/* Календарь года над тактом: двенадцать месяцев, закрашены те,
   в которые такт повторяется. */""",
      """/* Календарь года над тактом: карточка той же анатомии, что календари
   на «Стандартах» — обводка, шапка с подписями, клетки 8px. Колонка —
   квартал, строка — месяц внутри квартала; закрашены те месяцы,
   в которые такт повторяется. */""", files=[F])

WD = ('<div class="pg-flow-q"><span>I' + NB + 'кв</span><span>II' + NB + 'кв</span>'
      '<span>III' + NB + 'кв</span><span>IV' + NB + 'кв</span></div>')

def cells(on):
    """on — набор номеров месяцев (1..12), которые закрашены.
    Порядок ячеек: строка — месяц внутри квартала, колонка — квартал."""
    out = []
    for row in range(3):
        for q in range(4):
            m = q * 3 + row + 1
            d = (row * 4 + q) * 40
            cls = 'pg-flow-m on' if m in on else 'pg-flow-m'
            out.append('<i class="%s" style="--d:%dms"></i>' % (cls, d))
    return ''.join(out)

PATTERNS = [
    set(range(1, 13)),      # каждый месяц
    {1, 4, 7, 10},          # каждый квартал
    {1},                    # раз в год
]

src = open(P(F), encoding='utf-8').read()
found = re.findall(r'<div class="pg-flow-cal" aria-hidden="true">.*?</div>', src)
assert len(found) == 3, 'ожидалось три календаря, найдено %d' % len(found)
for old, on in zip(found, PATTERNS):
    new = ('<div class="pg-flow-cal" aria-hidden="true">' + WD +
           '<div class="pg-flow-ms">' + cells(on) + '</div></div>')
    assert src.count(old) == 1
    src = src.replace(old, new)
open(P(F), 'w', encoding='utf-8').write(src)
print('02/07 разметка календарей: 3')
