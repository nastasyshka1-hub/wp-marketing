# -*- coding: utf-8 -*-
"""Панель позиций в блоке «Примеры»: вместо шкалы с точками — сетка замеров.

Шкала не годится: у текста клиента выброс на 86-ю позицию, из-за него
все остальные значения слипаются у левого края, а на первом и третьем
замере метки двух текстов накладывались друг на друга. Сетка показывает
те же числа без искажения."""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import apply, P, NB

F = 'ai/wp-marketing-lab-ai-content.html'
LAB = [2, 2, 2, 7, 5]
CLI = [1, 86, 1, 35, 29]

cells = lambda vals, cls: ''.join('<i class="%s">%d</i>' % (cls, v) for v in vals)
GRID = ('<div class="pg-serp">'
        '<div class="pg-serp-r is-h"><span>Замер</span>' +
        ''.join('<b>%d</b>' % (i + 1) for i in range(5)) + '</div>'
        '<div class="pg-serp-r"><span>текст завода</span>' + cells(LAB, 'a') + '</div>'
        '<div class="pg-serp-r"><span>текст клиента</span>' + cells(CLI, 'b') + '</div>'
        '</div>')

s = open(P(F), encoding='utf-8').read()
m = re.search(r'<div class="pg-serp">.*?</div>\s*<div class="pg-serp-lg">.*?</div>', s, re.S)
assert m, 'панель позиций не найдена'
LG = ('<div class="pg-serp-lg"><span class="a">текст завода</span>'
      '<span class="b">текст клиента</span>'
      '<span class="ax">число' + NB + '— позиция в' + NB + 'выдаче, чем меньше, тем выше</span></div>')
s = s[:m.start()] + GRID + LG + s[m.end():]

CSS_OLD = re.compile(r'\.pg-serp\{.*?\.pg-serp-lg span\.ax::before\{display:none\}\n', re.S)
CSS_NEW = """.pg-serp{display:grid;gap:8px}
.pg-serp-r{display:grid;grid-template-columns:96px repeat(5,minmax(0,1fr));
  align-items:center;gap:8px}
.pg-serp-r>span{font-size:13px;line-height:16px;color:var(--ink-soft)}
.pg-serp-r.is-h>b{font-weight:400;font-size:13px;line-height:16px;
  text-align:center;color:var(--ink-faint)}
.pg-serp-r i{display:block;height:32px;border-radius:8px;font-style:normal;
  font-size:15px;line-height:32px;text-align:center}
.pg-serp-r i.a{background:var(--accent);color:var(--white)}
.pg-serp-r i.b{background:var(--white);color:var(--ink);
  box-shadow:inset 0 0 0 1px var(--line)}
.pg-serp-lg{display:flex;flex-wrap:wrap;gap:8px 24px;font-size:13px;
  line-height:16px;color:var(--ink-soft)}
.pg-serp-lg span{display:flex;align-items:center;gap:8px}
.pg-serp-lg span::before{content:"";width:8px;height:8px;border-radius:50%}
.pg-serp-lg span.a::before{background:var(--accent)}
.pg-serp-lg span.b::before{background:var(--steel)}
.pg-serp-lg span.ax::before{display:none}
"""
s2, n = CSS_OLD.subn(CSS_NEW, s)
assert n == 1, 'CSS панели позиций не найден'
open(P(F), 'w', encoding='utf-8').write(s2)
print('ok   A2/A3 панель позиций — сетка замеров')

# комментарий к компоненту и подпись раздела
apply('A2/A3 комментарий к панели',
      """Два ряда: заводской материал акцентом, копирайтерский — серым;
   цветом закодирован источник, а не величина. */""",
      """Два ряда: заводской материал акцентом, клиентский — контуром;
   цветом закодирован источник, а не величина. */""", files=[F])
apply('A2/A3 заголовок раздела',
      '<h3 class="sh-b">Реальные тексты: завод и' + NB + 'копирайтер</h3>',
      '<h3 class="sh-b">Реальные тексты: завод и' + NB + 'клиент</h3>', files=[F])
apply('A2/A3 диапазоны не разрываются',
      'у' + NB + 'текста завода разброс 2—7, у' + NB + 'текста клиента' + NB + '— 1—86',
      'у' + NB + 'текста завода разброс <span class="nbr">2—7</span>, '
      'у' + NB + 'текста клиента' + NB + '— <span class="nbr">1—86</span>', files=[F])
s = open(P(F), encoding='utf-8').read()
if '.nbr{' not in s:
    s = s.replace('.pg-serp{', '.nbr{white-space:nowrap}\n.pg-serp{', 1)
    open(P(F), 'w', encoding='utf-8').write(s)
    print('ok   A2/A3 добавлен .nbr')
