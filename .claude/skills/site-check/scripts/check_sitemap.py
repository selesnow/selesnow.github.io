#!/usr/bin/env python
"""Проверяет, что все адреса из sitemap.xml отдают 200.

    python check_sitemap.py                          # боевой сайт (после пуша и сборки Pages)
    python check_sitemap.py --base http://localhost:8765   # локальный сервер (его нужно поднять самому)

Код возврата 1, если есть адреса не с 200. Используется urllib, а не curl: у curl на этой машине
бывают проблемы с проверкой отзыва сертификатов.
"""
import argparse
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def status(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'site-check'})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:   # сеть, таймаут
        return f'{type(e).__name__}'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', help='подменить https://alexey-seleznev.pro на другой хост')
    a = ap.parse_args()
    xml = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
    urls = re.findall(r'<loc>([^<]+)</loc>', xml)
    if a.base:
        urls = [re.sub(r'^https?://[^/]+', a.base.rstrip('/'), u) for u in urls]
    with ThreadPoolExecutor(8) as ex:
        results = list(zip(urls, ex.map(status, urls)))
    bad = [(u, s) for u, s in results if s != 200]
    print(f'Адресов: {len(urls)}, не 200: {len(bad)}')
    for u, s in bad:
        print(f'  {s}  {u}')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
