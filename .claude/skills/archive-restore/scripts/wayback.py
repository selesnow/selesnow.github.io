#!/usr/bin/env python
"""Ищет снимок страницы в Web Archive через API availability.

    python wayback.py https://example.com/old-article            # ближайший снимок к сегодняшнему дню
    python wayback.py https://example.com/old-article 201905     # ближайший к маю 2019 (ГГГГММ[ДД])
    python wayback.py urls.txt 202001                            # файл со списком адресов (по одному в строке)

Печатает по строке на адрес: статус, дату снимка и готовую ссылку вида
https://web.archive.org/web/<ГГГГММДДччммсс>/<исходный URL>.

Зачем API, а не прямой запрос к web.archive.org: с этой машины прямые запросы к web.archive.org блокируются
как бот-трафик, а API archive.org/wayback/available отвечает нормально. Сами страницы снимков по ссылке
открываются у пользователя в браузере. Статус 200 у API означает «снимок найден», а не «страница доступна».
"""
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


def lookup(url, ts=''):
    q = 'https://archive.org/wayback/available?url=' + urllib.parse.quote(url, safe='') + (f'&timestamp={ts}' if ts else '')
    last = None
    for attempt in range(3):   # API иногда отвечает таймаутом, повтор обычно помогает
        try:
            req = urllib.request.Request(q, headers={'User-Agent': 'wayback-check'})
            with urllib.request.urlopen(req, timeout=30) as r:
                snap = json.load(r).get('archived_snapshots', {}).get('closest')
            if snap and snap.get('available'):
                stamp = snap['timestamp']
                return 'OK', stamp, f'https://web.archive.org/web/{stamp}/{url}', snap.get('status')
            return 'НЕТ СНИМКА', '', '', ''
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            last = type(e).__name__
            time.sleep(2 * (attempt + 1))
    return f'ОШИБКА API ({last})', '', '', ''


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src, ts = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else '')
    urls = Path(src).read_text(encoding='utf-8').split() if Path(src).is_file() else [src]
    for u in urls:
        state, stamp, link, http = lookup(u, ts)
        print(f'{state}\t{stamp}\t{http}\t{link or u}')


if __name__ == '__main__':
    main()
