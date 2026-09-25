# -*- coding: utf-8 -*-
"""Правки разметки и текстов по страницам. Продолжение patch01."""
import glob, io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = ' '


def pages():
    return sorted(glob.glob(os.path.join(ROOT, '*.html'))
                  + glob.glob(os.path.join(ROOT, '*', '*.html'))
                  + glob.glob(os.path.join(ROOT, '*', '*', '*.html')))


def apply(what, old, new, files=None, limit=None):
    """Замена по всем страницам. limit — ожидаемое число страниц."""
    n = 0
    for f in (files or pages()):
        s = io.open(f, encoding='utf-8').read()
        if old in s:
            io.open(f, 'w', encoding='utf-8').write(s.replace(old, new))
            n += 1
    mark = 'ok ' if (limit is None or n == limit) else 'ВНИМАНИЕ '
    print('%s%-3d %s' % (mark, n, what))
    return n


def sub(what, pat, repl, files=None, flags=0):
    n = 0
    for f in (files or pages()):
        s = io.open(f, encoding='utf-8').read()
        s2, k = re.subn(pat, repl, s, flags=flags)
        if k:
            io.open(f, 'w', encoding='utf-8').write(s2)
            n += k
    print('ok  %-3d %s' % (n, what))
    return n


P = lambda *a: os.path.join(ROOT, *a)
SERV = [P('services', 'wp-marketing-services.html')]
PPC = [P('services', 'wp-marketing-services-ppc.html')]
SEO = [P('services', 'wp-marketing-services-seo-geo.html')]
CONS = [P('services', 'wp-marketing-services-consulting.html')]


def main():
    # ── правка 25: в шапке услуг одна кнопка ──
    apply('25 · убрана кнопка «Посмотреть кейсы»',
          '<a class="btn btn-ghost" href="../cases/wp-marketing-cases.html">Посмотреть кейсы</a>',
          '', SERV, 1)

    # ── правка 29: «Услуги» в подвале ведут на страницу услуг ──
    # подвал у страниц в подпапках ссылается относительно своей папки
    sub('29 · «Услуги» в подвале — ссылка',
        r'<div class="foot-col">\n      <h2>Услуги</h2>\n      <a href="([^"]*)wp-marketing-services-consulting\.html"',
        lambda m: ('<div class="foot-col">\n      <h2><a href="%swp-marketing-services.html">Услуги</a></h2>'
                   '\n      <a href="%swp-marketing-services-consulting.html"'
                   % (m.group(1), m.group(1))))
    apply('29 · заголовок-ссылка в подвале не подчёркивается',
          '.foot-col a:hover{color:var(--white)}',
          '.foot-col a:hover{color:var(--white)}\n'
          '.foot-col h2 a{font:inherit;letter-spacing:inherit;text-transform:inherit;'
          'color:inherit;transition:color .2s ease}\n'
          '.foot-col h2 a:hover{color:var(--white)}')

    # ── правка 17: этап переименован, описание не серое ──
    apply('17 · «С 3-го месяца»',
          'С' + NB + 'третьего' + NB + 'месяца', 'С' + NB + '3-го' + NB + 'месяца',
          CONS, 1)
    apply('17 · описание этапа чёрным',
          '.pg-plan-ph p{margin:0;font-size:15px;line-height:1.45;color:var(--ink-soft);',
          '.pg-plan-ph p{margin:0;font-size:15px;line-height:1.45;color:var(--ink);',
          CONS, 1)

    # ── правка 05: серые стрелки в списке «что сделали» убраны ──
    sub('05 · стрелка в списке заменена точкой',
        r'<li><svg class="li-arw".*?</svg>', '<li>', flags=re.S)

    # ── правка 27: цены и срок сняты с заголовков пакетов ──
    for old, new in (('Стратегия' + NB + '·' + NB + '4—6' + NB + 'нед', 'Стратегия'),
                     ('Старт' + NB + '·' + NB + '130' + NB + '000' + NB + '₽/мес', 'Старт'),
                     ('Рост' + NB + '·' + NB + '170' + NB + '000' + NB + '₽/мес', 'Рост'),
                     ('Лидер' + NB + '·' + NB + '250' + NB + '000' + NB + '₽/мес', 'Лидер')):
        apply('27 · заголовок пакета «%s»' % new,
              '<b class="pg-stage-name">%s</b>' % old,
              '<b class="pg-stage-name">%s</b>' % new, PPC)

    # ── правка 21: приписка о связках — формулировка прототипа ──
    apply('21 · текст приписки о связках',
          'Ломается одно звено' + NB + '— не' + NB + 'работает вся связка, и' + NB
          + 'оптимизация ставок этого не' + NB + 'лечит. Собираем связки под' + NB
          + 'финмодель клиента и' + NB + 'регулярно тестируем: масштабируем рабочие, '
          'отключаем слабые',
          'Конверсионные связки' + NB + '— способ из' + NB + 'того' + NB + 'же трафика '
          'получать больше качественных заявок. Мы' + NB + 'собираем их' + NB + 'под'
          + NB + 'финмодель клиента и' + NB + 'регулярно тестируем: масштабируем '
          'рабочие, отключаем слабые.', PPC)


if __name__ == '__main__':
    main()
