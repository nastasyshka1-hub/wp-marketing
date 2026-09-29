# -*- coding: utf-8 -*-
"""FinTech: формы без иконок, макет отчёта — в планшете, колонки равной высоты."""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import apply, P

F = 'industries/wp-marketing-industries-fintech.html'

# ── иконки в шапках форм ────────────────────────────────────────────────
s = open(P(F), encoding='utf-8').read()
s, n = re.subn(r'<div class="pg-ms-h"><span class="pg-ms-ic">.*?</span>(.*?)</div>(?=<p|<div class="pg-ms-fields")',
               r'\1', s, flags=re.S)
assert n == 2, 'шапок с иконкой найдено: %d' % n
open(P(F), 'w', encoding='utf-8').write(s)
print('ok   иконки в шапках форм убраны:', n)

# ── колонки блока «Замер» одной высоты ──────────────────────────────────
apply('колонки блока «Замер» одной высоты',
      """.pg-ms{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));
  gap:var(--gutter);align-items:start}""",
      """.pg-ms{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));
  gap:var(--gutter);align-items:stretch}""", files=[F])

# ── макет отчёта переезжает в корпус планшета ───────────────────────────
s = open(P(F), encoding='utf-8').read()
m = re.search(r'<div class="pg-ms-mock">(.*?)</div>\s*</div>\s*</section>', s, re.S)
assert m, 'макет отчёта не найден'
s = (s[:m.start()] + '<div class="pg-ms-mock"><div class="pg-ms-scr">' + m.group(1)
     + '</div></div>\n  </div>\n</section>' + s[m.end():])
open(P(F), 'w', encoding='utf-8').write(s)
print('ok   макет отчёта завёрнут в экран планшета')

apply('корпус планшета',
      """.pg-ms-mock{display:flex;flex-direction:column;gap:16px;padding:32px;
  border-radius:var(--r-l);border:2px solid var(--graphite);
  background:var(--white)}""",
      """/* макет отчёта стоит в корпусе планшета: тёмная рамка, скруглённый
   экран и точка камеры на верхней кромке */
.pg-ms-mock{display:flex;flex-direction:column;gap:8px;padding:16px;
  border-radius:24px;background:var(--graphite)}
.pg-ms-mock::before{content:'';flex:none;align-self:center;width:8px;height:8px;
  border-radius:50%;background:rgba(255,255,255,.28)}
.pg-ms-scr{flex:1;display:flex;flex-direction:column;gap:16px;padding:32px;
  border-radius:var(--r-m);background:var(--white)}""", files=[F])
