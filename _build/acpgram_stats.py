"""AcpGram snapshot, collected by the site's existing daily stats workflow."""
import datetime as dt
import json
import os
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATH = ROOT / 'assets' / 'acpgram-stats.json'


def merge_clones(previous, payload):
    history = {p['date']: p for p in previous.get('history', [])}
    for p in payload['clones']:
        date = p['timestamp'][:10]
        history[date] = {'date': date, 'count': p['count'], 'uniques': p['uniques']}
    history = sorted(history.values(), key=lambda p: p['date'])
    return {'last14d': payload['count'], 'uniques14d': payload['uniques'],
            'total': sum(p['count'] for p in history), 'history': history,
            'since': history[0]['date'] if history else previous.get('since')}


def update_acpgram_stats():
    data = json.loads(PATH.read_text(encoding='utf-8')) if PATH.exists() else {
        'updated': None, 'github': {'stars': None, 'forks': None, 'clones': {
            'last14d': None, 'uniques14d': None, 'total': None, 'history': []}},
        'npm': {'version': None, 'last30d': None, 'total': None}}
    token = os.environ.get('GITHUB_PAT') or os.environ.get('GITHUB_TOKEN')
    if not token:
        try:
            token = subprocess.run(['gh', 'auth', 'token'], capture_output=True, text=True, timeout=10, check=True).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            token = None
    changed = False
    fetched = {}

    def get(url):
        headers = {'User-Agent': 'alexey-seleznev.pro stats', 'Accept': 'application/json'}
        if token and url.startswith('https://api.github.com/'):
            headers['Authorization'] = f'Bearer {token}'
        for attempt in range(3):
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=30) as response:
                    return json.load(response)
            except urllib.error.HTTPError as exc:
                if attempt == 2 or not (exc.code == 429 or exc.code >= 500):
                    raise
                time.sleep(min(30, int(exc.headers.get('Retry-After', 2 ** (attempt + 1)))))

    def collect(label, action):
        nonlocal changed
        try:
            action()
            fetched[label] = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
            changed = True
        except Exception as exc:
            # Never print headers or token values. Preserve the entire previous metric on failure.
            code = f' HTTP {exc.code}' if isinstance(exc, urllib.error.HTTPError) else f' {type(exc).__name__}'
            print(f'::warning::AcpGram {label}:{code}; previous values retained.')

    def github():
        repo = get('https://api.github.com/repos/selesnow/acpgram')
        data['github'].update(stars=repo['stargazers_count'], forks=repo['forks_count'])

    def npm_month():
        result = get('https://api.npmjs.org/downloads/point/last-month/acpgram')
        data['npm']['last30d'] = result['downloads']

    def npm_total():
        meta = get('https://registry.npmjs.org/acpgram')
        start = dt.date.fromisoformat(meta['time']['created'][:10])
        end = dt.datetime.now(dt.timezone.utc).date() - dt.timedelta(days=1)
        total = 0
        while start <= end:
            stop = min(end, start + dt.timedelta(days=364))
            total += get(f'https://api.npmjs.org/downloads/point/{start}:{stop}/acpgram')['downloads']
            start = stop + dt.timedelta(days=1)
        # Only assign after all chunks succeeded.
        data['npm'].update(version=meta['dist-tags']['latest'], total=total)

    def clones():
        result = get('https://api.github.com/repos/selesnow/acpgram/traffic/clones')
        data['github']['clones'] = merge_clones(data['github']['clones'], result)

    collect('github', github)
    collect('npmMonth', npm_month)
    collect('npmTotal', npm_total)
    collect('clones', clones)
    if changed:
        data['updated'] = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
        data.setdefault('sourcesUpdated', {}).update(fetched)
        PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return data


if __name__ == '__main__':
    update_acpgram_stats()
