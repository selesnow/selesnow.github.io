"""Импорт интервью JMS University из сохранённой страницы Web Archive → manual_posts/*.md (+ картинки в images_orig/).

Страница сохранена браузером в raw/jms/ («Веб-страница полностью»); сам Web Archive с сервера недоступен (блокирует ботов).
Запуск:  python _blog_export/jms_import.py
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
RAW = HERE / 'raw' / 'jms'
OUT = HERE / 'manual_posts'
IMGS = HERE / 'images_orig'

ARCHIVE_URL = 'https://web.archive.org/web/20201027182639/https://jms.university/blog/52849-yazyk-r-dlya-analitikov-i-internet-marketologov/'
ORIGINAL_URL = 'https://jms.university/blog/52849-yazyk-r-dlya-analitikov-i-internet-marketologov/'
WAYBACK = re.compile(r'^(?:https?://web\.archive\.org)?/web/\d+[a-z_]*/(https?://.+)$')


def clean_href(href):
    m = WAYBACK.match(href or '')
    return m.group(1) if m else href


def question_text(el):
    q = el.select_one('.attention-block.question') or el
    for t in q.select('svg, script, style'):
        t.decompose()
    return re.sub(r'\s+', ' ', q.get_text(' ', strip=True)).replace(' ,', ',').replace(' ?', '?')


def main():
    page = glob.glob(str(RAW / 'Язык R для*.html'))[0]
    files = Path(page[:-5] + '_files')
    soup = BeautifulSoup(open(page, encoding='utf-8', errors='replace').read(), 'html.parser')
    art = soup.select_one('article.post-52849')
    title = art.select_one('h1').get_text(strip=True)
    for t in art.select('svg, script, style'):
        t.decompose()
    body_el = max(art.find_all(['div', 'section']), key=lambda d: len(d.find_all('p', recursive=False)))
    desc = html.unescape(soup.find('meta', property='og:description')['content']).strip()

    parts, skipped = [], []
    for el in body_el.find_all(recursive=False):
        classes = el.get('class') or []
        if 'toc-block' in classes or 'entry-meta-author' in classes:
            continue
        if el.select_one('.attention-block.question') or 'question' in classes:
            parts.append(f'<p class="b-q">{html.escape(question_text(el))}</p>')
            continue
        for a in el.find_all('a'):
            href = clean_href(a.get('href', ''))
            if not href or href.startswith(('#', './', 'javascript')) or 'mihdan_infinite' in ' '.join(a.get('class') or []):
                a.unwrap()
            else:
                a['href'] = href
        if el.name == 'h2':
            parts.append('## ' + re.sub(r'\s*↑\s*$', '', el.get_text(' ', strip=True)))
        elif el.name in ('p', 'ul', 'ol'):
            txt = markdownify(str(el), heading_style='ATX', bullets='-').strip()
            if txt:
                parts.append(txt)
        elif el.name == 'figure':
            img = el.find('img')
            src = Path(img.get('src', '')).name if img else ''
            local = files / src
            if src and local.exists():
                name = 'jms-' + re.sub(r'[^\w.\-]+', '_', src)
                shutil.copy2(local, IMGS / name)
                cap = el.find('figcaption')
                alt = (img.get('alt') or '').strip()
                parts.append(f'![{alt}](../images/{Path(name).stem}.webp)')
                if cap and cap.get_text(strip=True):
                    parts.append(f'<p class="b-caption">{html.escape(cap.get_text(strip=True))}</p>')
            else:
                skipped.append(src or '(без src)')
        # прочее (теги, лайки, «предыдущая статья», комментарии) — служебное, не копируем

    meta = {
        'title': title,
        'date': '2020-08-26',
        'slug': 'yazyk-r-dlya-analitikov-i-internet-marketologov',
        'tags': ['Интервью', 'R', 'Веб-аналитика', 'Python', 'Excel', 'Обучение'],
        'categories': ['Интервью', 'R'],
        'description': re.sub(r'\*\*|\s+', lambda m: ' ' if m.group(0) != '**' else '', parts[0]).strip() or desc,   # og:description в источнике обрезан
        'original_url': ORIGINAL_URL,
        'archive_url': ARCHIVE_URL,
        'source_name': 'JMS University',
        'wp_id': 900001,
        'draft': False,
    }
    OUT.mkdir(exist_ok=True)
    out = OUT / '2020-08-26-yazyk-r-dlya-analitikov-i-internet-marketologov.md'
    fm = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False, width=1000)
    out.write_text(f'---\n{fm}---\n\n' + '\n\n'.join(parts) + '\n', encoding='utf-8')
    print('записано:', out.name, '— блоков:', len(parts), '| пропущены картинки:', skipped)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
