# -*- coding: utf-8 -*-
"""Сравнительная таблица: акцент на нашей колонке — типографикой, не заливкой.

Лиловая подложка спорила с обводками строк и выглядела грязно. Теперь
колонка альтернативы уходит в приглушённый серый, а наша остаётся
графитовой — контраст читается, а лишнего цвета в таблице нет."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import apply

OLD = """/* Сравнительная таблица: наша колонка — не ещё один столбец, а вывод.
   Подложка и вес отделяют её от левой части, шапка — лиловая. */
.pg-table.is-cmp .is-us{background:var(--lilac);font-weight:600;
  color:var(--graphite)}
.pg-table.is-cmp th.is-us{color:var(--accent)}
.pg-table.is-cmp thead th.is-us{border-radius:var(--r-m) var(--r-m) 0 0}
.pg-table.is-cmp tbody tr:last-child .is-us{border-radius:0 0 var(--r-m) var(--r-m)}
"""
NEW = """/* Сравнительная таблица: наша колонка — не ещё один столбец, а вывод.
   Отделяем её тоном текста, а не заливкой: альтернатива уходит
   в приглушённый серый, наш ответ остаётся графитовым. */
.pg-table.is-cmp td:nth-child(2){color:var(--ink-soft)}
.pg-table.is-cmp td.is-us{color:var(--graphite)}
"""
apply('сравнение без заливки', OLD, NEW)
