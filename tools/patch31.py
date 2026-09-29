# -*- coding: utf-8 -*-
"""Закрывающая плашка «Полный аудит репутации» — на лиловой подложке,
как «Следующий шаг» на страницах услуг."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import apply, NB

apply('плашка полного аудита на лиловом',
      '<div class="pg-cta is-row"><div class="pg-cta-txt"><h3>Полный аудит репутации '
      'с' + NB + 'планом работы</h3>',
      '<div class="pg-cta is-row is-plate"><div class="pg-cta-txt"><h3>Полный аудит репутации '
      'с' + NB + 'планом работы</h3>',
      files=['ai/wp-marketing-lab-reputation.html'])
