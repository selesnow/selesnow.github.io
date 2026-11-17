---
title: rfacebookstat 2.0.0 | Обзор релиза и 6 видео уроков по работе с Facebook Marketing API на языке R
date: '2019-12-23'
slug: rfacebookstat-2-0-0-obzor-reliza-i-6-video-urokov-po-rabote-s-facebook
tags:
- API
- Facebook
- R
- Пакеты R
categories:
- Программирование
- R
description: Последние несколько месяцев я много работал над функционалом пакета rfacebookstat, предназначенным для работы с Facebook Marketing API на языке R. В результате чего пакет был значительно улучшен, и работать с его помощью с одним из наиболее запутанных и сложных API, их тех с которыми мне вообще приходилось работать, станет намного проще. В этой статье я […]
original_url: https://alexeyseleznev.wordpress.com/2019/12/23/rfacebookstat-2-0-0-%d0%be%d0%b1%d0%b7%d0%be%d1%80-%d1%80%d0%b5%d0%bb%d0%b8%d0%b7%d0%b0-%d0%b8-6-%d0%b2%d0%b8%d0%b4%d0%b5%d0%be-%d1%83%d1%80%d0%be%d0%ba%d0%be%d0%b2-%d0%bf%d0%be-%d1%80%d0%b0%d0%b1/
wp_id: 1290
draft: false
cover: ../images/covers/1290.webp
cover_generated: true
---

Последние несколько месяцев я много работал над функционалом пакета `rfacebookstat`, предназначенным для работы с Facebook Marketing API на языке R.

В результате чего пакет был значительно улучшен, и работать с его помощью с одним из наиболее запутанных и сложных API, их тех с которыми мне вообще приходилось работать, станет намного проще.

В этой статье я приведу 6 видео уроков о том как использовать пакет `rfacebookstat` , и в конце статьи будет описание всех доработок вошедших в релиз 2.0.0

rfacebookstat 2.0.0

Установить новую версию пакета можно из CRAN или GitHub.

CRAN: `install.packages("rfacebookstat")`

GitHub: `devtools::install_github("selesnow/rfacebookstat")`

## 6 видео уроков по работе с Facebook Marketing API на языке R

#### 1. Простая авторизация в Facebook Marketing API

{{video: https://www.youtube.com/embed/SgcxDqZ-5Qg?version=3&rel=1&showsearch=0&showinfo=1&iv\_load\_policy=1&fs=1&hl=en&autohide=2&wmode=transparent&listType=playlist&list=PLD2LDq8edf4pItOb-vZTG5AXZK2niJ8\_R}}

#### 2. Авторизация в Facebook Marketing API через собственное приложение

{{video: https://www.youtube.com/embed/VLhsQDAyx5E?version=3&rel=1&showsearch=0&showinfo=1&iv\_load\_policy=1&fs=1&hl=en&autohide=2&wmode=transparent}}

#### 3. Автоматическая авторизация файл .Renviro

{{video: https://www.youtube.com/embed/oZhV1U5fMZ0?version=3&rel=1&showsearch=0&showinfo=1&iv\_load\_policy=1&fs=1&hl=en&autohide=2&wmode=transparent}}

#### 4. Автоматическая авторизация и создание переменных среды на Windows

{{video: https://www.youtube.com/embed/zoNvu2T6IFc?version=3&rel=1&showsearch=0&showinfo=1&iv\_load\_policy=1&fs=1&hl=en&autohide=2&wmode=transparent}}

#### 5. Опции пакета и загрузка объектов из рекламных кабинетов Facebook

{{video: https://www.youtube.com/embed/ZaOvO5k6Ses?version=3&rel=1&showsearch=0&showinfo=1&iv\_load\_policy=1&fs=1&hl=en&autohide=2&wmode=transparent}}

#### 6. Загрузка статистики, конверсии и окна атрибуции в Facebook Marketing API

{{video: https://www.youtube.com/embed/hc\_hknCWZc4?version=3&rel=1&showsearch=0&showinfo=1&iv\_load\_policy=1&fs=1&hl=en&autohide=2&wmode=transparent}}

## Список всех доработок вошедших в релиз rfacebookstat 2.0.0

- **Новые функции**
  - `fbAuth()` – Новая функция авторизации, подробности в разеле ***Авторизация***.
  - `fbGetUserAdAccounts()` – Загрузка списка аккаунтов к которым есть доступ у определённого пользователя facebook.
  - `fbGetAdAccountsConversions()` – Получить список конвесий настроенных в рекламной аккаунте.
  - `fbGetAdVideos()` – Загрузка списка видео из рекламного аккаунта
  - `fbGetSettings()` – Вывести в консоль все применённые в пакете настройки.
- **Доработанные функции**
  - В функцию `fbGetMarketingStat()` добавлен аргумент *attribution\_window* с помощью которого вы можете запрашивать поле *actions* и применять к нему различные окна атрибуции.
  - Так же был полностью переписан процесс разворачивания вложенных полей типа *actions*, и прочих. Теперь функция `fbGetMarketingStat()` работает с ними более стабильно.
  - Изменения в функциях `fbGetApps()` и `fbGetPages()` теперь вы можете запрашивать список продвигаемых страниц и приложений непосредственно из рекламных аккаунтов.
    - Теперь вы можете запрашивать список страниц и приложений из конкретного аккаунта, используя аргумент *accounts\_id*. Это новый аргумент который был добавлен вместо устаревшего *projects\_id*.
    - В обеих функциях значительно расширен список полей которые они возвращают.
  - В большинстве функций аргумент *accounts\_id* больше не является обязательным, и по умолчанию запрашивает данные по всем рекламным аккаунтам к которым у вас есть доступ, эта доработка коснулась следующих функций:
    - `fbGetCampaigns()`
    - `fbGetAdSets()`
    - `fbGetAds()`
    - `fbGetAdCreative()`
    - `fbGetApps()`
    - `fbGetPages()`
    - `fbGetAdAccountUsersPermissions()`
    - `fbGetAdAccountUsers()`
- **Удалённые функции**
  - Из пакета полностью удалена функция `fbGetProjects()`, в связи с тем, что в Facebook больше не существует проектов.
- **Авторизация**
  - Был значительно улучшен процесс авторизации, теперь помимо опций вы можете использовать переменные среды.
  - Так же при авторизации начиная с версии 2.0.0 учётные данные сохраняются в локальный файл, и по умолчанию вы получаете долгосрочный токен.
  - В пакет встроено собственное приложение, теперь нет необходимости регистрировать собственное приложение и запрашивать стандартнй доступ к API, он уже по умолчанию вшит в пакет.
- **Документация**
  - В виньетку по загрузке статистики добавлена информация про окна атрибуции: `vignette('rfacebookstat-get-statistics', package = 'rfacebookstat')`
  - В пакет добавлена новая виньетка посвящённая процессу авторизации и его автоматизации: `vignette('rfacebookstat-authorization', package = 'rfacebookstat')`
- **Прочее**
  - Пакет переведён на работу с версией API v5.0.
