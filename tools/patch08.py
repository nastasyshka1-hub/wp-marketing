# -*- coding: utf-8 -*-
"""Правки 08 и 09: заголовок блока уезжает внутрь голубой плашки материала."""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import apply, P, NB

FILES = [P('services', 'wp-marketing-services-seo-geo.html'),
         P('services', 'wp-marketing-services-ppc.html')]


def main():
    for f in FILES:
        s = io.open(f, encoding='utf-8').read()
        i = s.index('id="deck"')
        m = re.search(r'<div class="sec-head">(.*?)</div>\n    <div class="pg-mg">',
                      s[i:i + 900], re.S)
        assert m, 'шапка материала не найдена в %s' % f
        head = m.group(1)
        start, end = i + m.start(), i + m.end()
        new = ('<div class="pg-mg has-head"><div class="sec-head pg-mg-head">%s</div>'
               % head)
        s = s[:start] + new + s[end:]
        io.open(f, 'w', encoding='utf-8').write(s)
        print('ok      08/09 · заголовок внутри плашки: %s' % os.path.basename(f))

    apply('08/09 · стиль заголовка внутри плашки',
          '.pg-mg-l{display:flex;flex-direction:column;gap:16px}',
          '/* Заголовок блока внутри плашки: занимает обе колонки и отбивается\n'
          '   от содержимого, чтобы плашка читалась как один блок. */\n'
          '.pg-mg.has-head{row-gap:32px}\n'
          '.pg-mg-head{grid-column:1 / -1}\n'
          '.pg-mg-head .sh-b{max-width:34ch}\n'
          '.pg-mg-l{display:flex;flex-direction:column;gap:16px}')


if __name__ == '__main__':
    main()
