---
title: Обзор R пакетов для интернет маркетинга, часть 1
date: '2018-10-11'
slug: obzor-r-paketov-dlya-internet-marketinga-chast-1
tags:
- API
- Веб-аналитика
- R
- Пакеты R
- Facebook
- ВКонтакте
- Яндекс Директ
- Яндекс Метрика
categories:
- Программирование
- R
description: Всем привет, если вы занимаетесь интернет маркетингом наверняка вам ежедневно приходится сталкиваться со множеством рекламных сервисов и как минимум одной платформой веб аналитики, если вам требуется хотя бы раз в месяц, или может быть даже раз в неделю руками сводить данные о расходах, и прочую статистическую информацию из всех источников то это чревато не только […]
original_url: https://alexeyseleznev.wordpress.com/2018/10/11/%d0%be%d0%b1%d0%b7%d0%be%d1%80-r-%d0%bf%d0%b0%d0%ba%d0%b5%d1%82%d0%be%d0%b2-%d0%b4%d0%bb%d1%8f-%d0%b8%d0%bd%d1%82%d0%b5%d1%80%d0%bd%d0%b5%d1%82-%d0%bc%d0%b0%d1%80%d0%ba%d0%b5%d1%82%d0%b8%d0%bd%d0%b3/
wp_id: 1140
draft: false
cover: ../images/covers/1140.webp
cover_generated: true
---

Всем привет, если вы занимаетесь интернет маркетингом наверняка вам ежедневно приходится сталкиваться со множеством рекламных сервисов и как минимум одной платформой веб аналитики, если вам требуется хотя бы раз в месяц, или может быть даже раз в неделю руками сводить данные о расходах, и прочую статистическую информацию из всех источников то это чревато не только большими временными затратами, но и вероятность ошибки при консолидации данных из множества источников в ручном режиме достаточно велика. В этой статье я подскажу готовые расширения (пакеты) для языка R, с помощью которых вы можете автоматизировать процесс сбора данных из большинства популярных рекламных систем и платформ веб аналитики.

![ÐÐ¾ÑÐ¾Ð¶ÐµÐµ Ð¸Ð·Ð¾Ð±ÑÐ°Ð¶ÐµÐ½Ð¸Ðµ](https://i0.wp.com/s010.radikal.ru/i313/1112/e5/b4ee063ce576.jpg)

## Какой софт нам потребуется

Т.к. в данной статье мы говорим про язык R, то вам потребуется сам [R](https://cran.r-project.org/bin/windows/base/) и среда разработки [RStudio](https://www.rstudio.com/products/rstudio/download/).

И язык R, и RStudio являются бесплатным, свободно распространяемым программным обеспечением, поэтому вы свободно можете скачивать их из официальных сайтов.

> *[Статья была написана для Хабры и впервые опубликована там же.](https://habr.com/post/425425/)*

## Как начать работу с R пакетами

Ничего сложного для начала работы с R пакетами нет, осуществляется это следующим образом:

1. Установка пакета, как правило с помощью базовой команды `install.packages`;
2. Подключение пакета, каждый раз при старте нового сеанса работы с R, данная оперция может быть выполнена с помощью команды `library` или `require`.

Разница между `library` и `require` заключается только в том, что `library` выдаст ошибку в случае попытки подключения пакета, который у вас не установлен, а `require` в этом же случае просто покажет предупреждение, при этом выполнение скрипта будет продолжено.

Для установки приведённых в статье пакетов с GitHub вам предварительно необходимо установить пакет devtools, для этого выполните команду `install.packages("devtools")`.

## CRAN или GitHub

В ходе чтения данной статьи у вас возможно возникнет вопрос из какого репозитория лучше устанавливать тот, или иной пакет, на самом деле на GitHub как правило лежат наиболее актуальные dev версии пакетов от разработчиков, т.е. в них есть все новые функции которых возможно нет в версии пакета которая доступна на CRAN, но соответственно dev версия может быть на момент загрузки не достаточно протестирована и содержать ошибки.

Версия на CRAN перед загрузкой тщательно проверяется командой специалистов, и должна соответствовать всем [требованиям политики данного репозитория](https://cran.r-project.org/web/packages/policies.html), в случае загрузки пакета с CRAN вы можете быть уверены, что он никак не навредит вашим данным, не будет создать без вашего разрешения какие либо непонятные файлы на вашем ПК и т.д.

## Какие навыки нужны для работы с R пакетами

На самом деле от вас потребуется только понимание предметной области интернет маркетинга, никаких навыков программирования в данном случае не требуется, т.к. речь буде идти о готовых пакетах, используя функции из которых вы сможете автоматизировать руинную часть своей работы.

В статье не будет подробного описание по работе с каждой функцией рассматриваемых пакетов, т.к. такая статья была бы слишком длинной, но я опишу возможности каждого пакета, дам список основных функций которые вам потребуется, а так же дам ссылку на официальную документацию, с помощью которой вы уже сможете наиболее подробно разобраться со всеми доступными в том, или ином пакете функциями. К тому же к каждому пакету я приведу небольшой пример кода, что бы вам был более понятен синтаксис.

## [ryandexdirect](https://selesnow.github.io/ryandexdirect) — загрузка данных из Яндекс. Директ

Установка пакета с GitHub: `devtools::install_github("selesnow/ryandexdirect")`  
Официальная документация: [ссылка](https://selesnow.github.io/ryandexdirect)

Данный пакет предназначен для работы с API одной из наиболее популярных рекламных площадок в СНГ — Яндекс. Директ.

### Возможности пакета ryandexdirect

1. Авторизация в API Яндекса;
2. Загрузка списка рекламных кампаний, ключевых слов, объявлений;
3. Загрузка статистических данных из аккаунтов Яндекс. Директ с помощью [сервиса Reports](https://tech.yandex.ru/direct/doc/reports/reports-docpage/).
4. Остановка и возобновление показов объявлений на уровне рекламных кампаний, ключевых слов и объявлений.
5. Запрос остатка средств и других параметров общего счёта.
6. Загрузка справочной информации (курсы валют, географический справочник и т.д.)

### Основные функции

Основные функции доступные в ryandexdirect, которые могут вам понадобиться для работы с API Яндекс. Директ:

- `yadirAuth` — Авторизация в API;
- `yadirGetAds`, `yadirGetCampaignList`, `yadirGetKeyWords` — Загрузка списка объявлений, рекламных кампаний, ключевых слов;
- `yadirGetReport` — Загрузка статистики из Яндекс. Директ.
- `yadirGetDictionary` — Загрузка справочной информации.
- `yadirStartAds`, `yadirStartCampaigns`, `yadirStartKeyWords` —

**Пример кода для загрузки статистики с помощью пакета ryandexdirect**

```

library(ryandexdirect)
stat <- yadirGetReport(ReportType = "ACCOUNT_PERFORMANCE_REPORT", 
                       DateRangeType = "CUSTOM_DATE", 
                       DateFrom = "2018-01-01", 
                       DateTo = "2018-05-10", 
                       FieldNames = c("AdNetworkType",
                                               "Impressions",
                                               "Clicks",
                                               "Cost"), 
                       FilterList = c("CampaignId IN 123456 ,987654","Clicks GREATER_THAN 100"),
                       IncludeVAT = "YES", 
                       IncludeDiscount = "NO", 
                       Login = "ваш логин", 
                       TokenPath = "C:/token_yandex")
```

Более подробно о каждом аргументе можно узнать из официальной справке [ryandexdirect](https://selesnow.github.io/ryandexdirect) или Яндекс. Директ [API Reports сервис](https://tech.yandex.ru/direct/doc/reports/reports-docpage/).

## [RAdwords](https://www.rdocumentation.org/packages/RAdwords/) — загрузка данных из Google Ads (ex Google AdWords)

Установка пакета с CRAN: `install.packages("RAdwords")`  
Установка пакета с GitHub: `devtools::install_github("jburkhardt/RAdwords")`  
Официальная документация: [ссылка](https://jburkhardt.github.io/RAdwords/)

### Возможности пакета RAdwords

Основная возможность данного пакета — авторизация в API Google Ads и загрузка статистики из всех доступных в данном интерфейсе отчётов.

### Основные функции пакета RAdwords

На самом деле пакет в принципе содержит не особо много функций, но я за всё время пользовался всего тремя:

- `doAuth` — Авторизация;
- `statement` — Формирование тела запроса к API;
- `getData` — Загрузка данных из API.

**Пример работы с пакетом RAdwords**

```

<span class="hljs-keyword">library</span>(RAdwords)
# запрос токена
adw_token &lt;- doAyth()

# формирование запроса
<span class="hljs-keyword">body</span> &lt;- statement(<span class="hljs-keyword">select</span>=c(<span class="hljs-symbol">'AccountDescriptiveName</span>',
                           <span class="hljs-symbol">'ExternalCustomerId</span>',
                           <span class="hljs-symbol">'AccountCurrencyCode</span>',
                           <span class="hljs-symbol">'AdNetworkType1</span>',
                           <span class="hljs-symbol">'RegionCriteriaId</span>',
                           <span class="hljs-symbol">'CountryCriteriaId</span>',
                           <span class="hljs-symbol">'CityCriteriaId</span>',
                           <span class="hljs-symbol">'Device</span>',
                           <span class="hljs-symbol">'Month</span>',
                           <span class="hljs-symbol">'Year</span>',
                           <span class="hljs-symbol">'Impressions</span>',
                           <span class="hljs-symbol">'Clicks</span>',
                           <span class="hljs-symbol">'Interactions</span>',
                           <span class="hljs-symbol">'VideoViews</span>',
                           <span class="hljs-symbol">'Cost</span>',
                           <span class="hljs-symbol">'Conversions</span>'
),
    <span class="hljs-keyword">report</span>=<span class="hljs-string">"GEO_PERFORMANCE_REPORT"</span>,
    start=<span class="hljs-string">"2018-09-01"</span>,
    <span class="hljs-keyword">end</span>=<span class="hljs-string">"2018-09-20"</span>)

my_data &lt;- getData(clientCustomerId = <span class="hljs-string">"000-000-0000"</span>,
                   google_auth = adw_token ,
                   statement = <span class="hljs-keyword">body</span>,
                   transformation = T)
```

Список доступных в API Google Ads отчётов, и полей вы можете найти по [ссылке](https://developers.google.com/adwords/api/docs/appendix/reports) в официальной справке.

## [adwordsR](https://www.rdocumentation.org/packages/adwordsR/) — более новый и функциональный пакет для загрузка=и данных из Google Ads (ex Google AdWords)

Установка пакета с CRAN: `install.packages("adwordsR")`  
Установка пакета с GitHub: `devtools::install_github("cran/adwordsR")`

Пакет adwordsR по смыслу схож с RAdwords, но он более новый, и имеет гораздо больший набор функций.

### Возможности пакета adwordsR

Помимо описанных выше возможностей пакета RAdwords, adwordsR даёт вам широкие возможности по работе с TargetingIdeaService, службе с помощью которой можно получать варианты таргетинга прямо из инструмента или платформы, что помогает автоматизировать оптимизацию аккаунта.

### Основные функции пакета adwordsR

- `generateAdwordsToken` — Запрос токена для работы с API Google Ads;
- `loadAdwordsToken` — Загрузка запрошенного, и сохранённого ранее токена;
- `getReportData` — Загрузка статистики из аккаунта Google Ads.

**Пример работы с пакетом adwordsR**

```

library(adwordsR)
# Запрос токена
adw_token <- generateAdwordsToken(saveNewToken = TRUE, addGitignore = FALSE)
# Загрузка ранее сохранённого токена 
adw_token <- loadAdwordsToken()
# Запрос данных
AdWordsData <- getReportData(reportType             = "CAMPAIGN_PERFORMANCE_REPORT",
                             startDate              = "2018-08-01",
                             endDate                = "2018-08-15",
                             clientCustomerId       = "000-000-0000",
                             credentials            = adw_token,
                             attributes             = "CampaignName,CampaignStatus",
                             segment                = "Date,AdNetworkType1",
                             metrics                = "AverageCost,Clicks,Conversions",
                             includeZeroImpressions = TRUE,
                             useRequestedHeaders = FALSE)
```

## [rfacebookstat](https://www.rdocumentation.org/packages/rfacebookstat/) — загрузка данных из рекламных кабинетов Facebook

Установка пакета с CRAN: `install.packages("rfacebookstat")`  
Установка пакета с GitHub: `devtools::install_github("selesnow/rfacebookstat")`  
Официальная документация: [ссылка](https://selesnow.github.io/rfacebookstat)

### Возможности пакета rfacebookstat

1. Авторизация в API Facebook
2. Загрузка списка доступных вам бизнес-менеджеров;
3. Загрузка списка рекламных аккаунтов;
4. Загрузка списка рекламных кампаний, групп объявлений, объявлений.
5. Загрузка статистики на уровне рекламного аккаунта, рекламных кампаний, групп объявлений и объявлений.
6. Загрузка списка пользователей у которых есть доступ к рекламному аккаунту.
7. Управление доступами к рекламным аккаунтам.

### Основные функции пакета rfacebookstat

- `fbGetToken` — Авторизация в API Facebook;
- `fbGetBusinessManagers` — Загрузка списка бизнес менеджера;
- `fbGetAdAccounts` — Загрузка списка рекламных аккаунтов;
- `fbGetCampaigns`, `fbGetAds`, `fbGetAdSets` — Загрузка списка рекламных кампаний, объявлений и групп объявлений;
- `fbGetMarketingStat` — Загрузка статистики из рекламных аккаунтов Facebook.

**Пример кода для работы с rfacebookstat**

```

library(rfacebookstat)
token <- fbGetToken(app_id = 00000000000000)
fb_data <- fbGetMarketingStat(accounts_id = "act_00000000000000",
                              level = "campaign",
                              fields = "campaign_name,actions",
                              action_breakdowns = "action_link_click_destination",
                              date_start = "2017-11-01",
                              date_stop = "2017-11-20",
                              interval = "day",
                              access_token = token)
```

## [rvkstat](https://selesnow.github.io/rvkstat) — загрузка данных из API Вконтакте

Установка пакета с GitHub: `devtools::install_github("selesnow/rvkstat")`  
Официальная документация: [ссылка](https://selesnow.github.io/rvkstat)

Достаточно мощный и многофункциольный пакет для работы с API социальной сети Вконтакте.

### Возможности пакета rvkstat

1. Авторизация в API Вконтакте;
2. Загрузка данных из рекламных кабинетов Вконтакте;
3. Загрузка справочной информации из Вконтакте;
4. Загрузка некоторой информации о пользователе Вконтакте;
5. Загрузка статистики из рекламного кабинета Вконтакте;
6. Загрузка статистики о посещениях сообществ Вконтакте.

### Основные функции пакета rvkstat

Пакет rvkstat на момент написания статьи содержит более 30 функции, вот наиболее полезные из них:

- `vkAuth` — Авторизация;
- `vkGetAdStatistics` — Загрузка статистики из рекламного кабинета;
- `vkGetAdCampaigns`, `vkGetAds` — Загрузка списка рекламных кампаний и объявлений;
- `vkGetGroupStat` — Загрузка статистики о посещении групп и сообществ Вконтакте.

**Пример кода для работы с пакетом rvkstat**

```

library(rvkstat)
my_tok <- vkAuth(app_id = 111,app_secret = "efbscuyewb7cb4ru4bj")
# Список рекламных кампаний
camp <- vkGetAdCampaigns(account_id = 1, access_token = my_tok$access_token)
# Статистика по рекламным кампаниям
vk_stat_by_campaign <- vkGetAdStatistics(account_id = 1,
                                         ids_type = "campaign",
                                         ids = camp$id ,
                                         period = "day",
                                         date_from = "2010-01-01", 
                                         date_to = "2017-09-10",
                                         access_token = my_tok$access_token)
```

## [rmytarget](https://www.rdocumentation.org/packages/rmytarget/) — загрузка данных из API MyTarget

Установка пакета с CRAN: `install.packages("rmytarget")`  
Установка пакета с GitHub: `devtools::install_github("selesnow/rmytarget")`  
Официальная документация: [ссылка](https://selesnow.github.io/rmytarget)

### Возможности пакета rmytarget

1. Авторизация в API MyTarget по схеме Code Grant;
2. Загрузка списка рекламных кампаний, объявлений.
3. Загрузка статистики на уровне рекламных кампаний и объявлений.

### Основные функции пакета rmytarget

- `myTarAuth` — Авторизация;
- `myTarGetAdList`, `myTarGetCampaignList` — Загрузка списка объявлений и рекламных кампаний;
- `myTarGetStats` — Загрузка статистики по объявлениям и рекламным кампаниям.

**Пример кода для работы с rmytarget**

```

library(rmytarget)
# запрос списка объявлений 
Ads <- myTarGetAdList(login = "ваш логин")
# запрос статистики по объявлениям
a_stat <- myTarGetStats(date_from = "2016-08-01",
                        date_to = "2016-08-10",
                        object_type = "banners",
                        object_id = Ads$id,
                        stat_type = "day",
            login = "ваш логин")
```

## [rym](https://www.rdocumentation.org/packages/rym/) — загрузка данных из API Яндекс. Метрики

Установка пакета с CRAN: `install.packages("rym")`  
Установка пакета с GitHub: `devtools::install_github("selesnow/rym")`  
Официальная документация: [ссылка](https://selesnow.github.io/rym)

### Основные возможности пакета rym

Пакет rym позволяет вам работать со всеми доступными в Яндекс. Метрики API интерфейсами:

1. Авторизация по протоколу oAuth2;
2. Работа с [API управления](https://tech.yandex.ru/metrika/doc/api2/management/intro-docpage/);
3. Работа [с API отчётов](https://tech.yandex.ru/metrika/doc/api2/api_v1/intro-docpage/);
4. Работа с [API совместимым с Core API Google Analytics v3](https://tech.yandex.ru/metrika/doc/api2/ga/intro-docpage/);
5. Работа с [Logs API](https://tech.yandex.ru/metrika/doc/api2/logs/intro-docpage/).

### Основные функции пакета rym

- `rym_auth` — Авторизаця;
- `rym_get_counters` — Загрузка списка счётчиков Яндекс. Метрики;
- `rym_get_data` — Загрузка данных из API отчётов;
- `rym_get_ga` — Загрузка данных из API совместимым с Core API Google Analytics;
- `rym_get_logs` — Загрузка сырых данных из Logs API.

**Пример работы с пакетом rym**

```

reporting.api.stat <- rym_get_data(counters   = "00000000,111111111",
                                   date.from  = "2018-08-01",
                                   date.to    = "yesterday",
                                   dimensions = "ym:s:date,ym:s:lastTrafficSource",
                                   metrics    = "ym:s:visits,ym:s:pageviews,ym:s:users",
                                   filters    = "ym:s:trafficSourceName=='Переходы из поисковых систем' AND ym:s:isNewUser=='Yes'",
                                   sort       = "-ym:s:date",
                                   accuracy   = "full",
                                   login      = "ваш логин",
                                   token.path = "metrica_token",
                                   lang       = "ru")
```

# Заключение

Итак с помощью приведённых в этой статье пакетов вы вполне можете автоматизировать сбор данных из таких источников как Яндекс. Директ, Google Ads, Facebook, Вконтакте, MyTarget и Яндекс. Метрика. Конечно это далеко не исчерпывающий список сервисов которые используются интрент маркетологами, но уместить все инструменты в одну статью достаточно проблематично, поэтому если данная статья получит положительные отзывы я напишу продолжение.

Далее полученные данные можно преобразовывать с помощью пакета `dplyr`, и записывать в различные базы данных с помощью DBI интерфейса, но это уже довольно объёмные темы для следующих статей.

Если у вас в арсенале так же есть интересные пакеты, которые могут помочь в автоматизации сбора данных из рекламных источников или веб-аналитических платформ, оставляйте их в комментариях к этой статье.

---

[Оригинал статьи на Хабре.](https://habr.com/post/425425/)
