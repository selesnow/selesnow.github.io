#!/usr/bin/env python3
"""Чтение данных Google Analytics 4 (только чтение). Аутентификация — сервисный аккаунт.

Ключ:     $GOOGLE_SA_KEY или ~/.config/seo-access/service-account.json  (вне репозитория, не коммитить!)
Ресурс:   --property или $GA4_PROPERTY (числовой ID ресурса GA4; список доступных — команда `properties`)

Команды:
  properties                         какие ресурсы GA4 видит сервисный аккаунт
  preset NAME                        готовый отчёт: countries languages channels sources landing pages devices daily ai
  report --dims A,B --metrics X,Y    произвольный отчёт
"""
import argparse, csv, os, re, sys

SCOPE = 'https://www.googleapis.com/auth/analytics.readonly'    # только чтение
KEY = os.environ.get('GOOGLE_SA_KEY') or os.path.expanduser('~/.config/seo-access/service-account.json')
PROPERTY = os.environ.get('GA4_PROPERTY', '')

AI_RE = r'chatgpt|openai|perplexity|claude|anthropic|gemini|copilot|bard|you\.com|phind|kagi|deepseek|grok'
SESS = 'sessions,activeUsers,engagedSessions'
PRESETS = {
    'countries': ('country', SESS, []),
    'languages': ('language', SESS, []),
    'channels': ('sessionDefaultChannelGroup', SESS, []),
    'sources': ('sessionSource,sessionMedium', SESS, []),
    'landing': ('landingPagePlusQueryString', SESS, []),
    'pages': ('pagePath', 'screenPageViews,activeUsers,averageSessionDuration', []),
    'devices': ('deviceCategory', SESS, []),
    'daily': ('date', 'sessions,activeUsers,screenPageViews', []),
    'ai': ('sessionSource,landingPagePlusQueryString', SESS, [f'sessionSource=~{AI_RE}']),
}


def session():
    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import AuthorizedSession
    except ImportError:
        sys.exit('Нужны пакеты: pip install google-auth requests')
    if not os.path.exists(KEY):
        sys.exit(f'Нет ключа сервисного аккаунта: {KEY}\nСм. SKILL.md, раздел «Настройка».')
    return AuthorizedSession(service_account.Credentials.from_service_account_file(KEY, scopes=[SCOPE]))


def call(s, method, url, **kw):
    r = s.request(method, url, timeout=60, **kw)
    if r.status_code >= 400:
        try:
            msg = r.json().get('error', {}).get('message', r.text)
        except Exception:
            msg = r.text
        hint = ('\nПроверь: сервисный аккаунт добавлен в GA4 (Администратор → Управление доступом, роль «Просмотр») '
                'и включены API.') if r.status_code == 403 else ''
        sys.exit(f'HTTP {r.status_code}: {msg}{hint}')
    return r.json()


def filt(expr):
    """sessionSource~google (содержит), country=Ukraine (точно), sessionSource=~chatgpt|claude (регулярка)."""
    m = re.match(r'^(\w+)(=~|~|=)(.+)$', expr)
    if not m:
        sys.exit(f'Неверный фильтр: {expr}. Формат: измерение(=|~|=~)значение')
    dim, op, val = m.groups()
    mt = {'=': 'EXACT', '~': 'CONTAINS', '=~': 'PARTIAL_REGEXP'}[op]
    return {'filter': {'fieldName': dim, 'stringFilter': {'matchType': mt, 'value': val, 'caseSensitive': False}}}


def table(rows, header, path=None):
    if path:
        with open(path, 'w', newline='', encoding='utf-8-sig') as f:
            w = csv.writer(f)
            w.writerow(header)
            w.writerows(rows)
        print(f'сохранено: {path} ({len(rows)} строк)')
    w = [min(90, max(len(x) for x in col)) for col in zip(header, *rows)] if rows else [len(h) for h in header]
    fmt = lambda r: '  '.join(x[:90].ljust(n) for x, n in zip(r, w))
    print(fmt(header))
    print('  '.join('-' * n for n in w))
    for r in rows:
        print(fmt(r))


def run_report(a, dims, metrics, filters):
    if not a.property:
        sys.exit('Не задан ресурс: --property ID или переменная GA4_PROPERTY (ID видно в команде `properties`).')
    first_metric = metrics.split(',')[0]
    body = {'dateRanges': [{'startDate': a.start or f'{a.days}daysAgo', 'endDate': a.end or 'yesterday'}],
            'dimensions': [{'name': d} for d in dims.split(',') if d],
            'metrics': [{'name': m} for m in metrics.split(',')],
            'limit': a.limit, 'orderBys': [{'metric': {'metricName': first_metric}, 'desc': True}]}
    if dims == 'date':
        body['orderBys'] = [{'dimension': {'dimensionName': 'date'}}]
    fs = [filt(f) for f in filters]
    if fs:
        body['dimensionFilter'] = fs[0] if len(fs) == 1 else {'andGroup': {'expressions': fs}}
    data = call(session(), 'POST', f'https://analyticsdata.googleapis.com/v1beta/properties/{a.property}:runReport', json=body)
    rows = [[*(d['value'] for d in r.get('dimensionValues', [])), *(m['value'] for m in r['metricValues'])]
            for r in data.get('rows', [])]
    rng = body['dateRanges'][0]
    print(f"# property {a.property}  {rng['startDate']}..{rng['endDate']}  всего строк: {data.get('rowCount', 0)}")
    table(rows, [*[d for d in dims.split(',') if d], *metrics.split(',')], a.csv)


def cmd_properties(a):
    data = call(session(), 'GET', 'https://analyticsadmin.googleapis.com/v1beta/accountSummaries')
    for acc in data.get('accountSummaries', []):
        for p in acc.get('propertySummaries', []):
            print(f"{p['property'].split('/')[-1]}\t{p.get('displayName')}\t(аккаунт: {acc.get('displayName')})")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--property', default=PROPERTY)
    sub = p.add_subparsers(dest='cmd', required=True)
    sub.add_parser('properties')
    for name in ('preset', 'report'):
        q = sub.add_parser(name)
        q.add_argument('--days', type=int, default=28)
        q.add_argument('--start')
        q.add_argument('--end')
        q.add_argument('--filter', action='append', default=[])
        q.add_argument('--limit', type=int, default=50)
        q.add_argument('--csv', help='сохранить в CSV (вне репозитория!)')
    sub.choices['preset'].add_argument('name', choices=sorted(PRESETS))
    sub.choices['report'].add_argument('--dims', default='')
    sub.choices['report'].add_argument('--metrics', default='sessions,activeUsers')
    a = p.parse_args()
    if a.cmd == 'properties':
        cmd_properties(a)
    elif a.cmd == 'preset':
        d, m, f = PRESETS[a.name]
        run_report(a, d, m, [*f, *a.filter])
    else:
        run_report(a, a.dims, a.metrics, a.filter)


if __name__ == '__main__':
    main()
