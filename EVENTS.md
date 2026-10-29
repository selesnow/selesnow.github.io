# Карта событий Google Analytics 4 (GA4) для alexey-seleznev.pro

Идентификатор ресурса: **`G-Z56YHE916N`**

Документ содержит полный перечень событий, параметров и инструкции по настройке отслеживания в Google Analytics 4.

---

## 1. Сводная таблица событий

| Событие GA4 | Назначение | Конверсия в GA4 | Где срабатывает |
| :--- | :--- | :---: | :--- |
| **`generate_lead`** | Клик по кнопке связи для заказа рекламы в Telegram | **Да** | `/ads/` |
| **`contact_click`** | Клик по прямым контактам (Email, личный Telegram) | **Да** | Лендинг, футер всех страниц |
| **`community_join`** | Переход в Telegram-канал или на YouTube-канал R4marketing | Рекомендуется | Лендинг, футер, шапка, `/ads/` |
| **`course_click`** | Переход к изучению курса или учебника | Рекомендуется | Лендинг (слайдер), `/courses/` |
| **`course_resource_click`** | Переход к материалам курса (GitHub, YouTube-плейлист, Хабр) | Нет | `/courses/` |
| **`package_action`** | Клик по ссылкам R-пакетов (GitHub, CRAN, Docs, Видео, Статья) | Нет | Лендинг, `/opensource/` |
| **`video_open`** | Открытие модального видеоплеера (Cinema Lightbox) | Нет | Лендинг, `/videos/`, `/talks/`, `/interviews/` |
| **`spotlight_video_play`** | Запуск видео в блоке Spotlight на лендинге или в `/talks/` | Нет | Лендинг, `/talks/` |
| **`content_outbound_click`** | Переход к внешним статьям, докладам, интервью (Хабр, Блог и т.д.) | Нет | Лендинг, `/articles/`, `/interviews/`, `/talks/` |
| **`search`** | Поиск по каталогам (статьи, доклады, видео, пакеты) | Нет | `/articles/`, `/talks/`, `/videos/`, `/opensource/` |
| **`filter_click`** | Переключение фильтров и категорий | Нет | Лендинг, каталоги |
| **`language_select`** | Ручной выбор языка пользователем (EN / RU / UA) | Нет | Шапка на всех страницах |
| **`slider_navigation`** | Прокрутка слайдеров стрелками | Нет | Лендинг (курсы, доклады) |
| **`social_click`** | Переход в соцсети автора (LinkedIn, GitHub, Facebook, Instagram) | Нет | Блок контактов, футер |
| **`ad_stat_service_click`** | Клик по ссылкам внешней статистики канала (TGStat, Telemetr) | Нет | `/ads/` |
| **`ad_poll_click`** | Переход к опросам аудитории канала в Telegram | Нет | `/ads/` |

---

## 2. Детальное описание событий и параметров

### 2.1. Лиды и контакты

#### `generate_lead`
Отправляется при клике на основную кнопку связи на странице рекламы `/ads/`.
- **Параметры:**
  - `contact_type`: `'telegram'`
  - `source_page`: `'ads'`
  - `lead_topic`: `'advertising'`

#### `contact_click`
Отправляется при клике на email или личный Telegram в блоке контактов и футере.
- **Параметры:**
  - `contact_type`: `'email'` | `'telegram'`
  - `contact_value`: `'me@alexey-seleznev.pro'` | `'@AlexeySeleznev'`
  - `placement`: `'contacts_section'` | `'footer'`

#### `social_click`
Переход в личные профессиональные соцсети.
- **Параметры:**
  - `network`: `'github'` | `'linkedin'` | `'facebook'` | `'instagram'` | `'habr'`
  - `placement`: `'contacts_section'` | `'footer'` | `'nav'`

---

### 2.2. Сообщество R4marketing

#### `community_join`
Клики по ссылкам перехода в сообщество (Telegram-канал и YouTube-канал R4marketing).
- **Параметры:**
  - `platform`: `'telegram'` | `'youtube'`
  - `channel_name`: `'R4marketing'`
  - `placement`: `'nav'` | `'hero'` | `'content_section'` | `'mobile_menu'` | `'footer'` | `'ads_page'`

---

### 2.3. Курсы и учебники

#### `course_click`
Клик по кнопке перехода к самому курсу (ведет на сайт курса, интерактивный учебник или плейлист).
- **Параметры:**
  - `course_id`: идентификатор курса (`'r_for_marketing'`, `'r4excel_users'`, `'dplyr_1_0_0_course'`, `'iterations_in_r'`, `'build_telegram_bot_using_r'`, `'r_package_course'`, `'build_ai_tools_using_r'`)
  - `course_name`: название курса
  - `course_level`: `'beginner'` | `'middle'` | `'advanced'` | `'new'`
  - `target_type`: `'site'` | `'book'` | `'youtube_playlist'`
  - `placement`: `'landing_slider'` | `'courses_page'`

#### `course_resource_click`
Клик по вспомогательным материалам курса на странице `/courses/`.
- **Параметры:**
  - `course_id`: идентификатор курса
  - `resource_type`: `'playlist'` | `'materials'` (GitHub) | `'article'` (Хабр)

---

### 2.4. Open Source R-пакеты

#### `package_action`
Любое действие по пакету (переход на GitHub репозиторий, страницу CRAN, документацию pkgdown, видеообзор или статью).
- **Параметры:**
  - `package_name`: имя пакета (`'rgoogleads'`, `'rfacebookstat'`, `'rym'`, `'rytstat'`, `'timeperiodsR'` и т.д.)
  - `action_type`: `'github'` | `'cran'` | `'docs'` | `'video'` | `'article'`
  - `is_cran`: `'true'` | `'false'`
  - `is_archived`: `'true'` | `'false'`
  - `placement`: `'landing_grid'` | `'opensource_page'`

---

### 2.5. Медиа, видео и выступления

#### `video_open`
Открытие видео во встроенном модальном окне (Cinema Lightbox).
- **Параметры:**
  - `video_id`: YouTube Video ID (например, `EnImByySQEE`)
  - `video_title`: название доклада / урока
  - `section`: `'speaking'` | `'videos'` | `'talks'` | `'interviews'`

#### `spotlight_video_play`
Клик по запуску главного видео в блоке Spotlight на главной или в докладах.
- **Параметры:**
  - `video_id`: YouTube Video ID
  - `video_title`: название видео
  - `section`: `'landing_spotlight'` | `'talks_spotlight'`

#### `content_outbound_click`
Переход к внешним материалам (статьи на Хабре, в личном блоге WordPress, Netpeak Blog, Medium, видеоинтервью, слайды Google Slides).
- **Параметры:**
  - `content_type`: `'article'` | `'interview'` | `'slides'` | `'materials'`
  - `content_title`: заголовок материала
  - `platform`: `'habr'` | `'blog'` | `'netpeak'` | `'medium'` | `'slides'` | `'youtube'`
  - `link_url`: URL перехода

---

### 2.6. UX, навигация, фильтры и поиск

#### `search` (стандартное событие GA4)
Поиск в каталогах статей, видео, докладов и пакетов (отправляется с задержкой 700-800 мс после окончания ввода текста).
- **Параметры:**
  - `search_term`: введённая поисковая фраза
  - `search_section`: `'articles'` | `'talks'` | `'videos'` | `'packages'`
  - `results_count`: число найденных карточек (позволяет отследить запросы с 0 результатов)

#### `filter_click`
Клик по кнопкам фильтрации категорий, типов докладов или годов.
- **Параметры:**
  - `filter_group`: `'cat'` | `'type'` | `'speaking'`
  - `filter_value`: `'all'`, `'conference'`, `'webinar'`, `'marketing'`, `'api'` и т.д.
  - `section`: раздел сайта

#### `language_select`
Явный выбор языка пользователем через переключатель EN / RU / UA.
- **Параметры:**
  - `selected_language`: `'en'` | `'ru'` | `'ua'`
  - `previous_language`: предыдущий язык

#### `slider_navigation`
Клик по стрелкам навигации в горизонтальных каруселях.
- **Параметры:**
  - `slider_id`: `'courses'` | `'speaking'`
  - `direction`: `'left'` | `'right'`

---

### 2.7. Страница рекламы `/ads/`

#### `ad_stat_service_click`
Переход по внешним ссылкам сервисов аналитики канала.
- **Параметры:**
  - `service_name`: `'TGStat'` | `'Telemetr'`

#### `ad_poll_click`
Переход к первоисточникам опросов аудитории в канале.
- **Параметры:**
  - `poll_id`: `'geo'` | `'cities'` | `'age'` | `'income'` | `'education'` | `'field'` | `'tools'` | `'experience'`

---

## 3. Регистрация специальных параметров (Custom Dimensions) в GA4

Чтобы параметры событий были доступны в стандартных отчетах, Исследованиях (Explore) и Looker Studio, их необходимо зарегистрировать в панели управления GA4:

**Путь в GA4:** `Администратор` → В колонке ресурса `Отображение данных` → `Пользовательские определения` (Custom definitions) → `Создать специальный параметр`.

| Название параметра (Dimension Name) | Область действия (Scope) | Параметр события (Event Parameter) | Описание |
| :--- | :--- | :--- | :--- |
| **Тип контакта** | Событие | `contact_type` | `telegram`, `email` |
| **Место размещения** | Событие | `placement` | `hero`, `contacts_section`, `footer`, `nav` и т.д. |
| **Платформа сообщества** | Событие | `platform` | `telegram`, `youtube`, `habr`, `blog` |
| **ID курса** | Событие | `course_id` | Идентификатор курса |
| **Название курса** | Событие | `course_name` | Название курса |
| **Уровень курса** | Событие | `course_level` | `beginner`, `middle`, `advanced` |
| **Имя R-пакета** | Событие | `package_name` | Имя пакета (`rgoogleads`, `rym` и др.) |
| **Действие по пакету** | Событие | `action_type` | `github`, `cran`, `docs`, `video`, `article` |
| **ID видео YouTube** | Событие | `video_id` | Идентификатор видео на YouTube |
| **Заголовок видео/контента** | Событие | `video_title` / `content_title` | Название доклада, видео или статьи |
| **Раздел сайта** | Событие | `section` / `search_section` | `speaking`, `talks`, `videos`, `courses`, `articles` |
| **Количество результатов поиска** | Событие | `results_count` | Количество найденных карточек |
| **Группа фильтра** | Событие | `filter_group` | Группа примененного фильтра |
| **Значение фильтра** | Событие | `filter_value` | Значение фильтра |
| **Выбранный язык** | Событие | `selected_language` | `en`, `ru`, `ua` |
| **Направление слайдера** | Событие | `direction` | `left`, `right` |

---

## 4. Настройка ключевых событий (Conversions / Key Events)

В GA4 перейдите в:  
`Администратор` → `Отображение данных` → `Ключевые события` (Key events) → `Создать ключевое событие`.

Включите как ключевые события:
1. **`generate_lead`** — клик по кнопке заказа рекламы в Telegram (основная бизнес-конверсия).
2. **`contact_click`** — прямой контакт с автором по почте или в Telegram.
3. **`community_join`** — подписка / переход в сообщество R4marketing.
4. **`course_click`** — переход к изучению курсов.

---

## 5. Как проверить корректность работы (QA)

1. Установите расширение для браузера **Google Analytics Debugger** (Chrome) или используйте **Google Tag Assistant** (`tagassistant.google.com`).
2. В интерфейсе GA4 откройте: `Администратор` → `DebugView`.
3. Перейдите на сайт `https://alexey-seleznev.pro/` (или локальный сервер `python -m http.server 8765`).
4. Нажимайте на кнопки курсов, переключайте язык, открывайте видео, кликайте по пакетам и контактам — события с переданными параметрами будут в реальном времени отображаться в ленте `DebugView`.
