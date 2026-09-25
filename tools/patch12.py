# -*- coding: utf-8 -*-
"""Логотипы банков в ленте клиентов.

Файлы прислал заказчик, лежат рядом с остальными ассетами.
Высота каждого знака своя: у широких логотипов она меньше, чтобы
все знаки занимали примерно одинаковую оптическую площадь.
"""
import io, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import P

SRC = '/home/claude/logos'
NEW = [
    ('Сбер',         'sberbank-full.svg',  'logo-sber.svg',        30),
    ('ПСБ',          'psb-full.svg',       'logo-psb.svg',         30),
    ('Локо-Банк',    'loko-bank-full.svg', 'logo-loko.svg',        40),
    ('Ozon Банк',    'ozon-bank-full.svg', 'logo-ozon.svg',        26),
    ('Центр-инвест', 'centr invest.svg',   'logo-centr-invest.svg', 42),
]
PAGES = [(P('index.html'), 'a1/'),
         (P('wp-marketing-home.html'), 'a1/'),
         (P('about', 'wp-marketing-about.html'), '../a1/')]


def main():
    for _, src, dst, _h in NEW:
        shutil.copyfile(os.path.join(SRC, src), P('a1', dst))
    print('ok      логотипов положено в a1: %d' % len(NEW))

    for f, pre in PAGES:
        s = io.open(f, encoding='utf-8').read()
        if 'title="Сбер"' in s:
            print('--      уже есть: %s' % os.path.basename(f))
            continue
        slots = ''.join(
            '<span class="slot" title="%s"><img class="lg" style="--h:%dpx" '
            'alt="%s" src="%s%s"></span>' % (t, h, t, pre, dst)
            for t, _src, dst, h in NEW)
        anchor = '<span class="slot" title="Ростелеком">'
        assert anchor in s, 'лента не найдена в %s' % f
        io.open(f, 'w', encoding='utf-8').write(s.replace(anchor, slots + anchor, 1))
        print('ok      лента клиентов дополнена: %s' % os.path.basename(f))


if __name__ == '__main__':
    main()
