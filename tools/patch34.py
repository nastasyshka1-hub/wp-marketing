# -*- coding: utf-8 -*-
"""«Опыт работы с финансовыми компаниями» — полноценный заголовок раздела.

Была тихая подпись 13px по центру. Ставим обычный h2 раздела: Bounded,
графит, по левому краю сетки — как все заголовки на странице."""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import apply, P, NB

F = 'industries/wp-marketing-industries-fintech.html'
T = 'Опыт работы с' + NB + 'финансовыми компаниями'

apply('заголовок ленты логотипов',
      '<section class="ip-logos" aria-label="Опыт работы с финансовыми компаниями">\n'
      '  <div class="shell">\n'
      '    <p class="ls-lbl">Опыт работы с финансовыми компаниями</p>\n'
      '  </div>',
      '<section class="ip-logos">\n'
      '  <div class="shell">\n'
      '    <div class="sec-head"><h2>' + T + '</h2></div>\n'
      '  </div>',
      files=[F])

# подпись больше нигде не используется
s = open(P(F), encoding='utf-8').read()
assert 'class="ls-lbl"' not in s
s2 = re.sub(r'\.ls-lbl\{[^}]*\}\n', '', s)
open(P(F), 'w', encoding='utf-8').write(s2)
print('ok   стиль .ls-lbl убран:', s != s2)
