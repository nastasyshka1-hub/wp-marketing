# -*- coding: utf-8 -*-
"""Правка 04: заголовок бесплатного замера — новый текст и акцент с линией."""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import apply, P, NB

SEO = [P('services', 'wp-marketing-services-seo-geo.html')]


def main():
    apply('04 · заголовок замера исправлен, часть фразы — акцент с линией',
          '<div class="pg-offer-head"><h2>Бесплатный замер AI-видимости: соберём срез '
          'по' + NB + '30—50 вашим запросам</h2>',
          '<div class="pg-offer-head"><h2 class="rise">'
          '<span class="accent">Бесплатный замер AI-видимости<span class="bolt"></span>'
          '</span> по' + NB + 'вашему бренду, разовый' + NB + 'замер</h2>',
          SEO, 1)

    apply('04 · стиль акцента в заголовке блока',
          '.pg-offer-head{display:flex;flex-direction:column;gap:16px}',
          '.pg-offer-head{display:flex;flex-direction:column;gap:16px}\n'
          '/* Акцент в заголовке блока: тот же приём, что в h1 — фирменный\n'
          '   фиолетовый и наклонная линия, но линия дорисовывается не на загрузке,\n'
          '   а когда блок появляется на экране. */\n'
          '.pg-offer-head h2 .accent{position:relative;color:var(--accent)}\n'
          '.pg-offer-head h2 .bolt{animation:none;transform:skewX(-24deg) scaleX(0);\n'
          '  transition:transform .5s cubic-bezier(.2,.8,.2,1) .15s}\n'
          '.pg-offer-head h2.in .bolt{transform:skewX(-24deg) scaleX(1)}\n'
          '@media (prefers-reduced-motion:reduce){\n'
          '  .pg-offer-head h2 .bolt{transition:none;transform:skewX(-24deg) scaleX(1)}}',
          SEO, 1)


if __name__ == '__main__':
    main()
