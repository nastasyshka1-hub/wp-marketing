# -*- coding: utf-8 -*-
"""Правки уровня стилей и коротких текстов по всем страницам сайта.

Сборочных скриптов больше нет — страницы правятся напрямую. Каждая
замена описана словами: что меняем и почему. Скрипт идемпотентный:
повторный запуск ничего не сломает, потому что ищет исходную строку.
"""
import glob, io, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = ' '

# (что делаем, старое, новое)
EDITS = [
    # ── изображения в кейсах: единый радиус 16 и никаких обводок ──
    ('единый радиус у скриншотов кейса',
     'figure.shot img{display:block;width:100%;height:auto;border-radius:0}',
     'figure.shot img{display:block;width:100%;height:auto;border-radius:var(--r-m)}'),
    ('обводка у «светлого» скриншота снята',
     'figure.shot.framed img{border:1px solid var(--line)}',
     'figure.shot.framed img{border:0}'),
    ('скриншоты Data Fusion: без обводки, радиус 16',
     '.df-shots figure.shot img{border:1px solid var(--line);border-radius:var(--r-s)}',
     '.df-shots figure.shot img{border:0;border-radius:var(--r-m)}'),
    ('скриншоты в общих кейсах: без обводки, радиус 16',
     '.cp-shot img{display:block;width:100%;height:auto;border:1px solid var(--line);\n  border-radius:var(--r-s)}',
     '.cp-shot img{display:block;width:100%;height:auto;border:0;\n  border-radius:var(--r-m)}'),
    ('графики РЭЦ: без обводки, радиус 16',
     '.rc-res-row figure img{width:100%;height:auto;border:1px solid var(--line);\n  border-radius:var(--r-s)}',
     '.rc-res-row figure img{width:100%;height:auto;border:0;\n  border-radius:var(--r-m)}'),
    ('обложка кейса VK/DF: радиус 16',
     '.vk-cover{margin:0 0 40px;border-radius:var(--r-l);overflow:hidden;background:var(--vkb-bg)}',
     '.vk-cover{margin:0 0 40px;border-radius:var(--r-m);overflow:hidden;background:var(--vkb-bg)}'),
    ('обложка кейса-копии: радиус 16',
     '.cc-cover{margin:0 0 40px;border-radius:var(--r-l);overflow:hidden;background:var(--cb-bg)}',
     '.cc-cover{margin:0 0 40px;border-radius:var(--r-m);overflow:hidden;background:var(--cb-bg)}'),
    ('обложка общего кейса: радиус 16',
     '.cp-media{margin:0 0 40px;border-radius:var(--r-l);overflow:hidden;background:var(--cb-bg)}',
     '.cp-media{margin:0 0 40px;border-radius:var(--r-m);overflow:hidden;background:var(--cb-bg)}'),
    ('квадратные углы у ряда кадров сняты',
     'border-radius:0;background:transparent}',
     'border-radius:var(--r-m);background:transparent}'),
    ('таймлайн проекта: радиус 16',
     'figure.shot.cc-tl img{display:block;width:100%;height:auto;border-radius:0}',
     'figure.shot.cc-tl img{display:block;width:100%;height:auto;border-radius:var(--r-m)}'),
    ('галерея из четырёх кадров: радиус 16',
     '.cc-gal.g4 figure.shot img{width:100%;height:auto;max-height:none;object-fit:contain;\n  border-radius:0}',
     '.cc-gal.g4 figure.shot img{width:100%;height:auto;max-height:none;object-fit:contain;\n  border-radius:var(--r-m)}'),
    ('фото человека: тот же радиус, что у остальных изображений',
     'align-self:start;border-radius:var(--r-s);object-fit:cover;object-position:50% 20%;',
     'align-self:start;border-radius:var(--r-m);object-fit:cover;object-position:50% 20%;'),
    ('обложка РЭЦ: радиус 16',
     '.rc-hero-pic img{display:block;width:100%;height:auto}',
     '.rc-hero-pic img{display:block;width:100%;height:auto;border-radius:var(--r-m)}'),

    # ── правка 16: хлебные крошки при наведении фиолетовые, а не лиловые ──
    ('хлебные крошки при наведении — Indigo Grape',
     '.crumbs a:hover{color:var(--indigo-bright)}',
     '.crumbs a:hover{color:var(--accent)}'),

    # ── правки 06 и 14: стрелка в меню разворачивается на месте ──
    ('стрелка меню: сдвиг вынесен из поворота',
     'border-bottom:1.5px solid currentColor;transform:rotate(45deg) translateY(-1px);\n  transition:transform .2s ease}',
     'border-bottom:1.5px solid currentColor;transform:translateY(-1px) rotate(45deg);\n  transform-origin:50% 50%;transition:transform .2s ease}'),
    ('стрелка меню: раскрытое состояние',
     '.has-sub.open>a::after,.has-sub.open>.nav-sec::after{transform:rotate(225deg) translateY(-1px)}',
     '.has-sub.open>a::after,.has-sub.open>.nav-sec::after{transform:translateY(-1px) rotate(225deg)}'),

    # ── правка 23: черта в списках одинаковой толщины ──
    ('черта в списке материала: 2px вместо дробного 1px',
     ".pg-mg-cols span::before{content:'';position:absolute;left:0;top:.62em;width:8px;\n  height:1px;background:var(--accent)}",
     ".pg-mg-cols span::before{content:'';position:absolute;left:0;top:.6em;width:8px;\n  height:2px;border-radius:1px;background:var(--accent)}"),

    # ── правка 15: период в дашборде без плашки, фиолетовым ──
    ('период в дашборде набран как «Пример отчёта»',
     '.pg-db-per{flex:none;padding:8px 16px;border-radius:var(--r-s);\n  background:var(--lilac);font-size:14px;color:var(--ink);white-space:nowrap}',
     '.pg-db-per{flex:none;font-size:13px;font-weight:600;letter-spacing:.02em;\n  color:var(--accent);white-space:nowrap}'),

    # ── правка 03: подписи плашек крупнее описания ──
    ('«Артефакты» и «Контрольная точка» — заголовки плашек',
     '.pg-art span,.pg-cp span{display:block;font-size:13px;color:var(--ink-faint);\n  margin-bottom:8px}',
     '.pg-art span,.pg-cp span{display:block;font-size:17px;font-weight:600;\n  line-height:1.3;color:var(--graphite);margin-bottom:8px}'),

    # ── правка 12: подписи строк сравнения крупнее описания ──
    ('подписи строк «Было — стало» — заголовки пар',
     '.pg-cmp dt{font-size:14px;color:var(--ink-faint)}',
     '.pg-cmp dt{font-size:17px;font-weight:600;line-height:1.3;color:var(--graphite);\n  margin-bottom:8px}'),

    # ── правка 07: «Ритм коммуникации» — блоки разведены ──
    ('панели ритма отодвинуты от календарей',
     '.pg-sp{display:grid;grid-template-columns:minmax(0,340px) minmax(0,1fr);\n  gap:var(--gutter);margin-top:var(--gutter)}',
     '.pg-sp{display:grid;grid-template-columns:minmax(0,340px) minmax(0,1fr);\n  gap:var(--gutter);margin-top:48px}'),
    ('заголовок сводки отодвинут от панелей',
     '.pg-sum-h{margin:var(--s-56) 0 0}',
     '.pg-sum-h{margin:56px 0 0}'),

    # ── правка 27: чипы пакетов фиолетовые и справа ──
    ('срок и цена пакета прижаты вправо',
     '.pg-stage-foot{margin-top:auto;padding-top:16px;display:flex;flex-wrap:wrap;gap:8px}',
     '.pg-stage-foot{margin-top:auto;padding-top:16px;display:flex;flex-wrap:wrap;\n  justify-content:flex-end;gap:8px}'),
    ('чип пакета — фиолетовая обводка и текст',
     '.pg-chip{font-size:14px;color:var(--ink-soft);border:1px solid var(--line);\n  border-radius:99px;padding:8px 16px}',
     '.pg-chip{font-size:14px;color:var(--accent);border:1px solid var(--accent);\n  border-radius:99px;padding:8px 16px}'),

    # ── правка 05: плитки результата шире, четвёртая на две колонки ──
    ('плитки результата: минимум 152px и растяжение четвёртой',
     '.pg-mini-st{display:grid;grid-template-columns:repeat(auto-fit,minmax(136px,1fr));gap:8px}',
     '.pg-mini-st{display:grid;grid-template-columns:repeat(auto-fit,minmax(152px,1fr));gap:8px}\n'
     '@media (min-width:901px){\n  .pg-mini-st>div:nth-child(4):last-child{grid-column:span 2}}'),
    ('вместо стрелок — фиолетовые точки',
     ".pg-mini-do li{position:relative;padding-left:32px;font-size:15px;\n  line-height:1.5;color:var(--ink)}\n.pg-mini-do li::before{content:none}",
     ".pg-mini-do li{position:relative;padding-left:24px;font-size:15px;\n  line-height:1.5;color:var(--ink)}\n"
     ".pg-mini-do li::before{content:'';position:absolute;left:0;top:.6em;width:8px;\n  height:8px;border-radius:50%;background:var(--accent)}"),

    # ── правка 18: в подтверждении заявки нет имени ──
    ('подтверждение заявки без имени',
     'Мария свяжется с' + NB + 'вами в' + NB + 'течение рабочего дня и' + NB + 'пришлёт план первой' + NB + 'встречи.',
     'Свяжемся с' + NB + 'вами в' + NB + 'течение рабочего дня и' + NB + 'пришлём план первой' + NB + 'встречи.'),

    # ── правка 17: «С третьего месяца» → «С 3-го месяца» ──
    ('этап переименован в «С 3-го месяца»',
     'С третьего месяца', 'С 3-го месяца'),

    # ── правка 31: «Язык аудитории» → Vocabulary mining ──
    ('инструмент переименован в Vocabulary mining',
     'Язык аудитории', 'Vocabulary mining'),
]


def main():
    pages = sorted(glob.glob(os.path.join(ROOT, '*.html'))
                   + glob.glob(os.path.join(ROOT, '*', '*.html'))
                   + glob.glob(os.path.join(ROOT, '*', '*', '*.html')))
    total = 0
    for what, old, new in EDITS:
        n = 0
        for f in pages:
            s = io.open(f, encoding='utf-8').read()
            if old in s:
                io.open(f, 'w', encoding='utf-8').write(s.replace(old, new))
                n += 1
        total += n
        print('%-3d %s' % (n, what))
    print('\nстраниц: %d, правок применено на страницах: %d' % (len(pages), total))


if __name__ == '__main__':
    main()
