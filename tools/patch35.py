# -*- coding: utf-8 -*-
"""Кнопки «Смотреть фрагмент…» в карточках направлений.

Было две беды. Стрелка жила отдельным элементом гибкой строки: когда
подпись переносилась на две строки, стрелка уезжала к правому краю
карточки и повисала сама по себе. И сами кнопки стояли на разной высоте —
сразу после списка, а списки в карточках разной длины.

Теперь стрелка идёт строчным элементом сразу за последним словом,
а кнопка прижата к низу карточки: во всех трёх она на одной линии."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import apply

apply('кнопка-ссылка: стрелка в строке, кнопка по низу карточки',
      """.pg-stage-demo{align-self:flex-start;margin-top:8px;padding:0;border:0;text-align:left;
  background:none;font:inherit;font-size:15px;color:var(--accent);cursor:pointer;
  display:inline-flex;align-items:center;gap:8px}
.pg-stage-demo .pg-arw{margin-top:0;padding-top:0;align-self:center}""",
      """.pg-stage-demo{align-self:flex-start;margin-top:auto;padding:16px 0 0;border:0;
  text-align:left;background:none;font:inherit;font-size:15px;line-height:1.45;
  color:var(--accent);cursor:pointer;display:block}
/* стрелка — строчный знак после последнего слова, а не отдельная колонка:
   при переносе подписи она больше не уезжает к краю карточки */
.pg-stage-demo .pg-arw{display:inline-block;margin:0 0 0 8px;padding:0;
  vertical-align:middle;line-height:0}""")
