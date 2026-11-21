---
name: gsc-data
description: Прочитать данные Google Search Console сайта alexey-seleznev.pro (клики, показы, позиции, запросы, страны, страницы, индексация URL, карты сайта). Используй, когда нужны реальные данные поиска для SEO-аудита, вопросов про языки, падения трафика, ранжирования страницы, статуса индексации, «что говорит Search Console», «покажи запросы/страницы/страны». Только чтение.
---

# Search Console: чтение данных

Скрипт `scripts/gsc.py` ходит в Search Console API от имени сервисного аккаунта и **только читает** (scope `webmasters.readonly`).
Ничего не меняет ни в Search Console, ни на сайте. Данные запаздывают на 2–3 дня (скрипт по умолчанию заканчивает период на «сегодня − 3»).

```
python .claude/skills/gsc-data/scripts/gsc.py sites                      # к каким ресурсам есть доступ
python .claude/skills/gsc-data/scripts/gsc.py query --dims country --days 90
python .claude/skills/gsc-data/scripts/gsc.py query --dims query --filter "page~/opensource/" --limit 100
python .claude/skills/gsc-data/scripts/gsc.py query --dims page,country --filter "page~/blog/" --filter "country=ukr"
python .claude/skills/gsc-data/scripts/gsc.py query --dims date --days 180        # динамика по дням
python .claude/skills/gsc-data/scripts/gsc.py sitemaps
python .claude/skills/gsc-data/scripts/gsc.py inspect https://alexey-seleznev.pro/ https://alexey-seleznev.pro/opensource/
```

Измерения: `query, page, country, device, date, searchAppearance`. Фильтры: `dim~текст` (содержит), `dim!~текст` (не содержит),
`dim=значение` (равно), `dim=~regex`. Страны в Search Console — трёхбуквенные коды в нижнем регистре (`rus`, `ukr`, `usa`).
`--type` — web (по умолчанию), image, video, news, discover. `--csv файл` сохраняет таблицу (клади **вне репозитория**).

Ресурс по умолчанию `sc-domain:alexey-seleznev.pro`; другой — `--site https://alexey-seleznev.pro/` или переменная `GSC_SITE`.

## Что смотреть для типичных вопросов

- **Языки и страны:** `--dims country`, затем для топ-стран `--dims query` с `--filter country=...`: на каком языке ищут и какие страницы показываются.
- **Какой title/язык увидел Google:** `inspect URL` (канонический адрес, дата обхода, индексация); отрисованный HTML смотрится только в интерфейсе.
- **Страницы с показами, но без кликов:** `--dims page`, сортировка по impressions, низкий CTR — кандидаты на правку title/description.
- **Позиции 8–20:** `--dims query,page`, отфильтровать по position — быстрые победы.
- **Падение трафика:** `--dims date` за 180 дней и сравнение периодов `--start/--end`.

## Правила безопасности

- Ключ сервисного аккаунта читается из `$GOOGLE_SA_KEY` или `~/.config/seo-access/service-account.json`. **Никогда не клади его в репозиторий,
  не печатай, не коммить.** Если ключ вдруг оказался в рабочей копии — остановись и скажи пользователю.
- Результаты (CSV) не коммить: в них данные о посетителях сайта.

## Настройка (один раз, делает пользователь)

1. В [Google Cloud Console](https://console.cloud.google.com/) создать проект (или взять существующий) и включить API:
   **Google Search Console API**, а для GA4 ещё **Google Analytics Data API** и **Google Analytics Admin API**.
2. IAM и администрирование → Сервисные аккаунты → создать аккаунт (роли в проекте давать не нужно) → вкладка «Ключи» → добавить ключ → JSON.
3. Сохранить файл как `C:\Users\User\.config\seo-access\service-account.json` (папка вне репозитория). Из JSON понадобится поле `client_email`.
4. Search Console → Настройки → Пользователи и разрешения → Добавить пользователя: вставить `client_email`, права **«Ограниченные»** (только чтение). Для
   ресурса «Домен» добавлять надо именно в него.
5. `pip install google-auth requests`, затем `python .claude/skills/gsc-data/scripts/gsc.py sites` — должен показать ресурс.
