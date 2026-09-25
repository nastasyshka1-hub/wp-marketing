# -*- coding: utf-8 -*-
"""Правка 03: описания артефактов и контрольных точек — с прописной буквы."""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import pages

PAT = re.compile(r'(<div class="pg-(?:art|cp)"><span>[^<]*</span><p>)([а-яё])')


def main():
    n = 0
    for f in pages():
        s = io.open(f, encoding='utf-8').read()
        s2, k = PAT.subn(lambda m: m.group(1) + m.group(2).upper(), s)
        if k:
            io.open(f, 'w', encoding='utf-8').write(s2)
            n += k
    print('ok      03 · описаний с прописной буквы: %d' % n)


if __name__ == '__main__':
    main()
