# -*- coding: utf-8 -*-
"""Правки 10 и 24: заголовок блока уезжает внутрь карточки заявки.

10 — «Дорожная карта»: иконка убрана, заголовок в той же обводке.
24 — «Экспертная диагностика»: иконка и лиловая подпись убраны,
     обводки нет, весь блок на лиловой плашке.
"""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import apply, P, NB

F = P('industries', 'wp-marketing-industries.html')
IND = [F]


def move_head(s, sid, plate=False):
    """Переносит шапку секции внутрь формы, снимает иконку."""
    i = s.index('id="%s"' % sid)
    m = re.search(r'<div class="sec-head">(.*?)</div>\n    <form class="pg-ms-form is-solo"',
                  s[i:i + 900], re.S)
    assert m, 'шапка %s не найдена' % sid
    head = m.group(1)
    cls = 'pg-ms-form is-solo is-plate' if plate else 'pg-ms-form is-solo'
    new = ('<form class="%s"' % cls)
    s = s[:i + m.start()] + new + s[i + m.end():]

    # шапка встаёт первым элементом формы, круглая иконка снимается
    j = s.index('id="%s"' % sid)
    k = s.index('novalidate>', j) + len('novalidate>')
    m2 = re.match(r'<div class="pg-ms-h"><span class="pg-ms-ic">.*?</span>'
                  r'<div class="pg-ms-ht">(.*?)</div></div>', s[k:], re.S)
    assert m2, 'шапка формы %s не найдена' % sid
    inner = m2.group(1)
    ht = ('<div class="pg-ms-ht">%s</div></div>' % inner) if inner.strip() else ''
    block = ('<div class="sec-head pg-mg-head">%s</div>' % head)
    if ht:
        block += '<div class="pg-ms-h">' + ht
    s = s[:k] + block + s[k + m2.end():]
    return s


def main():
    s = io.open(F, encoding='utf-8').read()
    s = move_head(s, 'roadmap', plate=False)
    s = move_head(s, 'review', plate=True)
    io.open(F, 'w', encoding='utf-8').write(s)
    print('ok      10/24 · заголовки уехали внутрь карточек заявки')

    # лиловая подпись «Экспертная диагностика» внутри карточки больше не нужна
    apply('24 · лиловая подпись внутри карточки снята',
          '<span class="pg-ms-chip">Экспертная диагностика</span>', '', IND, 1)

    apply('10/24 · стили: заголовок внутри карточки и лиловый вариант',
          '.pg-ms-form.is-solo{padding:48px}',
          '.pg-ms-form.is-solo{padding:48px}\n'
          '/* Заголовок блока внутри карточки: снаружи он читался как отдельный\n'
          '   блок, хотя относится к этой же заявке. */\n'
          '.pg-ms-form .sec-head{margin:0 0 8px}\n'
          '.pg-ms-form .sec-head p{max-width:80ch}\n'
          '/* Вариант на фирменной лиловой плашке: без обводки, поля белые */\n'
          '.pg-ms-form.is-plate{background:var(--lilac);border-color:transparent}',
          IND, 1)


if __name__ == '__main__':
    main()
