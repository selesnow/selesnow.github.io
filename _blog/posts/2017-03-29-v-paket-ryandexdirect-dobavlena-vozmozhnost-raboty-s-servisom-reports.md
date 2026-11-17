---
title: В пакет ryandexdirect добавлена возможность работы с сервисом Reports, и возможность загрузки справочной информации.
date: '2017-03-29'
slug: v-paket-ryandexdirect-dobavlena-vozmozhnost-raboty-s-servisom-reports
tags:
- API
- Яндекс Директ
- Пакеты R
- R
categories:
- Программирование
- R
description: 1. Релиз сервиса Reports и возможность работы с ним из ryandexdirect. 22 марта 2017 года в официальном блоге Яндекс Директ был объявлен релиз сервиса Reports.
original_url: https://alexeyseleznev.wordpress.com/2017/03/29/%d0%b2-%d0%bf%d0%b0%d0%ba%d0%b5%d1%82-ryandexdirect-%d0%b4%d0%be%d0%b1%d0%b0%d0%b2%d0%bb%d0%b5%d0%bd%d0%b0-%d0%b2%d0%be%d0%b7%d0%bc%d0%be%d0%b6%d0%bd%d0%be%d1%81%d1%82%d1%8c-%d1%80%d0%b0%d0%b1%d0%be/
wp_id: 26
draft: false
cover: ../images/covers/26.webp
cover_generated: true
---

## 1. Релиз сервиса Reports и возможность работы с ним из ryandexdirect.

22 марта 2017 года в [официальном блоге Яндекс Директ был объявлен релиз сервиса Reports](https://yandex.ru/blog/adv/api-5-statistika).

> В API Директа появился долгожданный сервис Reports для выгрузки статистики по рекламным кампаниям.
>
> Описания параметров и инструкции по работе с сервисом подробно описаны в документации. Мы разработали несколько типов отчетов: от статистики по отдельным объявлениям до сводки по всему аккаунту рекламодателя. Есть и возможность получения статистики по поисковым запросам. А с помощью отчета CUSTOM\_REPORT вы можете собрать отчет с любой комбинацией полей и условий отбора данных.
>
> Отзывы и вопросы, как и всегда, можно отправить через [форму обратной связи](<https://tech.yandex.ru/direct/doc/support/troubleshooting/other-docpage/>).
>
> Успешной работы!

В связи с чем в пакет ryandexdirect была добавлена функция [yadirGetReport](https://github.com/selesnow/ryandexdirect/blob/master/README.md#yadirgetreportreporttype--campaign_performance_report-daterangetype--last_month-datefrom--null-dateto--null-fieldnames--ccampaignnameimpressionsclickscost-filterlist--null-includevat--no-includediscount--no-login--null-token--null) для работы с этим сервисом.

#### Пример работы с функцией [yadirGetReport](https://github.com/selesnow/ryandexdirect/blob/master/README.md#yadirgetreportreporttype--campaign_performance_report-daterangetype--last_month-datefrom--null-dateto--null-fieldnames--ccampaignnameimpressionsclickscost-filterlist--null-includevat--no-includediscount--no-login--null-token--null)

```

 library(ryandexdirect)
 myToken My_report DateRangeType = "CUSTOM_DATE",
 DateFrom = '2017-01-01',
 DateTo = '2017-01-31',
 FieldNames = c("CampaignName","Impressions","Clicks"),
 FilterList = c("Clicks GREATER_THAN 49","Impressions LESS_THAN 1001"),
 Login = <YourLogin>,
 Token = myToken)
```

Вместо **YourLogin** подставьте в виде строки ваш логин на Яндексе, для примеры работы с фильтрами данный запрос вернёт рекламные кампании по которым за выбранный период было более 49 кликов и менее 1001 показа.

Данные в отчете можно агрегировать по различным периодам. Для этого укажите в аргументе FieldNames одно из значений Date, Week, Month, Quarter или Year.

## # 2. Функция yadirGetDictionary для загрузки справочников из API Директа версии 5.

В пакет ryandexdirect добавлена функция [yadirGetDictionary](https://github.com/selesnow/ryandexdirect/blob/master/README.md#yadirgetdictionarydictionaryname--georegions-language--ru-login--null-token--null) с помощью которой можно получить любой доступный в 5 версии API Директа справочник.

#### Пример работы с функцией yadirGetDictionary для загрузки справочников из API v.5. Яндекс Директ.

```

library(ryandexdirect)
 myToken  Regions  Language = "ru",
 login = <YourLogin>,
 token = myToken
```

Вместо **YourLogin** подставьте в виде строки ваш логин на Яндексе, данный запрос загрузит в R справочник регионов Яндекс Директ.

На данный момент в API Директа версии 5, доступны следующие справочники.

|  |  |
| --- | --- |
| Название справочника | Описание справочника |
| AdCategories | Особые категории рекламируемых товаров и услуг. |
| Constants | Ограничения на значения параметров. |
| Currencies | Курсы валют, валютные параметры и ограничения. |
| GeoRegions | Регионы. |
| MetroStations | Станции метрополитена (только для Москвы, Санкт-Петербурга и Киева). |
| OperationSystemVersions | мобильных приложений. |
| ProductivityAssertions | Рекомендации по повышению продуктивности. |
| TimeZones | Часовые пояса. |
| SupplySidePlatforms | Внешние сети (SSP). |
| Interests | Интересы к категориям мобильных приложений. |

Более подробно посмотреть информацию доступную в каждом из справочников можно по [ссылке](https://tech.yandex.ru/direct/doc/ref-v5/dictionaries/get-docpage/).

Более подробно узнать о пакете функций ryandexdirect для загрузки данных из API Яндекс Директ и Яндекс Метрики в R можно получить на моём репозитории на GitHub перейдя по [ссылке](https://github.com/selesnow/ryandexdirect).
