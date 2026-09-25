# -*- coding: utf-8 -*-
"""Правки 11 и 13: призывы к действию с кнопкой справа."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import apply, P, NB

SERV = [P('services', 'wp-marketing-services.html')]
SEO = [P('services', 'wp-marketing-services-seo-geo.html')]
ALL = None  # стиль нужен на всех страницах


def main():
    # общий стиль: тот же ряд, но на лиловой плашке
    apply('стиль «ряд на плашке»',
          '.pg-cta.is-row{display:grid;grid-template-columns:minmax(0,1fr) auto;\n'
          '  align-items:center;gap:16px 48px;background:var(--white);\n'
          '  border:1px solid var(--line)}',
          '.pg-cta.is-row{display:grid;grid-template-columns:minmax(0,1fr) auto;\n'
          '  align-items:center;gap:16px 48px;background:var(--white);\n'
          '  border:1px solid var(--line)}\n'
          '/* Тот же ряд, но на фирменной лиловой плашке: кнопка справа,\n'
          '   текст слева, обводка не нужна. */\n'
          '.pg-cta.is-row.is-plate{background:var(--lilac);border-color:transparent}')

    # ── правка 11: текст прототипа, одна кнопка, кнопка справа ──
    apply('11 · блок «Соберём стратегию под ваш рынок»',
          '<div class="pg-cta"><h3>С' + NB + 'чего начать</h3><p>Разберём задачу за'
          + NB + 'одну встречу: цели, текущие каналы, аналитика и' + NB + 'точки '
          'потерь. На' + NB + 'выходе' + NB + '— первые гипотезы роста и' + NB
          + 'рекомендация, с' + NB + 'какого направления начинать.</p><div class="acts">'
          '<a class="btn btn-primary" href="../wp-marketing-home.html#contacts">'
          'Обсудить задачу</a><a class="btn btn-ghost" '
          'href="../standards/wp-marketing-standards.html">Стандарты работы</a></div></div>',
          '<div class="pg-cta is-row is-plate"><h3>Соберём стратегию под' + NB
          + 'ваш' + NB + 'рынок</h3><p>Пришлите ссылку на' + NB + 'сайт' + NB
          + '— вернёмся с' + NB + 'гипотезой, где' + NB + 'скрыт рост, за' + NB
          + '3 рабочих' + NB + 'дня.</p><div class="acts">'
          '<a class="btn btn-primary" href="../wp-marketing-home.html#contacts">'
          'Обсудить задачу</a></div></div>', SERV, 1)

    # ── правка 13: кнопка блока «Следующий шаг» справа ──
    apply('13 · кнопка блока «Следующий шаг» справа',
          '<div class="pg-cta"><h2 class="sh-a">Следующий шаг</h2>'
          '<h3 class="sh-b">Посмотрим на' + NB + 'вашу AI-видимость</h3>',
          '<div class="pg-cta is-row is-plate"><h2 class="sh-a">Следующий шаг</h2>'
          '<h3 class="sh-b">Посмотрим на' + NB + 'вашу AI-видимость</h3>', SEO, 1)


if __name__ == '__main__':
    main()
