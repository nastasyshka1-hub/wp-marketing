# -*- coding: utf-8 -*-
"""Шаги: между карточками серая стрелка вместо лиловой галочки.

Галочка была нарисована двумя бордюрами и читалась как знак «дальше»
только по привычке. Ставим ту же стрелку, что между тактами процесса,
серым Cold Steel. Колонки разводим на 40px, чтобы по обе стороны
от стрелки осталось ровно по 8px."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import apply

ARROW = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
         "width='24' height='24' viewBox='0 0 24 24' fill='none' "
         "stroke='%23000' stroke-width='1.5' stroke-linecap='round' "
         "stroke-linejoin='round'%3E%3Cpath d='M4 12h15'/%3E"
         "%3Cpath d='M15 8l4 4-4 4'/%3E%3C/svg%3E\")")

OLD = """.pg-cards.steps{position:relative}
.pg-cards.steps .pg-card{position:relative}
.pg-cards.steps .pg-card + .pg-card::before{content:'';position:absolute;
  left:calc(-1 * var(--gutter) / 2 - 5px);top:50%;width:10px;height:10px;
  border-top:2px solid var(--accent);border-right:2px solid var(--accent);
  transform:translateY(-50%) rotate(45deg);pointer-events:none}"""

NEW = """.pg-cards.steps{position:relative;column-gap:40px}
.pg-cards.steps .pg-card{position:relative}
.pg-cards.steps .pg-card + .pg-card::before{content:'';position:absolute;
  left:-32px;top:50%;width:24px;height:24px;
  transform:translateY(-50%);background:var(--steel);
  -webkit-mask:ARROW center / 24px 24px no-repeat;
  mask:ARROW center / 24px 24px no-repeat;pointer-events:none}""".replace("ARROW", ARROW)

apply('серая стрелка между шагами', OLD, NEW)
