# -*- coding: utf-8 -*-
"""Блок «Ревью процесса» полностью повторяет эталон — блок «Ритм управления
проектом» со «Стандартов»: карточка календаря во всю ширину колонки,
под ней подпись, лиловый заголовок и описание. Плашки-пилюли и серые
стрелки между тактами убраны — в эталоне их нет.

Календарь остаётся годовым (колонка — квартал, строка — месяц внутри
квартала): в эталоне такт читается заливкой, а на месячной сетке
«каждый месяц», «каждый квартал» и «раз в год» дали бы три одинаковых
календаря."""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import apply, P, NB

F = 'services/wp-marketing-services-seo-geo.html'

OLD = """.pg-flow{display:grid;grid-template-columns:1fr 24px 1fr 24px 1fr;
  gap:var(--gutter);align-items:stretch}
.pg-flow-i{display:flex;flex-direction:column;gap:8px}"""
NEW = """.pg-flow{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));
  gap:var(--gutter);align-items:start}
.pg-flow-i{display:flex;flex-direction:column;gap:8px}"""
apply('эталон: три равные колонки без стрелок', OLD, NEW, files=[F])

OLD = """.pg-flow-cal{display:flex;flex-direction:column;gap:8px;padding:8px;
  margin:0 0 16px;max-width:200px;background:var(--white);
  border:1px solid var(--line);border-radius:var(--r-m)}"""
NEW = """.pg-flow-cal{display:flex;flex-direction:column;gap:8px;padding:8px;
  margin:0;background:var(--white);
  border:1px solid var(--line);border-radius:var(--r-m)}"""
apply('эталон: карточка во всю ширину колонки', OLD, NEW, files=[F])

OLD = """.pg-flow-when{align-self:flex-start;font-size:13px;color:var(--white);
  background:var(--accent);border-radius:99px;padding:8px 16px}
.pg-flow-i h3{margin:16px 0 0;font-family:'Bounded','Geologica',sans-serif;"""
NEW = """/* подпись такта — тихой строкой, как дни недели в шапке календаря:
   в эталоне лиловых пилюль нет */
.pg-flow-when{margin-top:16px;font-size:13px;line-height:16px;
  color:var(--ink-soft)}
.pg-flow-i h3{margin:0;font-family:'Bounded','Geologica',sans-serif;"""
apply('эталон: подпись такта без пилюли', OLD, NEW, files=[F])

apply('эталон: описание как в эталоне',
      ".pg-flow-i p{margin:0;font-size:16px;line-height:1.5;color:var(--ink);",
      ".pg-flow-i p{margin:0;font-size:15px;line-height:1.45;color:var(--ink);",
      files=[F])

# стрелки между тактами убираем из разметки
s = open(P(F), encoding='utf-8').read()
ARW = re.compile(r'<span class="pg-flow-arw" aria-hidden="true">.*?</span>\s*(?=<div class="pg-flow-i)', re.S)
s, n = ARW.subn('', s)
open(P(F), 'w', encoding='utf-8').write(s)
print('эталон: убрано стрелок:', n)
