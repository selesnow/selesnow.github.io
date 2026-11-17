"""Импорт экспертной подборки Netpeak Blog (2016) из сохранённой страницы Web Archive → manual_posts/*.md.

Страница сохранена браузером в raw/netpeak/ («Веб-страница полностью»); фото экспертов в архиве не сохранились,
поэтому у каждого эксперта — аватар-круг с инициалами (как в оригинале — круглые аватарки). Если для эксперта есть фото
(AVATAR_PHOTOS), вместо инициалов подставляется оно.

Запуск:  python _blog_export/netpeak_import.py
"""
import glob
import html
import re
import shutil
import sys
from pathlib import Path

import yaml
from bs4 import BeautifulSoup
from markdownify import markdownify

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RAW = HERE / 'raw' / 'netpeak'
OUT = HERE / 'manual_posts'
IMGS = HERE / 'images_orig'

ARCHIVE_URL = 'https://web.archive.org/web/20161230185556/https://netpeak.net/ru/blog/chto-delayut-internet-marketologi-pod-novyi-god/'
ORIGINAL_URL = 'https://netpeak.net/ru/blog/chto-delayut-internet-marketologi-pod-novyi-god/'
WAYBACK = re.compile(r'^(?:https?://web\.archive\.org)?/web/\d+[a-z_]*/(https?://.+)$')

# имя эксперта → файл с фото (в images_orig). Собственное фото владельца сайта берём с сайта; остальные — только с разрешения.
AVATAR_PHOTOS = {
    # имя → (откуда берём: файл в raw/netpeak/photos/ или в корне сайта, имя в images_orig). Источники — в raw/netpeak/photo_sources.md
    'Алексей Селезнев': ('photo.jpg', 'netpeak-seleznev.jpg'),                    # собственное фото владельца сайта
    'Наталья Воскобойникова': ('photos/voskoboynikova.jpg', 'netpeak-voskoboynikova.jpg'),
    'Денис Рудик': ('photos/rudik.jpg', 'netpeak-rudik.jpg'),
    'Роман Скрупник': ('photos/skrupnyk.png', 'netpeak-skrupnyk.png'),
}


def clean_href(href):
    m = WAYBACK.match(href or '')
    return m.group(1) if m else href


def initials(name):
    parts = [p for p in re.split(r'\s+', name.strip()) if p]
    return ''.join(p[0] for p in parts[:2]).upper()


def inline_html(el):
    """Содержимое элемента как HTML-строка со ссылками, развёрнутыми из Web Archive в исходные адреса."""
    for a in el.find_all('a'):
        href = clean_href(a.get('href', ''))
        if href and href.startswith('http'):
            a['href'] = href
            a['target'] = '_blank'
            a['rel'] = 'noopener'
        else:
            a.unwrap()
    return el.decode_contents().strip()


def expert_block(div):
    head = div.find('p')
    strong = head.find('strong')
    name = strong.get_text(strip=True)
    strong.extract()
    role = inline_html(head).lstrip(',').strip().rstrip('.').strip()
    if name in AVATAR_PHOTOS:
        src, dst = AVATAR_PHOTOS[name]
        shutil.copy2(RAW / src if (RAW / src).exists() else ROOT / src, IMGS / dst)
        avatar = f'<span class="b-avatar"><img src="../images/{Path(dst).stem}.webp" alt="{html.escape(name)}"></span>'
    else:
        avatar = f'<span class="b-avatar b-avatar-initials" aria-hidden="true">{html.escape(initials(name))}</span>'
    return (f'<div class="b-expert">{avatar}<div class="b-expert-id"><strong>{html.escape(name)}</strong>'
            f'<span>{role}</span></div></div>')


def main():
    page = glob.glob(str(RAW / 'Что делают*.html'))[0]
    soup = BeautifulSoup(open(page, encoding='utf-8', errors='replace').read(), 'html.parser')
    title = soup.find('meta', property='og:title')['content'].strip()
    desc = soup.find('meta', property='og:description')['content'].strip()
    c = soup.select_one('div.blog-post-content')
    for t in c.select('script, style, svg, iframe'):
        t.decompose()      # встроенное видео (gifs.com) в архиве не сохранилось

    parts, experts = [], []
    skip = ('post-share', 'clear', 'post-source', 'post-rating', 'post-tags', 'post-author', 'post-subscribe')
    for el in c.find_all(recursive=False):
        classes = el.get('class') or []
        if any(k in classes for k in skip) or el.name == 'hr':
            continue
        if 'quote-color-0' in classes:
            parts.append(expert_block(el))
            experts.append(parts[-1])
            for p in el.find_all('p')[1:]:      # первый <p> — имя и должность, он уже выведен блоком эксперта
                txt = markdownify(inline_html_wrap(p), heading_style='ATX').strip()
                if txt:
                    parts.append(txt)
            continue
        text = el.get_text(' ', strip=True)
        if not text:
            continue
        if el.name == 'p':
            if text.startswith('Вопрос к экспертам'):
                parts.append(f'<p class="b-q">{html.escape(text)}</p>')
                continue
            parts.append(markdownify(inline_html_wrap(el), heading_style='ATX').strip())

    for i, part in enumerate(parts):      # после «От редактора…:» в оригинале шло видео, которого нет в архиве — поясняем, чтобы фраза не повисала
        if part.startswith('**От редактора**'):
            parts.insert(i + 1, '<p class="b-caption">(Видео, встроенное в оригинал, в архиве не сохранилось.)</p>')
            break

    meta = {
        'title': title,
        'date': '2016-12-29',
        'slug': 'chto-delayut-internet-marketologi-pod-novyi-god',
        'tags': ['Интервью', 'Итоги года', 'Веб-аналитика'],
        'categories': ['Интервью'],
        'description': desc,
        'original_url': ORIGINAL_URL,
        'archive_url': ARCHIVE_URL,
        'source_name': 'Netpeak Blog',
        'wp_id': 900002,
        'draft': False,
    }
    OUT.mkdir(exist_ok=True)
    out = OUT / '2016-12-29-chto-delayut-internet-marketologi-pod-novyi-god.md'
    fm = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False, width=1000)
    out.write_text(f'---\n{fm}---\n\n' + '\n\n'.join(parts) + '\n', encoding='utf-8')
    print('записано:', out.name, '| блоков:', len(parts), '| экспертов:', len(experts))


def inline_html_wrap(p):
    """Подготавливает <p> к markdownify: ссылки из Web Archive → исходные адреса."""
    for a in p.find_all('a'):
        href = clean_href(a.get('href', ''))
        if href and href.startswith('http'):
            a['href'] = href
        else:
            a.unwrap()
    return str(p)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
