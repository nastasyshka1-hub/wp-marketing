# -*- coding: utf-8 -*-
"""Одиночные формы: заголовок переезжает внутрь обводки, иконка убрана.

Раньше заголовок висел над карточкой, а внутри стоял кружок с иконкой
и пустая шапка — читалось как два разных блока."""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import apply, P

FILES = ['ai/wp-marketing-lab-ai-content.html',
         'ai/wp-marketing-lab-reputation.html',
         'ai/wp-marketing-lab-smm.html']

HEAD = re.compile(r'<div class="sec-head"><h2>(.*?)</h2></div>\s*(?=<form class="pg-ms-form is-solo")', re.S)
ICON = re.compile(r'<div class="pg-ms-h"><span class="pg-ms-ic">.*?</span><div class="pg-ms-ht"></div></div>', re.S)

for f in FILES:
    s = open(P(f), encoding='utf-8').read()
    m = HEAD.search(s)
    assert m, 'заголовок над формой не найден: ' + f
    title = m.group(1)
    s = s[:m.start()] + s[m.end():]
    s, n = ICON.subn('<h2>' + title + '</h2>', s, count=1)
    assert n == 1, 'шапка формы с иконкой не найдена: ' + f
    open(P(f), 'w', encoding='utf-8').write(s)
    print('ok   заголовок внутрь обводки:', f.split('/')[-1], '—', re.sub(r'\s+', ' ', title)[:46])

apply('заголовок формы того же кегля, что и h3',
      '.pg-ms-form h3{margin:0;font-family:',
      '.pg-ms-form h2,.pg-ms-form h3{margin:0;font-family:', files=FILES)
