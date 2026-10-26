"""Генератор внутренних страниц сайта alexey-seleznev.pro.

Собирает courses/, talks/, articles/ и interviews/ (index.html) из JSON-файлов в _build/data.
Запуск из корня репозитория:  python _build/build.py
Папка _build не публикуется GitHub Pages (Jekyll игнорирует каталоги, начинающиеся с "_").
"""
import html
import json
import urllib.parse
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = Path(__file__).resolve().parent / 'data'
SITE = 'https://alexey-seleznev.pro'
LANGS = ('ru', 'ua', 'en')


def load(name):
    return json.loads((DATA / f'{name}.json').read_text(encoding='utf-8'))


def esc(s):
    return html.escape(str(s), quote=True)


def url(u):
    """Кодирует кириллицу в URL, не трогая уже закодированные символы."""
    return urllib.parse.quote(u, safe=":/?&=%#+,;@!~*()'$[]")


def T(ru, ua=None, en=None):
    """Трёхъязычный текст в формате лендинга (ru-text / ua-text / en-text)."""
    ua = ru if ua is None else ua
    en = ru if en is None else en
    return f'<span class="ru-text">{ru}</span><span class="ua-text">{ua}</span><span class="en-text">{en}</span>'


def tr(d):
    return T(esc(d['ru']), esc(d['ua']), esc(d['en']))


MONTHS = {
    'ru': ['янв.', 'февр.', 'март', 'апр.', 'май', 'июнь', 'июль', 'авг.', 'сент.', 'окт.', 'нояб.', 'дек.'],
    'ua': ['січ.', 'лют.', 'берез.', 'квіт.', 'трав.', 'черв.', 'лип.', 'серп.', 'верес.', 'жовт.', 'листоп.', 'груд.'],
    'en': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
}


def plural_ru(n, one, few, many):
    """Согласование существительного с числом: 1 доклад, 2 доклада, 5 докладов."""
    n = abs(n) % 100
    if 11 <= n <= 14:
        return many
    return {1: one, 2: few, 3: few, 4: few}.get(n % 10, many)


def month_label(y, m):
    return T(*(f'{MONTHS[l][m - 1]} {y}' for l in LANGS))


def ym(s):
    y, m = s.split('-')
    return int(y), int(m)


# ---------------------------------------------------------------- навигация

PAGES = [
    ('opensource', 'fa-solid fa-code-branch', ('Open Source', 'Open Source', 'Open Source')),
    ('courses', 'fa-solid fa-graduation-cap', ('Курсы', 'Курси', 'Courses')),
    ('videos', 'fa-solid fa-circle-play', ('Видеоуроки', 'Відеоуроки', 'Video Lessons')),
    ('talks', 'fa-solid fa-microphone-lines', ('Доклады и вебинары', 'Доповіді та вебінари', 'Talks & Webinars')),
    ('articles', 'fa-solid fa-pen-nib', ('Статьи', 'Статті', 'Articles')),
    ('interviews', 'fa-regular fa-newspaper', ('Интервью', "Інтерв'ю", 'Interviews')),
]


# ---------------------------------------------------------------- структурированные данные (schema.org)

PERSON_ID = f'{SITE}/#person'
WEBSITE_ID = f'{SITE}/#website'

PERSON = {
    '@type': 'Person',
    '@id': PERSON_ID,
    'name': 'Alexey Seleznev',
    'alternateName': ['Алексей Селезнёв', 'Олексій Селезньов', 'selesnow'],
    'url': f'{SITE}/',
    'image': f'{SITE}/photo.jpg',
    'email': 'mailto:me@alexey-seleznev.pro',
    'jobTitle': 'Head of Analytics',
    'worksFor': {'@type': 'Organization', 'name': 'Netpeak Group'},
    'description': 'Head of Analytics at Netpeak Group, author of open source R packages, free R courses and the R4marketing project.',
    'knowsAbout': ['R', 'Data analytics', 'Marketing analytics', 'Web analytics', 'Business intelligence',
                   'Google BigQuery', 'Power BI', 'API integration', 'LLM tools'],
    'sameAs': [
        'https://github.com/selesnow',
        'https://linkedin.com/in/selesnow',
        'https://facebook.com/selesnow',
        'https://www.instagram.com/alexey.selesnow',
        'https://habr.com/ru/users/selesnow/',
        'https://alexeyseleznev.wordpress.com/',
        'https://t.me/R4marketing',
        'https://www.youtube.com/R4marketing',
    ],
}

WEBSITE = {
    '@type': 'WebSite',
    '@id': WEBSITE_ID,
    'url': f'{SITE}/',
    'name': 'ALEXEY-SELEZNEV.pro',
    'inLanguage': ['en', 'ru', 'uk'],
    'author': {'@id': PERSON_ID},
    'publisher': {'@id': PERSON_ID},
}


def landing_jsonld():
    """JSON-LD для лендинга: человек и сайт."""
    return {'@context': 'https://schema.org', '@graph': [PERSON, WEBSITE]}


def page_jsonld(slug, name, description, items=None):
    """JSON-LD для внутренней страницы: раздел сайта, автор, хлебные крошки и, при наличии, список элементов."""
    url = f'{SITE}/{slug}/'
    page = {
        '@type': 'CollectionPage',
        '@id': url,
        'url': url,
        'name': name,
        'description': description,
        'isPartOf': {'@id': WEBSITE_ID},
        'author': {'@id': PERSON_ID},
        'breadcrumb': {
            '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Alexey Seleznev', 'item': f'{SITE}/'},
                {'@type': 'ListItem', 'position': 2, 'name': name, 'item': url},
            ],
        },
    }
    if items:
        page['mainEntity'] = {
            '@type': 'ItemList',
            'numberOfItems': len(items),
            'itemListElement': [{'@type': 'ListItem', 'position': i, 'item': it} for i, it in enumerate(items, 1)],
        }
    return {'@context': 'https://schema.org', '@graph': [page, PERSON, WEBSITE]}


def course_items(courses):
    return [{
        '@type': 'Course',
        'name': c['title']['ru'],
        'alternateName': c['title']['en'],
        'description': c['tagline']['ru'],
        'url': c['url'],
        'image': c['cover'],
        'inLanguage': 'ru',
        'isAccessibleForFree': True,
        'provider': {'@id': PERSON_ID},
        'author': {'@id': PERSON_ID},
    } for c in courses]


def package_items(pkgs):
    items = []
    for p in pkgs:
        it = {
            '@type': 'SoftwareSourceCode',
            'name': p['name'],
            'description': p['tagline']['en'],
            'codeRepository': f'https://github.com/selesnow/{p["name"]}',
            'programmingLanguage': 'R',
            'author': {'@id': PERSON_ID},
        }
        if p['cran'] and not p.get('cranRemoved'):
            it['url'] = f'https://cran.r-project.org/package={p["name"]}'
        items.append(it)
    return items


# Идентификатор Google Analytics 4 (вида G-XXXXXXXXXX). Пустая строка — счётчик не подключается.
GA_ID = 'G-Z56YHE916N'

FONTS_URL = 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;700;800;900&display=swap'


def ga_snippet():
    if not GA_ID:
        return ''
    return f'''
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{GA_ID}');
    </script>'''


def head(slug, title, description, image=f'{SITE}/photo.jpg', jsonld=None):
    canonical = f'{SITE}/{slug}/'
    if jsonld is None and slug != '404':
        jsonld = page_jsonld(slug, title.split(' | ')[0], description)
    ld = ''
    if jsonld:
        ld = ('\n    <script type="application/ld+json">\n'
              + json.dumps(jsonld, ensure_ascii=False, indent=2)
              + '\n    </script>')
    return f'''<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="referrer" content="strict-origin-when-cross-origin">
    <meta name="robots" content="index, follow">
    <meta name="author" content="Alexey Seleznev">
    <meta name="theme-color" content="#030712">
    <link rel="canonical" href="{canonical}">

    <title>{esc(title)}</title>
    <meta name="title" content="{esc(title)}">
    <meta name="description" content="{esc(description)}">

    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical}">
    <meta property="og:site_name" content="ALEXEY-SELEZNEV.pro">
    <meta property="og:title" content="{esc(title)}">
    <meta property="og:description" content="{esc(description)}">
    <meta property="og:image" content="{image}">
    <meta property="og:image:alt" content="Алексей Селезнёв">
    <meta property="og:locale" content="ru_RU">

    <meta name="twitter:card" content="summary">
    <meta name="twitter:url" content="{canonical}">
    <meta name="twitter:title" content="{esc(title)}">
    <meta name="twitter:description" content="{esc(description)}">
    <meta name="twitter:image" content="{image}">

{ga_snippet()}
    <link rel="icon" type="image/jpeg" href="../logo.jpg">
    <link rel="apple-touch-icon" href="../logo.jpg">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="{FONTS_URL}">
    <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">
    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="../assets/site.css">
    <!-- Tailwind собран заранее (_build/build.py) и подключается последним, как это делал CDN-скрипт -->
    <link rel="stylesheet" href="../assets/tailwind.css">{ld}
</head>
<body class="relative lang-en">

    <!-- Interactive Background -->
    <div id="vanta-bg"></div>
'''


def nav(active):
    desktop = '\n'.join(
        f'                <a href="../{slug}/" class="nav-link hover:text-white transition-colors{" active" if slug == active else ""}">{T(*labels)}</a>'
        for slug, _, labels in PAGES)
    mobile = '\n'.join(f'''                <a href="../{slug}/" class="flex items-center gap-3.5 px-4 py-3 rounded-xl {"text-white bg-white/5" if slug == active else "text-slate-300"} hover:text-white hover:bg-white/5 font-semibold text-base transition-colors">
                    <i class="{icon} text-purple-400 w-5 text-center"></i>
                    {T(*labels)}
                </a>''' for slug, icon, labels in PAGES)
    return f'''
    <!-- NAVIGATION -->
    <nav class="fixed w-full z-50 top-0 left-0 border-b border-white/5 bg-slate-950/60 backdrop-blur-xl">
        <div class="max-w-7xl mx-auto px-3 sm:px-4 md:px-6 h-16 flex items-center justify-between">
            <a href="../" class="flex items-center gap-2 sm:gap-2.5 md:gap-3 group shrink min-w-0">
                <img src="../logo.jpg" alt="Alexey Seleznev" class="w-7 h-7 sm:w-8 sm:h-8 md:w-9 md:h-9 rounded-lg sm:rounded-xl object-cover shadow-md border border-white/10 group-hover:border-purple-500/50 group-hover:scale-105 transition-all shrink-0">
                <span class="text-xs min-[400px]:text-sm sm:text-base md:text-xl font-black tracking-tight uppercase outfit-font whitespace-nowrap text-white">ALEXEY-SELEZNEV<span class="text-purple-500 lowercase">.pro</span></span>
            </a>
            <div class="hidden xl:flex gap-6 text-sm font-semibold text-slate-400">
                <a href="../" class="nav-link hover:text-white transition-colors">{T('Главная', 'Головна', 'Home')}</a>
{desktop}
            </div>

            <div class="flex items-center gap-1.5 sm:gap-2 md:gap-4 shrink-0">
                <div class="lang-switcher flex gap-1 sm:gap-1.5 md:gap-2 text-[11px] sm:text-xs md:text-sm font-bold border-r border-white/10 pr-1.5 sm:pr-3 md:pr-4 mr-0.5 sm:mr-1 md:mr-2 outfit-font">
                    <button onclick="changeLang('en')" id="btn-en" class="active hover:text-white transition-colors">EN</button>
                    <span class="text-slate-600">/</span>
                    <button onclick="changeLang('ru')" id="btn-ru" class="text-slate-500 hover:text-white transition-colors">RU</button>
                    <span class="text-slate-600">/</span>
                    <button onclick="changeLang('ua')" id="btn-ua" class="text-slate-500 hover:text-white transition-colors">UA</button>
                </div>

                <a href="https://t.me/R4marketing" target="_blank" rel="noopener" class="text-slate-400 hover:text-blue-400 transition-colors hidden sm:block" aria-label="Telegram"><i class="fa-brands fa-telegram text-lg md:text-xl"></i></a>
                <a href="https://github.com/selesnow" target="_blank" rel="noopener" class="text-slate-400 hover:text-white transition-colors hidden sm:block" aria-label="GitHub"><i class="fa-brands fa-github text-lg md:text-xl"></i></a>

                <!-- Mobile Menu Button -->
                <button id="mobile-menu-btn" class="xl:hidden w-8 h-8 sm:w-10 sm:h-10 rounded-lg sm:rounded-xl bg-white/5 border border-white/10 flex items-center justify-center text-slate-300 hover:text-white hover:bg-purple-500/20 hover:border-purple-500/40 transition-all focus:outline-none" aria-label="Toggle Navigation Menu">
                    <i class="fa-solid fa-bars text-sm sm:text-lg" id="mobile-menu-icon"></i>
                </button>
            </div>
        </div>

        <!-- Mobile Navigation Menu Dropdown -->
        <div id="mobile-menu" class="hidden xl:hidden border-t border-white/10 bg-slate-950/95 backdrop-blur-2xl shadow-2xl overflow-y-auto max-h-[calc(100vh-4rem)] transition-all">
            <div class="max-w-7xl mx-auto px-6 py-6 space-y-1">
                <a href="../" class="flex items-center gap-3.5 px-4 py-3 rounded-xl text-slate-300 hover:text-white hover:bg-white/5 font-semibold text-base transition-colors">
                    <i class="fa-solid fa-house text-purple-400 w-5 text-center"></i>
                    {T('Главная', 'Головна', 'Home')}
                </a>
{mobile}

                <div class="pt-4 mt-3 border-t border-white/10 flex items-center justify-around text-slate-400">
                    <a href="https://t.me/R4marketing" target="_blank" rel="noopener" class="p-2 hover:text-blue-400 transition-colors flex items-center gap-2 text-sm font-semibold">
                        <i class="fa-brands fa-telegram text-xl"></i> Telegram
                    </a>
                    <a href="https://github.com/selesnow" target="_blank" rel="noopener" class="p-2 hover:text-white transition-colors flex items-center gap-2 text-sm font-semibold">
                        <i class="fa-brands fa-github text-xl"></i> GitHub
                    </a>
                    <a href="https://www.youtube.com/R4marketing" target="_blank" rel="noopener" class="p-2 hover:text-red-500 transition-colors flex items-center gap-2 text-sm font-semibold">
                        <i class="fa-brands fa-youtube text-xl"></i> YouTube
                    </a>
                </div>
            </div>
        </div>
    </nav>
'''


FOOTER_SOCIALS = [
    ('https://t.me/R4marketing', 'fa-brands fa-telegram', 'hover:text-blue-400 hover:border-blue-500/40', 'Telegram R4marketing'),
    ('https://www.youtube.com/R4marketing', 'fa-brands fa-youtube', 'hover:text-red-500 hover:border-red-500/40', 'YouTube R4marketing'),
    ('https://github.com/selesnow', 'fa-brands fa-github', 'hover:text-white hover:border-white/30', 'GitHub'),
    ('https://linkedin.com/in/selesnow', 'fa-brands fa-linkedin', 'hover:text-blue-500 hover:border-blue-500/40', 'LinkedIn'),
    ('https://facebook.com/selesnow', 'fa-brands fa-facebook', 'hover:text-blue-600 hover:border-blue-600/40', 'Facebook'),
    ('https://www.instagram.com/alexey.selesnow', 'fa-brands fa-instagram', 'hover:text-pink-500 hover:border-pink-500/40', 'Instagram'),
    ('https://habr.com/ru/users/selesnow/', 'fa-solid fa-h', 'hover:text-teal-400 hover:border-teal-400/40', 'Habr'),
]

FOOTER_RESOURCES = [
    ('https://t.me/R4marketing', 'fa-brands fa-telegram', ('Telegram-канал R4marketing', 'Telegram-канал R4marketing', 'R4marketing Telegram')),
    ('https://www.youtube.com/R4marketing', 'fa-brands fa-youtube', ('YouTube-канал R4marketing', 'YouTube-канал R4marketing', 'R4marketing YouTube')),
    ('https://alexeyseleznev.wordpress.com/', 'fa-solid fa-pen-nib', ('Личный блог', 'Особистий блог', 'Personal blog')),
    ('https://habr.com/ru/users/selesnow/', 'fa-solid fa-h', ('Профиль на Хабре', 'Профіль на Хабрі', 'Habr profile')),
    ('https://alexey-seleznev.pro/publications/', 'fa-solid fa-layer-group', ('Архив публикаций', 'Архів публікацій', 'Publications archive')),
    ('https://github.com/selesnow', 'fa-brands fa-github', ('GitHub', 'GitHub', 'GitHub')),
]


def footer(prefix='../'):
    """Футер в виде карты сайта. prefix='' — для лендинга (index.html), '../' — для внутренних страниц."""
    home = prefix or './'
    link_cls = 'flex items-center gap-2.5 text-sm text-slate-400 hover:text-white transition-colors group/link'
    icon_cls = 'w-4 text-center text-xs text-slate-600 group-hover/link:text-purple-400 transition-colors'

    def heading(ru, ua, en):
        return f'<h3 class="text-xs font-bold uppercase tracking-widest text-slate-500 mb-5 outfit-font">{T(ru, ua, en)}</h3>'

    socials = '\n'.join(
        f'                        <a href="{u}" target="_blank" rel="noopener" aria-label="{label}" class="w-10 h-10 rounded-xl border border-white/10 bg-white/5 flex items-center justify-center text-slate-400 {hover} transition-all hover:-translate-y-0.5"><i class="{icon}"></i></a>'
        for u, icon, hover, label in FOOTER_SOCIALS)
    pages = [f'<li><a href="{home}" class="{link_cls}"><i class="fa-solid fa-house {icon_cls}"></i>{T("Главная", "Головна", "Home")}</a></li>']
    pages += [f'<li><a href="{prefix}{slug}/" class="{link_cls}"><i class="{icon} {icon_cls}"></i>{T(*labels)}</a></li>' for slug, icon, labels in PAGES]
    resources = [f'<li><a href="{u}" target="_blank" rel="noopener" class="{link_cls}"><i class="{icon} {icon_cls}"></i>{T(*labels)}</a></li>' for u, icon, labels in FOOTER_RESOURCES]
    nl = '\n                        '
    contacts = [
        ('Email', 'mailto:me@alexey-seleznev.pro', 'me@alexey-seleznev.pro', 'hover:text-purple-300'),
        ('Telegram', 'https://t.me/AlexeySeleznev', '@AlexeySeleznev', 'hover:text-blue-300'),
        ('LinkedIn', 'https://linkedin.com/in/selesnow', 'linkedin.com/in/selesnow', 'hover:text-blue-300'),
    ]
    new_tab = ' target="_blank" rel="noopener"'
    contacts_html = nl.join(
        f'<li><div class="text-[11px] uppercase tracking-widest text-slate-600 font-bold mb-1">{label}</div>'
        f'<a href="{href}"{"" if href.startswith("mailto") else new_tab} class="text-sm text-slate-300 {hover} transition-colors break-all">{text}</a></li>'
        for label, href, text, hover in contacts)
    tagline = T('Head of Analytics в Netpeak Group. Автор open source R-пакетов, бесплатных курсов по R и проекта R4marketing.',
                'Head of Analytics у Netpeak Group. Автор open source R-пакетів, безкоштовних курсів з R та проєкту R4marketing.',
                'Head of Analytics at Netpeak Group. Author of open source R packages, free R courses and the R4marketing project.')
    to_top = "window.scrollTo({top: 0, behavior: 'smooth'}); return false;"
    return f'''
    <!-- FOOTER -->
    <footer class="border-t border-white/5 bg-slate-950/80 backdrop-blur-md pt-16 pb-8 relative z-10">
        <div class="max-w-7xl mx-auto px-6">
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-12 gap-10 lg:gap-8">
                <div class="sm:col-span-2 lg:col-span-4">
                    <a href="{home}" class="inline-flex items-center gap-3 group mb-5">
                        <img src="{prefix}logo.jpg" alt="Alexey Seleznev" class="w-10 h-10 rounded-xl object-cover border border-white/10 group-hover:border-purple-500/50 transition-colors">
                        <span class="text-lg font-black tracking-tight uppercase outfit-font text-white">ALEXEY-SELEZNEV<span class="text-purple-500 lowercase">.pro</span></span>
                    </a>
                    <p class="text-sm text-slate-400 leading-relaxed max-w-sm mb-6">{tagline}</p>
                    <div class="flex flex-wrap gap-2">
{socials}
                    </div>
                </div>

                <nav class="lg:col-span-2" aria-label="Site map">
                    {heading('Сайт', 'Сайт', 'Site')}
                    <ul class="space-y-3">
                        {nl.join(pages)}
                    </ul>
                </nav>

                <div class="lg:col-span-3">
                    {heading('R4marketing и публикации', 'R4marketing і публікації', 'R4marketing & writing')}
                    <ul class="space-y-3">
                        {nl.join(resources)}
                    </ul>
                </div>

                <div class="lg:col-span-3">
                    {heading('Контакты', 'Контакти', 'Contacts')}
                    <ul class="space-y-4">
                        {contacts_html}
                    </ul>
                </div>
            </div>

            <div class="mt-14 pt-6 border-t border-white/5 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500">
                <p>© 2026 Alexey Seleznev. {T('Все права защищены.', 'Усі права захищені.', 'All rights reserved.')}</p>
                <a href="#" onclick="{to_top}" class="inline-flex items-center gap-2 font-semibold hover:text-white transition-colors group">{T('Наверх', 'Нагору', 'Back to top')}<span class="w-7 h-7 rounded-full border border-white/10 flex items-center justify-center group-hover:bg-purple-500 group-hover:border-purple-500 transition-all"><i class="fa-solid fa-arrow-up text-[10px]"></i></span></a>
            </div>
        </div>
    </footer>
'''


VIDEO_MODAL = '''
    <!-- VIDEO MODAL (CINEMA LIGHTBOX) -->
    <div id="videoModal" class="fixed inset-0 z-[100] hidden items-center justify-center p-3 sm:p-6 md:p-10 bg-slate-950/90 backdrop-blur-xl transition-opacity duration-300 opacity-0" onclick="if (event.target.id === 'videoModal') closeVideoModal()">
        <div class="relative w-full max-w-5xl bg-slate-900 rounded-2xl md:rounded-3xl border border-white/10 overflow-hidden shadow-2xl flex flex-col transform transition-transform duration-300 scale-95" id="videoModalContent">
            <div class="flex items-center justify-between p-4 md:px-6 md:py-4 border-b border-white/10 bg-slate-950/80">
                <div id="videoModalTitle" class="text-sm md:text-base font-bold text-white truncate max-w-[85%] outfit-font"></div>
                <button onclick="closeVideoModal()" aria-label="Close video" class="w-10 h-10 rounded-full bg-white/5 hover:bg-white/15 text-slate-300 hover:text-white flex items-center justify-center transition-colors">
                    <i class="fa-solid fa-xmark text-lg"></i>
                </button>
            </div>
            <div class="relative w-full pb-[56.25%] bg-black">
                <iframe id="videoModalIframe" class="absolute inset-0 w-full h-full border-0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe>
            </div>
        </div>
    </div>
'''


def tail(modal=False):
    return (VIDEO_MODAL if modal else '') + '''
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.net.min.js"></script>
    <script src="../assets/site.js"></script>
</body>
</html>
'''


# Фото с конференций в шапках разделов (исходники в img/, оптимизированные копии в assets/photos/).
# pos — object-position: какую часть кадра оставить при обрезке под рамку.
PHOTOS = {
    'opensource': dict(src='matemarketing-2018.webp', w=1650, h=1100, pos='35% 40%',
                       event=('Матемаркетинг', 'Матемаркетинг', 'Matemarketing'), year='2018'),
    'courses': dict(src='goanalytics-2019.webp', w=1649, h=1100, pos='45% 35%',
                    event=('GoAnalytics',) * 3, year='2019'),
    'videos': dict(src='ecommerce-2017.webp', w=960, h=640, pos='45% 40%',
                   event=('eCommerce',) * 3, year='2017'),
    'talks': dict(src='analyze-2018.webp', w=960, h=599, pos='58% 50%',
                  event=('Analyze!',) * 3, year='2018'),
    'articles': dict(src='analyze-2017.webp', w=960, h=640, pos='62% 40%',
                     event=('Analyze!',) * 3, year='2017'),
    'interviews': dict(src='8p-2021.webp', w=1650, h=1100, pos='45% 45%',
                       event=('8P',) * 3, year='2021'),
}


def hero_photo(slug):
    p = PHOTOS[slug]
    return f'''
            <figure class="hero-photo lg:col-span-5" data-aos="fade-left" data-aos-delay="100">
                <div class="hero-photo-plate"></div>
                <div class="hero-photo-frame">
                    <img src="../assets/photos/{p['src']}" width="{p['w']}" height="{p['h']}" alt="Алексей Селезнёв на конференции {esc(p['event'][0])} {p['year']}" style="object-position: {p['pos']}" decoding="async">
                    <div class="hero-photo-tint"></div>
                    <div class="hero-photo-shade"></div>
                </div>
                <figcaption class="hero-photo-caption">
                    <i class="fa-solid fa-microphone-lines"></i>{T(*p["event"])}<span class="hero-photo-year">{p["year"]}</span>
                </figcaption>
            </figure>'''


def hero(icon, badge, title_html, lead, stats, back=True, photo=None):
    stats_html = '\n'.join(f'''                <div class="bento-content">
                    <div class="text-3xl md:text-4xl font-extrabold text-white outfit-font">{value}</div>
                    <div class="text-xs text-slate-400 uppercase font-bold mt-1">{label}</div>
                </div>''' for value, label in stats)
    intro = f'''<div data-aos="fade-up">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-400 text-xs font-bold tracking-widest uppercase mb-5 outfit-font">
                <i class="{icon}"></i> {badge}
            </div>
            <h1 class="text-5xl md:text-7xl font-black tracking-tight leading-tight uppercase mb-8">{title_html}</h1>
        </div>
        <div class="bento-glass no-lift p-6 md:p-10 border-l-4 border-purple-500/50 mb-8" data-aos="fade-up" data-aos-delay="100">
            <p class="text-lg md:text-xl text-slate-300 leading-relaxed font-light relative z-10">{lead}</p>
        </div>'''
    if photo:
        intro = f'''<div class="grid lg:grid-cols-12 gap-8 lg:gap-12 mb-8">
            <div class="lg:col-span-7 flex flex-col justify-end">
        {intro.replace(' mb-8" data-aos="fade-up" data-aos-delay="100"', '" data-aos="fade-up" data-aos-delay="100"')}
            </div>{hero_photo(photo)}
        </div>'''
    return f'''
    <!-- HERO -->
    <header class="pt-32 pb-12 px-6 max-w-7xl mx-auto relative z-10">
        <a href="../" class="inline-flex items-center gap-2 text-sm font-semibold text-slate-400 hover:text-white transition-colors mb-8 group" data-aos="fade-right">
            <i class="fa-solid fa-arrow-left text-xs group-hover:-translate-x-1 transition-transform"></i>
            {T('На главную', 'На головну', 'Back to home')}
        </a>
        {intro}
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6 bento-glass no-lift p-6 rounded-3xl" data-aos="fade-up" data-aos-delay="150">
{stats_html}
        </div>
    </header>
'''


def cover(img, icon, height='h-48', extra=''):
    img_tag = (f'<img src="{esc(url(img))}" alt="" loading="lazy" referrerpolicy="no-referrer" onerror="this.remove()">'
               if img else '')
    return f'''<div class="cover {height} rounded-2xl">
                        <div class="cover-fallback"><i class="{icon} text-5xl"></i></div>
                        {img_tag}
                        <div class="absolute inset-0 bg-gradient-to-t from-slate-950/85 via-slate-950/10 to-transparent"></div>
                        {extra}
                    </div>'''


def filter_btn(group, value, label, count, icon='', active=False):
    ic = f'<i class="{icon} text-xs text-purple-400"></i>' if icon else ''
    return (f'<button type="button" data-filter-group="{group}" data-filter-value="{value}" '
            f'class="filter-btn{" active" if active else ""} px-4 py-2 rounded-xl text-sm font-semibold flex items-center gap-2">'
            f'{ic}{label}<span class="text-xs opacity-80 bg-white/10 px-2 py-0.5 rounded-full font-mono">{count}</span></button>')


def search_box(ru, ua, en):
    return (f'<div class="relative w-full md:w-80"><i class="fa-solid fa-magnifying-glass absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 text-sm"></i>'
            f'<input type="search" data-filter-search class="search-input w-full rounded-xl pl-11 pr-4 py-2.5 text-sm text-white placeholder-slate-500" '
            f'placeholder="{esc(en)}" data-ph-ru="{esc(ru)}" data-ph-ua="{esc(ua)}" data-ph-en="{esc(en)}"></div>')


def empty_state():
    return f'''<div data-filter-empty class="hidden bento-glass no-lift p-10 text-center text-slate-400 rounded-3xl">
            <i class="fa-solid fa-magnifying-glass text-3xl text-purple-400/60 mb-4"></i>
            <p>{T('Ничего не найдено — попробуйте изменить фильтр или запрос.', 'Нічого не знайдено — спробуйте змінити фільтр або запит.', 'Nothing found — try another filter or query.')}</p>
        </div>'''


def cta_block():
    return f'''
    <section class="px-6 max-w-7xl mx-auto pb-24 relative z-10">
        <div class="grid md:grid-cols-2 gap-6" data-aos="fade-up">
            <a href="https://t.me/R4marketing" target="_blank" rel="noopener" class="bento-glass p-8 rounded-[2rem] flex items-center gap-6 group" style="background: linear-gradient(145deg, rgba(30, 41, 59, 0.4), rgba(59, 130, 246, 0.1));">
                <div class="bento-content w-16 h-16 bg-blue-500/20 rounded-2xl flex items-center justify-center text-blue-400 text-3xl shrink-0 group-hover:scale-110 transition-transform"><i class="fa-brands fa-telegram"></i></div>
                <div class="bento-content flex-1">
                    <h3 class="text-xl font-bold text-white mb-1 outfit-font">{T('Telegram-канал R4marketing', 'Telegram-канал R4marketing', 'R4marketing on Telegram')}</h3>
                    <p class="text-slate-400 text-sm">{T('Новые статьи, видео и заметки по R — первыми.', 'Нові статті, відео та нотатки з R — першими.', 'New articles, videos and R notes — first.')}</p>
                </div>
                <i class="bento-content fa-solid fa-arrow-right text-blue-400 group-hover:translate-x-1 transition-transform"></i>
            </a>
            <a href="https://www.youtube.com/R4marketing/?sub_confirmation=1" target="_blank" rel="noopener" class="bento-glass p-8 rounded-[2rem] flex items-center gap-6 group" style="background: linear-gradient(145deg, rgba(30, 41, 59, 0.4), rgba(239, 68, 68, 0.1));">
                <div class="bento-content w-16 h-16 bg-red-500/20 rounded-2xl flex items-center justify-center text-red-500 text-3xl shrink-0 group-hover:scale-110 transition-transform"><i class="fa-brands fa-youtube"></i></div>
                <div class="bento-content flex-1">
                    <h3 class="text-xl font-bold text-white mb-1 outfit-font">{T('YouTube-канал R4marketing', 'YouTube-канал R4marketing', 'R4marketing on YouTube')}</h3>
                    <p class="text-slate-400 text-sm">{T('Видеоуроки по R, аналитике и AI-инструментам.', 'Відеоуроки з R, аналітики та AI-інструментів.', 'Video lessons on R, analytics and AI tools.')}</p>
                </div>
                <i class="bento-content fa-solid fa-arrow-right text-red-400 group-hover:translate-x-1 transition-transform"></i>
            </a>
        </div>
    </section>
'''


def write(slug, content):
    out = ROOT / slug / 'index.html'
    out.parent.mkdir(exist_ok=True)
    out.write_text(content, encoding='utf-8', newline='\n')
    print(f'{out.relative_to(ROOT)}: {len(content):,} bytes')


# ---------------------------------------------------------------- курсы

LEVELS = {
    'beginner': ('BEGINNER', 'bg-green-500/20 border border-green-500/50 text-green-400', ('Для начинающих', 'Для початківців', 'Beginner')),
    'middle': ('MIDDLE', 'bg-blue-500/20 border border-blue-500/50 text-blue-400', ('Средний уровень', 'Середній рівень', 'Intermediate')),
    'advanced': ('ADVANCED', 'bg-orange-500/20 border border-orange-500/50 text-orange-400', ('Продвинутый', 'Просунутий', 'Advanced')),
    'new': ('NEW', 'bg-purple-500 border border-purple-400/50 text-white shadow-[0_0_15px_rgba(168,85,247,0.6)]', ('Новый курс', 'Новий курс', 'New course')),
}


def build_courses():
    courses = load('courses')
    path_steps = [
        ('beginner', 'fa-seedling', 'text-green-400', 'bg-green-500/10 border-green-500/30', ('Старт', 'Старт', 'Start')),
        ('middle', 'fa-layer-group', 'text-blue-400', 'bg-blue-500/10 border-blue-500/30', ('Углубление', 'Поглиблення', 'Level up')),
        ('advanced', 'fa-rocket', 'text-orange-400', 'bg-orange-500/10 border-orange-500/30', ('Продвинутый уровень', 'Просунутий рівень', 'Advanced')),
    ]
    steps = []
    for n, (lvl, icon, color, box, label) in enumerate(path_steps, 1):
        items = [c for c in courses if c['level'] == lvl or (lvl == 'advanced' and c['level'] == 'new')]
        links = '\n'.join(f'''                        <a href="#{c['id']}" class="flex items-center justify-between gap-3 px-4 py-3 rounded-xl bg-slate-900/50 border border-white/5 hover:border-purple-500/40 hover:bg-white/5 transition-all text-sm font-semibold text-slate-200 group/link">
                            <span>{tr(c['title'])}</span>
                            <i class="fa-solid fa-arrow-down text-xs text-slate-500 group-hover/link:text-purple-400 transition-colors"></i>
                        </a>''' for c in items)
        steps.append(f'''                <div class="bento-glass no-lift p-6 rounded-3xl" data-aos="fade-up" data-aos-delay="{n * 80}">
                    <div class="bento-content">
                        <div class="flex items-center gap-3 mb-5">
                            <div class="w-11 h-11 rounded-2xl border {box} flex items-center justify-center {color}"><i class="fa-solid {icon}"></i></div>
                            <div>
                                <div class="text-[11px] font-mono font-bold uppercase tracking-widest text-slate-500">{T('Шаг', 'Крок', 'Step')} {n}</div>
                                <div class="font-bold text-white outfit-font text-lg">{T(*label)}</div>
                            </div>
                        </div>
                        <div class="space-y-2">
{links}
                        </div>
                    </div>
                </div>''')

    cards = []
    for idx, c in enumerate(courses):
        badge, badge_cls, level_label = LEVELS[c['level']]
        reverse = 'lg:flex-row-reverse' if idx % 2 else 'lg:flex-row'
        is_new = c['level'] == 'new'
        stats = '\n'.join(f'<span class="px-3 py-1.5 rounded-lg bg-slate-900/60 border border-white/5 text-xs font-semibold text-slate-300">{tr(s)}</span>' for s in c['stats'])
        program = '\n'.join(f'''                            <li class="flex items-start gap-3 text-sm text-slate-300"><i class="fa-solid fa-check text-purple-400 text-xs mt-1.5"></i>{T(esc(c['program']['ru'][i]), esc(c['program']['ua'][i]), esc(c['program']['en'][i]))}</li>'''
                            for i in range(len(c['program']['ru'])))
        buttons = [f'''<a href="{esc(url(c['url']))}" target="_blank" rel="noopener" class="bg-purple-600 hover:bg-purple-500 text-white px-6 py-3 rounded-xl font-bold text-sm transition-all shadow-[0_0_20px_rgba(168,85,247,0.35)] hover:shadow-[0_0_30px_rgba(168,85,247,0.55)] flex items-center gap-2">{T('Перейти к курсу', 'Перейти до курсу', 'Go to course') if 'kindLabel' not in c else T('Читать учебник', 'Читати підручник', 'Read the book')} <i class="fa-solid fa-arrow-right text-xs"></i></a>''']
        if c.get('playlist'):
            buttons.append(f'''<a href="{esc(c['playlist'])}" target="_blank" rel="noopener" class="px-5 py-3 rounded-xl border border-white/10 hover:border-white/20 bg-slate-900/80 hover:bg-slate-800 text-slate-300 hover:text-white font-semibold text-sm transition-all flex items-center gap-2"><i class="fa-brands fa-youtube text-red-500"></i> {T('Плейлист', 'Плейлист', 'Playlist')}</a>''')
        if c.get('article'):
            buttons.append(f'''<a href="{esc(c['article'])}" target="_blank" rel="noopener" class="px-5 py-3 rounded-xl border border-white/10 hover:border-white/20 bg-slate-900/80 hover:bg-slate-800 text-slate-300 hover:text-white font-semibold text-sm transition-all flex items-center gap-2"><i class="fa-solid fa-h text-teal-400"></i> {T('Статья о курсе', 'Стаття про курс', 'About the course')}</a>''')
        if c.get('materials'):
            buttons.append(f'''<a href="{esc(c['materials'])}" target="_blank" rel="noopener" class="px-5 py-3 rounded-xl border border-white/10 hover:border-white/20 bg-slate-900/80 hover:bg-slate-800 text-slate-300 hover:text-white font-semibold text-sm transition-all flex items-center gap-2"><i class="fa-brands fa-github"></i> {T('Материалы', 'Матеріали', 'Materials')}</a>''')
        note = f'<p class="text-xs text-slate-500 mt-3 flex items-center gap-2"><i class="fa-solid fa-circle-info"></i>{tr(c["note"])}</p>' if c.get('note') else ''
        kind = f'<span class="text-[11px] font-mono font-bold uppercase tracking-widest text-slate-500">{tr(c["kindLabel"])}</span>' if c.get('kindLabel') else ''
        cards.append(f'''
        <article id="{c['id']}" class="bento-glass no-lift rounded-[2rem] p-3 md:p-4 scroll-mt-24{' border-purple-500/40 shadow-[0_0_35px_rgba(168,85,247,0.15)]' if is_new else ''}" data-aos="fade-up">
            <div class="bento-content flex flex-col {reverse} gap-6 lg:gap-10">
                <div class="lg:w-[42%] shrink-0">
                    <div class="cover h-60 md:h-80 lg:h-full lg:min-h-[420px] rounded-[1.5rem]">
                        <div class="cover-fallback"><i class="fa-brands fa-r-project text-6xl"></i></div>
                        <img src="{esc(c['cover'])}" alt="{esc(c['title']['ru'])}" loading="lazy" style="object-position: top" onerror="this.remove()">
                        <div class="absolute inset-0 bg-gradient-to-t from-slate-950/70 via-transparent to-transparent"></div>
                        <div class="absolute top-4 left-4 {badge_cls} text-[10px] uppercase font-bold px-3 py-1 rounded-full backdrop-blur-lg">{badge}</div>
                        <div class="absolute bottom-4 left-4 text-xs font-mono font-bold text-slate-300 bg-slate-950/70 border border-white/10 px-2.5 py-1 rounded-lg backdrop-blur-md">{c['year']}</div>
                    </div>
                </div>
                <div class="flex-1 py-2 lg:py-6 pr-1 lg:pr-6 flex flex-col">
                    <div class="flex flex-wrap items-center gap-3 mb-3">
                        <span class="text-xs font-bold uppercase tracking-wider text-purple-400">{T(*level_label)}</span>
                        {kind}
                    </div>
                    <h2 class="text-3xl md:text-4xl font-extrabold text-white outfit-font mb-3 leading-tight">{tr(c['title'])}</h2>
                    <p class="text-lg text-slate-300 font-medium mb-5">{tr(c['tagline'])}</p>
                    <p class="text-slate-400 leading-relaxed font-light mb-6">{tr(c['desc'])}</p>
                    <div class="grid md:grid-cols-2 gap-6 mb-6">
                        <div>
                            <div class="text-xs font-mono font-bold uppercase tracking-widest text-slate-500 mb-3">{T('Программа', 'Програма', 'Curriculum')}</div>
                            <ul class="space-y-2">
{program}
                            </ul>
                        </div>
                        <div>
                            <div class="text-xs font-mono font-bold uppercase tracking-widest text-slate-500 mb-3">{T('Для кого', 'Для кого', 'Who it is for')}</div>
                            <p class="text-sm text-slate-300 mb-5">{tr(c['audience'])}</p>
                            <div class="flex flex-wrap gap-2">
{stats}
                            </div>
                        </div>
                    </div>
                    <div class="mt-auto pt-5 border-t border-white/5">
                        <div class="flex flex-wrap gap-3">
                            {"".join(buttons)}
                        </div>
                        {note}
                    </div>
                </div>
            </div>
        </article>''')

    free = len(courses)
    courses_desc = 'Бесплатные авторские курсы Алексея Селезнёва по языку R: от R для пользователей Excel до разработки пакетов, Telegram-ботов и AI-инструментов.'
    page = head('courses', 'Курсы по языку R | Алексей Селезнёв', courses_desc,
                jsonld=page_jsonld('courses', 'Курсы по языку R', courses_desc, course_items(courses)))
    page += nav('courses')
    page += hero('fa-solid fa-graduation-cap', T('Обучение', 'Навчання', 'Learning'),
                 T('Авторские <span class="text-gradient">курсы</span>', 'Авторські <span class="text-gradient">курси</span>', 'Original <span class="text-gradient">Courses</span>'),
                 T('Курсы появились как внутренняя программа обучения аналитиков отдела Netpeak — от уровня Junior до Senior. Позже все программы были опубликованы в открытом доступе и стали востребованы среди тысяч специалистов. Все курсы бесплатные: видеолекции, конспекты, код, тесты и задания.',
                   'Курси з\'явилися як внутрішня програма навчання аналітиків відділу Netpeak — від рівня Junior до Senior. Пізніше всі програми були опубліковані у відкритому доступі та стали затребуваними серед тисяч фахівців. Усі курси безкоштовні: відеолекції, конспекти, код, тести та завдання.',
                   'These courses began as an internal training program for Netpeak\'s analytics team — from Junior to Senior. Later every program was published openly and is now used by thousands of specialists. All courses are free: video lectures, notes, code, quizzes and assignments.'),
                 [(str(free), T('Курсов', 'Курсів', 'Courses')), ('0 $', T('Стоимость', 'Вартість', 'Price')),
                  ('2018', T('Первый курс', 'Перший курс', 'First course')), ('3', T('Уровня сложности', 'Рівні складності', 'Skill levels'))], photo='courses')
    page += f'''
    <!-- LEARNING PATH -->
    <section class="px-6 max-w-7xl mx-auto pb-16 relative z-10">
        <h2 class="text-3xl font-extrabold mb-8 flex items-center gap-4 outfit-font" data-aos="fade-up">
            <div class="w-12 h-12 bg-purple-500/20 flex items-center justify-center rounded-2xl border border-purple-500/30"><i class="fa-solid fa-route text-purple-500 text-xl"></i></div>
            {T('С чего начать', 'З чого почати', 'Where to start')}
        </h2>
        <div class="grid md:grid-cols-3 gap-6">
{chr(10).join(steps)}
        </div>
    </section>

    <!-- COURSES -->
    <section class="px-6 max-w-7xl mx-auto pb-16 relative z-10 space-y-10">
{"".join(cards)}
    </section>

    <!-- COMMERCIAL TEACHING -->
    <section class="px-6 max-w-7xl mx-auto pb-16 relative z-10">
        <h2 class="text-3xl font-extrabold mb-8 flex items-center gap-4 outfit-font" data-aos="fade-up">
            <div class="w-12 h-12 bg-blue-500/20 flex items-center justify-center rounded-2xl border border-blue-500/30"><i class="fa-solid fa-chalkboard-user text-blue-400 text-xl"></i></div>
            {T('Преподавание на образовательных платформах', 'Викладання на освітніх платформах', 'Teaching for education platforms')}
        </h2>
        <div class="grid md:grid-cols-2 gap-6" data-aos="fade-up">
            <a href="https://r-for-marketing.netpeak.net/" target="_blank" rel="noopener" class="bento-glass p-8 rounded-3xl group block">
                <div class="bento-content">
                    <div class="text-xs font-mono font-bold uppercase tracking-widest text-blue-400 mb-3">NeedForData · Netpeak · 2018</div>
                    <h3 class="text-2xl font-bold text-white outfit-font mb-3 group-hover:text-purple-300 transition-colors">{T('«Язык R для интернет-маркетинга»', '«Мова R для інтернет-маркетингу»', '“R for Digital Marketing”')}</h3>
                    <p class="text-slate-400 text-sm leading-relaxed">{T('Автор и лектор онлайн-курса для платформы NeedForData: методичка, видеолекции и практические задания по автоматизации маркетинговой аналитики на R.', 'Автор і лектор онлайн-курсу для платформи NeedForData: методичка, відеолекції та практичні завдання з автоматизації маркетингової аналітики на R.', 'Author and lecturer of the online course for NeedForData: a handbook, video lectures and hands-on tasks on automating marketing analytics with R.')}</p>
                </div>
            </a>
            <div class="bento-glass p-8 rounded-3xl">
                <div class="bento-content">
                    <div class="text-xs font-mono font-bold uppercase tracking-widest text-blue-400 mb-3">WebPromoExperts</div>
                    <h3 class="text-2xl font-bold text-white outfit-font mb-3">{T('«Веб-аналитика PRO»', '«Веб-аналітика PRO»', '“Web Analytics PRO”')}</h3>
                    <p class="text-slate-400 text-sm leading-relaxed">{T('Соавтор программы и лектор продвинутого курса по веб-аналитике в академии WebPromoExperts.', 'Співавтор програми та лектор просунутого курсу з веб-аналітики в академії WebPromoExperts.', 'Co-author and lecturer of the advanced web analytics course at the WebPromoExperts Academy.')}</p>
                </div>
            </div>
        </div>
    </section>
'''
    page += cta_block() + footer() + tail()
    write('courses', page)


# ---------------------------------------------------------------- выступления

def build_talks():
    talks = load('talks')
    cats = Counter(t['cat'] for t in talks)
    years = sorted(ym(t['date'])[0] for t in talks)
    events = sorted({t['event'] for t in talks})

    def card(t, delay):
        y, m = ym(t['date'])
        is_conf = t['cat'] == 'conference'
        cat_badge = ('CONF', 'bg-purple-500/20 text-purple-300 border-purple-500/30') if is_conf else ('WEBINAR', 'bg-blue-500/20 text-blue-300 border-blue-500/30')
        search = ' '.join([t['title'][l] for l in LANGS] + [t['event'], t['desc']['ru']]).lower()
        if t.get('yt'):
            vid = t['yt'].split('?')[0]
            href = f'https://www.youtube.com/watch?v={vid}'
            if '?start=' in t['yt']:
                href += '&t=' + t['yt'].split('?start=')[1]
            img = f'https://img.youtube.com/vi/{vid}/hqdefault.jpg'
            attrs = f'data-video="{esc(t["yt"])}"'
            center = '''<div class="absolute inset-0 flex items-center justify-center"><div class="w-14 h-14 rounded-full bg-red-600/90 text-white flex items-center justify-center shadow-2xl backdrop-blur-sm group-hover:scale-110 group-hover:bg-red-500 transition-all duration-300 group-hover:shadow-[0_0_25px_rgba(239,68,68,0.7)]"><i class="fa-solid fa-play ml-1 text-lg"></i></div></div>'''
            action = f'<i class="fa-brands fa-youtube text-red-500 text-sm"></i> {T("Смотреть", "Дивитися", "Watch")}'
        else:
            href, attrs = t['url'], ''
            img = f"../assets/photos/{t['photo']}" if t.get('photo') else ''  # своё фото, если нет записи
            # на фото значок уходит в угол, чтобы не закрывать спикера
            center = '''<div class="absolute bottom-3 right-3 w-10 h-10 rounded-full bg-purple-600/80 text-white flex items-center justify-center shadow-2xl backdrop-blur-sm group-hover:scale-110 group-hover:bg-purple-500 transition-all duration-300"><i class="fa-solid fa-arrow-up-right-from-square text-sm"></i></div>''' if img else '''<div class="absolute inset-0 flex items-center justify-center"><div class="w-14 h-14 rounded-full bg-purple-600/80 text-white flex items-center justify-center shadow-2xl backdrop-blur-sm group-hover:scale-110 group-hover:bg-purple-500 transition-all duration-300"><i class="fa-solid fa-arrow-up-right-from-square text-base"></i></div></div>'''
            action = f'<i class="fa-solid fa-file-lines text-purple-400 text-sm"></i> {T("Материалы конференции", "Матеріали конференції", "Conference page")}'
        extra = f'''<div class="absolute top-3 left-3 text-[10px] font-mono font-bold uppercase tracking-wider px-2.5 py-1 rounded-lg backdrop-blur-md bg-slate-950/80 border border-white/10 text-purple-300">{month_label(y, m)} • {esc(t['event'])}</div>
                        <div class="absolute top-3 right-3 text-[10px] font-bold px-2 py-0.5 rounded backdrop-blur-md border {cat_badge[1]}">{cat_badge[0]}</div>
                        {center}'''
        return f'''
            <a href="{esc(href)}" target="_blank" rel="noopener" {attrs} class="bento-glass group flex flex-col p-3 rounded-3xl cursor-pointer" data-filter-item data-cat="{t['cat']}" data-search="{esc(search)}" data-aos="fade-up" data-aos-delay="{delay}">
                <div class="bento-content flex flex-col h-full">
                    {cover(img, 'fa-solid fa-users-gear', 'h-48 sm:h-52', extra)}
                    <div class="px-2 pt-4 pb-1 flex flex-col flex-1">
                        <div class="text-xs font-semibold text-purple-400 mb-2">{tr(t['kind'])}</div>
                        <h3 class="font-bold text-lg leading-snug text-slate-100 group-hover:text-white transition-colors outfit-font mb-3" data-video-title>{tr(t['title'])}</h3>
                        <p class="text-sm text-slate-400 leading-relaxed flex-1">{tr(t['desc'])}</p>
                        <div class="mt-4 pt-3 border-t border-white/5 flex items-center justify-between text-xs text-slate-400 group-hover:text-purple-300 transition-colors">
                            <span class="flex items-center gap-1.5 font-semibold">{action}</span>
                            <i class="fa-solid fa-arrow-right text-xs opacity-60 group-hover:opacity-100 group-hover:translate-x-1 transition-all"></i>
                        </div>
                    </div>
                </div>
            </a>'''

    featured = talks[0]
    fvid = featured['yt'].split('?')[0]
    grid = ''.join(card(t, (i % 3) * 60) for i, t in enumerate(talks))
    chips = ' '.join(f'<span class="px-3 py-1 rounded-full bg-slate-900/60 border border-white/10 text-xs font-semibold text-slate-300">{esc(e)}</span>' for e in events)

    page = head('talks', 'Доклады и вебинары | Алексей Селезнёв',
                f'{len(talks)} {plural_ru(len(talks), "доклад", "доклада", "докладов")}, воркшопов и вебинаров Алексея Селезнёва с конференций 8P, Матемаркетинг, GoAnalytics, Analyze! и других: язык R, API рекламных систем, BI и аналитика.')
    page += nav('talks')
    page += hero('fa-solid fa-microphone-lines', T('Спикер', 'Спікер', 'Speaker'),
                 T('Доклады и <span class="text-gradient">вебинары</span>', 'Доповіді та <span class="text-gradient">вебінари</span>', 'Talks & <span class="text-gradient">Webinars</span>'),
                 T('Регулярно выступаю на крупнейших отраслевых конференциях по аналитике и интернет-маркетингу — 8P, Матемаркетинг, GoAnalytics, Analyze! — и провожу вебинары и воркшопы для образовательных платформ. Делюсь практическим опытом автоматизации, работы с API рекламных систем и построения BI-решений. Нажмите на карточку, чтобы посмотреть запись прямо здесь.',
                   'Регулярно виступаю на найбільших галузевих конференціях з аналітики та інтернет-маркетингу — 8P, Матемаркетинг, GoAnalytics, Analyze! — і проводжу вебінари та воркшопи для освітніх платформ. Ділюся практичним досвідом автоматизації, роботи з API рекламних систем і побудови BI-рішень. Натисніть на картку, щоб переглянути запис просто тут.',
                   'I speak regularly at major analytics and digital marketing conferences — 8P, Matemarketing, GoAnalytics, Analyze! — and run webinars and workshops for education platforms, sharing hands-on experience in automation, ad-platform APIs and BI. Click any card to watch the recording right here.'),
                 [(str(len(talks)), T('Выступлений', 'Виступів', 'Talks')), (str(cats['conference']), T('Конференции', 'Конференції', 'Conferences')),
                  (str(cats['webinar']), T('Вебинары', 'Вебінари', 'Webinars')), (f'{years[0]}–{years[-1]}', T('Годы', 'Роки', 'Years'))], photo='talks')
    page += f'''
    <!-- FEATURED -->
    <section class="px-6 max-w-7xl mx-auto pb-16 relative z-10">
        <a href="https://www.youtube.com/watch?v={fvid}" target="_blank" rel="noopener" data-video="{esc(featured['yt'])}" class="bento-glass group block p-5 sm:p-7 lg:p-8 rounded-3xl border border-purple-500/30 shadow-[0_0_35px_rgba(168,85,247,0.15)]" data-aos="fade-up">
            <div class="bento-content grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8 items-center">
                <div class="lg:col-span-7">
                    <div class="relative w-full pb-[56.25%] rounded-2xl overflow-hidden bg-slate-950 shadow-2xl border border-white/10">
                        <img src="https://img.youtube.com/vi/{fvid}/hqdefault.jpg" alt="" class="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-700">
                        <div class="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-transparent to-black/30"></div>
                        <div class="absolute inset-0 flex items-center justify-center">
                            <div class="w-16 h-16 sm:w-20 sm:h-20 rounded-full bg-red-600/95 text-white flex items-center justify-center shadow-[0_0_30px_rgba(239,68,68,0.6)] backdrop-blur-md group-hover:scale-110 group-hover:bg-red-500 transition-all duration-300"><i class="fa-solid fa-play ml-1.5 text-xl sm:text-2xl"></i></div>
                        </div>
                    </div>
                </div>
                <div class="lg:col-span-5">
                    <span class="inline-flex px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-purple-500/20 text-purple-300 border border-purple-500/40 items-center gap-1.5 mb-4"><i class="fa-solid fa-star text-[10px] text-yellow-400"></i>{T('Последнее выступление', 'Останній виступ', 'Latest talk')}</span>
                    <div class="text-xs font-mono font-bold text-purple-400 uppercase tracking-widest mb-2">{month_label(*ym(featured['date']))} • {esc(featured['event'])}</div>
                    <h2 class="text-2xl lg:text-3xl font-extrabold text-white leading-snug outfit-font mb-4" data-video-title>{tr(featured['title'])}</h2>
                    <p class="text-sm text-slate-300 leading-relaxed font-light mb-6">{tr(featured['desc'])}</p>
                    <span class="inline-flex px-5 py-3 rounded-xl bg-purple-600 group-hover:bg-purple-500 text-white font-bold text-sm transition-all items-center gap-2 shadow-[0_0_20px_rgba(168,85,247,0.4)]"><i class="fa-solid fa-play text-xs"></i>{T('Смотреть', 'Дивитися', 'Play video')}</span>
                </div>
            </div>
        </a>
    </section>

    <!-- CATALOG -->
    <section class="px-6 max-w-7xl mx-auto pb-16 relative z-10">
        <div class="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-8" data-aos="fade-up">
            <div>
                <h2 class="text-3xl font-extrabold outfit-font mb-2">{T('Все записи', 'Усі записи', 'All recordings')}</h2>
                <p class="text-slate-400 text-sm">{T('Показано', 'Показано', 'Showing')}: <span data-filter-count class="font-mono text-white">{len(talks)}</span></p>
            </div>
            {search_box('Поиск по докладам…', 'Пошук за доповідями…', 'Search talks…')}
        </div>
        <div class="flex flex-wrap items-center gap-3 mb-8" data-aos="fade-up">
            {filter_btn('cat', 'all', T('Все', 'Усі', 'All'), len(talks), 'fa-solid fa-layer-group', True)}
            {filter_btn('cat', 'conference', T('Конференции', 'Конференції', 'Conferences'), cats['conference'], 'fa-solid fa-microphone')}
            {filter_btn('cat', 'webinar', T('Вебинары и воркшопы', 'Вебінари та воркшопи', 'Webinars & workshops'), cats['webinar'], 'fa-solid fa-video')}
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">{grid}
        </div>
        {empty_state()}
    </section>

    <!-- EVENTS -->
    <section class="px-6 max-w-7xl mx-auto pb-16 relative z-10">
        <div class="bento-glass no-lift p-6 md:p-8 rounded-3xl" data-aos="fade-up">
            <div class="bento-content">
                <div class="text-xs font-mono font-bold uppercase tracking-widest text-slate-500 mb-4">{T('Площадки и организаторы', 'Майданчики та організатори', 'Events & organizers')}</div>
                <div class="flex flex-wrap gap-2">{chips}</div>
            </div>
        </div>
    </section>
'''
    page += cta_block() + footer() + tail(modal=True)
    write('talks', page)


# ---------------------------------------------------------------- статьи

TOPICS = {
    'r': ('fa-brands fa-r-project', ('Язык R', 'Мова R', 'R language')),
    'research': ('fa-solid fa-chart-column', ('Исследования CPC', 'Дослідження CPC', 'CPC research')),
    'bq': ('fa-solid fa-database', ('BigQuery', 'BigQuery', 'BigQuery')),
    'pbi': ('fa-solid fa-chart-pie', ('Power BI', 'Power BI', 'Power BI')),
    'ga': ('fa-solid fa-chart-line', ('Веб-аналитика', 'Веб-аналітика', 'Web analytics')),
    'ppc': ('fa-solid fa-bullhorn', ('Реклама и API', 'Реклама та API', 'Ads & APIs')),
    'excel': ('fa-solid fa-table', ('Excel и Таблицы', 'Excel і Таблиці', 'Excel & Sheets')),
    'bot': ('fa-brands fa-telegram', ('Telegram-боты', 'Telegram-боти', 'Telegram bots')),
    'python': ('fa-brands fa-python', ('Python', 'Python', 'Python')),
    'bi': ('fa-solid fa-diagram-project', ('BI и кейсы', 'BI та кейси', 'BI & cases')),
}

SOURCES = [
    ('habr', 'bg-teal-400', ('Хабр', 'Хабр', 'Habr')),
    ('netpeak', 'bg-blue-500', ('Netpeak Journal', 'Netpeak Journal', 'Netpeak Journal')),
    ('blog', 'bg-purple-500', ('Личный блог', 'Особистий блог', 'Personal blog')),
    ('other', 'bg-pink-500', ('Другие издания', 'Інші видання', 'Other media')),
]


def source_key(a):
    if a['src'] == 'Хабр': return 'habr'
    if a['src'] == 'Netpeak Journal': return 'netpeak'
    if a['src'] == 'Блог Алексея Селезнёва': return 'blog'
    return 'other'


def source_label(a):
    if a['src'] == 'Блог Алексея Селезнёва':
        return T('Блог Алексея Селезнёва', 'Блог Олексія Селезньова', "Alexey Seleznev's blog")
    if a['src'] == 'Хабр':
        return T('Хабр', 'Хабр', 'Habr')
    return esc(a['src'])


def build_articles():
    arts = load('articles')
    for a in arts:
        a['skey'] = source_key(a)
    topic_counts = Counter(t for a in arts for t in a['topics'])
    src_counts = Counter(a['skey'] for a in arts)
    dots = {k: c for k, c, _ in SOURCES}
    years = sorted({a['y'] for a in arts}, reverse=True)

    def card(a, delay):
        main_icon = TOPICS[a['topics'][0]][0]
        via = ''
        if a['via'] == 'blog':
            via = f'<div class="absolute top-3 right-3 text-[10px] font-bold px-2 py-0.5 rounded backdrop-blur-md bg-purple-500/20 text-purple-200 border border-purple-500/30" title="Оригинал недоступен — ссылка ведёт на копию в блоге">{T("копия в блоге", "копія в блозі", "blog copy")}</div>'
        elif a['via'] == 'youtube':
            via = f'<div class="absolute top-3 right-3 text-[10px] font-bold px-2 py-0.5 rounded backdrop-blur-md bg-red-500/20 text-red-200 border border-red-500/30"><i class="fa-brands fa-youtube mr-1"></i>{T("плейлист", "плейлист", "playlist")}</div>'
        extra = f'<div class="absolute top-3 left-3 text-[10px] font-mono font-bold uppercase tracking-wider px-2.5 py-1 rounded-lg backdrop-blur-md bg-slate-950/80 border border-white/10 text-purple-300">{month_label(a["y"], a["m"])}</div>{via}'
        tags = ' '.join(f'<span class="px-2 py-0.5 rounded-md bg-white/5 border border-white/5 text-[11px] text-slate-400">{T(*TOPICS[t][1])}</span>' for t in a['topics'])
        search = f"{a['title']} {a['desc']} {a['src']}".lower()
        return f'''
                <a href="{esc(url(a['url']))}" target="_blank" rel="noopener" class="bento-glass group flex flex-col p-2 rounded-3xl" data-filter-item data-topic="{' '.join(a['topics'])}" data-source="{a['skey']}" data-search="{esc(search)}" data-aos="fade-up" data-aos-delay="{delay}">
                    <div class="bento-content flex flex-col h-full">
                    {cover(a['img'], main_icon, 'h-44', extra)}
                    <div class="px-3 pt-4 pb-3 flex flex-col flex-1">
                        <div class="text-xs text-slate-400 mb-2 flex items-center gap-2"><span class="w-1.5 h-1.5 rounded-full {dots[a['skey']]}"></span>{source_label(a)}</div>
                        <h3 class="font-bold text-[17px] leading-snug text-slate-100 group-hover:text-purple-300 transition-colors outfit-font line-clamp-3 mb-2">{esc(a['title'])}</h3>
                        <p class="text-sm text-slate-400 leading-relaxed line-clamp-3 flex-1">{esc(a['desc'])}</p>
                        <div class="mt-4 pt-3 border-t border-white/5 flex items-center justify-between gap-3">
                            <div class="flex flex-wrap gap-1.5">{tags}</div>
                            <i class="fa-solid fa-arrow-up-right-from-square text-xs text-slate-500 group-hover:text-purple-300 transition-colors shrink-0"></i>
                        </div>
                    </div>
                    </div>
                </a>'''

    groups = []
    for y in years:
        items = [a for a in arts if a['y'] == y]
        cards = ''.join(card(a, (i % 3) * 60) for i, a in enumerate(items))
        groups.append(f'''
        <div data-year-group class="mb-14">
            <div class="flex items-center gap-4 mb-6" data-aos="fade-right">
                <h3 class="text-4xl font-black text-white/90 outfit-font">{y}</h3>
                <div class="h-px flex-1 bg-gradient-to-r from-purple-500/40 to-transparent"></div>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">{cards}
            </div>
        </div>''')

    topic_btns = [filter_btn('topic', 'all', T('Все темы', 'Усі теми', 'All topics'), len(arts), 'fa-solid fa-layer-group', True)]
    for key, (icon, label) in TOPICS.items():
        if topic_counts[key]:
            topic_btns.append(filter_btn('topic', key, T(*label), topic_counts[key], icon))
    src_btns = [filter_btn('source', 'all', T('Все издания', 'Усі видання', 'All outlets'), len(arts), '', True)]
    for key, dot, label in SOURCES:
        src_btns.append(filter_btn('source', key, f'<span class="w-1.5 h-1.5 rounded-full {dot}"></span>{T(*label)}', src_counts[key]))

    outlets = len({a['src'] for a in arts})
    page = head('articles', 'Статьи | Алексей Селезнёв',
                f'{len(arts)} {plural_ru(len(arts), "статья", "статьи", "статей")} Алексея Селезнёва о языке R, Google BigQuery, Power BI, веб-аналитике, API рекламных систем и стоимости клика — Хабр, Netpeak Journal и другие издания.')
    page += nav('articles')
    page += hero('fa-solid fa-pen-nib', T('Публикации', 'Публікації', 'Publications'),
                 T('Статьи и <span class="text-gradient">туториалы</span>', 'Статті та <span class="text-gradient">туторіали</span>', 'Articles & <span class="text-gradient">Tutorials</span>'),
                 T('С 2015 года пишу о том, чем занимаюсь каждый день: язык R и автоматизация, Google BigQuery и Power BI, веб-аналитика, API рекламных систем и ежеквартальные исследования стоимости клика. Публикации выходили на Хабре, в Netpeak Journal и других изданиях; если оригинал больше недоступен, ссылка ведёт на копию в моём блоге.',
                   'З 2015 року пишу про те, чим займаюся щодня: мова R та автоматизація, Google BigQuery і Power BI, веб-аналітика, API рекламних систем і щоквартальні дослідження вартості кліку. Публікації виходили на Хабрі, у Netpeak Journal та інших виданнях; якщо оригінал більше недоступний, посилання веде на копію в моєму блозі. Статті написані російською мовою.',
                   'Since 2015 I have been writing about my daily work: R and automation, Google BigQuery and Power BI, web analytics, ad-platform APIs and quarterly cost-per-click research. The articles appeared on Habr, Netpeak Journal and other outlets; if an original is gone, the link points to a copy on my blog. Articles are written in Russian.'),
                 [(str(len(arts)), T('Статей', 'Статей', 'Articles')), (str(outlets), T('Изданий', 'Видань', 'Outlets')),
                  (str(min(years)), T('Первая статья', 'Перша стаття', 'First article')), (str(topic_counts['r']), T('Про язык R', 'Про мову R', 'About R'))], photo='articles')
    page += f'''
    <!-- CATALOG -->
    <section class="px-6 max-w-7xl mx-auto pb-16 relative z-10">
        <div class="bento-glass no-lift p-5 md:p-6 rounded-3xl mb-12 space-y-5" data-aos="fade-up">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 relative z-10">
                <p class="text-slate-400 text-sm">{T('Показано', 'Показано', 'Showing')}: <span data-filter-count class="font-mono text-white">{len(arts)}</span> / {len(arts)}</p>
                {search_box('Поиск по статьям…', 'Пошук за статтями…', 'Search articles…')}
            </div>
            <div class="flex flex-wrap gap-2 relative z-10">{''.join(topic_btns)}</div>
            <div class="flex flex-wrap gap-2 relative z-10">{''.join(src_btns)}</div>
        </div>
{''.join(groups)}
        {empty_state()}

        <a href="https://alexeyseleznev.wordpress.com/" target="_blank" rel="noopener" class="mt-4 bento-glass p-8 rounded-3xl flex flex-col md:flex-row items-center justify-between gap-8 group hover:border-purple-500/50 transition-all text-center md:text-left" data-aos="fade-up">
            <div class="bento-content flex flex-col md:flex-row items-center gap-6">
                <div class="w-16 h-16 bg-purple-500/20 rounded-full flex items-center justify-center text-purple-400 group-hover:bg-purple-500 group-hover:text-white transition-all text-2xl shrink-0"><i class="fa-solid fa-pen-nib"></i></div>
                <div>
                    <h3 class="text-2xl font-bold text-white outfit-font group-hover:text-purple-300 mb-1">{T('Личный блог', 'Особистий блог', 'Personal blog')}</h3>
                    <p class="text-slate-400 text-sm">{T('Агрегатор всех моих публикаций, анонсы докладов и заметки.', 'Агрегатор усіх моїх публікацій, анонси доповідей і нотатки.', 'An aggregator of all my publications, talk announcements and notes.')}</p>
                </div>
            </div>
            <div class="bento-content px-6 py-3 bg-white/5 border border-white/10 rounded-full font-bold text-sm text-white group-hover:bg-white group-hover:text-black transition-all whitespace-nowrap">alexeyseleznev.wordpress.com <i class="fa-solid fa-arrow-right ml-2"></i></div>
        </a>
    </section>
'''
    page += cta_block() + footer() + tail()
    write('articles', page)


# ---------------------------------------------------------------- интервью

KINDS = {
    'interview': ('fa-solid fa-comments', ('Интервью', "Інтерв'ю", 'Interview')),
    'survey': ('fa-solid fa-users', ('Экспертный опрос', 'Експертне опитування', 'Expert survey')),
    'comment': ('fa-solid fa-quote-left', ('Комментарий эксперта', 'Коментар експерта', 'Expert comment')),
}


def build_interviews():
    items = load('interviews')
    kinds = Counter(i['kind'] for i in items)
    years = sorted(ym(i['date'])[0] for i in items)

    def card(it, delay):
        y, m = ym(it['date'])
        icon, label = KINDS[it['kind']]
        outlet = T(esc(it['outlet']), esc(it['outlet']), esc(it.get('outletEn', it['outlet'])))
        via = ''
        if it.get('via') == 'blog':
            via = f'<div class="absolute top-4 right-4 text-[10px] font-bold px-2 py-0.5 rounded backdrop-blur-md bg-purple-500/20 text-purple-200 border border-purple-500/30">{T("копия в блоге", "копія в блозі", "blog copy")}</div>'
        extra = f'''<div class="absolute top-4 left-4 text-[10px] font-mono font-bold uppercase tracking-wider px-2.5 py-1 rounded-lg backdrop-blur-md bg-slate-950/80 border border-white/10 text-purple-300">{month_label(y, m)}</div>{via}
                        <div class="absolute bottom-4 left-4 flex items-center gap-2 text-sm font-bold text-white outfit-font"><span class="w-2 h-2 rounded-full bg-purple-400"></span>{outlet}</div>'''
        quote = ''
        if it.get('quote'):
            quote = f'''<blockquote class="relative mt-5 pl-5 border-l-2 border-purple-500/50 text-sm italic text-slate-300 leading-relaxed">
                            <i class="fa-solid fa-quote-left absolute -left-3 -top-2 text-purple-500/40 bg-[#0b1120] px-1"></i>
                            {tr(it['quote'])}
                        </blockquote>'''
        search = ' '.join([it['title'][l] for l in LANGS] + [it['outlet'], it['desc']['ru']]).lower()
        return f'''
            <a href="{esc(url(it['url']))}" target="_blank" rel="noopener" class="bento-glass group flex flex-col p-3 rounded-[2rem]" data-filter-item data-kind="{it['kind']}" data-search="{esc(search)}" data-aos="fade-up" data-aos-delay="{delay}">
                <div class="bento-content flex flex-col h-full">
                    {cover(it['img'], 'fa-regular fa-newspaper', 'h-52', extra)}
                    <div class="px-3 pt-5 pb-3 flex flex-col flex-1">
                        <div class="text-xs font-semibold text-purple-400 mb-2 flex items-center gap-2"><i class="{icon}"></i>{T(*label)}</div>
                        <h3 class="font-bold text-xl leading-snug text-slate-100 group-hover:text-purple-300 transition-colors outfit-font mb-3">{tr(it['title'])}</h3>
                        <p class="text-sm text-slate-400 leading-relaxed">{tr(it['desc'])}</p>
                        {quote}
                        <div class="mt-auto pt-5">
                            <div class="pt-3 border-t border-white/5 flex items-center justify-between text-xs text-slate-400 group-hover:text-purple-300 transition-colors">
                                <span class="font-semibold">{T('Читать полностью', 'Читати повністю', 'Read in full')}</span>
                                <i class="fa-solid fa-arrow-up-right-from-square text-xs"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </a>'''

    grid = ''.join(card(it, (i % 2) * 80) for i, it in enumerate(items))
    btns = [filter_btn('kind', 'all', T('Все', 'Усі', 'All'), len(items), 'fa-solid fa-layer-group', True)]
    for key, (icon, label) in KINDS.items():
        if kinds[key]:
            btns.append(filter_btn('kind', key, T(*label), kinds[key], icon))
    outlets = len({i['outlet'] for i in items})

    page = head('interviews', 'Интервью | Алексей Селезнёв',
                'Интервью, экспертные опросы и комментарии Алексея Селезнёва для vc.ru, SEOnews, AIN.UA, Лидзавода и других изданий — о языке R, веб-аналитике и рынке интернет-рекламы.')
    page += nav('interviews')
    page += hero('fa-regular fa-newspaper', T('В медиа', 'У медіа', 'In the media'),
                 T('Интервью и <span class="text-gradient">комментарии</span>', "Інтерв'ю та <span class=\"text-gradient\">коментарі</span>", 'Interviews & <span class="text-gradient">Comments</span>'),
                 T('Интервью, экспертные опросы и комментарии для профильных изданий: о языке R в маркетинге, профессии аналитика, сквозной аналитике, трендах веб-аналитики и изменениях на рекламном рынке Украины.',
                   "Інтерв'ю, експертні опитування та коментарі для профільних видань: про мову R у маркетингу, професію аналітика, наскрізну аналітику, тренди веб-аналітики та зміни на рекламному ринку України.",
                   'Interviews, expert surveys and comments for industry media: on R in marketing, the analyst profession, end-to-end analytics, web analytics trends and changes in Ukraine\'s advertising market.'),
                 [(str(len(items)), T('Публикаций', 'Публікацій', 'Publications')), (str(outlets), T('Изданий', 'Видань', 'Outlets')),
                  (str(kinds['interview']), T('Интервью', "Інтерв'ю", 'Interviews')), (f'{years[0]}–{years[-1]}', T('Годы', 'Роки', 'Years'))], photo='interviews')
    page += f'''
    <!-- CATALOG -->
    <section class="px-6 max-w-7xl mx-auto pb-16 relative z-10">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-10" data-aos="fade-up">
            <div class="flex flex-wrap gap-2">{''.join(btns)}</div>
            {search_box('Поиск…', 'Пошук…', 'Search…')}
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">{grid}
        </div>
        {empty_state()}
    </section>
'''
    page += cta_block() + footer() + tail()
    write('interviews', page)


# ---------------------------------------------------------------- видеоуроки

VIDEO_TOPICS = {
    'api': ('fa-solid fa-plug', ('API и пакеты', 'API та пакети', 'APIs & packages')),
    'data': ('fa-solid fa-table-cells', ('Работа с данными', 'Робота з даними', 'Working with data')),
    'deploy': ('fa-solid fa-gears', ('Автоматизация и деплой', 'Автоматизація та деплой', 'Automation & deploy')),
    'basics': ('fa-solid fa-screwdriver-wrench', ('Основы R', 'Основи R', 'R essentials')),
    'ai': ('fa-solid fa-wand-magic-sparkles', ('AI', 'AI', 'AI')),
}


def thumb(yt):
    return f'https://i.ytimg.com/vi/{yt}/hqdefault.jpg'


def build_videos():
    data = load('videos')
    series, lessons = data['series'], data['lessons']
    n_eps = sum(len(s['episodes']) for s in series)
    total = n_eps + len(lessons)
    years = sorted([ym(l['date'])[0] for l in lessons])
    topic_counts = Counter(l['topic'] for l in lessons)

    series_cards = []
    for i, s in enumerate(series):
        first = s['episodes'][0]['yt']
        eps = '\n'.join(f'''                            <button type="button" data-video="{e['yt']}" class="w-full flex items-center gap-3 p-2 rounded-xl hover:bg-white/5 border border-transparent hover:border-white/10 transition-all text-left group/ep">
                                <div class="relative w-24 h-14 rounded-lg overflow-hidden shrink-0 bg-slate-900">
                                    <img src="{thumb(e['yt'])}" alt="" loading="lazy" class="w-full h-full object-cover">
                                    <div class="absolute inset-0 flex items-center justify-center bg-slate-950/30 group-hover/ep:bg-slate-950/10 transition-colors"><i class="fa-solid fa-play text-white text-xs drop-shadow"></i></div>
                                </div>
                                <div class="min-w-0 flex-1">
                                    <div class="text-[11px] font-mono font-bold text-purple-400 mb-0.5">#{n}</div>
                                    <div class="text-sm font-semibold text-slate-200 group-hover/ep:text-white leading-snug line-clamp-2" data-video-title>{tr(e['title'])}</div>
                                </div>
                            </button>''' for n, e in enumerate(s['episodes'], 1))
        series_cards.append(f'''
            <article id="{s['id']}" class="bento-glass no-lift rounded-[2rem] p-3 flex flex-col scroll-mt-24" data-aos="fade-up" data-aos-delay="{(i % 2) * 80}">
                <div class="bento-content flex flex-col h-full">
                    <button type="button" data-video="{first}" class="block text-left group">
                        <div class="cover h-56 rounded-[1.5rem]">
                            <div class="cover-fallback"><i class="{s['icon']} text-5xl"></i></div>
                            <img src="{thumb(first)}" alt="" loading="lazy" onerror="this.remove()">
                            <div class="absolute inset-0 bg-gradient-to-t from-slate-950/90 via-slate-950/20 to-transparent"></div>
                            <div class="absolute top-4 left-4 text-[11px] font-mono font-bold px-2.5 py-1 rounded-lg backdrop-blur-md bg-slate-950/80 border border-white/10 text-purple-300 flex items-center gap-2"><i class="{s['icon']}"></i>{esc(s['pkg'])}</div>
                            <div class="absolute top-4 right-4 text-[11px] font-bold px-2.5 py-1 rounded-lg backdrop-blur-md bg-red-500/20 border border-red-500/30 text-red-200">{len(s['episodes'])} {T('видео', 'відео', 'videos')}</div>
                            <div class="absolute inset-0 flex items-center justify-center"><div class="w-16 h-16 rounded-full bg-red-600/90 text-white flex items-center justify-center shadow-2xl group-hover:scale-110 group-hover:bg-red-500 transition-all duration-300 group-hover:shadow-[0_0_25px_rgba(239,68,68,0.7)]"><i class="fa-solid fa-play ml-1 text-xl"></i></div></div>
                            <span class="hidden" data-video-title>{tr(s['episodes'][0]['title'])}</span>
                        </div>
                    </button>
                    <div class="px-3 pt-5 flex flex-col flex-1">
                        <div class="text-xs font-mono font-bold uppercase tracking-widest text-slate-500 mb-2">{T('Серия', 'Серія', 'Series')} · {s['period']}</div>
                        <h3 class="text-2xl font-bold text-white outfit-font leading-snug mb-2">{tr(s['title'])}</h3>
                        <p class="text-sm text-slate-400 leading-relaxed mb-5">{tr(s['desc'])}</p>
                        <div class="space-y-1 max-h-80 overflow-y-auto pr-1 -mx-1 mb-4">
{eps}
                        </div>
                        <div class="mt-auto pt-4 pb-2 border-t border-white/5">
                            <a href="{esc(s['playlist'])}" target="_blank" rel="noopener" class="inline-flex items-center gap-2 text-sm font-semibold text-slate-300 hover:text-white transition-colors"><i class="fa-brands fa-youtube text-red-500"></i>{T('Весь плейлист на YouTube', 'Увесь плейлист на YouTube', 'Full playlist on YouTube')} <i class="fa-solid fa-arrow-up-right-from-square text-xs opacity-60"></i></a>
                        </div>
                    </div>
                </div>
            </article>''')

    def lesson_card(l, delay):
        y, m = ym(l['date'])
        icon, label = VIDEO_TOPICS[l['topic']]
        extra = f'''<div class="absolute top-3 left-3 text-[10px] font-mono font-bold uppercase tracking-wider px-2.5 py-1 rounded-lg backdrop-blur-md bg-slate-950/80 border border-white/10 text-purple-300">{month_label(y, m)}</div>
                        <div class="absolute inset-0 flex items-center justify-center"><div class="w-14 h-14 rounded-full bg-red-600/90 text-white flex items-center justify-center shadow-2xl backdrop-blur-sm group-hover:scale-110 group-hover:bg-red-500 transition-all duration-300 group-hover:shadow-[0_0_25px_rgba(239,68,68,0.7)]"><i class="fa-solid fa-play ml-1 text-lg"></i></div></div>'''
        search = ' '.join([l['title'][x] for x in LANGS] + [l['desc']['ru']]).lower()
        return f'''
            <a href="https://www.youtube.com/watch?v={l['yt']}" target="_blank" rel="noopener" data-video="{l['yt']}" class="bento-glass group flex flex-col p-3 rounded-3xl cursor-pointer" data-filter-item data-topic="{l['topic']}" data-search="{esc(search)}" data-aos="fade-up" data-aos-delay="{delay}">
                <div class="bento-content flex flex-col h-full">
                    {cover(thumb(l['yt']), icon, 'h-48', extra)}
                    <div class="px-2 pt-4 pb-1 flex flex-col flex-1">
                        <div class="text-xs font-semibold text-purple-400 mb-2 flex items-center gap-2"><i class="{icon}"></i>{T(*label)}</div>
                        <h3 class="font-bold text-lg leading-snug text-slate-100 group-hover:text-white transition-colors outfit-font mb-3" data-video-title>{tr(l['title'])}</h3>
                        <p class="text-sm text-slate-400 leading-relaxed flex-1">{tr(l['desc'])}</p>
                        <div class="mt-4 pt-3 border-t border-white/5 flex items-center justify-between text-xs text-slate-400 group-hover:text-purple-300 transition-colors">
                            <span class="flex items-center gap-1.5 font-semibold"><i class="fa-brands fa-youtube text-red-500 text-sm"></i>{T('Смотреть', 'Дивитися', 'Watch')}</span>
                            <i class="fa-solid fa-arrow-right text-xs opacity-60 group-hover:opacity-100 group-hover:translate-x-1 transition-all"></i>
                        </div>
                    </div>
                </div>
            </a>'''

    grid = ''.join(lesson_card(l, (i % 3) * 60) for i, l in enumerate(lessons))
    btns = [filter_btn('topic', 'all', T('Все', 'Усі', 'All'), len(lessons), 'fa-solid fa-layer-group', True)]
    for key, (icon, label) in VIDEO_TOPICS.items():
        if topic_counts[key]:
            btns.append(filter_btn('topic', key, T(*label), topic_counts[key], icon))

    page = head('videos', 'Видеоуроки по R | Алексей Селезнёв',
                f'{total} {plural_ru(total, "бесплатный видеоурок", "бесплатных видеоурока", "бесплатных видеоуроков")} Алексея Селезнёва по языку R: серии по пакетам для работы с API рекламных систем, работа с данными, автоматизация, деплой и AI.',
                image=thumb(series[0]['episodes'][0]['yt']))
    page += nav('videos')
    page += hero('fa-solid fa-circle-play', T('YouTube · R4marketing', 'YouTube · R4marketing', 'YouTube · R4marketing'),
                 T('Видео<span class="text-gradient">уроки</span>', 'Відео<span class="text-gradient">уроки</span>', 'Video <span class="text-gradient">Lessons</span>'),
                 T('Бесплатные видеоуроки с YouTube-канала R4marketing: серии по моим R-пакетам для работы с API рекламных и аналитических систем, а также отдельные уроки по работе с данными, автоматизации, деплою и AI. Уроки, которые вошли в полноценные курсы, собраны на <a href="../courses/" class="text-purple-300 underline underline-offset-4 hover:text-white">странице курсов</a>.',
                   'Безкоштовні відеоуроки з YouTube-каналу R4marketing: серії з моїх R-пакетів для роботи з API рекламних і аналітичних систем, а також окремі уроки з роботи з даними, автоматизації, деплою та AI. Уроки, що увійшли до повноцінних курсів, зібрані на <a href="../courses/" class="text-purple-300 underline underline-offset-4 hover:text-white">сторінці курсів</a>.',
                   'Free video lessons from the R4marketing YouTube channel: series on my R packages for ad and analytics APIs, plus standalone lessons on data, automation, deployment and AI. Lessons that became full courses live on the <a href="../courses/" class="text-purple-300 underline underline-offset-4 hover:text-white">courses page</a>.'),
                 [(str(total), T('Видео', 'Відео', 'Videos')), (str(len(series)), T('Серий по пакетам', 'Серій за пакетами', 'Package series')),
                  (str(len(lessons)), T('Отдельных уроков', 'Окремих уроків', 'Standalone lessons')), (f'{years[0]}–{years[-1]}', T('Годы', 'Роки', 'Years'))], photo='videos')
    page += f'''
    <!-- SERIES -->
    <section class="px-6 max-w-7xl mx-auto pb-20 relative z-10">
        <h2 class="text-3xl font-extrabold mb-3 flex items-center gap-4 outfit-font" data-aos="fade-up">
            <div class="w-12 h-12 bg-purple-500/20 flex items-center justify-center rounded-2xl border border-purple-500/30"><i class="fa-solid fa-box-open text-purple-500 text-xl"></i></div>
            {T('Серии по R-пакетам', 'Серії з R-пакетів', 'R package series')}
        </h2>
        <p class="text-slate-400 mb-10 max-w-3xl" data-aos="fade-up">{T('Пошаговые плейлисты по пакетам, которые я разработал: от авторизации до готовых сценариев автоматизации.', 'Покрокові плейлисти з пакетів, які я розробив: від авторизації до готових сценаріїв автоматизації.', 'Step-by-step playlists for the packages I built: from authorization to ready-made automation scenarios.')}</p>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">{''.join(series_cards)}
        </div>
    </section>

    <!-- LESSONS -->
    <section class="px-6 max-w-7xl mx-auto pb-16 relative z-10">
        <div class="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-8" data-aos="fade-up">
            <div>
                <h2 class="text-3xl font-extrabold flex items-center gap-4 outfit-font mb-2">
                    <div class="w-12 h-12 bg-blue-500/20 flex items-center justify-center rounded-2xl border border-blue-500/30"><i class="fa-solid fa-film text-blue-400 text-xl"></i></div>
                    {T('Отдельные уроки', 'Окремі уроки', 'Standalone lessons')}
                </h2>
                <p class="text-slate-400 text-sm">{T('Показано', 'Показано', 'Showing')}: <span data-filter-count class="font-mono text-white">{len(lessons)}</span></p>
            </div>
            {search_box('Поиск по урокам…', 'Пошук за уроками…', 'Search lessons…')}
        </div>
        <div class="flex flex-wrap items-center gap-3 mb-8" data-aos="fade-up">{''.join(btns)}</div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">{grid}
        </div>
        {empty_state()}
    </section>
'''
    page += cta_block() + footer() + tail(modal=True)
    write('videos', page)


# ---------------------------------------------------------------- open source

PKG_CATS = {
    'ads': ('fa-solid fa-bullhorn', ('Рекламные платформы', 'Рекламні платформи', 'Ad platforms')),
    'analytics': ('fa-solid fa-chart-line', ('Аналитика', 'Аналітика', 'Analytics')),
    'crm': ('fa-solid fa-address-card', ('CRM и сервисы', 'CRM та сервіси', 'CRM & services')),
    'utils': ('fa-solid fa-screwdriver-wrench', ('Утилиты', 'Утиліти', 'Utilities')),
}


def fmt_num(n):
    if n >= 1000:
        return f'{n / 1000:.1f}'.replace('.0', '') + 'k'
    return str(n)


def update_package_stats(pkgs):
    """Обновляет снимок скачиваний с CRAN и звёзд GitHub. Без сети остаются прежние значения."""
    import datetime
    import urllib.request
    path = DATA / 'package_stats.json'
    stats = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'packages': {}}

    # Токен GitHub (переменная GITHUB_TOKEN или gh CLI) снимает лимит 60 анонимных запросов в час
    import os
    import subprocess
    token = os.environ.get('GITHUB_TOKEN', '')
    if not token:
        try:
            token = subprocess.run(['gh', 'auth', 'token'], capture_output=True, text=True, timeout=10).stdout.strip()
        except Exception:
            token = ''

    def get(u):
        headers = {'User-Agent': 'alexey-seleznev.pro build'}
        if token and 'api.github.com' in u:
            headers['Authorization'] = f'Bearer {token}'
        req = urllib.request.Request(u, headers=headers)
        return json.loads(urllib.request.urlopen(req, timeout=30).read().decode('utf-8'))

    cran = ','.join(p['name'] for p in pkgs if p['cran'])
    try:
        total = {x['package']: x['downloads'] for x in get(f'https://cranlogs.r-pkg.org/downloads/total/2015-01-01:last-day/{cran}')}
        month = {x['package']: x['downloads'] for x in get(f'https://cranlogs.r-pkg.org/downloads/total/last-month/{cran}')}
        for name in total:
            s = stats['packages'].setdefault(name, {})
            s['downloads'], s['month'] = total[name], month.get(name, 0)
        stats['date'] = datetime.date.today().isoformat()
    except Exception as e:
        print('  cranlogs недоступен, оставляю сохранённые значения:', e)
    for p in pkgs:
        try:
            stats['packages'].setdefault(p['name'], {})['stars'] = get(f'https://api.github.com/repos/selesnow/{p["name"]}')['stargazers_count']
        except Exception as e:
            print(f'  GitHub: не удалось обновить звёзды {p["name"]}:', e)
    names = {p['name'] for p in pkgs}
    stats['packages'] = {k: v for k, v in stats['packages'].items() if k in names}
    path.write_text(json.dumps(stats, ensure_ascii=False, indent=1), encoding='utf-8')

    # Публичная копия для страниц сайта: лендинг и /opensource/ читают её со своего домена
    public = {
        'updated': stats.get('date', ''),
        'total_downloads': sum(v.get('downloads', 0) for v in stats['packages'].values()),
        'packages': stats['packages'],
    }
    (ROOT / 'assets' / 'stats.json').write_text(json.dumps(public, ensure_ascii=False, indent=1), encoding='utf-8')
    return stats


OPENSOURCE_JS = '''
    <script>
    // Счётчики пакетов. Основной источник: assets/stats.json на этом же домене,
    // его раз в сутки обновляет GitHub Actions (cranlogs + GitHub API).
    // Если файл недоступен, идём в cranlogs через CORS-прокси; если не вышло и это, остаются значения из сборки.
    (function () {
        function fmt(n) {
            if (n >= 1000000) return (n / 1000000).toFixed(1).replace('.0', '') + 'M';
            if (n >= 1000) return (n / 1000).toFixed(1).replace('.0', '') + 'k';
            return String(n);
        }
        const cards = Array.from(document.querySelectorAll('[data-pkg]'));
        const set = (name, cls, value) => document.querySelectorAll(`[data-pkg="${name}"] ${cls}`).forEach(el => { el.textContent = fmt(value); });
        const setTotal = sum => { const t = document.getElementById('total-downloads'); if (t && sum > 0) t.textContent = Math.floor(sum / 1000) + 'k+'; };

        function fromStatsFile(d) {
            Object.entries(d.packages || {}).forEach(([name, s]) => {
                if (s.downloads != null) set(name, '.js-dl-total', s.downloads);
                if (s.month != null) set(name, '.js-dl-month', s.month);
                if (s.stars != null) set(name, '.js-stars', s.stars);
            });
            setTotal(d.total_downloads);
        }

        function fromCranlogs() {
            const proxied = url => fetch('https://api.allorigins.win/raw?url=' + encodeURIComponent(url)).then(r => { if (!r.ok) throw r; return r.json(); });
            const names = cards.filter(c => c.dataset.cran === '1').map(c => c.dataset.pkg).join(',');
            Promise.all([
                proxied(`https://cranlogs.r-pkg.org/downloads/total/2015-01-01:last-day/${names}`),
                proxied(`https://cranlogs.r-pkg.org/downloads/total/last-month/${names}`)
            ]).then(([total, month]) => {
                let sum = 0;
                total.forEach(x => { sum += x.downloads; set(x.package, '.js-dl-total', x.downloads); });
                month.forEach(x => set(x.package, '.js-dl-month', x.downloads));
                setTotal(sum);
            }).catch(() => {});
        }

        fetch('../assets/stats.json', { cache: 'no-cache' })
            .then(r => { if (!r.ok) throw r; return r.json(); })
            .then(fromStatsFile)
            .catch(fromCranlogs);
    })();
    </script>
'''


def build_opensource():
    pkgs = load('packages')
    stats = update_package_stats(pkgs)['packages']
    for p in pkgs:
        s = stats.get(p['name'], {})
        p['dl'], p['month'], p['stars'] = s.get('downloads', 0), s.get('month', 0), s.get('stars', 0)
    total_dl = sum(p['dl'] for p in pkgs)
    on_cran = sum(1 for p in pkgs if p['cran'])
    active = sorted([p for p in pkgs if not p.get('archived')], key=lambda p: (-p['cran'], -p['dl']))
    archived = sorted([p for p in pkgs if p.get('archived')], key=lambda p: -p['dl'])
    cat_counts = Counter(p['cat'] for p in pkgs)

    def link_btn(href, icon, label, accent=False):
        cls = ('bg-purple-500/15 border-purple-500/40 text-purple-200 hover:bg-purple-500 hover:text-white'
               if accent else 'bg-slate-900/70 border-white/10 text-slate-300 hover:text-white hover:border-white/20 hover:bg-slate-800')
        return f'<a href="{esc(href)}" target="_blank" rel="noopener" class="px-3 py-2 rounded-lg border text-xs font-semibold transition-all flex items-center gap-1.5 {cls}"><i class="{icon}"></i>{label}</a>'

    def card(p, delay):
        name = p['name']
        is_arch = p.get('archived')
        logo_path = ROOT / 'assets' / 'logos' / f'{name}.png'
        if logo_path.exists():
            logo = f'<img src="../assets/logos/{name}.png" alt="{name} logo" loading="lazy" class="w-[72px] h-[84px] object-contain drop-shadow-[0_8px_20px_rgba(0,0,0,0.45)] group-hover:scale-105 group-hover:-rotate-3 transition-transform duration-500{" grayscale-[35%]" if is_arch else ""}">'
        else:
            logo = f'''<div class="hex relative w-[72px] h-[84px] bg-gradient-to-br from-purple-500/40 via-slate-800 to-blue-500/30 flex flex-col items-center justify-center group-hover:scale-105 group-hover:-rotate-3 transition-transform duration-500">
                                <div class="hex absolute inset-[3px] bg-slate-900/95"></div>
                                <i class="{p['icon']} text-2xl text-purple-200 relative"></i>
                                <span class="text-[9px] font-bold text-slate-300 relative mt-1 outfit-font">{esc(name)}</span>
                            </div>'''
        badges = []
        if is_arch:
            badges.append(f'<span class="px-2 py-0.5 rounded-md text-[10px] font-bold uppercase tracking-wider bg-amber-500/15 text-amber-300 border border-amber-500/30 flex items-center gap-1"><i class="fa-solid fa-box-archive"></i>{T("Архив", "Архів", "Archived")}</span>')
        if p['cran'] and not p.get('cranRemoved'):
            badges.append('<span class="px-2 py-0.5 rounded-md text-[10px] font-bold uppercase tracking-wider bg-blue-500/15 text-blue-300 border border-blue-500/30">CRAN</span>')
        elif p.get('cranRemoved'):
            badges.append(f'<span class="px-2 py-0.5 rounded-md text-[10px] font-bold uppercase tracking-wider bg-slate-500/15 text-slate-400 border border-slate-500/30">{T("Удалён с CRAN", "Видалений з CRAN", "Removed from CRAN")}</span>')
        else:
            badges.append('<span class="px-2 py-0.5 rounded-md text-[10px] font-bold uppercase tracking-wider bg-slate-500/15 text-slate-300 border border-white/10">GitHub</span>')
        award = ''
        if p.get('award'):
            award = f'<div class="mb-4 inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-yellow-500/10 border border-yellow-500/25 text-yellow-300 text-xs font-semibold"><i class="fa-solid fa-trophy"></i>{tr(p["award"])}</div>'
        features = '\n'.join(f'<li class="flex items-start gap-2.5 text-sm text-slate-300"><i class="fa-solid fa-check text-purple-400 text-[10px] mt-1.5"></i>{T(esc(p["features"]["ru"][i]), esc(p["features"]["ua"][i]), esc(p["features"]["en"][i]))}</li>'
                             for i in range(len(p['features']['ru'])))
        if p['cran']:
            dl = f'''<div title="CRAN" class="flex items-center gap-2"><i class="fa-solid fa-download text-blue-400"></i><span class="js-dl-total font-bold text-white">{fmt_num(p['dl'])}</span></div>
                            <div title="{esc('last 30 days')}" class="flex items-center gap-1.5 text-slate-500"><span class="js-dl-month font-semibold text-slate-300">{fmt_num(p['month'])}</span>/{T('мес', 'міс', 'mo')}</div>'''
        else:
            dl = f'<div class="flex items-center gap-2 text-slate-500"><i class="fa-brands fa-github"></i>{T("только GitHub", "лише GitHub", "GitHub only")}</div>'
        links = [link_btn(f'https://github.com/selesnow/{name}', 'fa-brands fa-github', 'GitHub', accent=True)]
        if p['cran']:
            links.append(link_btn(f'https://cran.r-project.org/package={name}', 'fa-brands fa-r-project', 'CRAN'))
        if p.get('docs'):
            links.append(link_btn(p['docs'], 'fa-solid fa-book', T('Документация', 'Документація', 'Docs')))
        if p.get('video'):
            v = p['video']
            label = {'playlist': T(f'Плейлист · {v.get("count", "")}', f'Плейлист · {v.get("count", "")}', f'Playlist · {v.get("count", "")}'),
                     'video': T('Видеоурок', 'Відеоурок', 'Video lesson'),
                     'webinar': T('Вебинар', 'Вебінар', 'Webinar')}[v['kind']]
            links.append(link_btn(v['url'], 'fa-brands fa-youtube text-red-500', label))
        if p.get('article'):
            links.append(link_btn(p['article'], 'fa-solid fa-newspaper', T('Статья', 'Стаття', 'Article')))
        search = ' '.join([name, p['tagline']['ru'], p['tagline']['en'], p['desc']['ru'], p['desc']['en']]).lower()
        return f'''
            <article class="bento-glass group flex flex-col p-6 rounded-3xl{' opacity-90' if is_arch else ''}" data-filter-item data-cat="{p['cat']}" data-search="{esc(search)}" data-pkg="{name}" data-cran="{1 if p['cran'] else 0}" data-aos="fade-up" data-aos-delay="{delay}">
                <div class="bento-content flex flex-col h-full">
                    <div class="flex items-start gap-5 mb-5">
                        <div class="relative shrink-0">{logo}</div>
                        <div class="min-w-0 flex-1 pt-1">
                            <div class="flex flex-wrap items-center gap-1.5 mb-2">{''.join(badges)}</div>
                            <h3 class="text-2xl font-extrabold text-white outfit-font group-hover:text-purple-300 transition-colors break-words">{esc(name)}</h3>
                            <p class="text-sm text-slate-400 font-medium">{tr(p['tagline'])}</p>
                        </div>
                    </div>
                    {award}
                    <p class="text-sm text-slate-300 leading-relaxed font-light mb-4">{tr(p['desc'])}</p>
                    <ul class="space-y-1.5 mb-5">
{features}
                    </ul>
                    <div class="mt-auto">
                        <div class="flex flex-wrap items-center gap-x-5 gap-y-2 text-xs font-mono bg-slate-900/50 p-3 rounded-xl border border-white/5 mb-4">
                            <div title="GitHub stars" class="flex items-center gap-2"><i class="fa-solid fa-star text-yellow-500"></i><span class="js-stars font-bold text-white">{p['stars']}</span></div>
                            {dl}
                            <div class="flex items-center gap-1.5 text-slate-500 ml-auto"><i class="fa-regular fa-calendar"></i>{p['since']}</div>
                        </div>
                        <div class="flex flex-wrap gap-2">{''.join(links)}</div>
                    </div>
                </div>
            </article>'''

    active_grid = ''.join(card(p, (i % 3) * 60) for i, p in enumerate(active))
    arch_grid = ''.join(card(p, (i % 2) * 60) for i, p in enumerate(archived))
    btns = [filter_btn('cat', 'all', T('Все', 'Усі', 'All'), len(pkgs), 'fa-solid fa-layer-group', True)]
    for key, (icon, label) in PKG_CATS.items():
        btns.append(filter_btn('cat', key, T(*label), cat_counts[key], icon))
    stamp = ''
    if stats:
        import datetime
        d = json.loads((DATA / 'package_stats.json').read_text(encoding='utf-8')).get('date', '')
        if d:
            y, m, dd = map(int, d.split('-'))
            stamp = T(f'Счётчики скачиваний с CRAN (cranlogs) и звёзды GitHub обновляются автоматически; сохранённый снимок — {dd}.{m:02d}.{y}.',
                      f'Лічильники завантажень з CRAN (cranlogs) і зірки GitHub оновлюються автоматично; збережений знімок — {dd}.{m:02d}.{y}.',
                      f'CRAN download counts (cranlogs) and GitHub stars update automatically; saved snapshot from {dd}.{m:02d}.{y}.')

    services = load('services')
    svc_cards = []
    for i, sv in enumerate(services):
        if sv.get('img'):
            visual = f'''<div class="cover h-56 md:h-64 rounded-2xl border border-white/10">
                        <div class="cover-fallback"><i class="{sv['icon']} text-5xl"></i></div>
                        <img src="{sv['img']}" alt="{esc(sv['name'])}" loading="lazy" style="object-position: top left" onerror="this.remove()">
                        <div class="absolute inset-0 bg-gradient-to-t from-slate-950/70 via-transparent to-transparent"></div>
                    </div>'''
        else:
            cmds = ''.join(f'<span class="px-2.5 py-1 rounded-lg bg-blue-500/10 border border-blue-500/25 text-blue-200 text-xs font-mono">{esc(c)}</span>' for c in sv.get('commands', []))
            visual = f'''<div class="h-56 md:h-64 rounded-2xl border border-white/10 relative overflow-hidden flex flex-col justify-end p-5" style="background: radial-gradient(circle at 80% 20%, rgba(59,130,246,0.35), transparent 55%), radial-gradient(circle at 10% 90%, rgba(168,85,247,0.25), transparent 50%), #0b1120;">
                        <i class="{sv['icon']} absolute -right-6 -top-6 text-[180px] text-blue-400/10"></i>
                        <div class="relative flex items-center gap-3 mb-4">
                            <div class="w-12 h-12 rounded-2xl bg-blue-500/20 border border-blue-500/30 flex items-center justify-center text-blue-300 text-2xl"><i class="{sv['icon']}"></i></div>
                            <div class="text-sm text-slate-300 font-semibold">{T('Команды бота', 'Команди бота', 'Bot commands')}</div>
                        </div>
                        <div class="relative flex flex-wrap gap-2">{cmds}</div>
                    </div>'''
        feats = '\n'.join(f'<li class="flex items-start gap-2.5 text-sm text-slate-300"><i class="fa-solid fa-check text-purple-400 text-[10px] mt-1.5"></i>{T(esc(sv["features"]["ru"][k]), esc(sv["features"]["ua"][k]), esc(sv["features"]["en"][k]))}</li>' for k in range(len(sv['features']['ru'])))
        stack = ''.join(f'<span class="px-2 py-0.5 rounded-md bg-white/5 border border-white/10 text-[11px] text-slate-400 font-mono">{esc(t)}</span>' for t in sv['stack'])
        svc_cards.append(f'''
            <article class="bento-glass no-lift rounded-[2rem] p-4 flex flex-col" data-aos="fade-up" data-aos-delay="{i * 80}">
                <div class="bento-content flex flex-col h-full">
                    {visual}
                    <div class="px-2 pt-5 flex flex-col flex-1">
                        <div class="flex items-center gap-2 text-xs font-semibold text-purple-400 mb-2"><i class="{sv['icon']}"></i>{tr(sv['tagline'])}</div>
                        <h3 class="text-2xl font-extrabold text-white outfit-font mb-3">{esc(sv['name'])}</h3>
                        <p class="text-sm text-slate-300 leading-relaxed font-light mb-4">{tr(sv['desc'])}</p>
                        <ul class="space-y-1.5 mb-5">
{feats}
                        </ul>
                        <div class="mt-auto pt-4 border-t border-white/5 flex flex-wrap items-center justify-between gap-3">
                            <div class="flex flex-wrap gap-1.5">{stack}</div>
                            {link_btn(f"https://github.com/selesnow/{sv['repo']}", 'fa-brands fa-github', 'GitHub', accent=True)}
                        </div>
                    </div>
                </div>
            </article>''')
    services_html = f'''
        <div class="mb-16">
            <div class="flex items-center gap-4 mb-3" data-aos="fade-right">
                <h2 class="text-3xl font-extrabold outfit-font flex items-center gap-3"><i class="fa-solid fa-cubes text-purple-400 text-2xl"></i>{T('Сервисы и приложения', 'Сервіси та застосунки', 'Services & apps')}</h2>
                <div class="h-px flex-1 bg-gradient-to-r from-purple-500/30 to-transparent"></div>
            </div>
            <p class="text-slate-400 mb-8 max-w-3xl" data-aos="fade-up">{T('Внутренние инструменты отдела аналитики, написанные на R: система мониторинга и управления сервером, на котором работают сотни скриптов.', 'Внутрішні інструменти відділу аналітики, написані на R: система моніторингу та керування сервером, на якому працюють сотні скриптів.', 'Internal analytics-team tools written in R: a monitoring and control system for a server that runs hundreds of scripts.')}</p>
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">{''.join(svc_cards)}
            </div>
        </div>'''

    os_desc = f'{len(pkgs)} open source {plural_ru(len(pkgs), "R-пакет", "R-пакета", "R-пакетов")} Алексея Селезнёва для работы с API Google Ads, Facebook, TikTok, LinkedIn, Apple Ads, YouTube, TGStat, AppsFlyer и других сервисов. Более {total_dl // 1000}k скачиваний с CRAN.'
    page = head('opensource', 'Open Source R-пакеты | Алексей Селезнёв', os_desc,
                jsonld=page_jsonld('opensource', 'Open Source R-пакеты', os_desc, package_items(pkgs)))
    page += nav('opensource')
    page += hero('fa-solid fa-code-branch', 'Open Source',
                 T('R-<span class="text-gradient">пакеты</span>', 'R-<span class="text-gradient">пакети</span>', 'R <span class="text-gradient">Packages</span>'),
                 T('С 2016 года разрабатываю пакеты на языке R, которые упрощают сбор данных из рекламных, аналитических и CRM-платформ. С ними специалисты без глубоких навыков программирования автоматизируют отчётность и строят маркетинговую аналитику. Большинство пакетов опубликованы на CRAN, у многих есть документация и видеоуроки.',
                   'З 2016 року розробляю пакети мовою R, які спрощують збір даних з рекламних, аналітичних і CRM-платформ. З ними фахівці без глибоких навичок програмування автоматизують звітність і будують маркетингову аналітику. Більшість пакетів опубліковані на CRAN, у багатьох є документація та відеоуроки.',
                   'Since 2016 I have been building R packages that simplify collecting data from ad, analytics and CRM platforms, so specialists without deep coding skills can automate reporting and build marketing analytics. Most are published on CRAN, and many come with docs and video lessons.'),
                 [(str(len(pkgs)), T('R-пакет', 'R-пакет', 'R packages')), (str(on_cran), T('Опубликованы на CRAN', 'Опубліковані на CRAN', 'Published on CRAN')),
                  (f'<span id="total-downloads">{total_dl // 1000}k+</span>', T('Скачиваний с CRAN', 'Завантажень з CRAN', 'CRAN downloads')),
                  ('2016', T('Первый пакет', 'Перший пакет', 'First package'))], photo='opensource')
    page += f'''
    <!-- PACKAGES -->
    <section class="px-6 max-w-7xl mx-auto pb-10 relative z-10">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4" data-aos="fade-up">
            <div class="flex flex-wrap gap-2">{''.join(btns)}</div>
            {search_box('Поиск по пакетам…', 'Пошук за пакетами…', 'Search packages…')}
        </div>
        <p class="text-xs text-slate-500 mb-10 flex items-center gap-2" data-aos="fade-up"><i class="fa-solid fa-circle-info"></i>{stamp}</p>

        <div data-year-group class="mb-16">
            <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">{active_grid}
            </div>
        </div>

{services_html}
        <div data-year-group class="mb-10">
            <div class="flex items-center gap-4 mb-6" data-aos="fade-right">
                <h2 class="text-3xl font-extrabold outfit-font flex items-center gap-3"><i class="fa-solid fa-box-archive text-amber-400/80 text-2xl"></i>{T('Архивные пакеты', 'Архівні пакети', 'Archived packages')}</h2>
                <div class="h-px flex-1 bg-gradient-to-r from-amber-500/30 to-transparent"></div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">{arch_grid}
            </div>
        </div>
        {empty_state()}
    </section>
'''
    page += cta_block() + footer() + tail().replace('    <script src="../assets/site.js"></script>', '    <script src="../assets/site.js"></script>' + OPENSOURCE_JS)
    write('opensource', page)


# ---------------------------------------------------------------- 404

PAGE_BLURBS = {
    'opensource': ('Open source R-пакеты для API рекламных, аналитических и CRM-платформ', 'Open source R-пакети для API рекламних, аналітичних і CRM-платформ', 'Open source R packages for ad, analytics and CRM APIs'),
    'courses': ('Бесплатные курсы по R: от новичка до AI-инструментов', 'Безкоштовні курси з R: від новачка до AI-інструментів', 'Free R courses, from beginner to AI tools'),
    'videos': ('Серии уроков по пакетам и отдельные видеоуроки', 'Серії уроків за пакетами та окремі відеоуроки', 'Package series and standalone video lessons'),
    'talks': ('Доклады с конференций, вебинары и воркшопы', 'Доповіді з конференцій, вебінари та воркшопи', 'Conference talks, webinars and workshops'),
    'articles': ('Статьи и туториалы с 2015 года', 'Статті та туторіали з 2015 року', 'Articles and tutorials since 2015'),
    'interviews': ('Интервью, экспертные опросы и комментарии', "Інтерв'ю, експертні опитування та коментарі", 'Interviews, expert surveys and comments'),
}


def build_404():
    """404.html в корне сайта. GitHub Pages отдаёт её по любому несуществующему адресу,
    поэтому все пути на странице абсолютные."""
    cards = ''.join(f'''
                <a href="/{slug}/" class="bento-glass group p-5 rounded-2xl flex items-start gap-4">
                    <div class="bento-content w-11 h-11 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400 group-hover:bg-purple-500 group-hover:text-white transition-all shrink-0"><i class="{icon}"></i></div>
                    <div class="bento-content min-w-0">
                        <div class="font-bold text-white outfit-font group-hover:text-purple-300 transition-colors">{T(*labels)}</div>
                        <div class="text-xs text-slate-400 mt-1 leading-relaxed">{T(*PAGE_BLURBS[slug])}</div>
                    </div>
                </a>''' for slug, icon, labels in PAGES)

    page = head('404', 'Страница не найдена | Алексей Селезнёв', 'Такой страницы нет на сайте alexey-seleznev.pro.')
    page = page.replace('<meta name="robots" content="index, follow">', '<meta name="robots" content="noindex">')
    page = page.replace(f'    <link rel="canonical" href="{SITE}/404/">\n', '')
    page += nav('')
    page += f'''
    <main class="pt-32 pb-20 px-6 max-w-5xl mx-auto relative z-10 min-h-[80vh] flex flex-col justify-center">
        <div class="text-center mb-14" data-aos="fade-up">
            <div class="text-[120px] md:text-[180px] leading-none font-black outfit-font text-gradient select-none">404</div>
            <h1 class="text-3xl md:text-5xl font-extrabold uppercase tracking-tight mt-2 mb-5">{T('Страница не найдена', 'Сторінку не знайдено', 'Page not found')}</h1>
            <p class="text-slate-400 text-lg max-w-2xl mx-auto mb-8">{T('Возможно, ссылка устарела или в адресе опечатка. Вернитесь на главную или выберите нужный раздел ниже.', 'Можливо, посилання застаріло або в адресі помилка. Поверніться на головну або оберіть потрібний розділ нижче.', 'The link may be outdated or the address mistyped. Head back home or pick a section below.')}</p>
            <div class="flex flex-wrap justify-center gap-4">
                <a href="/" class="bg-purple-600 hover:bg-purple-500 text-white px-8 py-4 rounded-full font-bold transition-all shadow-[0_0_20px_rgba(168,85,247,0.4)] hover:shadow-[0_0_30px_rgba(168,85,247,0.6)] flex items-center gap-2"><i class="fa-solid fa-house text-sm"></i>{T('На главную', 'На головну', 'Back to home')}</a>
                <a href="https://t.me/AlexeySeleznev" target="_blank" rel="noopener" class="bento-glass px-8 py-4 rounded-full font-bold hover:bg-white/10 transition-all text-blue-400 flex items-center gap-2"><i class="fa-brands fa-telegram"></i>{T('Сообщить о битой ссылке', 'Повідомити про бите посилання', 'Report a broken link')}</a>
            </div>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4" data-aos="fade-up" data-aos-delay="100">{cards}
        </div>
    </main>
'''
    page += footer('/') + tail()
    # Относительные пути шаблона (../) превращаем в абсолютные
    page = page.replace('"../', '"/')
    out = ROOT / '404.html'
    out.write_text(page, encoding='utf-8', newline='\n')
    print(f'404.html: {len(page):,} bytes')


# ---------------------------------------------------------------- реклама в канале (страница без ссылок с сайта)

def fmt_date_ru(d):
    y, m, dd = map(int, d.split('-'))
    return f'{dd:02d}.{m:02d}.{y}'


def bar_chart(rows):
    """Горизонтальные полосы одной серии: подпись, полоса, значение. Ширина — относительно максимума."""
    top = max(v for _, v in rows)
    out = []
    for label, v in rows:
        tip = f'{label["en"]}: {v}%'
        out.append(f'''
                        <div class="grid grid-cols-[minmax(0,11rem)_1fr_3rem] items-center gap-3 py-1 group/bar" title="{esc(tip)}">
                            <div class="text-sm text-slate-300 leading-snug">{tr(label)}</div>
                            <div class="h-2.5 rounded-full bg-white/5 overflow-hidden">
                                <div class="h-full rounded-full bg-purple-500 group-hover/bar:bg-purple-400 transition-colors" style="width: {v / top * 100:.1f}%"></div>
                            </div>
                            <div class="text-sm font-semibold text-slate-200 text-right tabular-nums">{v}%</div>
                        </div>''')
    return ''.join(out)


def build_ads():
    d = load('ads')
    poll_word = T('опрос', 'опитування', 'poll')

    steps = ''.join(f'''
                <div class="bento-glass no-lift p-5 rounded-2xl flex gap-4 items-start" data-aos="fade-up" data-aos-delay="{i * 60}">
                    <div class="bento-content w-9 h-9 rounded-xl bg-purple-500/15 border border-purple-500/30 text-purple-300 font-black outfit-font flex items-center justify-center shrink-0">{i + 1}</div>
                    <div class="bento-content text-sm text-slate-200 pt-1.5">{tr(s)}</div>
                </div>''' for i, s in enumerate(d['steps']))

    rejected = ''.join(f'<li class="flex items-start gap-2.5 text-sm text-slate-300"><i class="fa-solid fa-xmark text-red-400 mt-1"></i>{tr(r)}</li>' for r in d['rejected'])

    payment = []
    for p in d['payment']:
        link = (f'<a href="{esc(p["url"])}" target="_blank" rel="noopener" class="mt-4 inline-flex items-center gap-2 text-sm font-semibold text-purple-300 hover:text-white transition-colors">'
                f'{T("Условия на бирже", "Умови на біржі", "Exchange terms")} <i class="fa-solid fa-arrow-up-right-from-square text-xs"></i></a>') if p.get('url') else ''
        payment.append(f'''
                <div class="bento-glass no-lift p-6 rounded-3xl flex flex-col" data-aos="fade-up">
                    <div class="bento-content w-12 h-12 rounded-2xl bg-blue-500/15 border border-blue-500/30 text-blue-300 flex items-center justify-center text-xl mb-4"><i class="{p['icon']}"></i></div>
                    <h3 class="bento-content text-lg font-bold text-white outfit-font mb-2">{tr(p['title'])}</h3>
                    <p class="bento-content text-sm text-slate-400 leading-relaxed">{tr(p['text'])}</p>
                    <div class="bento-content mt-auto">{link}</div>
                </div>''')

    stats_links = ''.join(f'''
                <a href="{esc(s['url'])}" target="_blank" rel="noopener" class="bento-glass p-6 rounded-3xl flex items-center gap-5 group">
                    <div class="bento-content w-12 h-12 rounded-2xl bg-purple-500/15 text-purple-300 flex items-center justify-center text-xl group-hover:bg-purple-500 group-hover:text-white transition-all"><i class="fa-solid fa-chart-line"></i></div>
                    <div class="bento-content flex-1">
                        <div class="font-bold text-white outfit-font text-lg">{esc(s['name'])}</div>
                        <div class="text-sm text-slate-400">{T('Подписчики, охваты и динамика канала', 'Підписники, охоплення та динаміка каналу', 'Subscribers, reach and channel dynamics')}</div>
                    </div>
                    <i class="bento-content fa-solid fa-arrow-up-right-from-square text-slate-500 group-hover:text-white transition-colors"></i>
                </a>''' for s in d['stats_links'])

    charts = []
    for a in d['audience']:
        if a.get('date'):
            meta = f'{T("Опрос", "Опитування", "Poll")} {fmt_date_ru(a["date"])} · <a href="{esc(a["poll"])}" target="_blank" rel="noopener" class="underline underline-offset-2 hover:text-white">{T("ссылка на опрос", "посилання на опитування", "poll link")}</a>'
        else:
            meta = tr(a['source'])
        multi = f'<div class="text-xs text-slate-500 mt-3">{T("Можно было выбрать несколько вариантов.", "Можна було обрати кілька варіантів.", "Multiple answers were allowed.")}</div>' if a.get('multi') else ''
        charts.append(f'''
                <div class="bento-glass no-lift p-6 rounded-3xl" data-aos="fade-up">
                    <div class="bento-content">
                        <h3 class="text-lg font-bold text-white outfit-font">{tr(a['title'])}</h3>
                        <div class="text-xs text-slate-500 mb-4">{meta}</div>
                        {bar_chart(a['rows'])}
                        {multi}
                    </div>
                </div>''')

    y, m = ym(d['updated'])
    contact_btn = f'''<a href="{d['contact']}" target="_blank" rel="noopener" class="bg-purple-600 hover:bg-purple-500 text-white px-8 py-4 rounded-full font-bold transition-all shadow-[0_0_20px_rgba(168,85,247,0.4)] hover:shadow-[0_0_30px_rgba(168,85,247,0.6)] flex items-center gap-2"><i class="fa-brands fa-telegram"></i>{T('Написать в Telegram', 'Написати в Telegram', 'Message me on Telegram')}</a>'''

    desc = 'Реклама в Telegram-канале R4marketing о языке R и аналитике данных: стоимость публикации, условия размещения, способы оплаты и аудитория канала.'
    page = head('ads', 'Реклама в Telegram-канале R4marketing | Алексей Селезнёв', desc)
    page += nav('')
    page += hero('fa-brands fa-telegram', 'R4marketing',
                 T('Реклама в <span class="text-gradient">R4marketing</span>', 'Реклама в <span class="text-gradient">R4marketing</span>', 'Advertise in <span class="text-gradient">R4marketing</span>'),
                 T('R4marketing — авторский Telegram-канал о языке R, аналитике данных и автоматизации маркетинга. Его читают аналитики, маркетологи и специалисты по данным. На этой странице — стоимость и условия размещения рекламы, способы оплаты и данные об аудитории.',
                   'R4marketing — авторський Telegram-канал про мову R, аналітику даних і автоматизацію маркетингу. Його читають аналітики, маркетологи та фахівці з даних. На цій сторінці — вартість і умови розміщення реклами, способи оплати та дані про аудиторію.',
                   'R4marketing is my Telegram channel about R, data analytics and marketing automation, read by analysts, marketers and data specialists. This page covers ad pricing and terms, payment options and audience data.'),
                 [(esc(d['price']), T('Одна публикация', 'Одна публікація', 'Per post')),
                  ('4 ' + T('ч', 'год', 'h'), T('Пост в топе канала', 'Пост у топі каналу', 'Pinned at the top')),
                  ('∞', T('Пост остаётся в ленте', 'Пост залишається у стрічці', 'Stays in the feed')),
                  ('3+', T('Пакет — цена индивидуально', 'Пакет — ціна індивідуально', 'Bundle — custom price'))])
    page += f'''
    <section class="px-6 max-w-7xl mx-auto pb-16 relative z-10">
        <div class="flex flex-wrap items-center gap-4 mb-16" data-aos="fade-up">
            {contact_btn}
            <a href="{d['channel']}" target="_blank" rel="noopener" class="bento-glass px-8 py-4 rounded-full font-bold hover:bg-white/10 transition-all text-blue-400 flex items-center gap-2"><i class="fa-solid fa-arrow-up-right-from-square text-sm"></i>{T('Открыть канал', 'Відкрити канал', 'Open the channel')}</a>
            <span class="text-xs text-slate-500">{T('Данные обновлены', 'Дані оновлено', 'Updated')}: {month_label(y, m)}</span>
        </div>

        <h2 class="text-3xl font-extrabold mb-8 flex items-center gap-4 outfit-font" data-aos="fade-up">
            <div class="w-12 h-12 bg-purple-500/20 flex items-center justify-center rounded-2xl border border-purple-500/30"><i class="fa-solid fa-list-check text-purple-400 text-xl"></i></div>
            {T('Как проходит размещение', 'Як відбувається розміщення', 'How it works')}
        </h2>
        <div class="grid sm:grid-cols-2 lg:grid-cols-5 gap-4 mb-6">{steps}
        </div>
        <p class="text-sm text-slate-400 mb-10" data-aos="fade-up"><i class="fa-solid fa-thumbtack text-purple-400 mr-2"></i>{T('Пост выходит в оговорённые дату и время, <strong class="text-white">висит в топе не менее 4 часов и остаётся в ленте навсегда</strong>.', 'Пост виходить у погоджені дату й час, <strong class="text-white">висить у топі щонайменше 4 години й залишається у стрічці назавжди</strong>.', 'The post goes live at the agreed time, <strong class="text-white">stays pinned for at least 4 hours and remains in the feed permanently</strong>.')}</p>

        <div class="grid md:grid-cols-2 gap-6 mb-6" data-aos="fade-up">
            <div class="bento-glass no-lift p-6 rounded-3xl border-l-4 border-green-500/50">
                <div class="bento-content">
                    <h3 class="text-lg font-bold text-white outfit-font mb-3 flex items-center gap-2"><i class="fa-solid fa-check text-green-400"></i>{T('Что берём', 'Що беремо', 'What we accept')}</h3>
                    <p class="text-sm text-slate-300 leading-relaxed">{tr(d['accepted'])}</p>
                </div>
            </div>
            <div class="bento-glass no-lift p-6 rounded-3xl border-l-4 border-red-500/50">
                <div class="bento-content">
                    <h3 class="text-lg font-bold text-white outfit-font mb-3 flex items-center gap-2"><i class="fa-solid fa-ban text-red-400"></i>{T('Что не берём', 'Що не беремо', 'What we decline')}</h3>
                    <ul class="space-y-2">{rejected}</ul>
                </div>
            </div>
        </div>
        <p class="text-sm text-slate-400 mb-20" data-aos="fade-up"><i class="fa-solid fa-circle-info text-purple-400 mr-2"></i>{tr(d['materials'])}</p>

        <h2 class="text-3xl font-extrabold mb-3 flex items-center gap-4 outfit-font" data-aos="fade-up">
            <div class="w-12 h-12 bg-blue-500/20 flex items-center justify-center rounded-2xl border border-blue-500/30"><i class="fa-solid fa-wallet text-blue-400 text-xl"></i></div>
            {T('Оплата', 'Оплата', 'Payment')}
        </h2>
        <p class="text-slate-400 mb-8" data-aos="fade-up">{T('Сначала согласуем пост, дату и время, затем я пришлю реквизиты удобного вам способа. Оплата — не позднее чем за день до публикации: если пост выходит 15 октября, оплатить нужно до 14 октября включительно.', 'Спершу погоджуємо пост, дату й час, потім я надішлю реквізити зручного для вас способу. Оплата — не пізніше ніж за день до публікації: якщо пост виходить 15 жовтня, оплатити треба до 14 жовтня включно.', 'First we agree on the post, date and time, then I send payment details for the method you prefer. Pay at least one day before publication: for a post on October 15, pay by October 14 inclusive.')}</p>
        <div class="grid {'md:grid-cols-3' if len(payment) > 1 else ''} gap-6 mb-20">{''.join(payment)}
        </div>

        <h2 class="text-3xl font-extrabold mb-8 flex items-center gap-4 outfit-font" data-aos="fade-up">
            <div class="w-12 h-12 bg-purple-500/20 flex items-center justify-center rounded-2xl border border-purple-500/30"><i class="fa-solid fa-chart-simple text-purple-400 text-xl"></i></div>
            {T('Статистика канала', 'Статистика каналу', 'Channel statistics')}
        </h2>
        <div class="grid md:grid-cols-2 gap-6 mb-6" data-aos="fade-up">{stats_links}
        </div>
        <a href="https://uk.tgstat.com/channel/@R4marketing" target="_blank" rel="noopener" class="block mb-20 rounded-3xl overflow-hidden border border-white/10 hover:border-purple-500/40 transition-colors" data-aos="fade-up">
            <!-- Живой виджет TGStat: картинка обновляется на стороне сервиса -->
            <img src="https://uk.tgstat.com/channel/@R4marketing/stat-widget.png" alt="{esc('Статистика канала R4marketing по данным TGStat')}" loading="lazy" referrerpolicy="no-referrer" class="w-full h-auto block bg-white">
        </a>

        <h2 class="text-3xl font-extrabold mb-3 flex items-center gap-4 outfit-font" data-aos="fade-up">
            <div class="w-12 h-12 bg-purple-500/20 flex items-center justify-center rounded-2xl border border-purple-500/30"><i class="fa-solid fa-users text-purple-400 text-xl"></i></div>
            {T('Аудитория канала', 'Аудиторія каналу', 'Channel audience')}
        </h2>
        <p class="text-slate-400 mb-8" data-aos="fade-up">{T('По результатам опросов подписчиков канала в 2021–2022 годах.', 'За результатами опитувань підписників каналу у 2021–2022 роках.', 'Based on channel subscriber polls in 2021–2022.')}</p>
        <div class="grid md:grid-cols-2 gap-6 mb-20">{''.join(charts)}
        </div>

        <div class="bento-glass no-lift p-8 md:p-10 rounded-[2rem] flex flex-col md:flex-row items-center justify-between gap-6 border border-purple-500/30" data-aos="fade-up" style="background: linear-gradient(145deg, rgba(30, 41, 59, 0.5), rgba(168, 85, 247, 0.12));">
            <div class="bento-content text-center md:text-left">
                <h2 class="text-2xl md:text-3xl font-extrabold text-white outfit-font mb-2">{T('Обсудим размещение?', 'Обговоримо розміщення?', 'Ready to discuss?')}</h2>
                <p class="text-slate-400">{T('Все вопросы по рекламе — в личные сообщения в Telegram.', 'Усі питання щодо реклами — в особисті повідомлення в Telegram.', 'All ad inquiries — via Telegram direct messages.')}</p>
            </div>
            <div class="bento-content">{contact_btn}</div>
        </div>
    </section>
'''
    page += footer() + tail()
    write('ads', page)


# ---------------------------------------------------------------- Tailwind CSS

TAILWIND_VERSION = '3.4.17'  # та же версия, что отдавал cdn.tailwindcss.com


def build_css():
    """Собирает assets/tailwind.css из классов всех страниц (нужен Node.js / npx).
    Запускается после генерации страниц, чтобы попали классы из свежего HTML."""
    import shutil
    import subprocess
    npx = shutil.which('npx')
    if not npx:
        print('  npx не найден: assets/tailwind.css не пересобран (установите Node.js)')
        return
    cmd = [npx, '-y', f'tailwindcss@{TAILWIND_VERSION}',
           '-c', '_build/tailwind.config.js', '-i', '_build/tailwind.input.css',
           '-o', 'assets/tailwind.css', '--minify']
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        print('  Ошибка сборки Tailwind:', result.stderr.strip()[-500:])
        return
    print(f'assets/tailwind.css: {(ROOT / "assets" / "tailwind.css").stat().st_size:,} bytes')


if __name__ == '__main__':
    import sys
    if '--stats-only' in sys.argv:
        update_package_stats(load('packages'))
        sys.exit()
    build_opensource()
    build_courses()
    build_videos()
    build_talks()
    build_articles()
    build_interviews()
    build_404()
    build_ads()
    build_css()
