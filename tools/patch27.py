# -*- coding: utf-8 -*-
"""Блок «Примеры»: предложения начинаются с прописной буквы.

Подписи-чипсы («структура ответа», «сущности») остаются строчными —
это ярлыки, а не предложения, и так же они набраны в прототипе."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import apply, NB

F = 'ai/wp-marketing-lab-ai-content.html'

for old, new, what in [
    ('<span>весь кластер из' + NB + 'семи запросов',
     '<span>Весь кластер из' + NB + 'семи запросов', 'подпись первой карточки'),
    ('<span>кластер того' + NB + 'же размера',
     '<span>Кластер того' + NB + 'же размера', 'подпись второй карточки'),
    ('<span>худшая позиция за' + NB + 'пять замеров',
     '<span>Худшая позиция за' + NB + 'пять замеров', 'подпись третьей карточки'),
    ('<span class="ax">число' + NB + '— позиция в' + NB + 'выдаче</span>',
     '<span class="ax">Число' + NB + '— позиция в' + NB + 'выдаче</span>', 'подпись под таблицей'),
    ('<div class="pg-serp-r"><span>завод</span>',
     '<div class="pg-serp-r"><span>Завод</span>', 'подпись строки «Завод»'),
    ('<div class="pg-serp-r"><span>клиент</span>',
     '<div class="pg-serp-r"><span>Клиент</span>', 'подпись строки «Клиент»'),
]:
    apply(what, old, new, files=[F])
