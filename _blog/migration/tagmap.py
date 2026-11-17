"""Унификация тегов и рубрик блога + автоматический тег AI."""
import re

# каноническое имя -> алиасы (сравнение без учёта регистра и лишних пробелов)
TAGS = {
    'R': ['R', 'R language', 'язык R', 'язык R для маркетолога', 'учить язык R', 'курс по языку R', 'курсы по языку R',
          'обучение языку R', 'R скрипты', 'Книги по R'],
    'Пакеты R': ['R пакеты', 'R Package', 'Пакеты R', 'Дайджест обновлений R пакетов', 'Обновление пакетов R', 'пакет rym',
                 'пакет telegram.bot'],
    'API': ['API', 'Коннекторы'],
    'Telegram': ['Telegram Bot API', 'API Telegram', 'Telegram Bot', 'Telegram API', 'telegram', 'Telegram бот на R',
                 'Разработка Telegram ботов', 'как написать телеграм бота', 'написать телеграм бота на R', 'программирование телеграм бота',
                 'разработка бота', 'разработка телеграм бота', 'создание телеграм бота', 'Как отправить сообщение из R в Telegram',
                 'telegram.bot'],
    'Яндекс Директ': ['Яндекс Директ', 'API ЯндексДирект', 'ryandexdirect'],
    'Яндекс Метрика': ['Яндекс Метрика', 'API Яндекс Метрики', 'Загрузка данныз из Яндекс.Метрики', 'Logs API', 'LogsAPI', 'rym'],
    'Google Ads': ['Google AdWords', 'Google Ads', 'Google Ads API', 'API Google Ads', 'Google AdWords API', 'RAdwords', 'adwordsR',
                   'rgoogleads', 'Показатель качества ключевых слов', 'Потерянный доход'],
    'Google Analytics': ['Google Analytics', 'Google Analytics API', 'API Google Analytics', 'Как получить данные из API Google Analytics',
                         'googleAnalyticsR', 'RGA', 'Как получить данные из API Google Analytics'],
    'Веб-аналитика': ['Web Analytics', 'Web Analytic', 'Analytic', 'Веб аналитика', 'Аналитика', 'Аналитика поведения пользователей',
                      'Аналитика блога', 'Анализ контента', 'сквозная аналитика', 'Cohort analisys', 'аналитические системы',
                      'инструменты аналитики'],
    'PPC': ['PPC', 'CPC', 'Контекстная реклама', 'Online Advertising', 'Стоимость клика', 'Конкурентный анализ'],
    'Facebook': ['Facebook API', 'Facebook Marketing API', 'rfacebookstat'],
    'ВКонтакте': ['rvkstat', 'как загрузить данные из ВК в Power BI'],
    'myTarget': ['MyTarget', 'rmytarget'],
    'BI': ['BI', 'BI системы', 'Bussines Intelegence', 'Бизнес аналитика', 'разработка BI', 'Tableau', 'QlikView', 'Qlik'],
    'Power BI': ['Power BI', 'Microsoft Power BI', 'Bookmarks'],
    'Google Data Studio': ['Google Data Studio', 'GDS'],
    'Визуализация данных': ['Визуализация данных', 'Графики', 'Диаграммы', 'Спарклайны', 'ggplot2'],
    'Google Таблицы': ['Google Spreadsheets', 'Google таблицы', 'google таблицы + RStudio', 'API Google Таблиц', 'google sheets api',
                       'Работа с google таблицами из R', 'Spreadsheets'],
    'Excel': ['Microsoft Excel', 'Microsoft Exel', 'Сводные таблицы', 'LibreOffice'],
    'BigQuery': ['Google BigQuery', 'BigQuery', 'BigData'],
    'SQL': ['SQL', 'язык SQL', 'SQL и R', 'SQL Clients', 'sqldf', 'MERGE', 'UPSERT', 'Оконные функции'],
    'Базы данных': ['Базы данных', 'Data Base', 'DataBases', 'MySQL', 'DBI', 'phpMyAdmin', 'phpPgAdmin', 'Хранение данных', 'S3'],
    'Python': ['Python', 'pandas', 'отправить таблицу из Python', 'отправка писем из Python', 'вставить pandas в письмо',
               'перевод DataFrame в HTML', 'R or Python'],
    'Автоматизация': ['Автоматизация', 'Расписание запуска скрипта', 'Script Schedule', 'CD/CI', 'GitHub Actions', 'Windows'],
    'GitHub': ['GitHub', 'GitHub Actions'],
    'Анализ данных': ['Анализ данных', 'Data Scince', 'data minimg', 'data engeneering', 'Статистика'],
    'Обработка данных': ['Обработка данных', 'Работа с данными', 'преобразование данных', 'манипуляция с данными', 'манипуляция данными',
                         'tidy data', 'data.frame', 'DataFrame', 'data.table', 'развернуть вложенные столбцы', 'развернуть столбец в R',
                         'Запись данных', 'сырые данные', 'работа с датами', 'timeperiodsR', 'rowwise()'],
    'tidyverse': ['tidyverse', 'dplyr', 'tidyr', 'tibble', 'lubridate', 'rlang'],
    'Параллельные вычисления': ['Паралелизация', 'Параллельное программирование', 'Парралельные вычисления', 'параллельные вычисления',
                                'многопоточность', 'параллелизм', 'параллельность', 'parallel', 'future', 'future.apply'],
    'Импорт данных': ['Импорт данных', 'Интеграция', 'Supermetrics', 'Загрузка данных'],
    'Обработка ошибок': ['R Error', 'R Errors', 'error handle', 'try()', 'tryCatch()', 'обработка ошибок в R', 'отловить ошибку в R'],
    'ООП': ['ООП', 'Классы в R'],
    'AI': ['AI', 'AI Tools'],
    'ChatGPT': ['ChatGPT', 'ChatGPT в работе', 'ChatGPT для аналитика данных', 'ChatGPT для генерации кода', 'Пользователmские ChatGPT'],
    'LLM': ['LLM', 'ellmer'],
    'MCP': ['MCP сервер', 'mcptools'],
    'Claude Code': ['Claude code'],
    'Gemini': ['Gemini'],
    'AcpGram': ['AcpGram'],
    'Vibe coding': ['VibeCoding'],
    'Вебинары': ['Вебинары', 'вебинар', 'вебинары по R на русском', 'воркшоп', 'Мастер класс'],
    'Выступления': ['Выступления', 'выступление', 'Доклады', 'Доклад', 'Конференции', 'Конференция', 'Презентации', 'мероприятия',
                    'Матемаркетинг', 'GoANalytics', 'Analyze', 'Analytical challenge', 'Analytics EDGE', 'Ideal Analytics', 'eCommerce'],
    'Интервью': ['Интервью', 'интервью', 'Корпоративный блог'],
    'Кейсы': ['Кейс', 'Кейсы'],
    'Исследования': ['Исследования', 'Опрос', 'SimilarWeb', 'тренды'],
    'Обучение': ['обучение', 'видео уроки', 'Видео'],
    'Дайджесты': ['Дайджесты', 'дайджест', 'анонс', 'обновления', 'Обновление R'],
    'Безопасность': ['безопасность'],
    'GUI': ['GUI', 'Графический интерфейс'],
}

# рубрики (категории WordPress) -> канонические
CATS = {
    'R': ['R'],
    'Программирование': ['Programming', 'Программирование'],
    'Реклама': ['Online Advertising'],
    'Google Ads': ['Google AdWords'],
    'Веб-аналитика': ['Web Analytic'],
    'Google Analytics': ['Google Analytics'],
    'Яндекс': ['Яндекс Директ', 'Яндекс Метрика'],
    'BI': ['Bussines Intelegence', 'Microsoft Power BI', 'Tableau', 'Qlik', 'Google Data Studio'],
    'Визуализация данных': ['Визуализация данных'],
    'Таблицы': ['Spreadsheets', 'Google Spreadsheets', 'Microsoft Excel'],
    'Базы данных': ['DataBases', 'MySQL', 'Google BigQuery'],
    'Python': ['Python'],
    'AI': ['AI'],
    'Выступления': ['Выступления', 'Вебинары', 'Доклады'],
    'Исследования': ['Исследования'],
    'Кейсы': ['Кейсы'],
    'Интервью': ['Интервью'],
}


DROP = {'programming', 'программирование', 'realise'}   # слишком общий тег: то же самое уже есть рубрикой


def _k(s):
    return re.sub(r'\s+', ' ', s.strip().lower())


def _inverse(m):
    inv = {}
    for canon, aliases in m.items():
        for a in aliases + [canon]:
            inv.setdefault(_k(a), canon)  # первое вхождение побеждает: порядок словаря = приоритет
    return inv


TAG_INV, CAT_INV = _inverse(TAGS), _inverse(CATS)

AI_RE = re.compile(r'(?<!\w)(?:AI|LLM|MCP|GPT-?\d*|ChatGPT|Claude|Gemini|Codex|OpenAI|Copilot|Antigravity)(?!\w)|(?<!\w)ИИ(?!\w)|нейросет\w*|искусственн\w+ интеллект\w*|кодинг[- ]агент')

# если после унификации тегов нет — подбираем по заголовку
TITLE_RULES = [
    (r'BigQuery', ['BigQuery', 'Импорт данных']),
    (r'Яндекс', ['Яндекс Метрика']),
    (r'Goodbye|итоги', ['Итоги года']),
    (r'Первая запись', ['Блог']),
]


def unify(title, desc, tags, cats, body=''):
    out_tags = []
    for t in tags:
        if _k(t) in DROP:
            continue
        c = TAG_INV.get(_k(t))
        if c is None and re.fullmatch(r'[A-Za-z][A-Za-z0-9._]{1,23}', t.strip()):
            c = t.strip()          # одиночные названия пакетов/функций оставляем как есть
        if c and c not in out_tags:
            out_tags.append(c)
    out_cats = []
    for c in cats:
        k = CAT_INV.get(_k(c))
        if k and k not in out_cats:
            out_cats.append(k)

    body = re.sub(r'```.*?```', ' ', body, flags=re.S)   # код не считаем
    head = f'{title} {desc} {" ".join(tags)}'
    is_ai = bool(AI_RE.search(head)) or len(AI_RE.findall(body)) >= 4
    if is_ai:
        if 'AI' not in out_tags:
            out_tags.insert(0, 'AI')
        if 'AI' not in out_cats:
            out_cats.append('AI')
    if not out_tags:
        out_tags = [c for c in out_cats if c != 'Программирование'][:2]
    if not out_tags:
        for rx, tg in TITLE_RULES:
            if re.search(rx, title, re.I):
                out_tags = list(tg)
                break
    return out_tags[:8], out_cats[:3], is_ai
