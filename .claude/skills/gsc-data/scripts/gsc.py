#!/usr/bin/env python3
"""Чтение данных Google Search Console (только чтение). Аутентификация — сервисный аккаунт.

Ключ:   $GOOGLE_SA_KEY или ~/.config/seo-access/service-account.json  (вне репозитория, не коммитить!)
Сайт:   --site или $GSC_SITE (по умолчанию sc-domain:alexey-seleznev.pro; список доступных — команда `sites`)

Команды:
  sites                         какие ресурсы видит сервисный аккаунт
  query                         отчёт «Эффективность» (клики, показы, CTR, позиция)
  sitemaps                      карты сайта и ошибки по ним
  inspect URL [URL ...]         индексация URL (URL Inspection API)
"""
import argparse, csv, datetime as dt, json, os, re, sys
from urllib.parse import quote

SCOPE = 'https://www.googleapis.com/auth/webmasters.readonly'   # только чтение
KEY = os.environ.get('GOOGLE_SA_KEY') or os.path.expanduser('~/.config/seo-access/service-account.json')
DEFAULT_SITE = os.environ.get('GSC_SITE', 'sc-domain:alexey-seleznev.pro')


def session():
    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import AuthorizedSession
    except ImportError:
        sys.exit('Нужны пакеты: pip install google-auth requests')
    if not os.path.exists(KEY):
        sys.exit(f'Нет ключа сервисного аккаунта: {KEY}\nСм. SKILL.md, раздел «Настройка».')
    creds = service_account.Credentials.from_service_account_file(KEY, scopes=[SCOPE])
    return AuthorizedSession(creds)


def call(s, method, url, **kw):
    r = s.request(method, url, timeout=60, **kw)
    if r.status_code >= 400:
        try:
            msg = r.json().get('error', {}).get('message', r.text)
        except Exception:
            msg = r.text
        hint = ''
        if r.status_code == 403:
            hint = ('\nПроверь: сервисный аккаунт добавлен в Search Console (Настройки → Пользователи) '
                    'и API включён в проекте Google Cloud.')
        sys.exit(f'HTTP {r.status_code}: {msg}{hint}')
    return r.json()


def parse_filter(expr):
    """page~/blog/ (содержит), page!~/tag/ (не содержит), country=rus (равно), page=~^/blog/ (регулярка)."""
    m = re.match(r'^(\w+)(!~|=~|~|=)(.+)$', expr)
    if not m:
        sys.exit(f'Неверный фильтр: {expr}. Формат: измерение(=|~|!~|=~)значение')
    dim, op, val = m.groups()
    operator = {'=': 'equals', '~': 'contains', '!~': 'notContains', '=~': 'includingRegex'}[op]
    return {'dimension': dim, 'operator': operator, 'expression': val}


def out(rows, header, path=None):
    rows = [[str(x) for x in r] for r in rows]
    if path:
        with open(path, 'w', newline='', encoding='utf-8-sig') as f:
            w = csv.writer(f)
            w.writerow(header)
            w.writerows(rows)
        print(f'сохранено: {path} ({len(rows)} строк)')
    widths = [min(90, max(len(x) for x in col)) for col in zip(header, *rows)] if rows else [len(h) for h in header]
    fmt = lambda r: '  '.join(x[:90].ljust(n) for x, n in zip(r, widths))
    print(fmt(header))
    print('  '.join('-' * n for n in widths))
    for r in rows:
        print(fmt(r))


def cmd_sites(a):
    for x in call(session(), 'GET', 'https://www.googleapis.com/webmasters/v3/sites').get('siteEntry', []):
        print(f"{x['siteUrl']}\t{x['permissionLevel']}")


def cmd_query(a):
    s = session()
    end = dt.date.fromisoformat(a.end) if a.end else dt.date.today() - dt.timedelta(days=3)   # данные запаздывают на 2–3 дня
    start = dt.date.fromisoformat(a.start) if a.start else end - dt.timedelta(days=a.days - 1)
    dims = [d for d in a.dims.split(',') if d]
    body = {'startDate': start.isoformat(), 'endDate': end.isoformat(), 'dimensions': dims, 'type': a.type,
            'rowLimit': min(a.limit, 25000), 'startRow': 0}
    if a.filter:
        body['dimensionFilterGroups'] = [{'groupType': 'and', 'filters': [parse_filter(f) for f in a.filter]}]
    url = f'https://www.googleapis.com/webmasters/v3/sites/{quote(a.site, safe="")}/searchAnalytics/query'
    rows = []
    while len(rows) < a.limit:
        data = call(s, 'POST', url, json=body).get('rows', [])
        rows += data
        if len(data) < body['rowLimit']:
            break
        body['startRow'] += len(data)
    rows = rows[:a.limit]
    print(f'# {a.site}  {start}..{end}  dims={dims or "(итого)"}  type={a.type}  строк: {len(rows)}')
    table = [[*r.get('keys', []), r['clicks'], r['impressions'], f"{r['ctr'] * 100:.1f}%", f"{r['position']:.1f}"] for r in rows]
    out(table, [*dims, 'clicks', 'impressions', 'ctr', 'position'], a.csv)


def cmd_sitemaps(a):
    data = call(session(), 'GET', f'https://www.googleapis.com/webmasters/v3/sites/{quote(a.site, safe="")}/sitemaps')
    for m in data.get('sitemap', []):
        contents = ', '.join(f"{c['type']}: отправлено {c.get('submitted')}, проиндексировано {c.get('indexed', 'н/д')}"
                             for c in m.get('contents', []))
        print(f"{m['path']}  обновлена {m.get('lastDownloaded', '—')}  ошибок {m.get('errors', 0)}  "
              f"предупреждений {m.get('warnings', 0)}  [{contents}]")
    if not data.get('sitemap'):
        print('Карты сайта не отправлены.')


def cmd_inspect(a):
    s = session()
    for u in a.urls:
        r = call(s, 'POST', 'https://searchconsole.googleapis.com/v1/urlInspection/index:inspect',
                 json={'inspectionUrl': u, 'siteUrl': a.site, 'languageCode': 'ru'})['inspectionResult']
        ix = r.get('indexStatusResult', {})
        print(f'\n== {u}')
        for k in ['verdict', 'coverageState', 'indexingState', 'robotsTxtState', 'pageFetchState', 'lastCrawlTime',
                  'crawledAs', 'googleCanonical', 'userCanonical']:
            print(f'  {k}: {ix.get(k, "—")}')
        for key in ('mobileUsabilityResult', 'richResultsResult'):
            if key in r:
                print(f'  {key}: {json.dumps(r[key], ensure_ascii=False)[:300]}')


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--site', default=DEFAULT_SITE, help='ресурс Search Console (sc-domain:... или https://.../)')
    sub = p.add_subparsers(dest='cmd', required=True)
    sub.add_parser('sites').set_defaults(f=cmd_sites)
    q = sub.add_parser('query')
    q.set_defaults(f=cmd_query)
    q.add_argument('--dims', default='query', help='query,page,country,device,date,searchAppearance через запятую; пусто = итого')
    q.add_argument('--days', type=int, default=28)
    q.add_argument('--start')
    q.add_argument('--end')
    q.add_argument('--filter', action='append', help='page~/blog/  country=rus  query!~слово  (можно несколько)')
    q.add_argument('--type', default='web', choices=['web', 'image', 'video', 'news', 'discover', 'googleNews'])
    q.add_argument('--limit', type=int, default=50)
    q.add_argument('--csv', help='сохранить в CSV (вне репозитория!)')
    sub.add_parser('sitemaps').set_defaults(f=cmd_sitemaps)
    i = sub.add_parser('inspect')
    i.set_defaults(f=cmd_inspect)
    i.add_argument('urls', nargs='+')
    a = p.parse_args()
    a.f(a)


if __name__ == '__main__':
    main()
