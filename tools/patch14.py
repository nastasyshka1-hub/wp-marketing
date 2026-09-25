# -*- coding: utf-8 -*-
"""Кадры в кейсах не растягиваются сверх своего размера.

Заказчик прислал скриншоты шириной 384—750 px. Растянутый на колонку
кадр выглядит мылом, поэтому каждому figure проставляем max-width
по натуральной ширине картинки.
"""
import io, os, re, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import pages, ROOT

FIG = re.compile(r'<figure class="shot"((?: data-plate="[^"]*")?)>\s*<img([^>]*?)src="([^"]+)"')


def main():
    n = 0
    for f in pages():
        d = os.path.dirname(f)
        s = io.open(f, encoding='utf-8').read()
        out, last = [], 0
        for m in FIG.finditer(s):
            src = m.group(3)
            if src.startswith('data:') or 'style="max-width' in m.group(0):
                continue
            path = os.path.normpath(os.path.join(d, src))
            if not os.path.exists(path):
                continue
            try:
                w = Image.open(path).width
            except Exception:
                continue
            out.append((m.start(), m.group(1), w))
        if not out:
            continue
        # вставляем справа налево, чтобы не сбить позиции
        for pos, plate, w in reversed(out):
            ins = '<figure class="shot"%s style="max-width:%dpx">' % (plate, w)
            end = s.index('>', pos) + 1
            s = s[:pos] + ins + s[end:]
            n += 1
        io.open(f, 'w', encoding='utf-8').write(s)
    print('ok      кадров ограничено натуральной шириной: %d' % n)


if __name__ == '__main__':
    main()
