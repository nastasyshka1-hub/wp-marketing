# -*- coding: utf-8 -*-
"""Логотипы банков: убрать из ленты клиентов, поставить на FinTech.

На прототипе банковские знаки стоят не в «Нам доверяют», а на странице
FinTech, в блоке «Опыт работы с финансовыми компаниями», и это бегущая
строка — тот же компонент, что на главной, но со своим составом.
Состав и порядок — с прототипа.
"""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import P

BANKS = [                       # порядок — как в прототипе
    ('ОТП Банк',       '../a2/b951476ae01ad4c4.webp', 36),
    ('Ренессанс Банк', '../a2/c785c495fda9d28c.webp', 38),
    ('ПСБ',            '../a1/logo-psb.svg',          30),
    ('Локо-Банк',      '../a1/logo-loko.svg',         40),
    ('Сбер',           '../a1/logo-sber.svg',         30),
    ('Согласие',       '../a1/59bdec93ad7fd675.webp', 40),
    ('Центр-инвест',   '../a1/logo-centr-invest.svg', 42),
    ('Ozon Банк',      '../a1/logo-ozon.svg',         26),
]
STRIP_PAGES = [P('index.html'), P('wp-marketing-home.html'),
               P('about', 'wp-marketing-about.html')]
FIN = P('industries', 'wp-marketing-industries-fintech.html')


def main():
    # ── 1. убираем банки из ленты клиентов: там их на прототипе нет ──
    names = ('Сбер', 'ПСБ', 'Локо-Банк', 'Ozon Банк', 'Центр-инвест')
    for f in STRIP_PAGES:
        s = io.open(f, encoding='utf-8').read()
        n = 0
        for t in names:
            pat = (r'<span class="slot" title="%s"><img class="lg" style="--h:\d+px" '
                   r'alt="%s" src="[^"]+"></span>' % (re.escape(t), re.escape(t)))
            s, k = re.subn(pat, '', s)
            n += k
        io.open(f, 'w', encoding='utf-8').write(s)
        print('ok      из ленты клиентов убрано знаков: %d — %s'
              % (n, os.path.basename(f)))

    # ── 2. блок на FinTech становится бегущей строкой с банками ──
    s = io.open(FIN, encoding='utf-8').read()
    i = s.index('<section class="ip-logos"')
    j = s.index('</section>', i) + len('</section>')
    slots = ''.join(
        '<span class="slot" title="%s"><img class="lg" style="--h:%dpx" alt="%s" '
        'src="%s"></span>' % (t, h, t, src) for t, src, h in BANKS)
    new = ('<section class="ip-logos" aria-label="Опыт работы с финансовыми компаниями">\n'
           '  <div class="shell">\n'
           '    <p class="ls-lbl">Опыт работы с финансовыми компаниями</p>\n'
           '  </div>\n'
           '  <div class="marquee" role="group" aria-label="Банки и страховые компании">\n'
           '    <div class="track" style="--dur:44s"><div class="lane">%s</div></div>\n'
           '  </div>\n'
           '</section>' % slots)
    io.open(FIN, 'w', encoding='utf-8').write(s[:i] + new + s[j:])
    print('ok      блок «Опыт работы с финансовыми компаниями» — бегущая строка, знаков: %d'
          % len(BANKS))


if __name__ == '__main__':
    main()
