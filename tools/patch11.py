# -*- coding: utf-8 -*-
"""Правка 22: у тактов ревью появляется календарь года.

Закрашены месяцы, в которые такт повторяется: ежемесячный — все
двенадцать, квартальный — четыре, годовой — один.
"""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import apply, P, NB

SEO = [P('services', 'wp-marketing-services-seo-geo.html')]


def cal(every):
    cells = ''.join('<i class="pg-flow-m%s" style="--d:%dms"></i>'
                    % (' on' if k % every == 0 else '', k * 40) for k in range(12))
    return '<div class="pg-flow-cal" aria-hidden="true">%s</div>' % cells


def main():
    for label, every in (('Каждый месяц', 1), ('Каждый квартал', 3), ('Раз в' + NB + 'год', 12)):
        apply('22 · календарь у такта «%s»' % label.replace(NB, ' '),
              '<div class="pg-flow-i rise"><span class="pg-flow-when">%s</span>' % label,
              '<div class="pg-flow-i rise">%s<span class="pg-flow-when">%s</span>'
              % (cal(every), label), SEO, 1)

    apply('22 · стиль календаря',
          '.pg-flow-when{align-self:flex-start;font-size:13px;color:var(--white);\n'
          '  background:var(--accent);border-radius:99px;padding:8px 16px}',
          '/* Календарь года над тактом: двенадцать месяцев, закрашены те,\n'
          '   в которые такт повторяется. */\n'
          '.pg-flow-cal{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));\n'
          '  gap:8px;margin:0 0 16px;max-width:216px}\n'
          '.pg-flow-m{display:block;aspect-ratio:1;border-radius:6px;\n'
          '  background:var(--cold);transform:scale(.6);opacity:0;\n'
          '  transition:transform .4s cubic-bezier(.16,.86,.26,1) var(--d,0ms),\n'
          '             opacity .4s ease var(--d,0ms)}\n'
          '.pg-flow-m.on{background:var(--accent)}\n'
          '.pg-flow-i.in .pg-flow-m{transform:none;opacity:1}\n'
          '@media (prefers-reduced-motion:reduce){\n'
          '  .pg-flow-m{transition:none;transform:none;opacity:1}}\n'
          '.pg-flow-when{align-self:flex-start;font-size:13px;color:var(--white);\n'
          '  background:var(--accent);border-radius:99px;padding:8px 16px}',
          SEO, 1)


if __name__ == '__main__':
    main()
