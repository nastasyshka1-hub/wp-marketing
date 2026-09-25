# -*- coding: utf-8 -*-
"""Битые внутренние ссылки и пропавшие файлы-ассеты."""
import glob, io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import pages, ROOT

REF = re.compile(r'(?:href|src)="([^"#:]+)"')


def main():
    bad = 0
    for f in pages():
        d = os.path.dirname(f)
        s = io.open(f, encoding='utf-8').read()
        for m in REF.finditer(s):
            u = m.group(1)
            if u.startswith(('http', 'data:', 'mailto:', '//')) or not u:
                continue
            t = os.path.normpath(os.path.join(d, u))
            if not os.path.exists(t):
                bad += 1
                print('НЕТ ФАЙЛА  %s → %s' % (os.path.relpath(f, ROOT), u))
    print('страниц: %d, битых ссылок: %d' % (len(pages()), bad))
    return bad


if __name__ == '__main__':
    sys.exit(1 if main() else 0)
