# -*- coding: utf-8 -*-
"""Ревью процесса без календарей: периодичность возвращается плашкой.

Календарь над тактом убран — он не добавлял смысла: у месяца, квартала
и года заливка получалась почти одинаковой. Периодичность снова читается
лиловой плашкой, под ней название такта и описание."""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import apply, P

F = 'services/wp-marketing-services-seo-geo.html'

# ── разметка: календари убираем, плашку возвращаем ──────────────────────
s = open(P(F), encoding='utf-8').read()
s, n = re.subn(r'<div class="pg-flow-cal" aria-hidden="true">.*?</div></div>', '', s, flags=re.S)
assert n == 3, 'календарей найдено: %d' % n
PAIR = re.compile(r'<h3>(.*?)</h3><b class="pg-flow-n">(.*?)</b>')
s, m = PAIR.subn(lambda x: '<span class="pg-flow-when">%s</span><h3>%s</h3>'
                 % (x.group(1), x.group(2)), s)
assert m == 3, 'тактов найдено: %d' % m
open(P(F), 'w', encoding='utf-8').write(s)
print('ok   календари убраны:', n, '| плашек возвращено:', m)

# ── стили: календарные правила уходят, плашка возвращается ──────────────
CAL = re.compile(
    r"/\* Календарь над тактом.*?\.pg-flow-m\{transition:none;transform:none;opacity:1\}\}\n",
    re.S)
s = open(P(F), encoding='utf-8').read()
s, k = CAL.subn('', s)
assert k == 1, 'стили календаря не найдены'
open(P(F), 'w', encoding='utf-8').write(s)
print('ok   стили календаря убраны')

apply('плашка периодичности и заголовок такта',
      """/* периодичность — лиловый заголовок такта, как в эталоне;
   название такта идёт под ним чёрным и помельче */
.pg-flow-i h3{margin:16px 0 0;font-family:'Bounded','Geologica',sans-serif;""",
      """/* периодичность — лиловой плашкой, под ней название такта */
.pg-flow-when{align-self:flex-start;font-size:13px;line-height:16px;
  color:var(--white);background:var(--accent);border-radius:32px;
  padding:8px 16px}
.pg-flow-i h3{margin:8px 0 0;font-family:'Bounded','Geologica',sans-serif;""",
      files=[F])

# .pg-flow-n больше не используется
s = open(P(F), encoding='utf-8').read()
s = re.sub(r"\.pg-flow-n\{[^}]*\}\n", '', s)
open(P(F), 'w', encoding='utf-8').write(s)
print('ok   .pg-flow-n убран')
