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


def month_label(y, m):
    return T(*(f'{MONTHS[l][m - 1]} {y}' for l in LANGS))


def ym(s):
    y, m = s.split('-')
    return int(y), int(m)


# ---------------------------------------------------------------- навигация

PAGES = [
    ('courses', 'fa-solid fa-graduation-cap', ('Курсы', 'Курси', 'Courses')),
    ('videos', 'fa-solid fa-circle-play', ('Видеоуроки', 'Відеоуроки', 'Video Lessons')),
    ('talks', 'fa-solid fa-microphone-lines', ('Доклады и вебинары', 'Доповіді та вебінари', 'Talks & Webinars')),
    ('articles', 'fa-solid fa-pen-nib', ('Статьи', 'Статті', 'Articles')),
    ('interviews', 'fa-regular fa-newspaper', ('Интервью', "Інтерв'ю", 'Interviews')),
]


def head(slug, title, description, image=f'{SITE}/photo.jpg'):
    canonical = f'{SITE}/{slug}/'
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

    <link rel="icon" type="image/jpeg" href="../logo.jpg">
    <link rel="apple-touch-icon" href="../logo.jpg">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">
    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="../assets/site.css">
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


def footer_links(prefix):
    """Строка ссылок на внутренние страницы — общая для лендинга и внутренних страниц."""
    links = '\n'.join(
        f'                <a href="{prefix}{slug}/" class="flex items-center gap-2 hover:text-white transition-colors"><i class="{icon} text-purple-400/80 text-xs"></i> {T(*labels)}</a>'
        for slug, icon, labels in PAGES)
    return f'''            <nav class="flex flex-wrap justify-center gap-x-8 gap-y-3 mb-12 text-sm font-semibold text-slate-400 outfit-font" aria-label="Site pages">
{links}
            </nav>'''


def footer():
    return f'''
    <!-- FOOTER -->
    <footer class="border-t border-white/5 bg-slate-950/80 backdrop-blur-md pt-20 pb-10 text-center relative z-10">
        <div class="max-w-7xl mx-auto px-6">
            <h2 class="text-3xl font-extrabold mb-10 outfit-font">{T('Следите за обновлениями в R4marketing', 'Стежте за оновленнями в R4marketing', 'Follow R4marketing updates')}</h2>
            <div class="flex justify-center gap-8 mb-16">
                <a href="https://t.me/R4marketing" class="w-16 h-16 rounded-3xl bg-blue-500/10 flex items-center justify-center text-blue-400 text-3xl hover:bg-blue-500 hover:text-white transition-all transform hover:scale-110 hover:-translate-y-2 border border-blue-500/20 shadow-lg" aria-label="Telegram"><i class="fa-brands fa-telegram"></i></a>
                <a href="https://www.youtube.com/R4marketing" class="w-16 h-16 rounded-3xl bg-red-500/10 flex items-center justify-center text-red-500 text-3xl hover:bg-red-500 hover:text-white transition-all transform hover:scale-110 hover:-translate-y-2 border border-red-500/20 shadow-lg" aria-label="YouTube"><i class="fa-brands fa-youtube"></i></a>
                <a href="https://habr.com/ru/users/selesnow/" class="w-16 h-16 rounded-3xl bg-slate-700/30 flex items-center justify-center text-white text-3xl hover:bg-slate-600 transition-all transform hover:scale-110 hover:-translate-y-2 border border-slate-600/50 shadow-lg" aria-label="Habr"><i class="fa-solid fa-h"></i></a>
            </div>
            <div class="mb-6"><a href="../" class="inline-flex items-center gap-2 text-sm font-semibold text-slate-400 hover:text-white transition-colors outfit-font"><i class="fa-solid fa-house text-purple-400/80 text-xs"></i> ALEXEY-SELEZNEV<span class="text-purple-500 -ml-2">.pro</span></a></div>
{footer_links('../')}
            <p class="text-slate-500 text-sm font-mono tracking-widest uppercase">© 2026 Alexey Seleznev. Modernized Vision.</p>
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


def hero(icon, badge, title_html, lead, stats, back=True):
    stats_html = '\n'.join(f'''                <div class="bento-content">
                    <div class="text-3xl md:text-4xl font-extrabold text-white outfit-font">{value}</div>
                    <div class="text-xs text-slate-400 uppercase font-bold mt-1">{label}</div>
                </div>''' for value, label in stats)
    return f'''
    <!-- HERO -->
    <header class="pt-32 pb-12 px-6 max-w-7xl mx-auto relative z-10">
        <a href="../" class="inline-flex items-center gap-2 text-sm font-semibold text-slate-400 hover:text-white transition-colors mb-8 group" data-aos="fade-right">
            <i class="fa-solid fa-arrow-left text-xs group-hover:-translate-x-1 transition-transform"></i>
            {T('На главную', 'На головну', 'Back to home')}
        </a>
        <div data-aos="fade-up">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-400 text-xs font-bold tracking-widest uppercase mb-5 outfit-font">
                <i class="{icon}"></i> {badge}
            </div>
            <h1 class="text-5xl md:text-7xl font-black tracking-tight leading-tight uppercase mb-8">{title_html}</h1>
        </div>
        <div class="bento-glass no-lift p-6 md:p-10 border-l-4 border-purple-500/50 mb-8" data-aos="fade-up" data-aos-delay="100">
            <p class="text-lg md:text-xl text-slate-300 leading-relaxed font-light relative z-10">{lead}</p>
        </div>
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
    page = head('courses', 'Курсы по языку R | Алексей Селезнёв',
                'Бесплатные авторские курсы Алексея Селезнёва по языку R: от R для пользователей Excel до разработки пакетов, Telegram-ботов и AI-инструментов.')
    page += nav('courses')
    page += hero('fa-solid fa-graduation-cap', T('Обучение', 'Навчання', 'Learning'),
                 T('Авторские <span class="text-gradient">курсы</span>', 'Авторські <span class="text-gradient">курси</span>', 'Original <span class="text-gradient">Courses</span>'),
                 T('Курсы появились как внутренняя программа обучения аналитиков отдела Netpeak — от уровня Junior до Senior. Позже все программы были опубликованы в открытом доступе и стали востребованы среди тысяч специалистов. Все курсы бесплатные: видеолекции, конспекты, код, тесты и задания.',
                   'Курси з\'явилися як внутрішня програма навчання аналітиків відділу Netpeak — від рівня Junior до Senior. Пізніше всі програми були опубліковані у відкритому доступі та стали затребуваними серед тисяч фахівців. Усі курси безкоштовні: відеолекції, конспекти, код, тести та завдання.',
                   'These courses began as an internal training program for Netpeak\'s analytics team — from Junior to Senior. Later every program was published openly and is now used by thousands of specialists. All courses are free: video lectures, notes, code, quizzes and assignments.'),
                 [(str(free), T('Курсов', 'Курсів', 'Courses')), ('0 $', T('Стоимость', 'Вартість', 'Price')),
                  ('2018', T('Первый курс', 'Перший курс', 'First course')), ('3', T('Уровня сложности', 'Рівні складності', 'Skill levels'))])
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
            href, img, attrs = t['url'], '', ''
            center = '''<div class="absolute inset-0 flex items-center justify-center"><div class="w-14 h-14 rounded-full bg-purple-600/80 text-white flex items-center justify-center shadow-2xl backdrop-blur-sm group-hover:scale-110 group-hover:bg-purple-500 transition-all duration-300"><i class="fa-solid fa-arrow-up-right-from-square text-base"></i></div></div>'''
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
                f'{len(talks)} докладов, воркшопов и вебинаров Алексея Селезнёва с конференций 8P, Матемаркетинг, GoAnalytics, Analyze! и других: язык R, API рекламных систем, BI и аналитика.')
    page += nav('talks')
    page += hero('fa-solid fa-microphone-lines', T('Спикер', 'Спікер', 'Speaker'),
                 T('Доклады и <span class="text-gradient">вебинары</span>', 'Доповіді та <span class="text-gradient">вебінари</span>', 'Talks & <span class="text-gradient">Webinars</span>'),
                 T('Регулярно выступаю на крупнейших отраслевых конференциях по аналитике и интернет-маркетингу — 8P, Матемаркетинг, GoAnalytics, Analyze! — и провожу вебинары и воркшопы для образовательных платформ. Делюсь практическим опытом автоматизации, работы с API рекламных систем и построения BI-решений. Нажмите на карточку, чтобы посмотреть запись прямо здесь.',
                   'Регулярно виступаю на найбільших галузевих конференціях з аналітики та інтернет-маркетингу — 8P, Матемаркетинг, GoAnalytics, Analyze! — і проводжу вебінари та воркшопи для освітніх платформ. Ділюся практичним досвідом автоматизації, роботи з API рекламних систем і побудови BI-рішень. Натисніть на картку, щоб переглянути запис просто тут.',
                   'I speak regularly at major analytics and digital marketing conferences — 8P, Matemarketing, GoAnalytics, Analyze! — and run webinars and workshops for education platforms, sharing hands-on experience in automation, ad-platform APIs and BI. Click any card to watch the recording right here.'),
                 [(str(len(talks)), T('Выступлений', 'Виступів', 'Talks')), (str(cats['conference']), T('Конференции', 'Конференції', 'Conferences')),
                  (str(cats['webinar']), T('Вебинары', 'Вебінари', 'Webinars')), (f'{years[0]}–{years[-1]}', T('Годы', 'Роки', 'Years'))])
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
                f'{len(arts)} статей Алексея Селезнёва о языке R, Google BigQuery, Power BI, веб-аналитике, API рекламных систем и стоимости клика — Хабр, Netpeak Journal и другие издания.')
    page += nav('articles')
    page += hero('fa-solid fa-pen-nib', T('Публикации', 'Публікації', 'Publications'),
                 T('Статьи и <span class="text-gradient">туториалы</span>', 'Статті та <span class="text-gradient">туторіали</span>', 'Articles & <span class="text-gradient">Tutorials</span>'),
                 T('С 2015 года пишу о том, чем занимаюсь каждый день: язык R и автоматизация, Google BigQuery и Power BI, веб-аналитика, API рекламных систем и ежеквартальные исследования стоимости клика. Публикации выходили на Хабре, в Netpeak Journal и других изданиях; если оригинал больше недоступен, ссылка ведёт на копию в моём блоге.',
                   'З 2015 року пишу про те, чим займаюся щодня: мова R та автоматизація, Google BigQuery і Power BI, веб-аналітика, API рекламних систем і щоквартальні дослідження вартості кліку. Публікації виходили на Хабрі, у Netpeak Journal та інших виданнях; якщо оригінал більше недоступний, посилання веде на копію в моєму блозі. Статті написані російською мовою.',
                   'Since 2015 I have been writing about my daily work: R and automation, Google BigQuery and Power BI, web analytics, ad-platform APIs and quarterly cost-per-click research. The articles appeared on Habr, Netpeak Journal and other outlets; if an original is gone, the link points to a copy on my blog. Articles are written in Russian.'),
                 [(str(len(arts)), T('Статей', 'Статей', 'Articles')), (str(outlets), T('Изданий', 'Видань', 'Outlets')),
                  (str(min(years)), T('Первая статья', 'Перша стаття', 'First article')), (str(topic_counts['r']), T('Про язык R', 'Про мову R', 'About R'))])
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
                  (str(kinds['interview']), T('Интервью', "Інтерв'ю", 'Interviews')), (f'{years[0]}–{years[-1]}', T('Годы', 'Роки', 'Years'))])
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
                f'{total} бесплатных видеоуроков Алексея Селезнёва по языку R: серии по пакетам для работы с API рекламных систем, работа с данными, автоматизация, деплой и AI.',
                image=thumb(series[0]['episodes'][0]['yt']))
    page += nav('videos')
    page += hero('fa-solid fa-circle-play', T('YouTube · R4marketing', 'YouTube · R4marketing', 'YouTube · R4marketing'),
                 T('Видео<span class="text-gradient">уроки</span>', 'Відео<span class="text-gradient">уроки</span>', 'Video <span class="text-gradient">Lessons</span>'),
                 T('Бесплатные видеоуроки с YouTube-канала R4marketing: серии по моим R-пакетам для работы с API рекламных и аналитических систем, а также отдельные уроки по работе с данными, автоматизации, деплою и AI. Уроки, которые вошли в полноценные курсы, собраны на <a href="../courses/" class="text-purple-300 underline underline-offset-4 hover:text-white">странице курсов</a>.',
                   'Безкоштовні відеоуроки з YouTube-каналу R4marketing: серії з моїх R-пакетів для роботи з API рекламних і аналітичних систем, а також окремі уроки з роботи з даними, автоматизації, деплою та AI. Уроки, що увійшли до повноцінних курсів, зібрані на <a href="../courses/" class="text-purple-300 underline underline-offset-4 hover:text-white">сторінці курсів</a>.',
                   'Free video lessons from the R4marketing YouTube channel: series on my R packages for ad and analytics APIs, plus standalone lessons on data, automation, deployment and AI. Lessons that became full courses live on the <a href="../courses/" class="text-purple-300 underline underline-offset-4 hover:text-white">courses page</a>.'),
                 [(str(total), T('Видео', 'Відео', 'Videos')), (str(len(series)), T('Серий по пакетам', 'Серій за пакетами', 'Package series')),
                  (str(len(lessons)), T('Отдельных уроков', 'Окремих уроків', 'Standalone lessons')), (f'{years[0]}–{years[-1]}', T('Годы', 'Роки', 'Years'))])
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


if __name__ == '__main__':
    build_courses()
    build_videos()
    build_talks()
    build_articles()
    build_interviews()
