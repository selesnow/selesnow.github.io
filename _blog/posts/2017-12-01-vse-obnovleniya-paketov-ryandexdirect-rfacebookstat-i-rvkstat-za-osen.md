---
title: Все обновления пакетов ryandexdirect, rfacebookstat и rvkstat за осень 2017.
date: '2017-12-01'
slug: vse-obnovleniya-paketov-ryandexdirect-rfacebookstat-i-rvkstat-za-osen
tags:
- API
- R
- Facebook
- ВКонтакте
- Яндекс Директ
categories:
- Программирование
- R
description: В этой статье я собрал все доработки R клиентов ryandexdirect, rfacebookstat и rvkstat за осень 2017 года.
original_url: https://alexeyseleznev.wordpress.com/2017/12/01/%d0%b2%d1%81%d0%b5-%d0%be%d0%b1%d0%bd%d0%be%d0%b2%d0%bb%d0%b5%d0%bd%d0%b8%d1%8f-%d0%bf%d0%b0%d0%ba%d0%b5%d1%82%d0%be%d0%b2-ryandexdirect-rfacebookstat-%d0%b8-rvkstat-%d0%b7%d0%b0-%d0%be%d1%81%d0%b5/
wp_id: 1069
draft: false
---

В этой статье я собрал все доработки R клиентов ryandexdirect, rfacebookstat и rvkstat за осень 2017 года.

![Картинки по запросу new features](../images/vse-obnovleniya-paketov-ryandexdirect-rfacebookstat-i-rvksta-b389226d.webp)

В каждом из трёх пакетов был ряд значительных доработок, о которых и пойдёт речь ниже:

# ryandexdirect

***ryandexdirect** – R клиент для работы с API Яндекс. Директ версий Live 4 и 5, а так же для работы с API Яндекс. Метрики.*

Репозиторий с подробным описанием функционала находится [тут](https://github.com/selesnow/ryandexdirect/).

Наиболее популярный из разработанных мной пакетов, почти 50% от посещений 7 опубликованных мной репозиториев на GitHub приходятся именно на ryandexdirect.

##### Доработки и релизы ryandexdirect за осень 2017:

- Добавлены 3 функции: yadirGetAds, yadirGetKeyWords, yadirGetAdGroups ([релиз версии 2.2.0. от 13 сентября 2017 года](https://github.com/selesnow/ryandexdirect/releases/tag/2.2.0)). С помощью этих функций вы можете получить список групп объявлений, объявлений, ключевых слов с различными их параметрами.
- Доработана функция yadirGetCampaignList ([релиз версии 2.2.0. от 13 сентября 2017 года](https://github.com/selesnow/ryandexdirect/releases/tag/2.2.0)), теперь она работает без каких либо ограничений на количество возвращаемых рекламных кампаний, теперь вы можете получить полный список рекламных кампаний даже из аккаунтов в которых более 10 000 рекламных кампаний.
- В пакет ryandexdirect добавлена функция yadirGetMetrikaGAData ([релиз версии 2.3.0. от 21 сентября 2017 года.](https://github.com/selesnow/ryandexdirect/releases/tag/2.3.0)) предназначенная для работы с API Яндекс Метрики совместимым с Google Analytics Core Reporting API (v3) и даёт возможность использовать привычные параметры запросов при сборе статистики, если ранее вы работали с Google Analytics Core Reporting API (v3).
- Добавлена функция `yadirGetBalance`, с помощью которой можно получить все параметры общего счёта включая текущий остаток средств. ([Релиз версии 2.4.0 от 4 октября 2017 года](https://github.com/selesnow/ryandexdirect/releases)).
- Векторизация функции yadirGetReport, это означает что в аргумент Login можно на вход давать вектор логинов, после чего функция соберёт данные из всех рекламным аккаунтов переданных в векторе логинов. ([Релиз версии 2.4.1. от 1 ноября 2017 года](https://github.com/selesnow/ryandexdirect/releases/tag/2.4.1)).
- Доработана функция yadirGetKeyWords, в результирующей таблице, которую возвращает данная функция добавлены поля ProductivityValue и ProductivityReferences. Отдельного релиза под эту доработку небыло, подробности можно узнать на [facebook](https://www.facebook.com/selesnow/posts/1739479252737709?pnref=story).
- Пакет ryandexdirect теперь можно установить на Linux, Unix и macOs, для этого воспользуйтесь командой install\_github(‘selesnow/ryandexdirect’, subdir = “utf8”).

# rfacebookstat

***rfacebookstat**–* R клиент для загрузки данных из бизнес менеджера и рекламных кабинетов Facebook в R.

Репозиторий пакета rfacebookstat, с подробным описанием всех доступных в пакете функций доступен по [ссылке](https://github.com/selesnow/).

##### Доработки и релизы rfacebookstat за осень 2017:

- [29 сентября 2017 года](https://github.com/selesnow/rfacebookstat/releases/tag/1.2.0) была переписана схема аутентификации и получения токена, для корректного прохождения аутентификации с помощью функции fbGetToken необходимо внести изменения в настройки вашего приложения на Facebook. В меню приложения перейдите в раздел «Вход через Facebook». В поле «Действительные URL-адреса для перенаправления OAuth» замените текущее значение на «https://selesnow.github.io/rfacebookstat/getToken/get\_token.html».
- Добавлено 2 новые функции: `fbGetBusinessManagers` и `fbGetAdAccountUsers`, для загрузки списка доступных бизнес менеджеров, а так же для загрузки списка пользователей рекламного кабинета, так же значительно доработана функция `fbGetAdAccounts` ([релиз версии 1.3.1 от 13 октября 2017 года](https://github.com/selesnow/rfacebookstat/releases/tag/1.3.1)).
- В функцию fbGetMarketingStat добавлен аргумент interval, с помощью которого вы можете получить данные с разбивкой по дням, неделям, месяцам, кварталам или годам. ([релиз версии 1.4.0 от 1 ноября 2017 года](https://github.com/selesnow/rfacebookstat/releases)).
- Функция fbGetMarketingStat теперь поддерживает работу с action\_breakdowns ([релиз версии 1.4.3 от 27 ноября 2017 года](https://github.com/selesnow/rfacebookstat/releases/tag/1.4.3)).

# rvkstat

***rvkstat**–* R клиент для загрузки данных из API интерфейса социальной сети Вконтакте в R.

Репозиторий rvkstat на GitHub, с полным описанием всех возможностей и функций пакета находится по [ссылке](https://github.com/selesnow/rvkstat/).

До осени текущего года с помощью rvkstat можно было получить статистику исключительно о посещениях и статистики сообществ Вконтакте.

##### Доработки и релизы rvkstat за осень 2017:

- Огромный [релиз версии 2.0.0](https://github.com/selesnow/rvkstat/releases/tag/2.0.0) был опубликован 19 сентября 2017 года, в общей сложности в этом релизе было добавлено более 20 новых функций для работы с рекламным кабинетом, загрузки справочников и загрузки данных о конкретном пользователи социальной сети.
- В версии 2.0.2 был доработан процесс прохождения авторазации в API Вконтакте, в связи с чем перед обновлением пакета необходимо внести корректировки в настройке вашего приложения. ([Релиз версии 2.0.2 от 29 сентября 2017 года](https://github.com/selesnow/rvkstat/releases)).
- С ноября 2017 года rvkstat теперь можно установить на Linux и Mac. ([Релиз версии 2.1.0](https://github.com/selesnow/rvkstat/releases)).

За тестирование версии 2.0.0 отдельное спасибо [Олегу Басманову.](https://www.facebook.com/basmanov)
