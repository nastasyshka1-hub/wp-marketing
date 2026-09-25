# -*- coding: utf-8 -*-
"""Самопроверка правок: каждая строка — факт в коде страницы, а не намерение."""
import glob, io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch02 import pages, P

NB = ' '
R = lambda *a: io.open(P(*a), encoding='utf-8').read()

SERV = R('services', 'wp-marketing-services.html')
PPC = R('services', 'wp-marketing-services-ppc.html')
SEO = R('services', 'wp-marketing-services-seo-geo.html')
CONS = R('services', 'wp-marketing-services-consulting.html')
IND = R('industries', 'wp-marketing-industries.html')
STD = R('standards', 'wp-marketing-standards.html')
HOME = R('index.html')
REP = R('ai', 'wp-marketing-lab-reputation.html')
DF = R('cases', 'detail', 'wp-marketing-case-datafusion.html')
FIN = R('industries', 'wp-marketing-industries-fintech.html')
ALL = {os.path.basename(f): io.open(f, encoding='utf-8').read() for f in pages()}
CASES = {k: v for k, v in ALL.items() if k.startswith('wp-marketing-case-')}
every = lambda fn: all(fn(v) for v in ALL.values())

CHECKS = [
 ('01/19', 'запятая в «5,1» отделена от единицы',
  lambda: '<b>5<span class="dcm">,</span>1</b>' in SEO and '.dcm{margin-right' in SEO),
 ('02', 'анимация появления у блока видимости снята',
  lambda: 'pg-rch-w pg-tl-hid' not in REP),
 ('03', 'подписи плашек крупнее описания',
  lambda: '.pg-art span,.pg-cp span{display:block;font-size:17px;font-weight:600' in SEO),
 ('03', 'описания плашек с прописной буквы',
  lambda: not re.search(r'<div class="pg-(?:art|cp)"><span>[^<]*</span><p>[а-яё]',
                        ''.join(ALL.values()))),
 ('04', 'заголовок замера исправлен и получил акцент с линией',
  lambda: 'по' + NB + 'вашему бренду, разовый' + NB + 'замер' in SEO
          and 'class="accent">Бесплатный замер AI-видимости<span class="bolt">' in SEO),
 ('05', 'вместо стрелок фиолетовые точки',
  lambda: 'li-arw' not in IND and ".pg-mini-do li::before{content:''" in IND),
 ('05', 'четвёртая плитка растянута на две колонки',
  lambda: '.pg-mini-st>div:nth-child(4):last-child{grid-column:span 2}' in IND),
 ('06/14', 'стрелка в меню разворачивается на месте',
  lambda: every(lambda s: 'transform:translateY(-1.5px) rotate(45deg)' in s
                and 'transform:translateY(2.75px) rotate(225deg)' in s)),
 ('07', 'блоки «Ритма коммуникации» разведены',
  lambda: 'margin-top:48px}' in STD and '.pg-sum-h{margin:56px 0 0}' in STD),
 ('08', 'заголовок материала внутри голубой плашки (SEO & GEO)',
  lambda: 'pg-mg has-head' in SEO and 'sec-head pg-mg-head' in SEO),
 ('09', 'заголовок материала внутри голубой плашки (PPC)',
  lambda: 'pg-mg has-head' in PPC),
 ('10', 'дорожная карта: без иконки, заголовок в той же обводке',
  lambda: 'Персональная дорожная карта лидогенерации' in IND
          and IND.index('id="roadmap"') < IND.index('sec-head pg-mg-head')),
 ('11', 'блок «Соберём стратегию под ваш рынок», кнопка справа',
  lambda: 'Соберём стратегию под' + NB + 'ваш' + NB + 'рынок' in SERV
          and 'pg-cta is-row is-plate' in SERV
          and 'Стандарты работы</a>' not in SERV),
 ('12', 'подписи строк сравнения чёрные и крупнее описания',
  lambda: '.pg-cmp dt{font-size:17px;font-weight:600' in CONS),
 ('13', 'кнопка блока «Следующий шаг» справа',
  lambda: 'pg-cta is-row is-plate' in SEO),
 ('15', 'плашка периода снята, текст фиолетовый',
  lambda: '.pg-db-per{flex:none;font-size:13px;font-weight:600' in SEO),
 ('16', 'хлебные крошки при наведении фиолетовые',
  lambda: every(lambda s: '.crumbs a:hover{color:var(--indigo-bright)}' not in s)),
 ('17', '«С 3-го месяца» и чёрное описание',
  lambda: 'С' + NB + '3-го' + NB + 'месяца' in CONS
          and '.pg-plan-ph p{margin:0;font-size:15px;line-height:1.45;color:var(--ink);' in CONS),
 ('18', 'в подтверждении заявки нет имени',
  lambda: every(lambda s: 'Мария свяжется с' not in s)),
 ('20', 'кейсы PPC — текст прототипа',
  lambda: all(t in PPC for t in (
      'Прирост MQL через digital', '2 364 регистрации юрлиц', 'Часть данных под',
      'ИТ-холдинг · MQL enterprise-уровня', 'Госсектор · регистрации',
      '103 млн', '593 тыс.'))),
 ('21', 'приписка о связках — формулировка прототипа, без дубля',
  lambda: PPC.count('Конверсионные связки') == 1 and 'Ломается одно звено' not in PPC),
 ('22', 'у тактов ревью появились календари',
  lambda: SEO.count('<div class="pg-flow-cal"') == 3 and 'pg-flow-m on' in SEO),
 ('23', 'черта в списках одинаковой толщины',
  lambda: 'height:2px;border-radius:1px;background:var(--accent)}' in SEO),
 ('24', 'экспертная диагностика: без иконки и плашки, на лиловом фоне',
  lambda: 'pg-ms-form is-solo is-plate' in IND
          and 'pg-ms-chip">Экспертная диагностика' not in IND),
 ('25', 'на странице услуг одна кнопка в шапке',
  lambda: 'Посмотреть кейсы' not in SERV),
 ('26', 'что получает клиент — два ряда по три, без описания',
  lambda: 'pg-checks c3' in SERV
          and 'Общая для' + NB + 'всех направлений рамка' not in SERV),
 ('27', 'цены и срок ушли из заголовков пакетов в чипы справа',
  lambda: 'Стратегия · 4—6 нед' not in PPC
          and '4—6' + NB + 'недель</span>' in PPC
          and 'justify-content:flex-end;gap:8px}' in PPC),
 ('28', 'направления: надзаголовок, текст прототипа, «Подробнее»',
  lambda: 'class="sh-a">Направления</h2>' in SERV
          and 'Что мы' + NB + 'делаем' in SERV
          and 'Маркетинговый аудит, целевая архитектура каналов' in SERV
          and SERV.count('pg-arw is-more') == 3
          and 'от' + NB + '200' + NB + '000' not in SERV),
 ('29', '«Услуги» в подвале кликабельны',
  lambda: every(lambda s: '<h2><a href="' in s and '>Услуги</a></h2>' in s)),
 ('30', 'как работаем: надзаголовок и текст прототипа',
  lambda: 'class="sh-a">Как работаем</h2>' in SERV
          and 'От' + NB + 'диагностики к' + NB + 'системе' in SERV
          and 'Аудит воронки, ниши, конкурентов и' + NB + 'текущих' + NB + 'каналов.' in SERV),
 ('31', '«Язык аудитории» переименован',
  lambda: 'Vocabulary mining' in CONS and 'Язык аудитории' not in CONS),
 ('картинки', 'обложка Data Fusion — кадр 1600×1000, а не 256×362',
  lambda: 'a1/3895d7877d1b3e1e.webp' in DF and 'object-position:50% 88%' in DF),
 ('картинки', 'обводок у изображений в кейсах нет',
  lambda: not any(re.search(r'figure\.shot(?:\.framed)? img\{[^}]*border:1px', v)
                  for v in CASES.values())),
 ('картинки', 'единый радиус 16px у изображений кейсов',
  lambda: all('border-radius:var(--r-m)' in v for v in CASES.values())
          and not any(re.search(r'(?:figure\.shot|\.cp-shot|\.cc-cover|\.cp-media|'
                                r'\.vk-cover)[^{}]*\{[^}]*border-radius:0\}', v)
                      for v in CASES.values())),
 ('п03', 'банковские логотипы — только на FinTech, бегущей строкой',
  lambda: all(('title="%s"' % t) in FIN for t in
              ('Сбер', 'ПСБ', 'Локо-Банк', 'Ozon Банк', 'Центр-инвест',
               'ОТП Банк', 'Ренессанс Банк', 'Согласие'))
          and 'marquee' in FIN.split('<section class="ip-logos"')[1][:1200]
          and not any(('title="%s"' % t) in HOME for t in
                      ('Сбер', 'ПСБ', 'Локо-Банк', 'Ozon Банк', 'Центр-инвест'))
          and all(os.path.exists(P('a1', n)) for n in
                  ('logo-sber.svg', 'logo-psb.svg', 'logo-loko.svg',
                   'logo-ozon.svg', 'logo-centr-invest.svg'))),
 ('п01/04', 'кнопка в строчной плашке прижата к низу',
  lambda: every(lambda s: '.pg-cta.is-row .acts{grid-column:2;align-self:end}' in s
                          if '.pg-cta.is-row .acts{' in s else True)
          and CONS.count('<div class="pg-cta-txt">') == 1
          and SEO.count('<div class="pg-cta-txt">') == 1
          and SERV.count('<div class="pg-cta-txt">') == 1),
 ('п02/07', 'блок «Ревью» повторяет эталон: календарь пн-вс, без пилюль и стрелок',
  lambda: '.pg-flow-cal{display:flex' in SEO
          and 'border:1px solid var(--line);border-radius:var(--r-m)}' in
              SEO.split('.pg-flow-cal{')[1][:320]
          and 'repeat(7,minmax(0,1fr))' in SEO.split('.pg-flow-q,.pg-flow-ms{')[1][:120]
          and SEO.count('<div class="pg-flow-q">') == 3
          and SEO.count('<span>пн</span>') >= 3
          and SEO.count('class="pg-flow-m"') + SEO.count('class="pg-flow-m on"') == 84
          and SEO.count('class="pg-flow-m on"') == 3
          and 'pg-flow-arw' not in SEO
          and 'repeat(3,minmax(0,1fr))' in SEO.split('.pg-flow{')[1][:80]
          and SEO.count('<b class="pg-flow-n">') == 3
          and 'pg-flow-when' not in SEO
          and 'color:var(--accent)' in SEO.split('.pg-flow-i h3{')[1][:260]
          and 'color:var(--graphite)' in SEO.split('.pg-flow-n{')[1][:160]),
 ('п06', 'заметка про ПСБ скрыта, но не удалена',
  lambda: '<!-- скрыто по просьбе заказчика: <div class="pg-note">' in FIN
          and 'пример третьего направления' in FIN),
]


def main():
    bad = 0
    for num, what, fn in CHECKS:
        try:
            ok = bool(fn())
        except Exception as e:
            ok, what = False, what + ' [ошибка проверки: %s]' % e
        if not ok:
            bad += 1
        print('%-9s %-4s %s' % (num, 'да' if ok else 'НЕТ', what))
    print('\nпроверок: %d, не подтвердилось: %d' % (len(CHECKS), bad))
    return bad


if __name__ == '__main__':
    sys.exit(1 if main() else 0)
