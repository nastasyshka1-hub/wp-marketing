# -*- coding: utf-8 -*-
"""Правки 26 и 30 на странице услуг: блок «Как работаем» и блок выгод."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import apply, P, NB

SERV = [P('services', 'wp-marketing-services.html')]
n = lambda t: t.replace(' ', NB)


def main():
    # ── правка 30: надзаголовок «Как работаем», заголовок «От диагностики
    #    к системе», описания этапов слово в слово с прототипа ──
    apply('30 · шапка блока «Как работаем»',
          '<div class="sec-head"><h2>Как' + NB + 'идёт работа</h2><p>Один и' + NB
          + 'тот' + NB + 'же' + NB + 'цикл на' + NB + 'любом направлении' + NB
          + '— меняется только содержание' + NB + 'этапов.</p></div>',
          '<div class="sec-head"><h2 class="sh-a">Как работаем</h2>'
          '<h3 class="sh-b">От' + NB + 'диагностики к' + NB + 'системе</h3></div>',
          SERV, 1)

    steps = [
        ('Диагностика',
         'Разбираем продукт, текущую воронку и' + NB + 'аналитику. На' + NB + 'выходе'
         + NB + '— точки потерь и' + NB + 'оценка потенциала в' + NB + 'цифрах, а' + NB
         + 'не' + NB + 'впечатление.',
         'Аудит воронки, ниши, конкурентов и' + NB + 'текущих' + NB + 'каналов.'),
        ('Стратегия',
         'Фиксируем цели, каналы и' + NB + 'KPI. Показываем, при' + NB + 'каких '
         'условиях показатель достижим и' + NB + 'где' + NB + 'зоны' + NB + 'риска.',
         'Цели, метрики, приоритизация каналов и' + NB + 'продуктовых' + NB
         + 'обещаний.'),
        ('Запуск',
         'Собираем инфраструктуру: аналитику, посадочные, материалы, кампании. '
         'Первые связки выходят в' + NB + 'работу.',
         'Продакшн посадочных, настройка каналов и' + NB + 'аналитики.'),
        ('Система',
         'Проект переходит в' + NB + 'ритм: еженедельная сверка, ежемесячный отчёт, '
         'квартальный пересмотр стратегии.',
         'Ежемесячный ритм гипотез, отчётности и' + NB + 'оптимизаций.'),
    ]
    for title, old, new in steps:
        apply('30 · описание этапа «%s»' % title,
              '<h3>%s</h3><p>%s</p>' % (title, old),
              '<h3>%s</h3><p>%s</p>' % (title, new), SERV, 1)

    # ── правка 26: описание снято, карточки в два ряда по три ──
    apply('26 · шапка блока выгод без описания',
          '<div class="sec-head"><h2>Что' + NB + 'получает клиент в' + NB + 'любом '
          'направлении</h2><p>Общая для' + NB + 'всех направлений рамка описана в'
          + NB + 'стандартах работы.</p></div>',
          '<div class="sec-head"><h2>Что' + NB + 'получает клиент в' + NB + 'любом '
          'направлении</h2></div>', SERV, 1)
    apply('26 · сетка «два ряда по три»',
          '<div class="pg-checks"><div class="pg-check rise">',
          '<div class="pg-checks c3"><div class="pg-check rise">', SERV, 1)
    apply('26 · правило сетки «два ряда по три»',
          '.pg-checks.c1 .pg-check{align-items:center}',
          '.pg-checks.c1 .pg-check{align-items:center}\n'
          '/* Вариант «c3»: два ряда по три, цифра над текстом, всё по левому краю. */\n'
          '.pg-checks.c3{grid-template-columns:repeat(3,minmax(0,1fr))}\n'
          '.pg-checks.c3 .pg-check{grid-template-columns:1fr;align-items:start;gap:16px}\n'
          '.pg-checks.c3 .pg-check-n{align-self:start}\n'
          '@media (max-width:900px){.pg-checks.c3{grid-template-columns:repeat(2,minmax(0,1fr))}}\n'
          '@media (max-width:640px){.pg-checks.c3{grid-template-columns:1fr}}',
          SERV, 1)


if __name__ == '__main__':
    main()
