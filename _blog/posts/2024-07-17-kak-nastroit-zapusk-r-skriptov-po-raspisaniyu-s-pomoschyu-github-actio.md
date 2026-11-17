---
title: Как настроить запуск R скриптов по расписанию с помощью GitHub Actions
date: '2024-07-17'
slug: kak-nastroit-zapusk-r-skriptov-po-raspisaniyu-s-pomoschyu-github-actio
tags:
- Автоматизация
- GitHub
categories:
- Программирование
- R
description: В этом видео уроке я погружаюсь в мир непрерывной интеграции и развёртывания (CI/CD), а также расскажу, как автоматизировать запуск скриптов с помощью GitHub Actions. Я покажу способ, который позволяет настроить расписание запуска ваших скриптов без необходимости аренды серверов.
original_url: https://alexeyseleznev.wordpress.com/2024/07/17/%d0%ba%d0%b0%d0%ba-%d0%bd%d0%b0%d1%81%d1%82%d1%80%d0%be%d0%b8%d1%82%d1%8c-%d0%b7%d0%b0%d0%bf%d1%83%d1%81%d0%ba-r-%d1%81%d0%ba%d1%80%d0%b8%d0%bf%d1%82%d0%be%d0%b2-%d0%bf%d0%be-%d1%80%d0%b0%d1%81%d0%bf/
wp_id: 1638
draft: false
cover: ../images/covers/1638.webp
cover_generated: true
---

В этом видео уроке я погружаюсь в мир непрерывной интеграции и развёртывания (CI/CD), а также расскажу, как автоматизировать запуск скриптов с помощью GitHub Actions. Я покажу способ, который позволяет настроить расписание запуска ваших скриптов без необходимости аренды серверов.

Из видео вы узнаете:

- Основы CI/CD и их роль в автоматизации.
- Настройка рабочего процесса с GitHub Actions.
- Конфигурация YAML файлов для управления задачами.
- Настройка автоматического запуска скриптов по расписанию.

## Видео

{{video: https://www.youtube.com/embed/SR69O1bkzmI?version=3&rel=1&showsearch=0&showinfo=1&iv\_load\_policy=1&fs=1&hl=en&autohide=2&wmode=transparent}}

### Тайм коды:

- 00:00 Вступление
- 00:49 CI/CD: Непрерывная интеграция и непрерывное развёртывание
- 01:45 Что такое GitHub Actions
- 02:30 Обзор рабочего процесса
- 03:05 Создание репозитория на GitHub
- 05:11 Добавляем в репозиторий R-скрипт
- 08:03 Настройка GitHub Actions
- 09:47 Конфигурация YAML файла, описывающего рабочий процесс
- 10:10 Настройка расписания запуска в YAML файле
- 12:17 Разбираем все команды в YAML файле рабочего процесса
- 19:01 Создание переменных среды в GitHub репозитории
- 20:26 Отправляем проект на GitHub
- 20:52 Запускаем GitHub Action
- 22:46 Заключение

### Презентация

{{video: https://www.slideshare.net/slideshow/embed\_code/2gfh3KyxpSFrHy?hostedIn=slideshare}}

## Конспект

### Что такое CI/CD

**CI/CD** — это методология и набор практик для автоматизации процессов разработки, тестирования и развертывания программного обеспечения. CI/CD расшифровывается как Continuous Integration (непрерывная интеграция) и Continuous Deployment (непрерывное развертывание) или Continuous Delivery (непрерывная доставка).

**Непрерывная интеграция (CI)** — это практика частого слияния изменений в основной кодовой базе. Основные принципы CI:

- Разработчики регулярно интегрируют свои изменения в основной репозиторий.
- После каждого слияния запускаются автоматические тесты, чтобы убедиться, что изменения не ломают существующий код.
- Выявленные ошибки устраняются сразу.

**Continuous Deployment** (непрерывное развертывание) и **Continuous Delivery** (непрерывная доставка) — это методы автоматического развертывания и доставки изменений в продакшн.

- •**Continuous****Delivery**: Изменения автоматически тестируются и подготавливаются к развертыванию, но финальное развертывание может требовать ручного подтверждения.
- •**Continuous****Deployment**: Все изменения, прошедшие автоматическое тестирование, автоматически развертываются в производственной среде.

### Что такое GitHub Actions

**GitHub Actions** — это платформа для автоматизации процессов в рамках репозитория GitHub. Она позволяет создавать и запускать рабочие процессы (workflows), которые автоматически выполняются при наступлении определенных событий в репозитории.

Основные компоненты GitHub Actions:

- •**Workflow** **(рабочий процесс**)**:** YAML-файл, который описывает автоматизируемый процесс.
- •**Job** **(задача):** Определенная часть рабочего процесса, которая выполняется на виртуальной машине.
- •**Step** **(шаг):** Отдельные шаги внутри задачи, которые могут включать команды или действия (actions).
- •**Action** **(действие):** Повторно используемый блок, который выполняет одну конкретную задачу, например, установка зависимостей, запуск тестов и т.д.

### Обзор рабочего процесса

Рабочий процесс выглядит следующим образом:

1. Создание репозитория на GitHub
2. Создание R-скрипта
3. Настройка GitHub Actions
4. Создание переменных среды в репозитории GitHub
5. Коммит и пуш изменений

### Создание репозитория:

- Создайте новый репозиторий на GitHub или используйте уже существующий. Добавьте ваш код на языке R в репозиторий.
- Скопируйте URL для клонирования репозитория

![](https://i0.wp.com/img.netpeak.ua/alsey/4OF2XV.png)

- Откройте RStudio: File -> New Project -> Version Control -> Git – > Вставить скопированный URL в поле Repository URL. Необходим установленный Git.

### Добавляем в проект R скрипт

Я для удобства использую функцию `use_tuis('currency_rate_sender')`, она создаст каталог R, и в нём файл скрипта.

Листинг нашего кода:

```
library(httr)
library(jsonlite)
library(telegram.bot)

# Функция для получения курса валют
get_exchange_rate <- function(api_key, currency) {
  url <- paste0("https://api.exchangerate-api.com/v4/latest/USD?apikey=", api_key)
  response <- GET(url)
  data <- fromJSON(content(response, "text"))
  return(data$rates[[currency]])
}

# Функция для отправки сообщения в Telegram
send_telegram_message <- function(bot_token, chat_id, message) {
  bot <- Bot(token = bot_token)
  bot$sendMessage(chat_id = chat_id, text = message)
}

# Получение переменных среды
api_key   <- Sys.getenv("EXCHANGE_RATE_API_KEY")
bot_token <- Sys.getenv("TELEGRAM_BOT_TOKEN")
chat_id   <- Sys.getenv("TELEGRAM_CHAT_ID")
currency  <- "EUR"

# Получение курса валют и отправка сообщения
exchange_rate <- get_exchange_rate(api_key, currency)
message <- paste("Курс", currency, "к USD:", exchange_rate)
send_telegram_message(bot_token, chat_id, message)
```

Данный код запрашивает по API курсы валют, после чего отправляет их в Telegram Чат. Для того что бы использовать этот же код вам необходимо создать Telgram бота через BotFather, и получить к нему API Token, так же получить ID вашего с ботом чата. О том, как это сделать можно узнать из видео урока, ссылку на которой я размещу в конце статьи.

Так же вам надо получить API ключ для <https://www.exchangerate-api.com/>.

### Настройка GitHub Actions

Теперь необходимо создать конфигурацию для нашего рабочего процесса, это делается с помощью yaml файла.

Используйте функцию `use_github_action('currency_rate_sender')`. Работа функции закончится ошибкой, но она создаст необходимую нам структуру папок `.github/workflows`.

Далее создайте в проекте, в папке workflows текстовый файл currency\_rate\_sender.yaml. И добавьте в него следующие команды:

```
name: Run R script daily

on:
  schedule:
    - cron: '0 10 * * *'  # Ежедневно в 10:00 UTC
    - cron: '51 17 * * *'  # Ежедневно в 19:00 по Каирскому времени
  workflow_dispatch:

jobs:
  run-r-script:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2
      
    - name: Set timezone to Cairo
      uses: szenius/set-timezone@v2.0
      with:
        timezoneLinux: "Africa/Cairo"
        
    - name: Log current time
      run: date

    - name: Set up R
      uses: r-lib/actions/setup-r@v2
      with:
        r-version: '4.0.3'
        
    - name: Install Linux package
      run: |
        sudo apt-get install libcurl4-openssl-dev

    - name: Install R packages
      run: |
        Rscript -e 'install.packages(c("curl", "httr", "jsonlite", "telegram.bot"), repos="https://cran.rstudio.com/")'

    - name: Run R script
      env:
        EXCHANGE_RATE_API_KEY: ${{ secrets.EXCHANGE_RATE_API_KEY }}
        TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
        TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
      run: |
        Rscript R/currency_rate_sender.R
```

Давайте рассмотрим все эти команды подробнее.

```
name: Run R script daily
```

Задаёт название рабочего процесса

```
on:
  schedule:
    - cron: '0 10 * * *'  # Ежедневно в 10:00 UTC
    - cron: '51 17 * * *'  # Ежедневно в 19:00 по Каирскому времени
  workflow_dispatch:
```

Блок **on** определяет, какие события в репозитории запускают workflow. В нем можно указать различные события, такие как push, pull\_request, schedule и другие. Рассмотрим некоторые из них:

- События **push** и **pull\_request –** Эти события запускают workflow при выполнении push или создании pull request соответственно.
- Событие **schedule** позволяет запускать workflow по расписанию, используя синтаксис cron. Cron выражения состоят из пяти полей, каждое из которых задает единицу времени:
  - Минуты (0-59)
  - Часы (0-23)
  - День месяца (1-31)
  - Месяц (1-12)
  - День недели (0-6, где 0 – воскресенье)
- Событие **workflow\_dispatch** позволяет вручную запускать workflow через интерфейс GitHub.
- Событие **release** запускает workflow при создании релиза.
- Событие **issue\_comment** запускает workflow при добавлении комментария к issue.

•Когда используется запуск GitHub Action через schedule необходимо учитывать следующие нюансы. Описанные в справке GitHub:

- Событие schedule может быть отложено в периоды высокой нагрузки при выполнении рабочего процесса GitHub Actions. Время высокой загрузки включает начало каждого часа. Если нагрузка достаточно высока, некоторые задания в очереди могут быть удалены. Чтобы уменьшить вероятность задержки, запланируйте выполнение рабочего процесса в другое время часа.
- В общедоступном репозитории запланированные рабочие процессы автоматически отключаются, если в течение 60 дней не происходит никаких действий с репозиторием.

```
jobs:
  run-r-script:
    runs-on: ubuntu-latest
```

Создаёт виртуальную машину на ubuntu, можно создать и на Windows.

```
steps:
    - name: Checkout repository
      uses: actions/checkout@v2
```

Копирует в виртуальную машину всё содержимое репозитория.

```
- name: Set up R
      uses: r-lib/actions/setup-r@v2
      with:
        r-version: '4.0.3'
```

Устанавливает указанную версию R.

```
- name: Install Linux package
      run: |
        sudo apt-get install libcurl4-openssl-dev
```

Устанавливает на Linux специальный программный пакет, необходимый для установки R пакета httr и telegram.bot.

```
- name: Install R packages
      run: |
        Rscript -e 'install.packages(c("httr", "jsonlite", "telegram.bot"), repos="https://cran.rstudio.com/")'
```

Устанавливает на виртуальную машину необходимые пакеты.

```
- name: Run R script
      env:
        EXCHANGE_RATE_API_KEY: ${{ secrets.EXCHANGE_RATE_API_KEY }}
        TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
        TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
      run: |
        Rscript R/currency_rate_sender.R
```

Считывает переменные среды из репозитория, и запускает выполнение R скрипта.

### Создание переменных среды в репозитории GitHub

1. Перейдите в ваш репозиторий на GitHub.
2. Перейдите в раздел Settings.
3. В левом меню выберите Secrets and variables -> Actions.
4. Нажмите на кнопку New repository secret и создайте следующие переменные:
5. Создайте все необходимые вам переменные среды.

### Публикация на GitHub

Теперь отправьте всё, что мы сделали коммитом на GitHub.

1. В RStudio откройте вкладку Git
2. Выделите все файлы галочками
3. Нажмите кнопку Commit
4. Напишите комментарий
5. Нажмите кнопку Commit
6. Нажмите кнопку Push

Теперь вы опубликовали ваш проект на GitHub.

### Тестирование рабочего процесса на GitHub

Теперь вернитесь в свой репозиторий на GitHub, перейдите в Actions.

![](https://i0.wp.com/img.netpeak.ua/alsey/4OJCIW.png)

## Ссылки

Приведённые ниже ссылки позволят разобраться с некоторыми моментами, которые не рассматривались подробно в статье

- [Видео урок по созданию telegram бота](https://www.youtube.com/watch?v=Tu9tHHhQU0g)
- [Урок по интеграции RStudio с GitHub](https://www.youtube.com/watch?v=OPiMVVBYZsM)
