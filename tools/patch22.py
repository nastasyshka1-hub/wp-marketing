# -*- coding: utf-8 -*-
"""Правки A2 и A3: блок «Примеры» на странице AI контент-завода наполняем
реальными данными из съёма позиций по двум статьям заказчика.

Сами тексты и адреса страниц не показываем — заказчик просил этого
не делать. На странице остаётся только динамика позиций.

Данные (частотность — пять замеров подряд):

  текст завода, кластер «как продавать…»
    205  2  2  2  7  5      15  1 1 1 5 2      5  2 1 1 3 3
      1  3  1  —  7  6       6  5 2 9 6 5      1  3 2 3 8 5
      8  3  2  —  5  5

  текст клиента, кластер «контроль обучения…»
     88 13 14 14 13 15      74  4 4 4 4 5    115  4 5 4 5 5
     44  1 86  1 35 29      38  1 — 2 47 83    8 85 95 — — 65
      8  9 88  —  75 80
"""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import P, NB

F = 'ai/wp-marketing-lab-ai-content.html'

# ключевой запрос каждого кластера по пяти замерам
LAB = [2, 2, 2, 7, 5]          # текст завода
CLI = [1, 86, 1, 35, 29]       # текст клиента
MAX = max(LAB + CLI)           # шкала: дальше от левого края — ниже позиция

def left(pos):
    return round((pos - 1) / (MAX - 1) * 100, 1)

rows = ''.join(
    '<div class="pg-serp-r"><span>Замер' + NB + '%d</span><div class="pg-serp-t">'
    '<i class="a" style="left:%s%%">%d</i><i class="b" style="left:%s%%">%d</i>'
    '</div></div>' % (n + 1, left(a), a, left(b), b)
    for n, (a, b) in enumerate(zip(LAB, CLI)))

NEW = (
 '<figure class="pg-sheets">'
 # ── текст завода ─────────────────────────────────────────────────────
 '<div class="pg-sheet is-win"><span class="pg-sheet-lb">Текст завода</span>'
 '<div class="pg-sheet-body" aria-hidden="true"><i style="width:100%"></i>'
 '<i style="width:94%"></i><i style="width:88%"></i><i style="width:96%"></i>'
 '<i style="width:72%"></i></div>'
 '<div class="pg-sheet-tags"><span>структура ответа</span><span>сущности</span>'
 '<span>разметка</span><span>FAQ</span></div>'
 '<div class="pg-sheet-res"><b>Топ-5</b><span>весь кластер из' + NB + 'семи запросов '
 'держится в' + NB + 'первой пятёрке пять замеров подряд</span></div></div>'
 # ── текст клиента ────────────────────────────────────────────────────
 '<div class="pg-sheet"><span class="pg-sheet-lb">Текст клиента</span>'
 '<div class="pg-sheet-body" aria-hidden="true"><i style="width:100%"></i>'
 '<i style="width:90%"></i><i style="width:84%"></i><i style="width:68%"></i></div>'
 '<div class="pg-sheet-tags"><span>писал сам клиент</span>'
 '<span>без' + NB + 'требований выдачи</span></div>'
 '<div class="pg-sheet-res"><b>От' + NB + '1 до' + NB + '86</b><span>кластер того' + NB + 'же размера, '
 'но' + NB + 'позиции скачут от' + NB + 'замера к' + NB + 'замеру</span></div></div>'
 # ── позиции ──────────────────────────────────────────────────────────
 '<div class="pg-sheet is-serp"><span class="pg-sheet-lb">Позиции в' + NB + 'топе</span>'
 '<div class="pg-serp">' + rows + '</div>'
 '<div class="pg-serp-lg"><span class="a">текст завода</span>'
 '<span class="b">текст клиента</span><span class="ax">первое место' + NB + '— слева</span></div>'
 '<div class="pg-sheet-res"><b>Стабильность против скачков</b><span>ключевой запрос '
 'кластера: у' + NB + 'текста завода разброс 2—7, у' + NB + 'текста клиента' + NB + '— 1—86</span></div></div>'
 '<figcaption>Слева материал из' + NB + 'цикла, в' + NB + 'центре текст, который клиент писал сам, '
 'справа' + NB + '— их позиции по' + NB + 'пяти замерам подряд. Сами тексты и' + NB + 'адреса страниц '
 'не' + NB + 'показываем: сравниваем только динамику съёма выдачи</figcaption>'
 '</figure>')

s = open(P(F), encoding='utf-8').read()
m = re.search(r'<figure class="pg-sheets">.*?</figure>', s, re.S)
assert m, 'блок «Примеры» не найден'
open(P(F), 'w', encoding='utf-8').write(s[:m.start()] + NEW + s[m.end():])
print('ok   A2/A3 блок «Примеры» наполнен данными, замеров:', len(LAB))
