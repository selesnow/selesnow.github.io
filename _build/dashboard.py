#!/usr/bin/env python3
"""Дашборд эффективности сайта: /dashboard/ (служебная страница, noindex, без ссылок и без записи в sitemap).

Данные берутся из Search Console и GA4 через навыки `.claude/skills/gsc-data` и `ga4-data` (сервисный аккаунт, только чтение).
Ключ лежит ВНЕ репозитория (~/.config/seo-access/service-account.json), поэтому скрипт запускается локально и НЕ входит в ночной workflow.
В страницу попадают только агрегированные числа: ни ключей, ни токенов, ни персональных данных.

  python _build/dashboard.py            обновить данные и пересобрать dashboard/index.html
  python _build/dashboard.py --index    дополнительно проверить индексацию всех URL из sitemap (URL Inspection API, ~1–2 мин)
                                        и добавить снимок в dashboard/history.json (раз в 2–4 недели)
  python _build/dashboard.py --offline  пересобрать страницу из сохранённых dashboard/data.json (без обращения к Google)

Переменная GA4_PROPERTY переопределяет ID ресурса GA4; по умолчанию 282495698.
"""
import argparse, datetime as dt, importlib.util, json, os, re, sys, time
from collections import defaultdict
from urllib.parse import quote

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = os.path.join(ROOT, 'dashboard')
SKILLS = os.path.join(ROOT, '.claude', 'skills')
SITE = 'https://alexey-seleznev.pro'
GSC_SITE = os.environ.get('GSC_SITE', 'sc-domain:alexey-seleznev.pro')
GA4_PROPERTY = os.environ.get('GA4_PROPERTY', '282495698')
AI_RE = r'chatgpt|openai|perplexity|claude|anthropic|gemini|copilot|bard|you\.com|phind|kagi|deepseek|grok'

# Правки сайта: вертикальные линии на графиках, чтобы видеть эффект. Добавляй новые строки сюда.
EVENTS = [
    ('2026-11-21', 'SEO-правки блога, llms.txt'),
    ('2026-11-22', 'Плашки и запись о переезде на старом блоге'),
]
# Точка отсчёта на 21.11.2026 (Search Console 2026-08-21..2026-11-18, GA4 за 90 дней до 20.11.2026)
BASELINE = {'date': '2026-11-21', 'gsc_clicks': 2, 'gsc_impressions': 192, 'gsc_position': 10.3,
            'ga_organic': 787, 'ga_google': 186, 'ga_ai': 3, 'ga_sessions': 2233}


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(SKILLS, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


gsc = load('gsc', 'gsc-data/scripts/gsc.py')
ga4 = load('ga4', 'ga4-data/scripts/ga4.py')
_gs, _ga = None, None


def gsc_query(start, end, dims=(), limit=1000, filters=()):
    global _gs
    _gs = _gs or gsc.session()
    body = {'startDate': start.isoformat(), 'endDate': end.isoformat(), 'dimensions': list(dims), 'type': 'web',
            'rowLimit': min(limit, 25000), 'startRow': 0}
    if filters:
        body['dimensionFilterGroups'] = [{'groupType': 'and', 'filters': [gsc.parse_filter(f) for f in filters]}]
    url = f'https://www.googleapis.com/webmasters/v3/sites/{quote(GSC_SITE, safe="")}/searchAnalytics/query'
    return gsc.call(_gs, 'POST', url, json=body).get('rows', [])


def ga_report(start, end, dims, metrics, filters=(), limit=10000):
    global _ga
    _ga = _ga or ga4.session()
    body = {'dateRanges': [{'startDate': start.isoformat(), 'endDate': end.isoformat()}],
            'dimensions': [{'name': d} for d in dims], 'metrics': [{'name': m} for m in metrics], 'limit': limit}
    fs = [ga4.filt(f) for f in filters]
    if fs:
        body['dimensionFilter'] = fs[0] if len(fs) == 1 else {'andGroup': {'expressions': fs}}
    data = ga4.call(_ga, 'POST', f'https://analyticsdata.googleapis.com/v1beta/properties/{GA4_PROPERTY}:runReport', json=body)
    return [([d['value'] for d in r.get('dimensionValues', [])], [float(m['value']) for m in r['metricValues']])
            for r in data.get('rows', [])]


def safe(label, fn, default=None):
    try:
        return fn()
    except SystemExit as e:           # gsc.call / ga4.call завершаются через sys.exit(сообщение)
        print(f'  ! {label}: {e}', file=sys.stderr)
    except Exception as e:
        print(f'  ! {label}: {type(e).__name__}: {e}', file=sys.stderr)
    return default


def totals(rows):
    r = rows[0] if rows else {'clicks': 0, 'impressions': 0, 'ctr': 0, 'position': 0}
    return {'clicks': r['clicks'], 'impressions': r['impressions'], 'ctr': r['ctr'], 'position': r['position']}


def week_start(d):
    d = dt.date.fromisoformat(d)
    return (d - dt.timedelta(days=d.weekday())).isoformat()


def collect():
    today = dt.date.today()
    g_end = today - dt.timedelta(days=3)               # Search Console запаздывает на 2–3 дня
    a_end = today - dt.timedelta(days=1)
    d28 = lambda end, n=28, back=0: (end - dt.timedelta(days=back + n - 1), end - dt.timedelta(days=back))
    D = {'generated': dt.datetime.now().strftime('%Y-%m-%d %H:%M'), 'gsc_end': g_end.isoformat(), 'ga_end': a_end.isoformat(),
         'events': EVENTS, 'baseline': BASELINE}
    print('Search Console…')
    cur, prev = d28(g_end), d28(g_end, back=28)
    D['gsc_cur'] = safe('gsc cur', lambda: totals(gsc_query(*cur)))
    D['gsc_prev'] = safe('gsc prev', lambda: totals(gsc_query(*prev)))
    D['gsc_90'] = safe('gsc 90', lambda: totals(gsc_query(*d28(g_end, 90))))
    D['gsc_daily'] = safe('gsc daily', lambda: [[r['keys'][0], r['clicks'], r['impressions']] for r in
                                                 sorted(gsc_query(*d28(g_end, 180), dims=['date']), key=lambda r: r['keys'][0])], [])
    pick = lambda dim, n: safe(f'gsc {dim}', lambda: [[r['keys'][0], r['clicks'], r['impressions'], round(r['position'], 1)] for r in
                                                       sorted(gsc_query(*d28(g_end, 90), dims=[dim]), key=lambda r: -r['impressions'])[:n]], [])
    D['gsc_pages'], D['gsc_queries'], D['gsc_countries'] = pick('page', 15), pick('query', 15), pick('country', 10)
    D['gsc_blog'] = safe('gsc blog', lambda: totals(gsc_query(*d28(g_end, 90), filters=['page~/blog/'])))
    print('GA4…')
    sess = ['sessions', 'activeUsers', 'engagedSessions']
    def ga_tot(rng, filters=()):
        rows = ga_report(*rng, [], sess, filters)
        return dict(zip(sess, rows[0][1])) if rows else dict.fromkeys(sess, 0)
    D['ga_cur'] = safe('ga cur', lambda: ga_tot(d28(a_end)))
    D['ga_prev'] = safe('ga prev', lambda: ga_tot(d28(a_end, back=28)))
    D['ga_90'] = safe('ga 90', lambda: ga_tot(d28(a_end, 90)))
    D['ga_organic_90'] = safe('ga organic', lambda: ga_tot(d28(a_end, 90), ['sessionDefaultChannelGroup=Organic Search']))
    D['ga_google_90'] = safe('ga google', lambda: ga_tot(d28(a_end, 90), ['sessionSource=google', 'sessionMedium=organic']))
    D['ga_ai_90'] = safe('ga ai', lambda: ga_tot(d28(a_end, 90), [f'sessionSource=~{AI_RE}']))
    D['ga_ai_cur'] = safe('ga ai cur', lambda: ga_tot(d28(a_end), [f'sessionSource=~{AI_RE}']))
    D['ga_ai_sources'] = safe('ga ai src', lambda: [[k[0], int(v[0])] for k, v in sorted(
        ga_report(*d28(a_end, 180), ['sessionSource'], ['sessions'], [f'sessionSource=~{AI_RE}']), key=lambda r: -r[1][0])], [])

    def weekly():
        w = defaultdict(lambda: defaultdict(float))
        for (d, ch), (s,) in ga_report(*d28(a_end, 180), ['date', 'sessionDefaultChannelGroup'], ['sessions']):
            iso = f'{d[:4]}-{d[4:6]}-{d[6:]}'
            w[week_start(iso)][ch] += s
        weeks = sorted(w)[1:]                                  # первая неделя обычно неполная
        chans = sorted({c for x in weeks for c in w[x]}, key=lambda c: -sum(w[x].get(c, 0) for x in weeks))
        return {'weeks': weeks, 'series': {c: [int(w[x].get(c, 0)) for x in weeks] for c in chans}}
    D['ga_weekly'] = safe('ga weekly', weekly, {'weeks': [], 'series': {}})

    def by(dim, n, filters=()):
        rows = ga_report(*d28(a_end, 90), [dim], ['sessions', 'engagedSessions'], filters)
        rows = sorted(rows, key=lambda r: -r[1][0])[:n]
        return [[k[0], int(v[0]), int(v[1])] for k, v in rows]
    D['ga_countries'] = safe('ga countries', lambda: by('country', 12), [])
    D['ga_languages'] = safe('ga languages', lambda: by('language', 8), [])
    D['ga_landing'] = safe('ga landing', lambda: by('landingPage', 15, ['sessionDefaultChannelGroup=Organic Search']), [])
    return D


def sitemap_urls():
    return re.findall(r'<loc>([^<]+)</loc>', open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read())


def index_snapshot():
    """Проверка индексации всех URL из sitemap. Один запрос ~7 с, поэтому идём в 6 потоков (квота API: 600 в минуту, 2000 в сутки)."""
    import threading
    from concurrent.futures import ThreadPoolExecutor
    urls = sitemap_urls()
    local = threading.local()
    print(f'Индексация: {len(urls)} URL…', flush=True)

    def check(u):
        if not hasattr(local, 's'):
            local.s = gsc.session()
        try:
            r = gsc.call(local.s, 'POST', 'https://searchconsole.googleapis.com/v1/urlInspection/index:inspect',
                         json={'inspectionUrl': u, 'siteUrl': GSC_SITE, 'languageCode': 'ru'})['inspectionResult']['indexStatusResult']
            return u, r.get('coverageState', 'неизвестно'), r.get('verdict') == 'PASS'
        except SystemExit as e:
            print(f'  ! {u}: {e}', file=sys.stderr, flush=True)
            return u, 'ошибка проверки', False

    states, bad, done = defaultdict(int), [], 0
    with ThreadPoolExecutor(max_workers=6) as ex:
        for u, st, ok in ex.map(check, urls):
            states[st] += 1
            if not ok:
                bad.append([u, st])
            done += 1
            if done % 30 == 0:
                print(f'  {done}/{len(urls)}', flush=True)
    return {'date': dt.date.today().isoformat(), 'total': len(urls), 'states': dict(states), 'not_indexed': bad[:60]}


def render(D):
    tpl = open(os.path.join(os.path.dirname(__file__), 'dashboard_template.html'), encoding='utf-8').read()
    blob = json.dumps(D, ensure_ascii=False).replace('</', '<\\/')
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8', newline='\n').write(tpl.replace('/*__DATA__*/null', blob))
    print(f'dashboard/index.html: {len(tpl) + len(blob)} байт')


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--index', action='store_true')
    p.add_argument('--offline', action='store_true')
    a = p.parse_args()
    data_path, hist_path = os.path.join(OUT, 'data.json'), os.path.join(OUT, 'history.json')
    os.makedirs(OUT, exist_ok=True)
    if a.offline:
        D = json.load(open(data_path, encoding='utf-8'))
    else:
        D = collect()
        D['index_history'] = json.load(open(hist_path, encoding='utf-8')) if os.path.exists(hist_path) else []
    if a.index and not a.offline:
        D['index_history'].append(index_snapshot())
        json.dump(D['index_history'], open(hist_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(D, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False)
    render(D)


if __name__ == '__main__':
    main()
