#!/usr/bin/env python3
"""Регистрирует в Google Analytics 4 специальные параметры (custom dimensions) для событий сайта — GA4 Admin API.

Параметры перечислены в DIMENSIONS (см. EVENTS.md, раздел 3). Уже существующие пропускаются, так что скрипт можно
запускать повторно после добавления новых событий.

Ключ сервисного аккаунта: $GOOGLE_SA_KEY (вне репозитория, не коммитить). Аккаунту нужна роль «Редактор» в ресурсе GA4.

  python _build/setup_ga4.py            показать, что зарегистрировано и чего не хватает
  python _build/setup_ga4.py --apply    создать недостающие
"""
import os
import sys

MEASUREMENT_ID = 'G-Z56YHE916N'
API = 'https://analyticsadmin.googleapis.com/v1beta'
SCOPE = 'https://www.googleapis.com/auth/analytics.edit'

# параметр события, название в интерфейсе GA4, описание
DIMENSIONS = [
    ('chat_language', 'Язык чата справки', 'AI-чат справки AcpGram: язык страницы в момент вопроса (ru, ua, en)'),
    ('chat_turn', 'Номер вопроса в чате', 'AI-чат справки AcpGram: какой по счёту вопрос в диалоге'),
    ('section_id', 'Раздел справки', 'AI-чат справки AcpGram: якорь раздела, к которому перешли из ответа'),
    ('error_code', 'Код ошибки чата', 'AI-чат справки AcpGram: rate_minute, rate_day, quota, busy, unavailable, too_long'),
]


def session():
    from google.oauth2 import service_account
    from google.auth.transport.requests import AuthorizedSession
    key = os.environ.get('GOOGLE_SA_KEY')
    if not key or not os.path.exists(key):
        sys.exit('Укажи путь к ключу сервисного аккаунта в переменной GOOGLE_SA_KEY')
    return AuthorizedSession(service_account.Credentials.from_service_account_file(key, scopes=[SCOPE]))


def call(s, method, url, **kw):
    r = s.request(method, url, timeout=60, **kw)
    if r.status_code >= 400:
        try:
            message = r.json().get('error', {}).get('message', r.text)
        except Exception:
            message = r.text
        sys.exit(f'HTTP {r.status_code}: {message}')
    return r.json()


def pages(s, url, field):
    token = ''
    while True:
        data = call(s, 'GET', url, params={'pageSize': 200, **({'pageToken': token} if token else {})})
        yield from data.get(field, [])
        token = data.get('nextPageToken')
        if not token:
            return


def find_property(s):
    for account in pages(s, f'{API}/accountSummaries', 'accountSummaries'):
        for prop in account.get('propertySummaries', []):
            for stream in pages(s, f'{API}/{prop["property"]}/dataStreams', 'dataStreams'):
                if stream.get('webStreamData', {}).get('measurementId') == MEASUREMENT_ID:
                    return prop['property'], prop.get('displayName', '')
    sys.exit(f'Сервисный аккаунт не видит ресурс с потоком {MEASUREMENT_ID}')


def main():
    apply = '--apply' in sys.argv
    s = session()
    prop, name = find_property(s)
    existing = {d['parameterName']: d for d in pages(s, f'{API}/{prop}/customDimensions', 'customDimensions') if d.get('scope') == 'EVENT'}
    print(f'{prop} «{name}»: параметров уровня события уже {len(existing)}')
    for param, title, description in DIMENSIONS:
        if param in existing:
            print(f'  есть      {param}  «{existing[param].get("displayName")}»')
        elif apply:
            call(s, 'POST', f'{API}/{prop}/customDimensions',
                 json={'parameterName': param, 'displayName': title, 'description': description, 'scope': 'EVENT'})
            print(f'  создан    {param}  «{title}»')
        else:
            print(f'  нет       {param}  «{title}»')
    if not apply and any(p not in existing for p, _, _ in DIMENSIONS):
        print('Запусти с --apply, чтобы создать недостающие.')


if __name__ == '__main__':
    main()
