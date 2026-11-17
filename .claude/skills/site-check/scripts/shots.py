#!/usr/bin/env python
"""Скриншоты страниц сайта через headless Chrome при разных ширинах окна.

Сам поднимает `python -m http.server` из корня репозитория и гарантированно гасит его в конце
(на Windows нет pkill, а забытый сервер держит порт).

    python shots.py                       # главная, 1440 и 1920 px (в Git Bash главная = «home»: одиночный «/» MSYS ломает)
    python shots.py blog courses          # свои страницы (в Git Bash пишите без ведущего «/»:
                                          # MSYS превращает «/blog/» в «C:/Program Files/Git/blog/»)
    python shots.py /blog/ -w 1280 1920 -H 1400

Печатает пути к PNG — их можно открыть инструментом Read.
"""
import argparse
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]   # .claude/skills/site-check/scripts -> корень репозитория
CHROME_CANDIDATES = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    '/usr/bin/google-chrome', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
]


def find_chrome():
    for c in [os.environ.get('CHROME'), *CHROME_CANDIDATES, shutil.which('google-chrome'), shutil.which('chromium')]:
        if c and Path(c).exists():
            return c
        if c and shutil.which(c):
            return shutil.which(c)
    sys.exit('Chrome не найден: задайте переменную окружения CHROME')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('paths', nargs='*', default=['/'])
    ap.add_argument('-w', '--widths', nargs='+', type=int, default=[1440, 1920])
    ap.add_argument('-H', '--height', type=int, default=900)
    ap.add_argument('--port', type=int, default=0, help='0 = свободный порт (по умолчанию), чтобы не мешать уже запущенным серверам')
    ap.add_argument('--out', default=None, help='папка для PNG (по умолчанию временная)')
    a = ap.parse_args()

    chrome = find_chrome()
    if not a.port:
        with socket.socket() as sk:
            sk.bind(('127.0.0.1', 0))
            a.port = sk.getsockname()[1]
    out = Path(a.out) if a.out else Path(tempfile.mkdtemp(prefix='site-shots-'))
    out.mkdir(parents=True, exist_ok=True)
    server = subprocess.Popen([sys.executable, '-m', 'http.server', str(a.port)], cwd=ROOT,
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(1.5)
        for p in a.paths:
            p = '/' if p in ('home', '.') or not p.strip('/') else '/' + p.strip('/') + '/'   # «blog», «/blog» и «blog/» — одно и то же
            slug = p.strip('/').replace('/', '_') or 'home'
            for w in a.widths:
                png = out / f'{slug}-{w}.png'
                subprocess.run([chrome, '--headless', '--disable-gpu', '--hide-scrollbars',
                                f'--window-size={w},{a.height}', '--virtual-time-budget=6000',
                                f'--screenshot={png}', f'http://localhost:{a.port}{p}'],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90)
                print(png if png.exists() else f'НЕ УДАЛОСЬ: {p} @ {w}')
    finally:
        server.terminate()
        try:
            server.wait(5)
        except subprocess.TimeoutExpired:
            server.kill()


if __name__ == '__main__':
    main()
