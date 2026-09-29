# -*- coding: utf-8 -*-
"""Правки из «Комментарии к сайту 18.09»: пункты S3, R3, R4, R6 и баг B1."""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import apply, P, NB

REP = 'ai/wp-marketing-lab-reputation.html'
SMM = 'ai/wp-marketing-lab-smm.html'

def read(f):  return open(P(f), encoding='utf-8').read()
def write(f, s): open(P(f), 'w', encoding='utf-8').write(s)
def body(s):  return s.rindex('</style>')      # начало разметки: всё после стилей

def cut(f, what, pat):
    """Вырезает первое вхождение pat в разметке (не в CSS)."""
    s = read(f); b = body(s)
    m = re.compile(pat, re.S).search(s, b)
    assert m, 'не найдено: ' + what
    write(f, s[:m.start()] + s[m.end():])
    print('ok   ' + what)

# ── B1: лид блока «Проблема» дословно повторял заголовок первой карточки ──
apply('B1 лид блока «Проблема»',
      '<p>Решение принимается до' + NB + 'контакта с' + NB + 'вами</p></div>',
      '<p>Четыре причины, по' + NB + 'которым репутация съедает спрос ещё до' + NB + 'рекламы.</p></div>',
      files=[REP], limit=1)

# ── R3: связка «проблема — решение» перед методологией ──────────────────
BRIDGE = ('<div class="pg-note"><p>Все четыре причины сходятся в' + NB + 'одном: репутационную '
          'выдачу никто не' + NB + 'измеряет. Поэтому начинаем не' + NB + 'с' + NB + 'ответов на' + NB + 'отзывы, '
          'а' + NB + 'со' + NB + 'съёма выдачи' + NB + '— и' + NB + 'дальше по' + NB + 'шагам.</p></div>')
s = read(REP)
if 'Все четыре причины сходятся' not in s:
    m = re.search(r'<section class="sec" id="problem">.*?</div>(?=\s*</div>\s*</section>)', s, re.S)
    assert m, 'блок «Проблема» не найден'
    write(REP, s[:m.end()] + '\n    ' + BRIDGE + s[m.end():])
    print('ok   R3 связка «проблема — решение»')

# ── R4: блок видимости — только мысль исходника, без цифр из кейса ──────
apply('R4 формулировка исходника',
      'чем' + NB + 'сотня нейтральных: всё решает то,' + NB + 'по' + NB + 'скольким запросам '
      'страница ранжируется и' + NB + 'с' + NB + 'какой' + NB + 'позиции.',
      'чем' + NB + 'сотня нейтральных: одна карточка агрегатора ранжируется '
      'по' + NB + 'десяткам запросов с' + NB + 'первой' + NB + 'позиции.',
      files=[REP])
cut(REP, 'R4 двухколоночная схема убрана',
    r'<div class="pg-rch-g">.*?(?=<p class="pg-rch-foot">)')

# CSS схемы больше не нужен
s = read(REP)
s2 = re.sub(r'\.pg-rch-g\{.*?\.pg-rch-cap\{[^}]*\}\n', '', s, flags=re.S)
write(REP, s2)
print('ok   R4 CSS схемы убран:', s != s2)

# ── R6: лид-магнит без обещанных цифр ───────────────────────────────────
cut(REP, 'R6 цифры лид-магнита убраны',
    r'<div class="pg-offer-nums">.*?(?=<ul class="pg-offer-list">)')

# ── S3: сравнение читается как сравнение ────────────────────────────────
apply('S3 лид сравнения',
      '<h3 class="sh-b">Конвейер против классической схемы</h3></div>',
      '<h3 class="sh-b">Конвейер против классической схемы</h3>'
      '<p>Слева' + NB + '— как это устроено в' + NB + 'ручном производстве, '
      'справа' + NB + '— что меняет конвейер.</p></div>',
      files=[SMM])

s = read(SMM)
if 'is-cmp' not in s:
    s = s.replace('<table class="pg-table">', '<table class="pg-table is-cmp">', 1)
    s = s.replace('<th scope="col">Наш конвейер</th>',
                  '<th scope="col" class="is-us">Наш конвейер</th>', 1)
    s = re.sub(r'(<tr><td>[^<]*</td><td>[^<]*</td>)<td>([^<]*)</td></tr>',
               r'\1<td class="is-us">\2</td></tr>', s)
    CSS = """/* Сравнительная таблица: наша колонка — не ещё один столбец, а вывод.
   Подложка и вес отделяют её от левой части, шапка — лиловая. */
.pg-table.is-cmp .is-us{background:var(--lilac);font-weight:600;
  color:var(--graphite)}
.pg-table.is-cmp th.is-us{color:var(--accent)}
.pg-table.is-cmp thead th.is-us{border-radius:var(--r-m) var(--r-m) 0 0}
.pg-table.is-cmp tbody tr:last-child .is-us{border-radius:0 0 var(--r-m) var(--r-m)}
</style>"""
    s = s.replace('</style>', CSS, 1)
    write(SMM, s)
    print('ok   S3 колонка «Наш конвейер» выделена:', s.count('class="is-us"'))
