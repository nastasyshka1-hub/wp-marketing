# -*- coding: utf-8 -*-
"""Иерархия в такте: периодичность — лиловый заголовок (как «Постоянно»,
«Еженедельно» в эталоне), название такта — чёрный подзаголовок помельче."""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import apply, P

F = 'services/wp-marketing-services-seo-geo.html'

apply('иерархия: периодичность лиловым, название чёрным',
      """/* подпись такта — тихой строкой, как дни недели в шапке календаря:
   в эталоне лиловых пилюль нет */
.pg-flow-when{margin-top:16px;font-size:13px;line-height:16px;
  color:var(--ink-soft)}
.pg-flow-i h3{margin:0;font-family:'Bounded','Geologica',sans-serif;
  font-weight:400;font-size:19px;line-height:1.25;letter-spacing:-.01em;
  color:var(--accent);hyphens:manual;overflow-wrap:normal;word-break:normal}""",
      """/* периодичность — лиловый заголовок такта, как в эталоне;
   название такта идёт под ним чёрным и помельче */
.pg-flow-i h3{margin:16px 0 0;font-family:'Bounded','Geologica',sans-serif;
  font-weight:400;font-size:19px;line-height:1.25;letter-spacing:-.01em;
  color:var(--accent);hyphens:manual;overflow-wrap:normal;word-break:normal}
.pg-flow-n{font-size:17px;font-weight:600;line-height:1.35;
  color:var(--graphite);hyphens:manual;overflow-wrap:normal;word-break:normal}""",
      files=[F])

s = open(P(F), encoding='utf-8').read()
PAIR = re.compile(r'<span class="pg-flow-when">(.*?)</span><h3>(.*?)</h3>')
s, n = PAIR.subn(lambda m: '<h3>%s</h3><b class="pg-flow-n">%s</b>' % (m.group(1), m.group(2)), s)
open(P(F), 'w', encoding='utf-8').write(s)
print('иерархия: перестроено тактов:', n)
