# -*- coding: utf-8 -*-
"""Отступы: у сообщения об ошибке отправки формы стояли браузерные
margin'ы абзаца (1em = 14px) — единственное место на сайте, выпадавшее
из сетки кратности восьми."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import apply

apply('отступы сообщения об ошибке формы',
      '.lead-err{display:none;font-size:14px;color:var(--red);max-width:52ch}',
      '.lead-err{display:none;margin:16px 0 0;font-size:14px;color:var(--red);'
      'max-width:52ch}')
