#!/usr/bin/env python3
"""Плашка «статья перенесена» в начале записей старого блога на WordPress.com.

Старый блог: alexeyseleznev.wordpress.com. Для каждой записи, у которой в _blog/posts/*.md есть original_url,
добавляет в начало записи ссылку на новый адрес https://alexey-seleznev.pro/blog/<slug>/.

Токен и данные приложения лежат ВНЕ репозитория: ~/.config/seo-access/wpcom_token.json (не коммитить!).
Перед правкой оригинал записи сохраняется в ~/.config/seo-access/wp-backups/<ID>.json.

  python _blog/migration/wp_notice.py                    сухой прогон: список записей и текст плашки, ничего не меняется
  python _blog/migration/wp_notice.py --apply 1234       добавить плашку в одну запись (ID записи)
  python _blog/migration/wp_notice.py --apply all        во все сопоставленные записи (повторный запуск безопасен)
  python _blog/migration/wp_notice.py --restore 1234|all вернуть оригинал из резервной копии
"""
import argparse, glob, json, os, re, sys, time
import urllib.parse as up
import requests

HOME = os.path.expanduser('~/.config/seo-access')
TOKEN = json.load(open(os.path.join(HOME, 'wpcom_token.json'), encoding='utf-8'))
BACKUPS = os.path.join(HOME, 'wp-backups')
H = {'Authorization': 'Bearer ' + TOKEN['access_token']}
V11 = f"https://public-api.wordpress.com/rest/v1.1/sites/{TOKEN['blog_id']}"
V2 = f"https://public-api.wordpress.com/wp/v2/sites/{TOKEN['blog_id']}"
SITE = 'https://alexey-seleznev.pro'
MARK = '<!-- moved-notice -->'
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def notice(slug):
    url = f'{SITE}/blog/{slug}/'
    return (f'{MARK}<p style="padding:12px 16px;border-left:4px solid #8b5cf6;background:#f5f3ff;">'
            f'<strong>Эта статья перенесена на новый сайт.</strong> Актуальная версия: '
            f'<a href="{url}">{url}</a></p>\n')


def key(u):
    return up.unquote(u).rstrip('/').lower()


def mapping():
    m = {}
    for f in glob.glob(os.path.join(ROOT, '_blog', 'posts', '*.md')):
        fm = open(f, encoding='utf-8').read().split('---\n', 2)[1]
        u, s = re.search(r'original_url: (\S+)', fm), re.search(r'slug: (\S+)', fm)
        if u and s:
            m[key(u.group(1))] = s.group(1)
    return m


def old_posts():
    posts, page = [], 1
    while True:
        r = requests.get(V11 + '/posts', headers=H, timeout=60, params={
            'number': 100, 'page': page, 'status': 'publish', 'type': 'post', 'fields': 'ID,URL,title,date'})
        r.raise_for_status()
        d = r.json().get('posts', [])
        posts += d
        if len(d) < 100:
            return posts
        page += 1


def raw(pid):
    r = requests.get(f'{V2}/posts/{pid}', headers=H, params={'context': 'edit'}, timeout=60)
    r.raise_for_status()
    return r.json()['content']['raw']


def put(pid, content):
    r = requests.post(f'{V2}/posts/{pid}', headers=H, json={'content': content}, timeout=60)
    r.raise_for_status()


def plan():
    m = mapping()
    out = [(p, m[key(p['URL'])]) for p in old_posts() if key(p['URL']) in m]
    return out


def apply_one(p, slug):
    pid = p['ID']
    content = raw(pid)
    if MARK in content:
        return 'уже есть'
    os.makedirs(BACKUPS, exist_ok=True)
    path = os.path.join(BACKUPS, f'{pid}.json')
    if not os.path.exists(path):
        json.dump({'ID': pid, 'URL': p['URL'], 'content': content}, open(path, 'w', encoding='utf-8'), ensure_ascii=False)
    put(pid, notice(slug) + content)
    return 'добавлено'


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument('--apply', metavar='ID|all')
    a.add_argument('--restore', metavar='ID|all')
    a = a.parse_args()
    if a.restore:
        files = glob.glob(os.path.join(BACKUPS, '*.json')) if a.restore == 'all' else [os.path.join(BACKUPS, f'{a.restore}.json')]
        for f in files:
            b = json.load(open(f, encoding='utf-8'))
            put(b['ID'], b['content'])
            print('восстановлено', b['ID'], b['URL'])
        return
    items = plan()
    if not a.apply:
        print(f'Сухой прогон. Записей к правке: {len(items)}. Ничего не изменено.\n')
        print('Плашка (пример):\n' + notice(items[0][1]) if items else 'нет сопоставленных записей')
        for p, slug in items[:10]:
            print(f"  {p['ID']:>5}  {p['date'][:10]}  {p['title'][:50]:<50} -> /blog/{slug}/")
        print('  ...')
        return
    todo = items if a.apply == 'all' else [(p, s) for p, s in items if str(p['ID']) == a.apply]
    if not todo:
        sys.exit('Запись не найдена среди сопоставленных.')
    for p, slug in todo:
        print(p['ID'], apply_one(p, slug), '->', f'/blog/{slug}/')
        time.sleep(0.5)


if __name__ == '__main__':
    main()
