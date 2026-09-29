# -*- coding: utf-8 -*-
"""Плашки, ведущие на форму: чередование фона.

Правило заказчика: кнопка всегда справа снизу; подложка лиловая, если
блок выше белый, голубой или с обводкой, и белая с обводкой, если блок
выше уже лиловый — чтобы две лиловые плашки не стояли подряд.

Ниже — что стоит над каждой плашкой (замерено в браузере):
  консалтинг · «Следующий шаг»          голубая плашка материала  → лиловая
  консалтинг · «Соберём стратегию…»     лиловая плашка выше       → обводка
  SEO & GEO  · «Прогноз перед стартом»  белый фон страницы        → лиловая
  SEO & GEO  · «Следующий шаг»          голубая плашка материала  → лиловая
  услуги     · «Соберём стратегию…»     белый фон страницы        → лиловая
  контент    · «Соберём контент-завод»  тёмный блок эксперимента  → лиловая
  репутация  · «Полный аудит»           белая форма с обводкой    → лиловая
  B2B        · «Разберём воронку»       карточки с обводкой       → лиловая
  стандарты  · «Нужен полный SLA»       голубая плашка материала  → лиловая
"""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import P

# файл → заголовок плашки → нужна ли лиловая подложка
RULES = [
    ('services/wp-marketing-services-consulting.html', 'Следующий шаг', True),
    ('services/wp-marketing-services-consulting.html', 'Соберём стратегию, которую', False),
    ('services/wp-marketing-services-seo-geo.html', 'Прогноз перед стартом работ', True),
    ('services/wp-marketing-services-seo-geo.html', 'Следующий шаг', True),
    ('services/wp-marketing-services.html', 'Соберём стратегию под', True),
    ('ai/wp-marketing-lab-ai-content.html', 'Соберём контент-завод', True),
    ('ai/wp-marketing-lab-reputation.html', 'Полный аудит репутации', True),
    ('industries/wp-marketing-industries-b2b.html', 'Разберём вашу B2B-воронку', True),
    ('standards/wp-marketing-standards.html', 'Нужен полный SLA', True),
]

BLK = re.compile(r'<div class="pg-cta is-row( is-plate)?"><div class="pg-cta-txt">(.{0,400}?)</p>', re.S)

for f, title, want_plate in RULES:
    s = open(P(f), encoding='utf-8').read()
    key = title.replace('\u00a0', ' ')
    hit = None
    for m in BLK.finditer(s):
        txt = re.sub(r'<[^>]+>', ' ', m.group(2)).replace('\u00a0', ' ')
        if key in txt:
            hit = m; break
    assert hit, 'плашка не найдена: %s · %s' % (f, title)
    now = bool(hit.group(1))
    label = 'лиловая' if want_plate else 'с обводкой'
    if now == want_plate:
        print('—    %-40s %-30s уже %s' % (f.split('/')[-1], title[:28], label))
        continue
    cls = 'pg-cta is-row is-plate' if want_plate else 'pg-cta is-row'
    head = '<div class="%s"><div class="pg-cta-txt">' % cls
    old_head_len = len('<div class="pg-cta is-row%s"><div class="pg-cta-txt">'
                       % (' is-plate' if now else ''))
    s = s[:hit.start()] + head + s[hit.start() + old_head_len:]
    open(P(f), 'w', encoding='utf-8').write(s)
    print('ok   %-40s %-30s → %s' % (f.split('/')[-1], title[:28], label))
