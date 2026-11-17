"""Блог: собирает /blog/ из Markdown-источников в _blog/posts/*.md.

Вызывается из _build/build.py (build_blog) — локально и в ночном workflow; можно и отдельно: python _build/blog.py
Шаблоны сайта (шапка, меню, футер, фон Vanta, фильтры site.js) берутся из _build/build.py, поэтому блог выглядит как весь сайт.

Источники:      _blog/posts/*.md   — статьи (YAML-шапка + Markdown), см. _blog/README.md
                _blog/images/      — НОВЫЕ картинки в любом формате: при сборке оптимизируются в blog/images/ (WebP, ширина ≤ 1600)
                _blog/blog.css     — стили блога (копируются в blog/blog.css + подсветка кода Pygments)
                _blog/cover_tpl.html — шаблон собственных обложек (рисуются через headless Chrome)
Результат:      blog/index.html, blog/<slug>/index.html, blog/blog.css, обновлённый блок /blog/ в sitemap.xml
                blog/images/ — хранилище опубликованных картинок (в git, сборка его не очищает)
"""
import collections, hashlib, html, json, math, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

import markdown
import yaml
from pygments.formatters import HtmlFormatter

HERE = Path(__file__).resolve().parent          # _build/
ROOT = HERE.parent
SRC = ROOT / '_blog'
OUT = ROOT / 'blog'
IMAGES_SRC = SRC / 'images'
IMAGES_OUT = OUT / 'images'

B = T = esc = None   # шаблоны сайта (модуль _build/build.py) подставляются в build_blog()

GEN_MONTHS = {  # месяцы в родительном падеже для полной даты: «17 июля 2024»
    'ru': ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'],
    'ua': ['січня', 'лютого', 'березня', 'квітня', 'травня', 'червня', 'липня', 'серпня', 'вересня', 'жовтня', 'листопада', 'грудня'],
    'en': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
}
OUTDATED_BEFORE = 2023   # статьи старше этого года получают плашку «может устареть»
TOP_CATS, TOP_TAGS = 12, 16

TR = dict(zip('абвгдеёжзийклмнопрстуфхцчшщъыьэюяіїєґ',
              ['a', 'b', 'v', 'g', 'd', 'e', 'e', 'zh', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f',
               'h', 'ts', 'ch', 'sh', 'sch', '', 'y', '', 'e', 'yu', 'ya', 'i', 'yi', 'ye', 'g']))


def slugify(s, limit=70):
    s = ''.join(TR.get(c, c) for c in s.lower())
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s[:limit].strip('-') or 'post'



# ---------------------------------------------------------------- картинки

MAX_W = 1600                  # максимальная ширина картинки на сайте
JPG_Q, PNG_LOSSY_Q = 82, 90   # качество WebP: из JPG; из крупных PNG-скриншотов
PNG_LOSSY_FROM = 150_000      # PNG тяжелее этого (в байтах) пробуем сжать с потерями


def _pil():
    try:
        from PIL import Image, ImageOps
        return Image, ImageOps
    except ImportError:
        return None, None


def _convert_image(src, dst):
    """Оптимизация: растровые форматы → WebP (≤ MAX_W по ширине); SVG и GIF копируются как есть."""
    Image, ImageOps = _pil()
    ext = src.suffix.lower()
    dst.parent.mkdir(parents=True, exist_ok=True)
    if ext in ('.svg', '.gif') or Image is None:
        shutil.copy2(src, dst)
        return
    im = Image.open(src)
    im.load()
    im = ImageOps.exif_transpose(im)
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    alpha = im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info)
    im = im.convert('RGBA' if alpha else 'RGB')
    if ext in ('.jpg', '.jpeg'):
        im.save(dst, 'WEBP', quality=JPG_Q, method=5)
        return
    im.save(dst, 'WEBP', lossless=True, method=4)
    if not alpha and dst.stat().st_size > PNG_LOSSY_FROM:
        tmp = dst.with_suffix('.tmp.webp')
        im.save(tmp, 'WEBP', quality=PNG_LOSSY_Q, method=5)
        if tmp.stat().st_size < dst.stat().st_size * 0.7:
            tmp.replace(dst)
        else:
            tmp.unlink()


_published = {}
_sizes = {}


def ensure_image(name):
    """Имя из ссылки '../images/<name>' → имя опубликованного файла в blog/images/.
    Если исходник лежит в _blog/images/ (новая картинка), он оптимизируется в blog/images/ (PNG/JPG → WebP).
    Картинки, которых нет в _blog/images/, считаются уже опубликованными (blog/images/)."""
    if name in _published:
        return _published[name]
    out_name = name
    src = IMAGES_SRC / name
    if src.is_file():
        p = Path(name)
        out_name = name if p.suffix.lower() in ('.svg', '.gif') else p.with_suffix('.webp').as_posix()
        dst = IMAGES_OUT / out_name
        if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
            _convert_image(src, dst)
    _published[name] = out_name
    return out_name


def img_size(rel):
    """(ширина, высота) опубликованной картинки — для width/height в вёрстке (страница не «прыгает» при загрузке)."""
    if rel not in _sizes:
        Image, _ = _pil()
        try:
            with Image.open(IMAGES_OUT / rel) as im:
                _sizes[rel] = im.size
        except Exception:
            _sizes[rel] = None
    return _sizes[rel]


def good_cover(rel):
    """Картинка годится в обложку: не меньше 500×250 и соотношение сторон от 1.25 до 3."""
    size = img_size(rel)
    return bool(size) and size[0] >= 500 and size[1] >= 250 and 1.25 <= size[0] / size[1] <= 3


# ---------------------------------------------------------------- собственные обложки

COVER_ICONS = {
    'AI': 'fa-solid fa-robot', 'Claude Code': 'fa-solid fa-terminal', 'MCP': 'fa-solid fa-plug', 'ChatGPT': 'fa-solid fa-comments',
    'LLM': 'fa-solid fa-brain', 'Gemini': 'fa-solid fa-wand-magic-sparkles', 'AcpGram': 'fa-solid fa-paper-plane', 'OpenCode': 'fa-solid fa-terminal',
    'Vibe coding': 'fa-solid fa-wand-magic-sparkles', 'Telegram': 'fa-brands fa-telegram', 'Яндекс Директ': 'fa-solid fa-bullhorn',
    'Яндекс Метрика': 'fa-solid fa-chart-line', 'Google Ads': 'fa-solid fa-rectangle-ad', 'Google Analytics': 'fa-solid fa-chart-line',
    'Facebook': 'fa-brands fa-facebook', 'ВКонтакте': 'fa-brands fa-vk', 'myTarget': 'fa-solid fa-bullseye', 'PPC': 'fa-solid fa-bullseye',
    'Веб-аналитика': 'fa-solid fa-chart-line', 'Power BI': 'fa-solid fa-chart-column', 'Google Data Studio': 'fa-solid fa-chart-pie',
    'BI': 'fa-solid fa-chart-pie', 'Визуализация данных': 'fa-solid fa-chart-pie', 'Google Таблицы': 'fa-solid fa-table',
    'Excel': 'fa-solid fa-file-excel', 'BigQuery': 'fa-solid fa-database', 'SQL': 'fa-solid fa-database', 'Базы данных': 'fa-solid fa-server',
    'Python': 'fa-brands fa-python', 'GitHub': 'fa-brands fa-github', 'Автоматизация': 'fa-solid fa-gears',
    'Параллельные вычисления': 'fa-solid fa-microchip', 'Обработка ошибок': 'fa-solid fa-bug', 'tidyverse': 'fa-solid fa-filter',
    'Обработка данных': 'fa-solid fa-filter', 'Анализ данных': 'fa-solid fa-magnifying-glass-chart', 'Пакеты R': 'fa-solid fa-box-open',
    'Импорт данных': 'fa-solid fa-file-import', 'Вебинары': 'fa-solid fa-video', 'Выступления': 'fa-solid fa-microphone-lines',
    'Интервью': 'fa-regular fa-newspaper', 'Исследования': 'fa-solid fa-magnifying-glass-chart', 'Кейсы': 'fa-solid fa-briefcase',
    'Дайджесты': 'fa-solid fa-newspaper', 'Обучение': 'fa-solid fa-graduation-cap', 'API': 'fa-solid fa-plug', 'R': 'fa-solid fa-code',
}


def _find_chrome():
    env = os.environ.get('CHROME')
    if env and Path(env).exists():
        return env
    for name in ('google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser', 'chrome'):
        found = shutil.which(name)
        if found:
            return found
    for p in (r'C:\Program Files\Google\Chrome\Application\chrome.exe', r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
              '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'):
        if Path(p).exists():
            return p
    return None


def generate_cover(post):
    """Рисует обложку blog/images/covers/<slug>.webp по шаблону _blog/cover_tpl.html (headless Chrome → WebP).
    Возвращает 'images/covers/<slug>.webp' или None, если Chrome/Pillow недоступны — тогда у карточки останется заглушка."""
    Image, _ = _pil()
    chrome, tpl = _find_chrome(), SRC / 'cover_tpl.html'
    if Image is None or not chrome or not tpl.exists():
        print(f'  обложка для «{post["slug"]}» не нарисована (нет Chrome или Pillow) — будет заглушка')
        return None
    tags, cats = post['tags'], post['cats']
    icon_tag = next((t for t in tags if t in COVER_ICONS), None)
    kw = icon_tag or (tags[0] if tags else (cats[0] if cats else 'Блог'))
    data = dict(kw=kw[:18], icon=COVER_ICONS.get(icon_tag, 'fa-solid fa-feather-pointed'), cat=(cats[0] if cats else 'Блог'),
                chips=[t for t in tags if t != kw][:3], year=str(post['y']), seed=int(hashlib.md5(post['slug'].encode()).hexdigest()[:6], 16))
    import urllib.parse
    url = tpl.resolve().as_uri() + '#' + urllib.parse.quote(json.dumps(data, ensure_ascii=False))
    out = IMAGES_OUT / 'covers' / f'{post["slug"]}.webp'
    out.parent.mkdir(parents=True, exist_ok=True)
    png = Path(tempfile.gettempdir()) / f'cover_{post["slug"]}.png'
    for _ in range(3):
        png.unlink(missing_ok=True)
        try:
            with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as prof:
                subprocess.run([chrome, '--headless=new', '--disable-gpu', '--no-sandbox', '--hide-scrollbars', f'--user-data-dir={prof}',
                                '--window-size=1200,630', '--virtual-time-budget=9000', f'--screenshot={png}', url],
                               capture_output=True, timeout=90)
        except Exception:
            pass
        if png.exists() and png.stat().st_size > 10_000:
            with Image.open(png) as im:
                im.convert('RGB').resize((1200, 630)).save(out, 'WEBP', quality=84, method=6)
            png.unlink(missing_ok=True)
            print(f'  нарисована обложка: {out.relative_to(ROOT).as_posix()}')
            return f'images/covers/{post["slug"]}.webp'
    print(f'  обложка для «{post["slug"]}» не нарисована (Chrome не отдал картинку) — будет заглушка')
    return None


# ---------------------------------------------------------------- загрузка постов

def load_posts():
    posts, used = [], set()
    for f in sorted((SRC / 'posts').glob('*.md'), key=lambda f: f.name, reverse=True):
        raw = f.read_text(encoding='utf-8')
        _, fm, body = raw.split('---\n', 2)
        meta = yaml.safe_load(fm)
        if meta.get('draft'):
            continue
        slug = str(meta.get('slug') or slugify(meta['title']))   # адрес статьи; у всех постов задан явно, чтобы URL не менялись
        n = 2
        while slug in used:
            slug, n = f'{slug}-{n}', n + 1
        used.add(slug)
        text = re.sub(r'[#*_`>\[\]()!|-]+', ' ', re.sub(r'```.*?```', ' ', body, flags=re.S))
        words = len(re.findall(r'\w+', text))
        y, m, _d = meta['date'].split('-') if isinstance(meta['date'], str) else str(meta['date']).split('-')
        desc = (meta.get('description') or '').strip()
        if len(desc) < 40:
            desc = re.sub(r'\s+', ' ', text).strip()
        desc = re.sub(r'\s*\[…\]|\s*\[\.\.\.\]', '…', desc)
        if len(desc) > 190:
            desc = desc[:187].rsplit(' ', 1)[0] + '…'
        post = dict(meta=meta, slug=slug, body=body, title=str(meta['title']).strip(), desc=desc,
                    y=int(y), m=int(m), date=str(meta['date']), minutes=max(1, round(words / 180)), words=words,
                    cats=meta.get('categories') or [], tags=meta.get('tags') or [])
        # обложка: явная (cover:) → иначе первая подходящая картинка из текста → иначе нарисованная (blog/images/covers/<slug>.webp)
        explicit = meta.get('cover')
        first_img = re.search(r'!\[[^\]]*\]\(\.\./images/([^)\s]+)', body)
        cover, own = None, bool(explicit)
        if explicit:
            rel = ensure_image(str(explicit).replace('../images/', ''))
            cover = f'images/{rel}' if (IMAGES_OUT / rel).exists() else None
        elif first_img:
            rel = ensure_image(first_img.group(1))
            cover = f'images/{rel}' if good_cover(rel) else None
        if cover is None:
            made = IMAGES_OUT / 'covers' / f'{slug}.webp'
            cover = f'images/covers/{slug}.webp' if made.exists() else generate_cover(post)
            own = cover is not None
        post.update(cover=cover, own_cover=own)
        posts.append(post)
    return posts

def normalize(posts):
    """Сводит теги/категории, различающиеся только регистром/пробелами; возвращает счётчики и словари."""
    out = {}
    for kind in ('cats', 'tags'):
        spell = collections.defaultdict(collections.Counter)
        for p in posts:
            for t in p[kind]:
                spell[re.sub(r'\s+', ' ', t.strip().lower())][t.strip()] += 1
        names = {k: c.most_common(1)[0][0] for k, c in spell.items()}
        counts = collections.Counter()
        for p in posts:
            keys = []
            for t in p[kind]:
                k = re.sub(r'\s+', ' ', t.strip().lower())
                if k not in keys:
                    keys.append(k)
            p[kind] = keys
            counts.update(keys)
        out[kind] = (names, counts)
    return out


def tslug(key):
    return slugify(key, 40)


# ---------------------------------------------------------------- карточка

def cover_html(p, prefix, height='h-44', extra=''):
    img = f'<img src="{prefix}{esc(p["cover"])}" alt="" loading="lazy" width="640" height="360" onerror="this.remove()">' if p['cover'] else ''
    return (f'<div class="cover {height} rounded-2xl"><div class="cover-fallback"><i class="fa-solid fa-feather-pointed text-5xl"></i></div>'
            f'{img}<div class="absolute inset-0 bg-gradient-to-t from-slate-950/85 via-slate-950/10 to-transparent"></div>{extra}</div>')


def card(p, names, prefix='', delay=0, filt=True):
    extra = (f'<div class="absolute top-3 left-3 text-[10px] font-mono font-bold uppercase tracking-wider px-2.5 py-1 rounded-lg '
             f'backdrop-blur-md bg-slate-950/80 border border-white/10 text-purple-300">{B.month_label(p["y"], p["m"])}</div>')
    if p['y'] < OUTDATED_BEFORE:
        extra += ('<div class="absolute top-3 right-3 text-[10px] font-bold px-2 py-0.5 rounded backdrop-blur-md bg-amber-500/20 '
                  'text-amber-200 border border-amber-500/30" title="">'
                  f'<i class="fa-regular fa-clock mr-1"></i>{p["y"]}</div>')
    tags = ' '.join(f'<span class="px-2 py-0.5 rounded-md bg-white/5 border border-white/5 text-[11px] text-slate-400">{esc(names[t])}</span>'
                    for t in p['tags'][:2])
    attrs = ''
    if filt:
        attrs = (f' data-filter-item data-cat="{" ".join(tslug(c) for c in p["cats"])}" data-tag="{" ".join(tslug(t) for t in p["tags"])}"'
                 f' data-year="{p["y"]}" data-search="{esc((p["title"] + " " + p["desc"] + " " + " ".join(names[t] for t in p["tags"])).lower())}"')
    return f'''
                <a href="{prefix}{p['slug']}/" class="bento-glass group flex flex-col p-2 rounded-3xl"{attrs} data-aos="fade-up" data-aos-delay="{delay}">
                    <div class="bento-content flex flex-col h-full">
                    {cover_html(p, prefix, extra=extra)}
                    <div class="px-3 pt-4 pb-3 flex flex-col flex-1">
                        <div class="text-xs text-slate-400 mb-2 flex items-center gap-2"><i class="fa-regular fa-clock text-purple-400" aria-hidden="true"></i>{T(f"{p['minutes']} мин чтения", f"{p['minutes']} хв читання", f"{p['minutes']} min read")}<span class="b-lang" title="Русский">RU</span></div>
                        <h3 class="font-bold text-[17px] leading-snug text-slate-100 group-hover:text-purple-300 transition-colors outfit-font line-clamp-3 mb-2">{esc(p['title'])}</h3>
                        <p class="text-sm text-slate-400 leading-relaxed line-clamp-3 flex-1">{esc(p['desc'])}</p>
                        <div class="mt-4 pt-3 border-t border-white/5 flex items-center justify-between gap-3">
                            <div class="flex flex-wrap gap-1.5">{tags}</div>
                            <i class="fa-solid fa-arrow-right text-xs text-slate-500 group-hover:text-purple-300 transition-colors shrink-0" aria-hidden="true"></i>
                        </div>
                    </div>
                    </div>
                </a>'''


# ---------------------------------------------------------------- общая обвязка

def deep(s):
    """Страницы статей лежат на уровень глубже: /blog/<slug>/ — поднимаем относительные пути шаблонов."""
    return s.replace('="../', '="../../')


def with_css(page, prefix):
    return page.replace('</head>', f'    <link rel="stylesheet" href="{prefix}blog.css">\n</head>', 1)


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8', newline='\n')


def blog_css():
    pyg = HtmlFormatter(style='monokai').get_style_defs('.codehilite')
    return (SRC / 'blog.css').read_text(encoding='utf-8') + '\n/* pygments monokai */\n' + pyg


# ---------------------------------------------------------------- главная блога

def build_index(posts, norm):
    names_c, cnt_c = norm['cats']
    names_t, cnt_t = norm['tags']
    names = {**names_c, **names_t}
    years = sorted({p['y'] for p in posts}, reverse=True)
    cats = [k for k, _ in cnt_c.most_common(TOP_CATS)]
    tags = [k for k, _ in cnt_t.most_common(TOP_TAGS)]

    def btn(group, value, label, count, active=False):
        return B.filter_btn(group, value, label, count, '', active).replace('<button ', '<button aria-pressed="%s" ' % ('true' if active else 'false'), 1)

    def extras(group, btns, top):
        """Первые top кнопок видны, остальные скрыты за переключателем «+N» (aria-expanded)."""
        shown, rest = btns[:top], btns[top:]
        rest = [b.replace('<button ', f'<button hidden data-extra="{group}" ', 1) for b in rest]
        toggle = (f'<button type="button" class="filter-btn b-toggle" data-toggle="{group}" aria-expanded="false" '
                  f'data-more="+{len(rest)}" data-less="−">+{len(rest)}</button>') if rest else ''
        return shown + rest + [toggle]

    cat_btns = [btn('cat', 'all', T('Все рубрики', 'Усі рубрики', 'All categories'), len(posts), True)]
    cat_btns += extras('cat', [btn('cat', tslug(k), esc(names_c[k]), cnt_c[k]) for k, _ in cnt_c.most_common()], TOP_CATS)
    tag_btns = [btn('tag', 'all', T('Все теги', 'Усі теги', 'All tags'), len(posts), True)]
    tag_btns += extras('tag', [btn('tag', tslug(k), esc(names_t[k]), cnt_t[k]) for k, _ in cnt_t.most_common()], TOP_TAGS)
    year_btns = [btn('year', 'all', T('Все годы', 'Усі роки', 'All years'), len(posts), True)]
    year_btns += [btn('year', str(y), str(y), sum(1 for p in posts if p['y'] == y)) for y in years]

    cards = ''.join(card(p, names, '', (i % 3) * 60) for i, p in enumerate(posts))
    page = B.head('blog', 'Блог | Алексей Селезнёв',
                  f'Блог Алексея Селезнёва: {len(posts)} материалов о языке R, веб-аналитике, Google BigQuery, Power BI и автоматизации маркетинга.',
                  jsonld={'@context': 'https://schema.org', '@type': 'Blog', 'name': 'Блог Алексея Селезнёва', 'url': f'{B.SITE}/blog/'})
    page = with_css(page, '')
    page += B.nav('blog')
    page += B.hero('fa-solid fa-feather-pointed', T('Блог', 'Блог', 'Blog'),
                   T('Заметки об <span class="text-gradient">R и аналитике</span>', 'Нотатки про <span class="text-gradient">R та аналітику</span>',
                     'Notes on <span class="text-gradient">R & analytics</span>'),
                   T('Уроки, разборы и опыт автоматизации маркетинга и аналитики: язык R, Google Analytics, BigQuery, Power BI, API рекламных систем. Материалы написаны на русском языке.',
                     'Уроки, розбори та досвід автоматизації маркетингу й аналітики: мова R, Google Analytics, BigQuery, Power BI, API рекламних систем. Матеріали написані російською мовою.',
                     'Lessons, walkthroughs and hands-on experience in marketing and analytics automation: R, Google Analytics, BigQuery, Power BI, ad-platform APIs. Posts are written in Russian.'),
                   [(str(len(posts)), T('Материалов', 'Матеріалів', 'Posts')), (str(len(cnt_c)), T('Рубрик', 'Рубрик', 'Categories')),
                    (str(min(years)), T('С года', 'З року', 'Since')), (str(sum(p['minutes'] for p in posts) // 60), T('Часов чтения', 'Годин читання', 'Hours of reading'))])
    page += f'''
    <!-- CATALOG -->
    <section class="px-6 max-w-7xl mx-auto pb-16 relative z-10" id="posts">
        <div class="bento-glass no-lift p-5 md:p-6 rounded-3xl mb-10 space-y-5" data-aos="fade-up">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 relative z-10">
                <p class="text-slate-400 text-sm" aria-live="polite">{T('Показано', 'Показано', 'Showing')}: <span data-filter-count class="font-mono text-white">{len(posts)}</span> / {len(posts)}</p>
                {B.search_box('Поиск по заголовкам и тегам…', 'Пошук за заголовками й тегами…', 'Search titles and tags…')}
            </div>
            <div class="b-filter-row relative z-10"><span class="b-filter-label">{T('Рубрика', 'Рубрика', 'Category')}</span><div class="flex flex-wrap gap-2">{''.join(cat_btns)}</div></div>
            <div class="b-filter-row relative z-10"><span class="b-filter-label">{T('Тег', 'Тег', 'Tag')}</span><div class="flex flex-wrap gap-2">{''.join(tag_btns)}</div></div>
            <div class="b-filter-row relative z-10"><span class="b-filter-label">{T('Год', 'Рік', 'Year')}</span><div class="flex flex-wrap gap-2">{''.join(year_btns)}</div></div>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">{cards}
        </div>
        <div class="b-more-wrap"><button type="button" id="b-more" class="b-more">{T('Показать ещё', 'Показати ще', 'Show more')} <span class="b-more-count font-mono" aria-live="polite"></span></button></div>
        <div class="mt-6">{B.empty_state()}</div>
    </section>
'''
    page += B.cta_block() + B.footer('../') + B.tail()
    page = page.replace('</body>', INDEX_JS + '</body>')
    write(OUT / 'index.html', page)


INDEX_JS = '''
    <script>
    // aria-pressed у кнопок-фильтров и deep link: /blog/?cat=r&tag=api&year=2020
    (function () {
        const btns = Array.from(document.querySelectorAll('[data-filter-group]'));
        const sync = () => btns.forEach(b => b.setAttribute('aria-pressed', b.classList.contains('active')));
        btns.forEach(b => b.addEventListener('click', () => setTimeout(sync, 0)));
        const setExtra = (g, open) => {
            document.querySelectorAll('[data-extra="' + g + '"]').forEach(x => { x.hidden = !open; });
            const t = document.querySelector('[data-toggle="' + g + '"]');
            if (t) { t.setAttribute('aria-expanded', open); t.textContent = open ? t.dataset.less : t.dataset.more; }
        };
        document.querySelectorAll('[data-toggle]').forEach(t => t.addEventListener('click', () => setExtra(t.dataset.toggle, t.getAttribute('aria-expanded') !== 'true')));
        const params = new URLSearchParams(location.search);
        ['cat', 'tag', 'year'].forEach(g => {
            const v = params.get(g);
            const b = v && btns.find(x => x.dataset.filterGroup === g && x.dataset.filterValue === v);
            if (b) { if (b.hidden) setExtra(g, true); b.click(); }
        });
        sync();
    })();

    // пагинация «Показать ещё»: работает поверх фильтров site.js (класс is-hidden)
    (function () {
        const PAGE = 12;
        let limit = PAGE;
        const items = Array.from(document.querySelectorAll('[data-filter-item]'));
        const btn = document.getElementById('b-more');
        const count = btn.querySelector('.b-more-count');
        function paginate() {
            let shown = 0, total = 0;
            items.forEach(it => {
                if (it.classList.contains('is-hidden')) { it.classList.remove('b-more-hidden'); return; }
                total++;
                if (shown < limit) { shown++; it.classList.remove('b-more-hidden'); }
                else it.classList.add('b-more-hidden');
            });
            const rest = total - shown;
            btn.parentElement.hidden = rest <= 0;
            count.textContent = rest > 0 ? '(' + rest + ')' : '';
            if (typeof AOS !== 'undefined') AOS.refresh();
        }
        const reset = () => { limit = PAGE; setTimeout(paginate, 0); };
        btn.addEventListener('click', () => { limit += PAGE; paginate(); });
        document.querySelectorAll('[data-filter-group]').forEach(b => b.addEventListener('click', reset));
        const search = document.querySelector('[data-filter-search]');
        if (search) search.addEventListener('input', reset);
        paginate();
    })();
    </script>
'''

ARTICLE_JS = '''
    <script>
    (function () {
        // кнопка «Копировать» у блоков кода
        document.querySelectorAll('.b-prose .codehilite').forEach(box => {
            const btn = document.createElement('button');
            btn.type = 'button'; btn.className = 'b-copy'; btn.setAttribute('aria-label', 'Copy code');
            btn.innerHTML = '<i class="fa-regular fa-copy" aria-hidden="true"></i>';
            btn.addEventListener('click', () => {
                navigator.clipboard.writeText(box.querySelector('pre').innerText).then(() => {
                    btn.innerHTML = '<i class="fa-solid fa-check" aria-hidden="true"></i>';
                    setTimeout(() => btn.innerHTML = '<i class="fa-regular fa-copy" aria-hidden="true"></i>', 1500);
                });
            });
            box.appendChild(btn);
        });
        // подсветка текущего раздела в оглавлении
        const links = Array.from(document.querySelectorAll('.b-toc a'));
        if (links.length && 'IntersectionObserver' in window) {
            const map = new Map(links.map(a => [a.getAttribute('href').slice(1), a]));
            const io = new IntersectionObserver(es => es.forEach(e => {
                if (e.isIntersecting) { links.forEach(l => l.classList.remove('active')); const a = map.get(e.target.id); if (a) a.classList.add('active'); }
            }), { rootMargin: '-80px 0px -70% 0px' });
            map.forEach((_, id) => { const el = document.getElementById(id); if (el) io.observe(el); });
        }
    })();
    </script>
'''


# ---------------------------------------------------------------- страница статьи

IMG_RE = re.compile(r'<img ([^>]*?)src="\.\./images/([^"]+)"')


def img_dims(m):
    """Подставляет опубликованное имя файла и width/height: браузер резервирует место, страница не «прыгает» при загрузке."""
    rel = ensure_image(m.group(2))
    size = img_size(rel)
    dims = f'width="{size[0]}" height="{size[1]}" ' if size and 'width=' not in m.group(1) else ''
    return f'<img {m.group(1)}{dims}src="../images/{rel}"'


VIDEO_RE = re.compile(r'^\{\{video:\s*(\S+?)\s*\}\}\s*$', re.M)
EMBED_HOSTS = ('embedd.srv.habr.com', 'player.vimeo.com', 'rutube.ru/play/embed', 'vk.com/video_ext', 'vkvideo.ru/video_ext')


def video_html(m):
    """{{video: URL}} из экспорта → адаптивный плеер: YouTube (nocookie, 16:9), SlideShare (4:3), презентации Google Docs (16:9)
    и прочие известные хосты; для неизвестного хоста — просто ссылка."""
    u = m.group(1).replace('\\_', '_')         # конвертер экранировал подчёркивания: embed\_code → embed_code
    kind, src = 'video', None
    yt = re.search(r'(?:youtube(?:-nocookie)?\.com/embed/|youtu\.be/|youtube\.com/watch\?v=)([\w-]{11})', u)
    sl = re.search(r'slideshare\.net/slideshow/embed_code/(?:key/)?([\w-]+)', u)
    if yt:
        src = f'https://www.youtube-nocookie.com/embed/{yt.group(1)}'
    elif sl:
        # числовые id работают как есть, буквенно-цифровые — только через /key/
        kind, src = 'slides', 'https://www.slideshare.net/slideshow/embed_code/' + ('' if sl.group(1).isdigit() else 'key/') + sl.group(1)
    elif 'docs.google.com/presentation' in u:
        kind, src = 'gslides', u
    elif any(h in u for h in EMBED_HOSTS):
        src = u
    if not src:
        return (f'\n\n<p class="b-video-link"><a href="{esc(u)}" target="_blank" rel="noopener">'
                f'<i class="fa-solid fa-circle-play" aria-hidden="true"></i> {esc(u)}</a></p>\n\n')
    title = 'Presentation' if kind in ('slides', 'gslides') else 'Video'
    link = ''
    if kind in ('slides', 'gslides'):   # запасной путь, если сервис не даёт встраиваться (cookie, блокировщики)
        link = (f'<p class="b-embed-link"><a href="{esc(src)}" target="_blank" rel="noopener">'
                f'<i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i> '
                f'{T("Открыть презентацию в новой вкладке", "Відкрити презентацію в новій вкладці", "Open the presentation in a new tab")}</a></p>')
    return (f'\n\n<div class="b-video b-{kind}"><iframe src="{esc(src)}" title="{title}" loading="lazy" allowfullscreen '
            f'referrerpolicy="strict-origin-when-cross-origin"></iframe></div>\n\n{link}\n\n')


def toc_html(tokens):
    def walk(items):
        return ''.join(f'<li><a href="#{t["id"]}">{html.escape(t["name"])}</a>' + (f'<ul>{walk(t["children"])}</ul>' if t['children'] else '') + '</li>'
                       for t in items)
    return f'<ul>{walk(tokens)}</ul>'


def build_article(p, posts, norm):
    names = {**norm['cats'][0], **norm['tags'][0]}
    md = markdown.Markdown(extensions=['fenced_code', 'tables', 'toc', 'sane_lists', 'codehilite'],
                           extension_configs={'codehilite': {'guess_lang': False, 'css_class': 'codehilite'},
                                              'toc': {'toc_depth': '2-3'}})
    body = md.convert(VIDEO_RE.sub(video_html, p['body']))
    body = body.replace('<img ', '<img loading="lazy" decoding="async" ')
    body = IMG_RE.sub(img_dims, body)
    body = body.replace('<table>', '<div class="b-table"><table>').replace('</table>', '</table></div>')
    body = re.sub(r'<a href="(https?://(?!(?:www\.)?alexey-seleznev\.pro))', r'<a target="_blank" rel="noopener" href="\1', body)   # внешние — в новой вкладке, свой сайт — в той же
    tokens = md.toc_tokens
    has_toc = len(tokens) >= 3

    related = sorted((q for q in posts if q is not p),
                     key=lambda q: (-(len(set(q['tags']) & set(p['tags'])) * 2 + len(set(q['cats']) & set(p['cats']))),
                                    tuple(-int(x) for x in q['date'].split('-')), q['slug']))[:3]   # при равенстве — новее, затем по slug: сборка воспроизводима
    related_html = ''.join(card(q, names, '../', i * 60, filt=False) for i, q in enumerate(related))

    cats = ''.join(f'<a class="b-chip b-chip-cat" href="../?cat={tslug(c)}#posts">{esc(names[c])}</a>' for c in p['cats'][:3])
    tags = ''.join(f'<a class="b-chip" href="../?tag={tslug(t)}#posts">{esc(names[t])}</a>' for t in p['tags'][:8])
    source_footer = ''
    if p['meta'].get('archive_url'):      # строка-источник в конце статьи: откуда текст и где лежит снимок оригинала
        sn, yr = esc(p['meta'].get('source_name') or ''), p['y']
        source_footer = (f'<p class="b-source"><i class="fa-solid fa-box-archive" aria-hidden="true"></i><span>'
                         f'{T(f"Источник: {sn}, {yr}. Оригинал больше недоступен — материал восстановлен из архива.", f"Джерело: {sn}, {yr}. Оригінал більше недоступний — матеріал відновлено з архіву.", f"Source: {sn}, {yr}. The original is no longer online — restored from the archive.")} '
                         f'<a href="{esc(p["meta"]["archive_url"])}" target="_blank" rel="noopener">'
                         f'{T("Снимок в Web Archive", "Знімок у Web Archive", "Snapshot in the Web Archive")} <i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i></a></span></p>')
    outdated = ''
    if p['meta'].get('archive_url'):      # материал, оригинал которого пропал: даём ссылку на снимок в Web Archive как подтверждение
        src_name = esc(p['meta'].get('source_name') or 'оригинал')
        outdated = (f'<div class="b-note b-note-archive"><i class="fa-solid fa-box-archive" aria-hidden="true"></i><div>'
                    f'{T(f"Интервью из архива. Оригинал на {src_name} ({p["y"]}) больше недоступен — текст восстановлен по снимку страницы.", f"Інтерв’ю з архіву. Оригінал на {src_name} ({p["y"]}) більше недоступний — текст відновлено за знімком сторінки.", f"Interview from the archive. The original on {src_name} ({p["y"]}) is no longer online — the text is restored from a page snapshot.")} '
                    f'<a href="{esc(p["meta"]["archive_url"])}" target="_blank" rel="noopener">'
                    f'{T("Снимок в Web Archive", "Знімок у Web Archive", "Snapshot in the Web Archive")} <i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i></a>'
                    f'</div></div>')
    elif p['y'] < OUTDATED_BEFORE:
        outdated = (f'<div class="b-note"><i class="fa-regular fa-clock" aria-hidden="true"></i><div>'
                    f'{T(f"Материал опубликован в {p['y']} году — описанные инструменты и интерфейсы могли измениться.", f"Матеріал опубліковано у {p['y']} році — описані інструменти та інтерфейси могли змінитися.", f"Published in {p['y']} — the tools and interfaces described may have changed since.")}'
                    f'</div></div>')
    cover_img = f'<figure class="b-cover"><img src="../{esc(p["cover"])}" alt="" width="1200" height="630" decoding="async"></figure>' if (p['cover'] and p['own_cover']) else ''
    ld = {'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': p['title'], 'datePublished': p['date'],
          'inLanguage': 'ru', 'description': p['desc'], 'author': {'@id': B.PERSON_ID},
          'mainEntityOfPage': f'{B.SITE}/blog/{p["slug"]}/'}
    page = B.head(f'blog/{p["slug"]}', f'{p["title"]} | Алексей Селезнёв', p['desc'], jsonld=ld)
    page = with_css(deep(page), '../')
    page += deep(B.nav('blog'))
    toc_block = (f'<aside class="b-toc" aria-label="Contents"><div class="b-toc-title">{T("Содержание", "Зміст", "Contents")}</div>{toc_html(tokens)}</aside>'
                 if has_toc else '')
    page += f'''
    <main class="b-wrap relative z-10">
        <nav class="b-crumbs" aria-label="breadcrumb">
            <a href="../../">{T('Главная', 'Головна', 'Home')}</a><span>/</span><a href="../">{T('Блог', 'Блог', 'Blog')}</a>{('<span>/</span><a href="../?cat=' + tslug(p['cats'][0]) + '#posts">' + esc(names[p['cats'][0]]) + '</a>') if p['cats'] else ''}
        </nav>
        <div class="b-layout{' has-toc' if has_toc else ''}">
            <article class="bento-glass no-lift b-article" data-aos="fade-up">
                <div class="bento-content">
                    <div class="b-cats">{cats}</div>
                    <h1 class="b-title outfit-font">{esc(p['title'])}</h1>
                    <div class="b-meta">
                        <span><i class="fa-regular fa-calendar" aria-hidden="true"></i>{T(*(f"{int(p['date'][8:10])} {GEN_MONTHS[l][p['m'] - 1]} {p['y']}" for l in B.LANGS))}</span>
                        <span><i class="fa-regular fa-clock" aria-hidden="true"></i>{T(f"{p['minutes']} мин чтения", f"{p['minutes']} хв читання", f"{p['minutes']} min read")}</span>
                        <span class="b-lang" title="Русский">RU</span>
                    </div>
                    {outdated}
                    {cover_img}
                    <div class="b-prose">{body}</div>
                    {source_footer}
                    <div class="b-tags">{tags}</div>
                </div>
            </article>
            {toc_block}
        </div>
        <section class="b-related">
            <h2 class="outfit-font">{T('Читайте также', 'Читайте також', 'Related posts')}</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">{related_html}</div>
        </section>
        <a href="../" class="b-back"><i class="fa-solid fa-arrow-left" aria-hidden="true"></i>{T('Ко всем материалам', 'До всіх матеріалів', 'All posts')}</a>
    </main>
'''
    page += B.cta_block() + B.footer('../../') + deep(B.tail())
    page = page.replace('</body>', ARTICLE_JS + '</body>')
    write(OUT / p['slug'] / 'index.html', page)


def update_sitemap(posts):
    """Блок /blog/ в sitemap.xml: /blog/ и все статьи (остальные адреса не трогаем). Даты берутся из постов — сборка воспроизводима."""
    path = ROOT / 'sitemap.xml'
    raw = path.read_bytes().decode('utf-8')
    crlf = '\r\n' in raw
    raw = re.sub(r'[ \t]*<url>\s*<loc>[^<]*/blog/[^<]*</loc>.*?</url>[ \t]*(?:\r?\n)?', '', raw, flags=re.S)   # только сама запись и её перевод строки

    def url(loc, last, freq, prio):
        return f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{last}</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>\n'
    newest = max(p['date'] for p in posts)
    block = url(f'{B.SITE}/blog/', newest, 'weekly', '0.8')
    for p in sorted(posts, key=lambda p: (p['date'], p['slug']), reverse=True):
        block += url(f'{B.SITE}/blog/{p["slug"]}/', p['date'], 'yearly', '0.6')
    if crlf:
        raw = raw.replace('\r\n', '\n')
    # блок блога стоит перед блоком курса (если он есть), иначе в конце: порядок не зависит от того, запускается весь build.py или только блог
    course = re.search(r'[ \t]*<url>\s*<loc>[^<]*/r_for_marketing_course/', raw)
    pos = course.start() if course else raw.index('</urlset>')
    raw = raw[:pos] + block + raw[pos:]
    path.write_bytes((raw.replace('\n', '\r\n') if crlf else raw).encode('utf-8'))


def _check_versions():
    """Предупреждает, если версии Markdown/Pygments отличаются от закреплённых в requirements.txt: тогда страницы с кодом
    соберутся иначе, чем на сервере (кавычки в блоках кода, CSS подсветки), и git покажет «лишние» изменения."""
    try:
        from importlib.metadata import version
        pins = re.findall(r'(?m)^([A-Za-z0-9_.-]+)==([^\s#]+)', (HERE / 'requirements.txt').read_text(encoding='utf-8'))
        off = [f'{name} {version(name)} (нужно {want})' for name, want in pins if version(name) != want]
    except Exception:
        return
    if off:
        print('  ВНИМАНИЕ: версии отличаются от закреплённых — ' + ', '.join(off) +
              '. Выполните: pip install -r _build/requirements.txt (иначе blog/ пересоберётся не так, как на сервере)')


def build_blog(b):
    """Точка входа для _build/build.py: b — модуль build (шаблоны сайта)."""
    global B, T, esc
    B, T, esc = b, b.T, b.esc
    _check_versions()
    posts = load_posts()
    norm = normalize(posts)
    OUT.mkdir(exist_ok=True)
    for child in OUT.iterdir():          # страницы пересобираем целиком; хранилище картинок images/ не трогаем
        if child.name != 'images':
            shutil.rmtree(child) if child.is_dir() else child.unlink()
    write(OUT / 'blog.css', blog_css())
    build_index(posts, norm)
    for p in posts:
        build_article(p, posts, norm)
    update_sitemap(posts)
    print(f'blog: {len(posts)} posts, {OUT.relative_to(ROOT).as_posix()}/')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.path.insert(0, str(HERE))
    import build as _site
    build_blog(_site)
