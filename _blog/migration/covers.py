"""Генерирует обложки для постов, у которых нет подходящей картинки, и прописывает cover в front matter.

Подходящая обложка: есть featured image или первая картинка из текста — локальный файл не меньше 500×250 и
с соотношением сторон от 1.25 до 3. Иначе рисуется собственная (шаблон cover_tpl.html, headless Chrome → WebP).
Запуск (после export.py):  python _blog_export/covers.py [--force]
"""
import concurrent.futures as cf
import json
import re
import subprocess
import sys
import tempfile
import urllib.parse
from pathlib import Path

import yaml
from PIL import Image

HERE = Path(__file__).resolve().parent
POSTS, IMAGES, TPL = HERE / 'posts', HERE / 'images', HERE / 'cover_tpl.html'
COVERS = IMAGES / 'covers'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

# порядок = приоритет: по первому подошедшему тегу выбираем иконку и главное слово обложки
ICONS = {
    'AI': 'fa-solid fa-robot', 'Claude Code': 'fa-solid fa-terminal', 'MCP': 'fa-solid fa-plug', 'ChatGPT': 'fa-solid fa-comments',
    'LLM': 'fa-solid fa-brain', 'Gemini': 'fa-solid fa-wand-magic-sparkles', 'AcpGram': 'fa-solid fa-paper-plane', 'Vibe coding': 'fa-solid fa-wand-magic-sparkles',
    'Telegram': 'fa-brands fa-telegram', 'Яндекс Директ': 'fa-solid fa-bullhorn', 'Яндекс Метрика': 'fa-solid fa-chart-line',
    'Google Ads': 'fa-solid fa-rectangle-ad', 'Google Analytics': 'fa-solid fa-chart-line', 'Facebook': 'fa-brands fa-facebook',
    'ВКонтакте': 'fa-brands fa-vk', 'myTarget': 'fa-solid fa-bullseye', 'PPC': 'fa-solid fa-bullseye', 'Веб-аналитика': 'fa-solid fa-chart-line',
    'Power BI': 'fa-solid fa-chart-column', 'Google Data Studio': 'fa-solid fa-chart-pie', 'BI': 'fa-solid fa-chart-pie',
    'Визуализация данных': 'fa-solid fa-chart-pie', 'Google Таблицы': 'fa-solid fa-table', 'Excel': 'fa-solid fa-file-excel',
    'BigQuery': 'fa-solid fa-database', 'SQL': 'fa-solid fa-database', 'Базы данных': 'fa-solid fa-server', 'Python': 'fa-brands fa-python',
    'GitHub': 'fa-brands fa-github', 'Автоматизация': 'fa-solid fa-gears', 'Параллельные вычисления': 'fa-solid fa-microchip',
    'Обработка ошибок': 'fa-solid fa-bug', 'tidyverse': 'fa-solid fa-filter', 'Обработка данных': 'fa-solid fa-filter',
    'Анализ данных': 'fa-solid fa-magnifying-glass-chart', 'Пакеты R': 'fa-solid fa-box-open', 'Импорт данных': 'fa-solid fa-file-import',
    'Вебинары': 'fa-solid fa-video', 'Выступления': 'fa-solid fa-microphone-lines', 'Интервью': 'fa-regular fa-newspaper',
    'Исследования': 'fa-solid fa-magnifying-glass-chart', 'Кейсы': 'fa-solid fa-briefcase', 'Дайджесты': 'fa-solid fa-newspaper',
    'Обучение': 'fa-solid fa-graduation-cap', 'API': 'fa-solid fa-plug', 'R': 'fa-solid fa-code',
}


def split(raw):
    _, fm, body = raw.split('---\n', 2)
    return yaml.safe_load(fm), body


def good_cover(meta, body):
    ref = meta.get('cover')
    if not ref:
        m = re.search(r'!\[[^\]]*\]\((\.\./images/[^)\s]+)', body)
        ref = m.group(1) if m else None
    if not ref:
        return False
    path = (POSTS / ref).resolve()
    try:
        with Image.open(path) as im:
            w, h = im.size
    except Exception:
        return False
    return w >= 500 and h >= 250 and 1.25 <= w / h <= 3


def spec(meta):
    tags, cats = meta.get('tags') or [], meta.get('categories') or []
    icon_tag = next((t for t in tags if t in ICONS), None)
    kw = icon_tag or (tags[0] if tags else (cats[0] if cats else 'Блог'))
    icon = ICONS.get(icon_tag) or ICONS.get(next((c for c in cats if c in ICONS), ''), 'fa-solid fa-feather-pointed')
    chips = [t for t in tags if t != kw][:3]
    cat = (cats[0] if cats else 'Блог')
    return dict(kw=kw[:18], icon=icon, cat=cat, chips=chips, year=str(meta['date'])[:4], seed=int(meta.get('wp_id', 1)))


def render(job):
    wp_id, data = job
    out = COVERS / f'{wp_id}.webp'
    png = Path(tempfile.gettempdir()) / f'cover_{wp_id}.png'
    url = TPL.as_uri() + '#' + urllib.parse.quote(json.dumps(data, ensure_ascii=False))
    for attempt in range(3):
        png.unlink(missing_ok=True)
        try:
            with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as prof:
                subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', f'--user-data-dir={prof}', '--window-size=1200,630',
                                '--virtual-time-budget=9000', f'--screenshot={png}', url], capture_output=True, timeout=60)
        except subprocess.TimeoutExpired:
            pass
        if png.exists() and png.stat().st_size > 10_000:
            break
    else:
        raise RuntimeError(f'не удалось нарисовать обложку {wp_id}')
    with Image.open(png) as im:
        im.convert('RGB').resize((1200, 630)).save(out, 'WEBP', quality=84, method=6)
    png.unlink(missing_ok=True)
    return wp_id


def main():
    COVERS.mkdir(parents=True, exist_ok=True)
    regen = '--regen' in sys.argv
    todo, attach = [], []
    for f in sorted(list(POSTS.glob('*.md')) + list((HERE / 'manual_posts').glob('*.md'))):
        meta, body = split(f.read_text(encoding='utf-8'))
        wp = meta['wp_id']
        ref = f'../images/covers/{wp}.webp'
        is_gen = meta.get('cover') == ref
        if not is_gen and good_cover(meta, body):
            continue                      # у поста уже есть нормальная картинка
        if regen or not (COVERS / f'{wp}.webp').exists():
            todo.append((wp, spec(meta)))
        if not is_gen:
            attach.append(f)
    print(f'рисуем обложек: {len(todo)}, прописываем cover в {len(attach)} постах')
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        list(ex.map(render, todo))
    for f in attach:
        meta, body = split(f.read_text(encoding='utf-8'))
        meta['cover'] = f'../images/covers/{meta["wp_id"]}.webp'
        meta['cover_generated'] = True
        fm = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False, width=1000)
        f.write_text(f'---\n{fm}---\n{body}', encoding='utf-8')
    print('готово')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
