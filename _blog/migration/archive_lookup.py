"""Для публикаций, чей оригинал пропал: ищет в Web Archive ближайший к дате публикации снимок (API доступности, status 200).
Результат кэшируется в raw/archive_lookup.json."""
import difflib, html, json, re, sys, time, urllib.parse, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CACHE = HERE / 'raw' / 'archive_lookup.json'


def publications_links():
    t = (HERE / 'raw' / 'publications.html').read_text(encoding='utf-8', errors='replace')
    out = []
    for u, txt in re.findall(r'<a [^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>', t, re.S):
        txt = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', html.unescape(txt))).strip()
        if len(txt) > 12 and 'wordpress.com' not in u:
            out.append((txt, u))
    return out


def norm(s):
    return re.sub(r'[^\w]+', ' ', s.lower().replace('ё', 'е')).strip()


def snapshot(url, stamp):
    api = 'https://archive.org/wayback/available?url=' + urllib.parse.quote(url, safe='') + f'&timestamp={stamp}'
    for _ in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(api, headers={'User-Agent': 'Mozilla/5.0'}), timeout=60) as r:
                snap = json.load(r).get('archived_snapshots', {}).get('closest')
                return snap if snap and snap.get('status') == '200' and snap.get('available') else None
        except Exception:
            time.sleep(3)
    return None


def main():
    arts = json.loads((ROOT / '_build' / 'data' / 'articles.json').read_bytes().decode('utf-8'))
    links = publications_links()
    cache = json.loads(CACHE.read_text(encoding='utf-8')) if CACHE.exists() else {}
    for a in arts:
        if a.get('via') != 'blog':
            continue
        best = max((difflib.SequenceMatcher(None, norm(a['title']), norm(t)).ratio(), t, u) for t, u in links)
        orig = best[2]
        key = a['url']
        if key in cache and cache[key].get('archive'):
            continue
        snap = snapshot(orig, f"{a['y']}{a['m']:02d}15")
        cache[key] = {'title': a['title'], 'original': orig, 'score': round(best[0], 2),
                      'archive': snap['url'].replace('http://', 'https://') if snap else None,
                      'stamp': snap['timestamp'] if snap else None}
        print(('OK ' if snap else '-- '), a['y'], a['m'], orig[:80], '→', cache[key]['stamp'])
        CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding='utf-8')
        time.sleep(1)
    print('найдено снимков:', sum(1 for v in cache.values() if v['archive']), 'из', len(cache))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
