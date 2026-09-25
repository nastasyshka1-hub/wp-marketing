# -*- coding: utf-8 -*-
"""Правка 28: блок направлений на странице услуг.

Надзаголовок «Направления» и заголовок «Что мы делаем», цены сняты,
описания и перечисления — слово в слово с прототипа, у стрелки
появилась подпись «Подробнее».
"""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import apply, P, NB

F = P('services', 'wp-marketing-services.html')
SERV = [F]
n = lambda t: t.replace(' ', NB)

CARDS = [
    ('Консалтинг и' + NB + 'стратегия', 'Консалтинг и' + NB + 'стратегия',
     'Маркетинговый аудит, целевая архитектура каналов, юнит-экономика, '
     'дорожная карта роста на' + NB + '12—24' + NB + 'месяца.',
     ['Аудит текущего' + NB + 'маркетинга',
      'Стратегия и' + NB + 'продуктовый' + NB + 'нарратив',
      'Дорожная карта и' + NB + 'KPI-модель']),
    ('SEO и' + NB + 'GEO / AEO', 'SEO' + NB + '&amp; GEO / AEO',
     'Единая система покрытия спроса: классический поиск, ответы '
     'AI-ассистентов и' + NB + 'цитируемость в' + NB + 'нейросетях.',
     ['Тех. SEO и' + NB + 'коммерческий' + NB + 'трафик',
      'AI-видимость: ChatGPT, Perplexity,' + NB + 'Алиса',
      'Контент как' + NB + 'отчуждаемый' + NB + 'актив']),
    ('PPC и' + NB + 'лидогенерация', 'PPC' + NB + '&amp; Лидогенерация',
     'Перформанс-маркетинг с' + NB + 'KPI в' + NB + 'договоре: контекст, таргет, '
     'посевы, программатика, отраслевые' + NB + 'СМИ.',
     ['Яндекс.Директ · VK ·' + NB + 'Telegram Ads',
      'Свои лендинги и' + NB + 'лид-магниты',
      'Сквозная аналитика, отсев' + NB + 'фрода']),
]


def main():
    s = io.open(F, encoding='utf-8').read()

    # шапка секции
    old = ('<div class="sec-head"><h2>Что' + NB + 'входит в' + NB + 'каждое '
           'направление</h2><p>Цены' + NB + '— нижняя граница по' + NB + 'направлению. '
           'Итоговая зависит от' + NB + 'объёма семантики, числа продуктов и' + NB
           + 'региональной сетки.</p></div>')
    assert old in s, 'шапка блока направлений не найдена'
    s = s.replace(old, '<div class="sec-head"><h2 class="sh-a">Направления</h2>'
                       '<h3 class="sh-b">Что мы' + NB + 'делаем</h3></div>', 1)

    # карточки: цена снята, текст с прототипа, к стрелке подпись
    for title_old, title_new, desc, ul in CARDS:
        m = re.search(r'<span class="tag">[^<]*</span><b class="hl">'
                      + re.escape(title_old)
                      + r'</b><span>.*?</span><ul>.*?</ul>', s, re.S)
        assert m, 'карточка «%s» не найдена' % title_old
        new = ('<b class="hl">%s</b><span>%s</span><ul>%s</ul>'
               % (title_new, desc, ''.join('<li>%s</li>' % x for x in ul)))
        s = s[:m.start()] + new + s[m.end():]

    # подпись у стрелки только в карточках этого блока
    i = s.index('id="directions"')
    j = s.index('</section>', i)
    block = s[i:j].replace('<span class="pg-arw">',
                           '<span class="pg-arw is-more"><span>Подробнее</span>')
    s = s[:i] + block + s[j:]

    io.open(F, 'w', encoding='utf-8').write(s)
    print('ok      28 · блок направлений переписан по прототипу')

    apply('28 · стиль подписи у стрелки',
          '.pg-arw{display:block;margin-top:auto;padding-top:16px;align-self:flex-end;\n'
          '  line-height:0;color:var(--ink-faint);transition:color .25s ease}',
          '.pg-arw{display:block;margin-top:auto;padding-top:16px;align-self:flex-end;\n'
          '  line-height:0;color:var(--ink-faint);transition:color .25s ease}\n'
          '/* Карточка направления: у стрелки есть подпись, как в прототипе */\n'
          '.pg-arw.is-more{align-self:flex-start;display:inline-flex;align-items:center;\n'
          '  gap:8px;line-height:1.3;font-size:15px;color:var(--accent)}\n'
          '.pg-arw.is-more .arw{display:block}', SERV, 1)


if __name__ == '__main__':
    main()
