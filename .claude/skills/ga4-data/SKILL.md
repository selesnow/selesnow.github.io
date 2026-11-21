---
name: ga4-data
description: Прочитать данные Google Analytics 4 сайта alexey-seleznev.pro (сессии, пользователи, страны, языки браузера, каналы, источники, посадочные страницы, переходы из AI-ассистентов). Используй, когда нужны реальные данные посещаемости для SEO-аудита, решения по языкам сайта, оценки AI-трафика, популярных страниц, «покажи аналитику/трафик/страны/языки пользователей». Только чтение.
---

# Google Analytics 4: чтение данных

Скрипт `scripts/ga4.py` обращается к Analytics Data API от имени сервисного аккаунта и **только читает** (scope `analytics.readonly`).
Ничего не меняет в GA4 и на сайте. Ресурс GA4 — `G-Z56YHE916N` (поток данных); для API нужен **числовой ID ресурса**, его покажет команда `properties`.

```
python .claude/skills/ga4-data/scripts/ga4.py properties                      # какие ресурсы доступны и их ID
export GA4_PROPERTY=123456789                                                  # или --property 123456789
python .claude/skills/ga4-data/scripts/ga4.py preset countries --days 90
python .claude/skills/ga4-data/scripts/ga4.py preset languages --days 90      # язык браузера посетителей
python .claude/skills/ga4-data/scripts/ga4.py preset channels
python .claude/skills/ga4-data/scripts/ga4.py preset landing --limit 30
python .claude/skills/ga4-data/scripts/ga4.py preset ai --days 180            # переходы из ChatGPT, Perplexity, Claude, Gemini, Copilot и др.
python .claude/skills/ga4-data/scripts/ga4.py report --dims country,language --metrics sessions,activeUsers --filter "pagePath~/blog/"
```

Готовые отчёты (`preset`): `countries, languages, channels, sources, landing, pages, devices, daily, ai`.
Произвольные: `report --dims A,B --metrics X,Y` (имена из [справочника измерений и показателей GA4](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema)).
Фильтры: `dim~текст` (содержит), `dim=значение` (точно), `dim=~regex`; несколько флагов `--filter` объединяются по «И».
Период: `--days N` (по умолчанию 28, до «вчера») или `--start 2026-01-01 --end 2026-03-31`. `--csv файл` — сохранить таблицу (**вне репозитория**).

## Что смотреть для типичных вопросов

- **Нужны ли языковые версии:** `preset languages` и `preset countries` за 90–180 дней: доля пользователей с английским/украинским интерфейсом и из каких стран.
- **AI-трафик:** `preset ai`; приходят не все переходы (многие ассистенты не передают реферер), поэтому смотри и рост «direct».
- **Какие страницы приводят людей:** `preset landing`, для блога `--filter "landingPagePlusQueryString~/blog/"`.
- Данные GA4 и Search Console сверяй: GA4 — поведение на сайте, Search Console — показы и клики в поиске (скилл `gsc-data`).

## Правила безопасности

- Ключ читается из `$GOOGLE_SA_KEY` или `~/.config/seo-access/service-account.json` — **не клади его в репозиторий, не печатай, не коммить**.
- CSV с выгрузками не коммить.

## Настройка

Тот же сервисный аккаунт и ключ, что для `gsc-data` (шаги 1–3 в `.claude/skills/gsc-data/SKILL.md`). Дополнительно:
GA4 → Администратор → Управление доступом к ресурсу → «+» → вставить `client_email`, роль **«Просмотр»** (Viewer).
Должны быть включены Google Analytics Data API и Google Analytics Admin API. Затем `pip install google-auth requests` и `ga4.py properties`.
