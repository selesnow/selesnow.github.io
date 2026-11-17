"""Веб-интерфейс курса «Язык R для интернет-маркетинга»: /r_for_marketing_course/.

Страницы: главная курса, 3 модуля и страница на каждый урок (видео, конспект, материалы для скачивания).
Данные:
  _build/data/rcourse_playlist.csv   плейлист YouTube (Rscript _build/rcourse_fetch_playlist.R)
  _build/data/rcourse.json           модули, названия уроков, конспекты и темы (пишутся вручную)
  _build/data/rcourse_materials.json состав ZIP-архивов с материалами (python _build/rcourse_materials.py)
Курс одноязычный (видео на русском), поэтому содержимое страниц без T(); шапка и подвал — общие по сайту.
Все пути на страницах абсолютные (/assets/..., /courses/), как на 404.html: страницы лежат на глубину 2-3 уровня.
"""
import csv
import json
import re
import urllib.parse
from pathlib import Path

from build import (DATA, ROOT, SITE, PERSON_ID, T, cta_block, esc, footer, head, load, nav, plural_ru,
                   tail, url)

SLUG = 'r_for_marketing_course'
BASE = f'/{SLUG}'
COURSE_NAME = 'Язык R для интернет-маркетинга'
TITLE_PREFIX = 'Язык R для интернет маркетинга: '
COVER = f'{SITE}/r_for_marketing/cover.png'
REPO_BLOB = 'https://github.com/selesnow/r_for_marketing/blob/master/'
REPO_TREE = 'https://github.com/selesnow/r_for_marketing/tree/master/'

BTN_PRIMARY = ('bg-purple-600 hover:bg-purple-500 text-white px-6 py-3 rounded-xl font-bold text-sm transition-all '
               'shadow-[0_0_20px_rgba(168,85,247,0.35)] hover:shadow-[0_0_30px_rgba(168,85,247,0.55)] '
               'inline-flex items-center justify-center gap-2')
BTN_GHOST = ('px-5 py-3 rounded-xl border border-white/10 hover:border-white/20 bg-slate-900/80 hover:bg-slate-800 '
             'text-slate-300 hover:text-white font-semibold text-sm transition-all inline-flex items-center gap-2')


# ---------------------------------------------------------------- данные

def parse_duration(iso):
    m = re.fullmatch(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', iso or '')
    if not m:
        return 0
    h, mi, s = (int(x or 0) for x in m.groups())
    return h * 3600 + mi * 60 + s


def fmt_duration(sec, short=False):
    h, rest = divmod(int(sec), 3600)
    m = rest // 60
    if short or not h:
        return f'{h * 60 + m} мин' if (h or m) else f'{sec} с'
    return f'{h} ч {m:02d} мин'


def fmt_size(n):
    if n >= 1024 * 1024:
        return f'{n / 1024 / 1024:.1f} МБ'.replace('.', ',')
    return f'{max(1, round(n / 1024))} КБ'


def clean_title(s):
    s = re.sub(r'\s+', ' ', s).replace('Manegment', 'Management').replace(' )', ')').replace(',загрузка', ', загрузка')
    return s.strip()


def timecodes(desc):
    """Тайм-коды из блока «Тайм коды» описания видео: [(секунды, подпись)]."""
    for block in re.split(r'\|=+\|', desc.replace('\r', '')):
        if block.strip().lower().startswith('тайм'):
            out = []
            for t, label in re.findall(r'^\s*(\d{1,2}:\d{2}(?::\d{2})?)\s+(.+?)\s*$', block, re.M):
                parts = [int(x) for x in t.split(':')]
                sec = parts[0] * 3600 + parts[1] * 60 + parts[2] if len(parts) == 3 else parts[0] * 60 + parts[1]
                out.append((sec, t, label))
            return out
    return []


def material_keys(desc):
    m = re.search(r'Материалы к этому уроку:\s*(\S+)', desc)
    return [urllib.parse.unquote(m.group(1).split('/tree/master/')[-1])] if m else []


def load_course():
    meta = load('rcourse')
    manifest = json.loads((DATA / 'rcourse_materials.json').read_text(encoding='utf-8'))
    with open(DATA / 'rcourse_playlist.csv', encoding='utf-8', newline='') as f:
        rows = list(csv.DictReader(f))

    about = None
    lessons = {}          # (модуль, ключ урока) -> урок
    for r in rows:
        title = clean_title(r['title'].replace(TITLE_PREFIX, ''))
        video = dict(id=r['video_id'], duration=parse_duration(r['duration']), tc=timecodes(r['description']),
                     mats=material_keys(r['description']), label='', title=title)
        if title == 'О курсе':
            about = video
            continue
        if m := re.fullmatch(r'Введение в модуль (\d)', title):
            mod, key = int(m[1]), 'intro'
        elif title == 'Заключение':
            mod, key = 3, 'conclusion'
        else:
            m = re.match(r'^(\d+)\.(\d+)(?:\.(\d+))?\.?\s*(.*)$', title)
            mod, key = int(m[1]), f'{m[1]}.{m[2]}'
            video['label'] = f'{m[1]}.{m[2]}.{m[3]}' if m[3] else key
            video['title'] = m[4].strip()
        lessons.setdefault((mod, key), []).append(video)

    modules = []
    for mod in meta['modules']:
        n = mod['n']
        items = []
        for key, info in mod['lessons'].items():
            vids = lessons[(n, key)]
            if len(vids) > 1:   # общий префикс «Сервис - тема» выносим в название урока
                heads = {v['title'].split(' - ')[0] for v in vids if ' - ' in v['title']}
                if len(heads) == 1 and all(' - ' in v['title'] for v in vids):
                    for v in vids:
                        v['title'] = v['title'].split(' - ', 1)[1].strip()
            keys = list(dict.fromkeys(info.get('materials', []) + [k for v in vids for k in v['mats']]))
            mats = [dict(manifest[k], key=k) for k in keys if k in manifest]
            sort = 0 if key == 'intro' else 999 if key == 'conclusion' else int(key.split('.')[1])
            items.append(dict(
                module=n, key=key, sort=sort, videos=vids, mats=mats,
                slug={'intro': 'intro', 'conclusion': 'conclusion'}.get(key, key.replace('.', '-')),
                label={'intro': 'Введение', 'conclusion': 'Заключение'}.get(key, f'Урок {key}'),
                short={'intro': 'Введение', 'conclusion': 'Заключение'}.get(key, key),
                title=info['title'], summary=info['summary'], topics=info['topics'], extra=info.get('extra'),
                duration=sum(v['duration'] for v in vids)))
        items.sort(key=lambda x: x['sort'])
        modules.append(dict(mod, lessons=items, duration=sum(i['duration'] for i in items)))
    flat = [l for m in modules for l in m['lessons']]
    for i, l in enumerate(flat):
        l['prev'] = flat[i - 1] if i else None
        l['next'] = flat[i + 1] if i + 1 < len(flat) else None
    assert sum(len(l['videos']) for l in flat) + 1 == len(rows), 'не все видео плейлиста попали в уроки'
    return dict(meta=meta, about=about, modules=modules, lessons=flat, rows=len(rows))


def lesson_url(l):
    return f'{BASE}/module-{l["module"]}/{l["slug"]}/'


def module_url(m):
    return f'{BASE}/module-{m["n"]}/'


def lesson_id(l):
    return f'{l["module"]}.{l["slug"]}'


# ---------------------------------------------------------------- общие блоки

def count_label(n, one, few, many):
    return f'{n} {plural_ru(n, one, few, many)}'


def poster(video_id, title, cls=''):
    return f'''<a href="https://www.youtube.com/watch?v={video_id}" target="_blank" rel="noopener" class="rc-poster {cls}" data-rc-poster="{video_id}" aria-label="Смотреть видео: {esc(title)}">
                    <img src="https://i.ytimg.com/vi/{video_id}/hqdefault.jpg" alt="" width="480" height="360" decoding="async">
                    <span class="rc-play" aria-hidden="true"><i class="fa-solid fa-play"></i></span>
                </a>'''


def crumbs(items):
    """Хлебные крошки: [(название, url|None)]. Последний пункт — текущая страница."""
    out = []
    for i, (label, href) in enumerate(items):
        last = i == len(items) - 1
        if last:
            out.append(f'<li aria-current="page" class="text-slate-300 font-semibold">{esc(label)}</li>')
        else:
            out.append(f'<li><a href="{href}" class="hover:text-white transition-colors">{esc(label)}</a></li>'
                       '<li aria-hidden="true" class="text-slate-600"><i class="fa-solid fa-chevron-right text-[9px]"></i></li>')
    return f'<nav aria-label="Хлебные крошки"><ol class="flex flex-wrap items-center gap-x-2.5 gap-y-1 text-sm text-slate-400 mb-6">{"".join(out)}</ol></nav>'


def chip(icon, text, cls=''):
    return (f'<span class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900/60 border border-white/5 '
            f'text-xs font-semibold text-slate-300 {cls}"><i class="{icon} text-purple-400 text-[11px]" aria-hidden="true"></i>{text}</span>')


def section_title(icon, color, text, level=2):
    return (f'<h{level} class="text-xl md:text-2xl font-extrabold mb-5 flex items-center gap-3 outfit-font">'
            f'<span class="w-10 h-10 bg-{color}-500/20 flex items-center justify-center rounded-xl border border-{color}-500/30 shrink-0">'
            f'<i class="{icon} text-{color}-400 text-base" aria-hidden="true"></i></span>{text}</h{level}>')


def stats_block(items):
    cells = '\n'.join(f'''                <div class="bento-content">
                    <div class="text-3xl md:text-4xl font-extrabold text-white outfit-font">{v}</div>
                    <div class="text-xs text-slate-400 uppercase font-bold mt-1">{label}</div>
                </div>''' for v, label in items)
    return f'<div class="grid grid-cols-2 md:grid-cols-4 gap-6 bento-glass no-lift p-6 rounded-3xl" data-aos="fade-up" data-aos-delay="150">\n{cells}\n        </div>'


def page_shell(slug, title, description, body, jsonld, active='courses', image=COVER):
    page = head(f'{SLUG}/{slug}' if slug else SLUG, title, description, image=image, jsonld=jsonld)
    page = page.replace('    <!-- Tailwind собран', f'    <link rel="stylesheet" href="../assets/rcourse.css">\n    <!-- Tailwind собран')
    page += nav(active) + body + cta_block() + footer('/')
    page += tail().replace('<script src="../assets/site.js"></script>',
                           '<script src="../assets/site.js"></script>\n    <script src="../assets/rcourse.js"></script>')
    return page.replace('"../', '"/')


def write_page(slug, content):
    out = ROOT / SLUG / slug / 'index.html' if slug else ROOT / SLUG / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding='utf-8', newline='\n')
    return out


def course_ld(c, page_url, extra=None):
    nodes = [{
        '@type': 'Course', '@id': f'{SITE}{BASE}/#course', 'name': COURSE_NAME, 'url': f'{SITE}{BASE}/',
        'description': 'Бесплатный видеокурс по языку R для маркетологов и веб-аналитиков: '
                       f'{len(c["modules"])} модуля, {c["rows"]} видео и материалы для скачивания.',
        'inLanguage': 'ru', 'isAccessibleForFree': True, 'image': COVER,
        'provider': {'@id': PERSON_ID}, 'author': {'@id': PERSON_ID},
        'hasCourseInstance': {'@type': 'CourseInstance', 'courseMode': 'online', 'courseWorkload': f'PT{c["total"] // 60}M'},
    }]
    return nodes


def breadcrumb_ld(trail):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i, 'name': n, 'item': u} for i, (n, u) in enumerate(trail, 1)]}


def iso_dur(sec):
    return f'PT{sec // 3600}H{sec % 3600 // 60}M{sec % 60}S' if sec >= 3600 else f'PT{sec // 60}M{sec % 60}S'


def lesson_row(l, module_num):
    """Строка урока в списке на главной: данные для поиска лежат в data-text."""
    text = ' '.join([l['label'], l['title'], l['summary'], ' '.join(l['topics']), ' '.join(v['title'] for v in l['videos'])]).lower()
    mat = '<i class="fa-solid fa-download text-[11px] text-purple-400" title="Есть материалы" aria-label="Есть материалы"></i>' if l['mats'] else ''
    return f'''<li><a href="{lesson_url(l)}" data-rc-row data-text="{esc(text)}" data-lesson="{lesson_id(l)}" class="rc-row group/row">
                            <span class="rc-num">{l['short']}</span>
                            <span class="min-w-0 flex-1"><span class="block text-slate-100 font-semibold group-hover/row:text-white leading-snug">{esc(l['title'])}</span></span>
                            <span class="hidden sm:flex items-center gap-3 text-xs text-slate-400 shrink-0">{mat}<span class="font-mono">{fmt_duration(l['duration'], True)}</span></span>
                            <i class="rc-done-mark fa-solid fa-circle-check" aria-hidden="true"></i>
                        </a></li>'''


# ---------------------------------------------------------------- главная курса

def build_index(c):
    m_cnt, l_cnt = len(c['modules']), len([l for l in c['lessons'] if l['key'] not in ('intro', 'conclusion')])
    v_cnt = sum(len(l['videos']) for l in c['lessons']) + 1
    mats_cnt = len({k['key'] for l in c['lessons'] for k in l['mats']})
    meta = c['meta']
    desc = ('Бесплатный видеокурс по языку R для маркетологов и веб-аналитиков: три модуля, '
            f'{v_cnt} видео, конспекты уроков и материалы для скачивания.')

    modules_html = []
    for m in c['modules']:
        rows = '\n'.join(lesson_row(l, m['n']) for l in m['lessons'])
        n_lessons = len([l for l in m['lessons'] if l['key'] not in ('intro', 'conclusion')])
        modules_html.append(f'''
        <article class="bento-glass no-lift rounded-[2rem] p-5 md:p-8" data-rc-module data-aos="fade-up">
            <div class="bento-content">
                <div class="flex flex-col md:flex-row md:items-start justify-between gap-5 mb-6">
                    <div class="flex items-start gap-4">
                        <div class="w-14 h-14 rounded-2xl bg-purple-500/15 border border-purple-500/30 flex items-center justify-center text-purple-400 text-2xl shrink-0"><i class="{m['icon']}" aria-hidden="true"></i></div>
                        <div>
                            <div class="text-[11px] font-mono font-bold uppercase tracking-widest text-purple-400 mb-1">Модуль {m['n']}</div>
                            <h3 class="text-2xl md:text-3xl font-extrabold text-white outfit-font leading-tight"><a href="{module_url(m)}" class="hover:text-purple-300 transition-colors">{esc(m['title'])}</a></h3>
                            <p class="text-slate-400 text-sm mt-2 max-w-2xl">{esc(m['tagline'])}</p>
                        </div>
                    </div>
                    <div class="flex flex-wrap md:flex-col md:items-end gap-2 shrink-0">
                        {chip('fa-solid fa-list-check', count_label(n_lessons, 'урок', 'урока', 'уроков'))}
                        {chip('fa-regular fa-clock', fmt_duration(m['duration']))}
                    </div>
                </div>
                <ul class="rc-rows space-y-2" data-rc-list>
{rows}
                </ul>
                <div class="mt-6 flex flex-wrap gap-3">
                    <a href="{module_url(m)}" class="{BTN_GHOST}">Страница модуля <i class="fa-solid fa-arrow-right text-xs" aria-hidden="true"></i></a>
                </div>
            </div>
        </article>''')

    first = c['lessons'][0]
    learn = '\n'.join(f'<li class="flex items-start gap-3 text-slate-300"><i class="fa-solid fa-check text-purple-400 text-xs mt-1.5" aria-hidden="true"></i>{esc(x)}</li>'
                      for x in ['Основы синтаксиса R, строки, даты, циклы и функции',
                                'Работа с таблицами: dplyr, data.table, tidyr, SQL',
                                'R-скрипты внутри Power BI',
                                'Загрузка данных из API рекламных систем и веб-аналитики',
                                'Парсинг сайтов и HTTP-запросы',
                                'Google Таблицы, ggplot2 и базы данных',
                                'Рассылка отчётов, запуск скриптов по расписанию и Telegram-боты'])
    body = f'''
    <!-- HERO -->
    <header class="pt-32 pb-12 px-6 max-w-7xl mx-auto relative z-10">
        {crumbs([('Курсы', '/courses/'), (COURSE_NAME, None)])}
        <div data-aos="fade-up">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-400 text-xs font-bold tracking-widest uppercase mb-5 outfit-font">
                <i class="fa-solid fa-graduation-cap" aria-hidden="true"></i> Бесплатный курс · 2018
            </div>
            <h1 class="text-4xl md:text-7xl font-black tracking-tight leading-tight uppercase mb-8">Язык R для <span class="text-gradient">интернет-маркетинга</span></h1>
        </div>
        <div class="bento-glass no-lift p-6 md:p-10 border-l-4 border-purple-500/50 mb-8" data-aos="fade-up" data-aos-delay="100">
            <p class="text-lg md:text-xl text-slate-300 leading-relaxed font-light relative z-10">Автоматизация рутины маркетолога и веб-аналитика: от основ синтаксиса до Telegram-ботов. Курс создан в 2018 году вместе с NeedForData и Netpeak и с тех пор неоднократно дополнен. Три модуля, видеоуроки с конспектами и материалы к каждому уроку.</p>
            <div class="relative z-10 mt-6 flex flex-wrap gap-3">
                <a href="{lesson_url(first)}" class="{BTN_PRIMARY}" data-ga-event="course_click" data-ga-course-id="r4marketing" data-ga-placement="rcourse_start">Начать с первого урока <i class="fa-solid fa-arrow-right text-xs" aria-hidden="true"></i></a>
                <a href="{meta['playlist']}" target="_blank" rel="noopener" class="{BTN_GHOST}" data-ga-event="course_resource_click" data-ga-course-id="r4marketing" data-ga-resource-type="playlist"><i class="fa-brands fa-youtube text-red-500" aria-hidden="true"></i> Плейлист на YouTube</a>
                <a href="{meta['repo']}" target="_blank" rel="noopener" class="{BTN_GHOST}" data-ga-event="course_resource_click" data-ga-course-id="r4marketing" data-ga-resource-type="materials"><i class="fa-brands fa-github" aria-hidden="true"></i> Все материалы на GitHub</a>
            </div>
        </div>
        {stats_block([(str(m_cnt), 'Модуля'), (str(l_cnt), 'Уроков'), (str(v_cnt), 'Видео'), (fmt_duration(c['total']).replace(' мин', 'м').replace(' ч ', 'ч '), 'Видео в сумме')])}
    </header>

    <main>
    <!-- ABOUT -->
    <section class="px-6 max-w-7xl mx-auto pb-16 relative z-10">
        <div class="grid lg:grid-cols-12 gap-6">
            <div class="lg:col-span-7 bento-glass no-lift p-3 rounded-[2rem]" data-aos="fade-up">
                <div class="bento-content">
                    <div class="rc-frame rounded-[1.5rem] overflow-hidden" data-rc-player-single>
                        {poster(c['about']['id'], 'О курсе')}
                    </div>
                    <div class="px-3 pt-4 pb-2 flex items-center justify-between gap-3">
                        <div class="font-bold text-white outfit-font">О курсе <span class="text-slate-500 font-normal">· {fmt_duration(c['about']['duration'])}</span></div>
                    </div>
                </div>
            </div>
            <div class="lg:col-span-5 bento-glass no-lift p-6 md:p-8 rounded-[2rem]" data-aos="fade-up" data-aos-delay="100">
                <div class="bento-content">
                    {section_title('fa-solid fa-bullseye', 'purple', 'Чему вы научитесь')}
                    <ul class="space-y-3 text-sm">
{learn}
                    </ul>
                    <p class="text-sm text-slate-400 mt-6 pt-5 border-t border-white/5"><i class="fa-solid fa-user-check text-purple-400 mr-2" aria-hidden="true"></i>Для интернет-маркетологов и веб-аналитиков без опыта программирования.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- LESSONS -->
    <section class="px-6 max-w-7xl mx-auto pb-16 relative z-10" id="lessons">
        <div class="flex flex-col md:flex-row md:items-end justify-between gap-5 mb-8" data-aos="fade-up">
            <div>
                <h2 class="text-3xl font-extrabold flex items-center gap-4 outfit-font">
                    <div class="w-12 h-12 bg-purple-500/20 flex items-center justify-center rounded-2xl border border-purple-500/30"><i class="fa-solid fa-list-ol text-purple-500 text-xl" aria-hidden="true"></i></div>
                    Программа курса
                </h2>
                <p class="text-slate-400 text-sm mt-3" data-rc-progress hidden></p>
            </div>
            <div class="relative w-full md:w-80"><i class="fa-solid fa-magnifying-glass absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 text-sm" aria-hidden="true"></i>
                <label for="rc-search" class="sr-only">Поиск по урокам</label>
                <input id="rc-search" type="search" data-rc-search autocomplete="off" class="search-input w-full rounded-xl pl-11 pr-4 py-3 text-sm text-white placeholder-slate-500" placeholder="Поиск: ClickHouse, ggplot2, Директ…"></div>
        </div>
        <div class="space-y-8" data-rc-modules>
{''.join(modules_html)}
        </div>
        <p data-rc-empty hidden class="bento-glass no-lift p-8 text-center text-slate-400 rounded-3xl mt-6"><i class="fa-solid fa-magnifying-glass text-3xl text-purple-400/60 mb-4 block" aria-hidden="true"></i>Ничего не найдено — попробуйте другой запрос.</p>
    </section>

    <!-- MATERIALS -->
    <section class="px-6 max-w-7xl mx-auto pb-16 relative z-10">
        <div class="bento-glass no-lift p-6 md:p-10 rounded-[2rem]" data-aos="fade-up">
            <div class="bento-content grid md:grid-cols-12 gap-6 items-center">
                <div class="md:col-span-8">
                    {section_title('fa-brands fa-github', 'blue', 'Материалы и методичка')}
                    <p class="text-slate-300 leading-relaxed">К {mats_cnt} урокам приложены файлы: скрипты, данные, презентации. Архив с материалами есть на странице каждого урока, а весь репозиторий курса лежит на GitHub. Текстовая методичка со всеми видео доступна на платформе NeedForData (нужна бесплатная регистрация).</p>
                </div>
                <div class="md:col-span-4 flex flex-col gap-3">
                    <a href="{meta['repo']}" target="_blank" rel="noopener" class="{BTN_PRIMARY}"><i class="fa-brands fa-github" aria-hidden="true"></i> Репозиторий курса</a>
                    <a href="{meta['handbook']}" target="_blank" rel="noopener" class="{BTN_GHOST} justify-center"><i class="fa-solid fa-book-open text-blue-400" aria-hidden="true"></i> Методичка на NeedForData</a>
                </div>
            </div>
        </div>
    </section>
    </main>
'''
    ld = {'@context': 'https://schema.org', '@graph': course_ld(c, f'{SITE}{BASE}/') + [breadcrumb_ld([
        ('Alexey Seleznev', f'{SITE}/'), ('Курсы', f'{SITE}/courses/'), (COURSE_NAME, f'{SITE}{BASE}/')])]}
    write_page('', page_shell('', f'{COURSE_NAME} — бесплатный видеокурс | Алексей Селезнёв', desc, body, ld))


# ---------------------------------------------------------------- модуль

def build_module(c, m, idx):
    n_lessons = len([l for l in m['lessons'] if l['key'] not in ('intro', 'conclusion')])
    v_cnt = sum(len(l['videos']) for l in m['lessons'])
    mats = len({k['key'] for l in m['lessons'] for k in l['mats']})
    cards = []
    for l in m['lessons']:
        vchip = chip('fa-solid fa-circle-play', count_label(len(l['videos']), 'видео', 'видео', 'видео')) if len(l['videos']) > 1 else ''
        matchip = chip('fa-solid fa-download', 'Есть материалы') if l['mats'] else ''
        cards.append(f'''
            <a href="{lesson_url(l)}" data-lesson="{lesson_id(l)}" class="bento-glass rc-card group rounded-3xl p-5 md:p-6 flex gap-5 items-start" data-aos="fade-up">
                <span class="bento-content rc-num rc-num-lg">{l['short']}</span>
                <span class="bento-content min-w-0 flex-1">
                    <span class="flex items-start justify-between gap-3">
                        <span class="block text-xl font-bold text-white outfit-font leading-snug group-hover:text-purple-300 transition-colors">{esc(l['title'])}</span>
                        <i class="rc-done-mark fa-solid fa-circle-check mt-1" aria-hidden="true"></i>
                    </span>
                    <span class="block text-sm text-slate-400 leading-relaxed mt-2 line-clamp-2">{esc(l['summary'])}</span>
                    <span class="flex flex-wrap gap-2 mt-4">{chip('fa-regular fa-clock', fmt_duration(l['duration']))}{vchip}{matchip}</span>
                </span>
            </a>''')
    prev_m = c['modules'][idx - 1] if idx else None
    next_m = c['modules'][idx + 1] if idx + 1 < len(c['modules']) else None

    def mod_link(mm, direction):
        if not mm:
            return '<span></span>'
        arrow_l = '<i class="fa-solid fa-arrow-left text-xs" aria-hidden="true"></i> ' if direction == 'prev' else ''
        arrow_r = ' <i class="fa-solid fa-arrow-right text-xs" aria-hidden="true"></i>' if direction == 'next' else ''
        return f'<a href="{module_url(mm)}" class="{BTN_GHOST}">{arrow_l}Модуль {mm["n"]}: {esc(mm["title"])}{arrow_r}</a>'

    body = f'''
    <header class="pt-32 pb-12 px-6 max-w-7xl mx-auto relative z-10">
        {crumbs([('Курсы', '/courses/'), (COURSE_NAME, f'{BASE}/'), (f'Модуль {m["n"]}', None)])}
        <div data-aos="fade-up">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-400 text-xs font-bold tracking-widest uppercase mb-5 outfit-font">
                <i class="{m['icon']}" aria-hidden="true"></i> Модуль {m['n']} из {len(c['modules'])}
            </div>
            <h1 class="text-4xl md:text-6xl font-black tracking-tight leading-tight uppercase mb-8">{esc(m['title'])}</h1>
        </div>
        <div class="bento-glass no-lift p-6 md:p-10 border-l-4 border-purple-500/50 mb-8" data-aos="fade-up" data-aos-delay="100">
            <p class="text-lg md:text-xl text-slate-300 leading-relaxed font-light relative z-10">{esc(m['desc'])}</p>
        </div>
        {stats_block([(str(n_lessons), plural_ru(n_lessons, 'Урок', 'Урока', 'Уроков')), (str(v_cnt), 'Видео'), (fmt_duration(m['duration']).replace(' мин', 'м').replace(' ч ', 'ч '), 'Видео в сумме'), (str(mats), 'Архивов с материалами')])}
    </header>

    <main class="px-6 max-w-7xl mx-auto pb-16 relative z-10">
        <div class="grid gap-4">{''.join(cards)}
        </div>
        <div class="mt-10 flex flex-wrap justify-between gap-3">
            {mod_link(prev_m, 'prev')}
            {mod_link(next_m, 'next')}
        </div>
    </main>
'''
    title = f'Модуль {m["n"]}. {m["title"]} | {COURSE_NAME}'
    desc = f'{m["desc"][:200].rsplit(" ", 1)[0]}… Видеоуроки, конспекты и материалы.'
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'CollectionPage', '@id': f'{SITE}{module_url(m)}', 'url': f'{SITE}{module_url(m)}', 'name': title, 'description': m['desc'],
         'isPartOf': {'@id': f'{SITE}{BASE}/#course'}, 'inLanguage': 'ru',
         'mainEntity': {'@type': 'ItemList', 'itemListElement': [
             {'@type': 'ListItem', 'position': i, 'name': l['title'], 'url': f'{SITE}{lesson_url(l)}'} for i, l in enumerate(m['lessons'], 1)]}},
        breadcrumb_ld([('Alexey Seleznev', f'{SITE}/'), ('Курсы', f'{SITE}/courses/'), (COURSE_NAME, f'{SITE}{BASE}/'),
                       (f'Модуль {m["n"]}', f'{SITE}{module_url(m)}')])]}
    write_page(f'module-{m["n"]}', page_shell(f'module-{m["n"]}', title, desc, body, ld))


# ---------------------------------------------------------------- урок

FILE_ICONS = {'.r': 'fa-regular fa-file-code', '.rmd': 'fa-regular fa-file-code', '.csv': 'fa-solid fa-file-csv',
              '.xlsx': 'fa-regular fa-file-excel', '.pdf': 'fa-regular fa-file-pdf', '.pptx': 'fa-regular fa-file-powerpoint',
              '.png': 'fa-regular fa-file-image', '.json': 'fa-regular fa-file-code', '.html': 'fa-regular fa-file-code',
              '.pbix': 'fa-solid fa-chart-column', '.db': 'fa-solid fa-database', '.zip': 'fa-regular fa-file-zipper'}


def materials_block(l, c):
    if not l['mats']:
        return f'''<section id="materials" class="bento-glass no-lift p-6 md:p-8 rounded-3xl" aria-labelledby="mat-h">
                    <div class="bento-content">
                        {section_title('fa-solid fa-download', 'blue', 'Материалы к уроку').replace('<h2 ', '<h2 id="mat-h" ')}
                        <p class="text-slate-400 text-sm leading-relaxed">К этому уроку нет отдельных файлов: всё, что нужно, показано в видео. Материалы остальных уроков — в <a href="{c['meta']['repo']}" target="_blank" rel="noopener" class="text-purple-400 hover:text-purple-300 underline underline-offset-2">репозитории курса</a>.</p>
                    </div>
                </section>'''
    parts = []
    for mat in l['mats']:
        files = '\n'.join(f'''<li class="flex items-center gap-3 py-2.5 border-b border-white/5 last:border-0">
                                <i class="{FILE_ICONS.get(Path(f['name']).suffix.lower(), 'fa-regular fa-file')} text-slate-500 w-5 text-center" aria-hidden="true"></i>
                                <a href="{esc(url(REPO_BLOB + f['repo_path']))}" target="_blank" rel="noopener" class="min-w-0 flex-1 text-sm text-slate-300 hover:text-white break-words transition-colors">{esc(f['name'])}</a>
                                <span class="text-xs text-slate-500 font-mono shrink-0">{fmt_size(f['size'])}</span>
                            </li>''' for f in mat['files'])
        folder = mat['key'].split('/', 1)[1]
        multi = f'<div class="text-xs font-mono font-bold uppercase tracking-widest text-slate-500 mb-3">{esc(folder)}</div>' if len(l['mats']) > 1 else ''
        parts.append(f'''{multi}<div class="flex flex-wrap items-center gap-3 mb-5">
                            <a href="{BASE}/materials/{mat['zip']}" download class="{BTN_PRIMARY}" data-ga-event="material_download" data-ga-course-id="r4marketing" data-ga-lesson="{lesson_id(l)}" data-ga-file="{mat['zip']}"><i class="fa-solid fa-file-zipper" aria-hidden="true"></i> Скачать архив · {fmt_size(mat['size'])}</a>
                            <a href="{esc(url(REPO_TREE + mat['key']))}" target="_blank" rel="noopener" class="{BTN_GHOST}"><i class="fa-brands fa-github" aria-hidden="true"></i> Папка на GitHub</a>
                        </div>
                        <ul class="mb-2">{files}</ul>''')
    n_files = sum(len(m['files']) for m in l['mats'])
    return f'''<section id="materials" class="bento-glass no-lift p-6 md:p-8 rounded-3xl" aria-labelledby="mat-h">
                    <div class="bento-content">
                        {section_title('fa-solid fa-download', 'blue', 'Материалы к уроку').replace('<h2 ', '<h2 id="mat-h" ')}
                        <p class="text-sm text-slate-400 mb-5">{count_label(n_files, 'файл', 'файла', 'файлов')} — скрипты, данные и презентации, которые показаны в видео.</p>
{''.join(parts)}
                        <p class="text-xs text-slate-500 mt-4 flex items-start gap-2"><i class="fa-solid fa-circle-info mt-0.5" aria-hidden="true"></i>В архивах токены, секреты и пароли из примеров заменены заглушками &lt;ВАШ_ЗНАЧЕНИЕ&gt;: подставьте свои.</p>
                    </div>
                </section>'''


def build_lesson(c, m, l):
    vids = l['videos']
    multi = len(vids) > 1
    first = vids[0]
    parts = ''
    if multi:
        items = '\n'.join(f'''<li><a href="https://www.youtube.com/watch?v={v['id']}" target="_blank" rel="noopener" data-rc-part="{v['id']}" data-title="{esc(v['title'])}"{' aria-current="true"' if i == 0 else ''} class="rc-part{' is-active' if i == 0 else ''}">
                                <span class="rc-num">{v['label'] or i + 1}</span>
                                <span class="min-w-0 flex-1 text-left leading-snug">{esc(v['title'])}</span>
                                <span class="text-xs text-slate-400 font-mono shrink-0">{fmt_duration(v['duration'], True)}</span>
                            </a></li>''' for i, v in enumerate(vids))
        parts = f'''<section class="bento-glass no-lift p-4 md:p-5 rounded-3xl" aria-labelledby="parts-h">
                    <div class="bento-content">
                        <h2 id="parts-h" class="text-xs font-mono font-bold uppercase tracking-widest text-slate-500 mb-3 px-1">Видео урока · {len(vids)}</h2>
                        <ol class="space-y-1.5">{items}</ol>
                    </div>
                </section>'''
    tcs = ''
    for i, v in enumerate(vids):
        if v['tc']:
            rows = '\n'.join(f'<li><button type="button" data-rc-seek="{s}" data-video="{v["id"]}" class="rc-tc"><span class="font-mono text-purple-400">{t}</span><span class="text-left">{esc(lab)}</span></button></li>'
                             for s, t, lab in v['tc'])
            tcs += f'''<div data-rc-tc="{v['id']}"{'' if i == 0 else ' hidden'}>
                            <ul class="grid gap-1">{rows}</ul>
                        </div>'''
    tc_block = f'''<section class="bento-glass no-lift p-6 md:p-8 rounded-3xl" aria-labelledby="tc-h">
                    <div class="bento-content">
                        {section_title('fa-regular fa-clock', 'orange', 'Содержание видео').replace('<h2 ', '<h2 id="tc-h" ')}
                        {tcs}
                    </div>
                </section>''' if tcs else ''

    topics = '\n'.join(f'<li class="flex items-start gap-3 text-slate-300"><i class="fa-solid fa-check text-purple-400 text-xs mt-1.5" aria-hidden="true"></i>{esc(t)}</li>' for t in l['topics'])
    extra = ''
    if l.get('extra'):
        extra = f'<a href="{esc(l["extra"]["url"])}" class="{BTN_GHOST} mt-6"><i class="fa-solid fa-book text-purple-400" aria-hidden="true"></i> {esc(l["extra"]["label"])}</a>'
    notes = f'''<section class="bento-glass no-lift p-6 md:p-8 rounded-3xl" aria-labelledby="notes-h">
                    <div class="bento-content">
                        {section_title('fa-solid fa-lightbulb', 'purple', 'Конспект урока').replace('<h2 ', '<h2 id="notes-h" ')}
                        <p class="text-slate-300 leading-relaxed text-base md:text-lg mb-6 max-w-3xl">{esc(l['summary'])}</p>
                        <div class="text-xs font-mono font-bold uppercase tracking-widest text-slate-500 mb-3">Что разбираем</div>
                        <ul class="space-y-2.5 text-sm md:text-base">
{topics}
                        </ul>
                        {extra}
                    </div>
                </section>'''

    def nav_card(target, direction):
        if not target:
            return '<span></span>'
        label = 'Предыдущий урок' if direction == 'prev' else 'Следующий урок'
        align = 'text-left' if direction == 'prev' else 'text-right md:flex-row-reverse'
        arrow = 'fa-arrow-left' if direction == 'prev' else 'fa-arrow-right'
        mod_tag = f' · Модуль {target["module"]}' if target['module'] != l['module'] else ''
        return f'''<a href="{lesson_url(target)}" class="bento-bar group flex items-center gap-4 p-4 md:p-5 rounded-2xl border border-white/10 bg-slate-900/60 hover:border-purple-500/40 hover:bg-white/5 transition-all {align}">
                        <i class="fa-solid {arrow} text-purple-400 group-hover:text-white transition-colors" aria-hidden="true"></i>
                        <span class="min-w-0"><span class="block text-[11px] font-mono font-bold uppercase tracking-widest text-slate-500">{label}{mod_tag}</span><span class="block text-white font-semibold leading-snug">{esc(target['short'] if target['key'] in ('intro', 'conclusion') else target['short'] + '. ' + target['title'])}</span></span>
                    </a>'''

    side = '\n'.join(f'''<li><a href="{lesson_url(x)}" data-lesson="{lesson_id(x)}"{' aria-current="page"' if x is l else ''} class="rc-side{' is-active' if x is l else ''}">
                                <span class="rc-num rc-num-sm">{x['short']}</span>
                                <span class="min-w-0 flex-1 leading-snug">{esc(x['title'])}</span>
                                <i class="rc-done-mark fa-solid fa-circle-check" aria-hidden="true"></i>
                            </a></li>''' for x in m['lessons'])

    meta_chips = chip('fa-regular fa-clock', fmt_duration(l['duration'])) + (chip('fa-solid fa-circle-play', f'{len(vids)} видео') if multi else '') \
        + (chip('fa-solid fa-download', 'Есть материалы') if l['mats'] else '')
    title_h1 = l['title'] if l['key'] in ('intro', 'conclusion') else f'{l["short"]}. {l["title"]}'
    body = f'''
    <main class="pt-28 pb-16 px-6 max-w-7xl mx-auto relative z-10">
        {crumbs([('Курсы', '/courses/'), (COURSE_NAME, f'{BASE}/'), (f'Модуль {m["n"]}', module_url(m)), (l['label'], None)])}
        <div class="grid lg:grid-cols-12 gap-8 items-start">
            <div class="lg:col-span-8 min-w-0 space-y-6">
                <header data-aos="fade-up">
                    <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-400 text-xs font-bold tracking-widest uppercase mb-4 outfit-font">
                        <i class="{m['icon']}" aria-hidden="true"></i> Модуль {m['n']} · {l['label']}
                    </div>
                    <h1 class="text-3xl md:text-5xl font-black tracking-tight leading-tight mb-5 outfit-font">{esc(title_h1)}</h1>
                    <div class="flex flex-wrap items-center gap-2">{meta_chips}
                        <button type="button" data-rc-done="{lesson_id(l)}" aria-pressed="false" class="rc-done-btn" hidden><i class="fa-regular fa-circle-check" aria-hidden="true"></i><span>Отметить пройденным</span></button>
                    </div>
                </header>

                <div class="bento-glass no-lift p-2 md:p-3 rounded-[2rem]" data-aos="fade-up" data-aos-delay="50">
                    <div class="bento-content">
                        <div id="rc-player" class="rc-frame rounded-[1.5rem] overflow-hidden" data-rc-player data-video="{first['id']}">
                            {poster(first['id'], first['title'] if multi else l['title'])}
                        </div>
                    </div>
                </div>
                {parts}
                {tc_block}
                {notes}
                {materials_block(l, c)}
                <div class="grid sm:grid-cols-2 gap-4 pt-2">
                    {nav_card(l['prev'], 'prev')}
                    {nav_card(l['next'], 'next')}
                </div>
            </div>

            <aside class="lg:col-span-4 lg:sticky lg:top-24 space-y-6" aria-label="Уроки модуля">
                <div class="bento-glass no-lift p-4 md:p-5 rounded-3xl">
                    <div class="bento-content">
                        <h2 class="text-xs font-mono font-bold uppercase tracking-widest text-slate-500 mb-3 px-1">Модуль {m['n']}: {esc(m['title'])}</h2>
                        <ul class="rc-side-list space-y-1">{side}</ul>
                        <a href="{BASE}/" class="mt-4 flex items-center gap-2 px-1 text-sm font-semibold text-slate-400 hover:text-white transition-colors"><i class="fa-solid fa-list-ol text-xs text-purple-400" aria-hidden="true"></i> Программа всего курса</a>
                    </div>
                </div>
            </aside>
        </div>
    </main>
'''
    title = f'{l["label"]}. {l["title"]} | {COURSE_NAME}' if l['key'] not in ('intro', 'conclusion') else f'{l["title"]} | {COURSE_NAME}'
    desc = f'{l["summary"]} Видеоурок, конспект и материалы для скачивания.'
    page_url = f'{SITE}{lesson_url(l)}'
    video = {'@type': 'VideoObject', 'name': l['title'], 'description': l['summary'],
             'thumbnailUrl': f'https://i.ytimg.com/vi/{first["id"]}/hqdefault.jpg', 'uploadDate': c['published'][first['id']],
             'duration': iso_dur(first['duration']), 'embedUrl': f'https://www.youtube.com/embed/{first["id"]}',
             'inLanguage': 'ru', 'isAccessibleForFree': True}
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'LearningResource', '@id': page_url, 'url': page_url, 'name': l['title'], 'description': l['summary'],
         'inLanguage': 'ru', 'isAccessibleForFree': True, 'learningResourceType': 'video lesson',
         'isPartOf': {'@id': f'{SITE}{BASE}/#course'}, 'author': {'@id': PERSON_ID}, 'video': video,
         'teaches': l['topics']},
        breadcrumb_ld([('Alexey Seleznev', f'{SITE}/'), ('Курсы', f'{SITE}/courses/'), (COURSE_NAME, f'{SITE}{BASE}/'),
                       (f'Модуль {m["n"]}', f'{SITE}{module_url(m)}'), (l['title'], page_url)])]}
    write_page(f'module-{m["n"]}/{l["slug"]}', page_shell(f'module-{m["n"]}/{l["slug"]}', title, desc, body, ld,
                                                          image=f'https://i.ytimg.com/vi/{first["id"]}/hqdefault.jpg'))


# ---------------------------------------------------------------- sitemap

def update_sitemap(c):
    """Идемпотентно заменяет адреса курса в sitemap.xml (без lastmod — чтобы ночная сборка не плодила коммиты)."""
    path = ROOT / 'sitemap.xml'
    xml = path.read_text(encoding='utf-8')
    xml = re.sub(rf'\s*<url>\s*<loc>{re.escape(SITE)}{BASE}/[^<]*</loc>.*?</url>', '', xml, flags=re.S)
    urls = [(f'{BASE}/', '0.8')] + [(module_url(m), '0.7') for m in c['modules']] + [(lesson_url(l), '0.6') for l in c['lessons']]
    block = ''.join(f'\n  <url>\n    <loc>{SITE}{u}</loc>\n    <changefreq>yearly</changefreq>\n    <priority>{p}</priority>\n  </url>' for u, p in urls)
    xml = xml.replace('\n</urlset>', block + '\n</urlset>')
    path.write_text(xml, encoding='utf-8', newline='\n')


def build_rcourse():
    c = load_course()
    with open(DATA / 'rcourse_playlist.csv', encoding='utf-8', newline='') as f:
        c['published'] = {r['video_id']: r['published_at'] for r in csv.DictReader(f)}
    c['total'] = sum(l['duration'] for l in c['lessons']) + c['about']['duration']
    build_index(c)
    for i, m in enumerate(c['modules']):
        build_module(c, m, i)
        for l in m['lessons']:
            build_lesson(c, m, l)
    update_sitemap(c)
    print(f'{SLUG}/: {1 + len(c["modules"]) + len(c["lessons"])} страниц, {c["rows"]} видео')
