# -*- coding: utf-8 -*-
"""Отступы: стрелка внутри кнопки «Смотреть фрагмент…» брала правила
карточной стрелки — margin-top:auto и padding-top:16px. В однострочной
кнопке это не видно, а в двухстрочной стрелка уезжала вниз на 7px."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import apply

apply('стрелка в кнопке-ссылке не наследует карточные отступы',
      '.pg-stage-demo:hover{color:var(--indigo-bright)}',
      '.pg-stage-demo .pg-arw{margin-top:0;padding-top:0;align-self:center}\n'
      '.pg-stage-demo:hover{color:var(--indigo-bright)}')
