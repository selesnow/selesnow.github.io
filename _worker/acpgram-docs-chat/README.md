# acpgram-docs-chat

Cloudflare Worker для AI-чата на странице справки AcpGram (`/acpgram/docs/`).
Адрес: `https://acpgram-docs-chat.selesnow.workers.dev/api/ask`. Каталог `_worker/` на сайт не публикуется.

## Как это работает

1. Страница (`acpgram/docs/chat.js`) отправляет `POST /api/ask` с языком и последними сообщениями диалога.
2. Воркер проверяет `Origin`, размер вопроса и лимиты, берёт текст справки на языке читателя
   (`https://alexey-seleznev.pro/acpgram/docs/docs.<ru|ua|en>.txt`, кэш 10 минут) и кладёт его целиком в системный промпт.
3. Запрос уходит в OpenRouter (`MODEL`, по умолчанию роутер бесплатных моделей `openrouter/free`), ответ потоком
   возвращается на страницу. Поиска и векторной базы нет: справка помещается в контекст модели.

Файлы `docs.<lang>.txt` пишет `python _build/acpgram_docs.py` из `_build/acpgram_docs/*.md`. После правки справки
достаточно пересобрать и опубликовать сайт: воркер подхватит новый текст сам, передеплой не нужен.

## Настройки (`wrangler.toml`)

| Переменная | Значение |
|---|---|
| `ALLOWED_ORIGINS` | сайты, с которых разрешён чат |
| `DOCS_URL` | откуда брать текст справки |
| `MODEL` | модель OpenRouter |
| `MAX_TOKENS` | предел длины ответа (у «думающих» моделей в него входят рассуждения) |
| `PER_MINUTE`, `PER_DAY` | вопросов с одного адреса в минуту и в сутки |
| `TOTAL_PER_DAY` | вопросов в сутки всего (сутки по UTC) |

Секрет `OPENROUTER_API_KEY` в репозитории не хранится:

```sh
npx wrangler secret put OPENROUTER_API_KEY
```

Счётчики лимитов лежат в D1 (`acpgram-docs-chat`, таблица `usage`, см. `schema.sql`). Адрес читателя хранится
как короткий хэш, строки прошлых дней воркер удаляет сам. Тексты вопросов не сохраняются и не пишутся в лог.

## Команды

Запускать из этого каталога.

```sh
npx wrangler deploy          # выкатить изменения
npx wrangler tail            # живой лог: вопросы (язык, длина), срабатывания лимитов, ошибки OpenRouter
npx wrangler d1 execute acpgram-docs-chat --remote --command "SELECT * FROM usage WHERE key = '*' ORDER BY bucket DESC LIMIT 14"   # вопросов по дням
```

## Локальная проверка без ключа

Три терминала: сайт, подставной OpenRouter и воркер.

```sh
python -m http.server 8765                      # из корня репозитория
node test/mock-openrouter.mjs                   # порт 8799, отдаёт готовый ответ потоком
npx wrangler d1 execute acpgram-docs-chat --local --file schema.sql
npx wrangler dev --local --port 8787 --var DOCS_URL:http://127.0.0.1:8765/acpgram/docs --var OPENROUTER_URL:http://127.0.0.1:8799 --var ALLOWED_ORIGINS:http://localhost:8765 --var OPENROUTER_API_KEY:test
```

Страница: `http://localhost:8765/acpgram/docs/?chat-api=http://127.0.0.1:8787/api/ask`
(параметр `chat-api` работает только на `localhost`). Вопрос со словом `429` или `500` заставляет подставной сервер вернуть эту ошибку.

## Коды ошибок

`bad_request`, `too_long`, `forbidden` (чужой сайт), `rate_minute`, `rate_day`, `quota` (общий суточный предел),
`busy` (OpenRouter ответил 429), `unavailable` (нет ключа, справки или ответа модели). Тексты для читателя — в `failure()` в `chat.js`.
