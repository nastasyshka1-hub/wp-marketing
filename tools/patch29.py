# -*- coding: utf-8 -*-
"""Закрывающие плашки: кнопка справа снизу, как в плашках на услугах.

Раньше эти плашки шли колонкой — заголовок, описание и кнопка под ними
слева. Переводим на ту же строчную раскладку: текст слева, кнопка
в правой колонке и на базовой линии последней строки."""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import P

FILES = ['ai/wp-marketing-lab-ai-content.html',
         'ai/wp-marketing-lab-reputation.html',
         'industries/wp-marketing-industries-b2b.html',
         'services/wp-marketing-services-consulting.html',
         'services/wp-marketing-services-seo-geo.html',
         'standards/wp-marketing-standards.html']

BLK = re.compile(r'<div class="pg-cta">(.*?)(<div class="acts">)', re.S)
total = 0
for f in FILES:
    s = open(P(f), encoding='utf-8').read()
    e = s.rindex('</style>')
    head, body = s[:e], s[e:]

    def wrap(m):
        global total
        total += 1
        return ('<div class="pg-cta is-row"><div class="pg-cta-txt">'
                + m.group(1) + '</div>' + m.group(2))

    body2, n = BLK.subn(wrap, body)
    assert n >= 1, 'плашка не найдена: ' + f
    open(P(f), 'w', encoding='utf-8').write(head + body2)
    print('ok   %-46s плашек: %d' % (f.split('/')[-1], n))
print('всего плашек переведено в строку:', total)
