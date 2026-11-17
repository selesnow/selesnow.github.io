---
title: Релиз версии 2.2.0 пакета ryandexdirect
date: '2017-09-13'
slug: reliz-versii-2-2-0-paketa-ryandexdirect
tags:
- API
- Автоматизация
- R
categories:
- Яндекс
- Программирование
- R
description: Сегодня я добавил в пакет ryandexdirect 3 новые функции. yadirGetAdGroups – Получение списка групп объявлений yadirGetKeyWords – Получение списка ключевых слов yadirGetAds – Получение списка объявлений С помощью этих функций вы можете получить список групп объявлений, объявлений, ключевых слов с различными их параметрами.
original_url: https://alexeyseleznev.wordpress.com/2017/09/13/%d1%80%d0%b5%d0%bb%d0%b8%d0%b7-%d0%b2%d0%b5%d1%80%d1%81%d0%b8%d0%b8-2-2-0-%d0%bf%d0%b0%d0%ba%d0%b5%d1%82%d0%b0-ryandexdirect/
wp_id: 969
draft: false
cover: ../images/covers/969.webp
cover_generated: true
---

Сегодня я добавил в пакет ryandexdirect 3 новые функции.

- [yadirGetAdGroups](https://github.com/selesnow/ryandexdirect/blob/master/README.md#yadirgetadgroupscampaignids--c123login--null-token--null) – Получение списка групп объявлений
- [yadirGetKeyWords](https://github.com/selesnow/ryandexdirect/blob/master/README.md#yadirgetkeywordscampaignids--c123-withstats--t-login--null-token--null) – Получение списка ключевых слов
- [yadirGetAds](https://github.com/selesnow/ryandexdirect/blob/master/README.md#yadirgetadscampaignids--c123-login--null-token--null) – Получение списка объявлений

С помощью этих функций вы можете получить список групп объявлений, объявлений, ключевых слов с различными их параметрами.

![Картинки по запросу релиз](https://phptime.ru/uploads/images/00/00/01/2015/12/04/848ba2.png)

## yadirGetAdGroups

Функция возвращает дата фрейм со списком групп объявлений и некоторых их параметров по логину.

#### Аргументы:

**CampaignIds** – Вектор с ID рекламных кампаний, по которым необходимо загрузить список групп объявлений

**Login** – Логин на Яндексе

**Token** – Токен дотупа к API

#### Структура возвращаемого функцией `yadirGetAdGroups` дата фрейма:

|  |  |  |
| --- | --- | --- |
| Поле | Тип данных | Описание |
| Id | num | Идентификатор группы объявлений. |
| Name | Factor | Название группы. |
| CampaignId | int | Идентификатор кампании. |
| Type | Factor | Тип группы объявлений. [См. Тип группы.](https://tech.yandex.ru/direct/doc/dg/objects/adgroup-docpage/#types) |
| Subtype | Factor | Подтип группы объявлений. Для групп с типом, отличным от DYNAMIC\_TEXT\_AD\_GROUP, возвращается значение NONE. |
| Status | Factor | Статус группы. [См. Статус группы.](https://tech.yandex.ru/direct/doc/dg/objects/adgroup-docpage/#status) |
| ServingStatus | Factor | Статус возможности показов группы. [См. Статус возможности показов группы.](https://tech.yandex.ru/direct/doc/dg/objects/adgroup-docpage/#serving-status) |
| NegativeKeywords | chr | Минус-фразы, общие для всех ключевых фраз группы объявлений. |
| TrackingParams | Factor | ET-параметры для отслеживания источников переходов на сайт, которые добавляются в ссылку всех объявлений группы (не более 1024 символов). Могут содержать [подстановочные переменные.](https://yandex.ru/support/direct/statistics/url-tags.html) Например: from=direct&ad={ad\_id} Параметр можно указать для группы любого типа, однако в настоящее время он используется только для групп динамических объявлений. Для других типов групп указанные GET-параметры в ссылку не добавляются. |
| RegionIds | Factor | Идентификаторы регионов, для которых показы включены или выключены. Идентификатор 0 — показывать во всех регионах. Минус перед идентификатором региона — выключить показы в данном регионе. Например [1,-219] — показывать для Москвы и Московской области, кроме Черноголовки. |
| RestrictedRegionIds | chr | Идентификаторы регионов, в которых объявления не будут показаны в связи с законодательными ограничениями. |
| MobileAppAdGroupStoreUrl | chr | Ссылка на приложение в магазине приложений AppStore или Google Play (не более 1024 символов). Должна содержать протокол. Недоступна для изменения. |
| MobileAppAdGroupTargetDeviceType | chr | На каких устройствах показывать объявления: DEVICE\_TYPE\_MOBILE — смартфоны; DEVICE\_TYPE\_TABLET — планшеты. |
| MobileAppAdGroupTargetCarrier | chr | По каким типам подключения к интернету показывать объявления: WI\_FI\_ONLY — только по Wi-FI; WI\_FI\_AND\_CELLULAR — по мобильной связи и Wi-Fi. |
| MobileAppAdGroupTargetOperatingSystemVersion | chr | Минимальная версия операционной системы, на которой может быть показано объявление. Например, 2.3. Примечание. Если минимальная версия ОС в магазине приложений выше, чем заданная в параметре, то объявления будут показаны только для версий ОС как в магазине приложений или выше. |
| MobileAppAdGroupAppIconModerationStatus | chr | Результат модерации иконки мобильного приложения: ACCEPTED — принята модерацией; MODERATION — находится на модерации; REJECTED — отклонена. |
| MobileAppAdGroupAppIconModerationStatusClarification | chr | Текстовое пояснение к статусу и/или причины отклонения на модерации. |
| MobileAppAdGroupAppOperatingSystemType | chr | Тип операционной системы (определяется автоматически на основании данных из магазина приложений): IOS — iOS; ANDROID — Android; OS\_TYPE\_UNKNOWN — данные из магазина приложений еще не получены. |
| MobileAppAdGroupAppAvailabilityStatus | chr | Доступно ли приложение в магазине приложений: AVAILABLE — доступно; NOT\_AVAILABLE — недоступно; UNPROCESSED — данные из магазина приложений еще не получены. |
| DynamicTextAdGroupDomainUrl | chr | Доменное имя сайта, для которого требуется сгенерировать динамические объявления (не более 100 символов). Протокол указывать не нужно. |
| DynamicTextAdGroupDomainUrlProcessingStatus | chr | Статус генерации динамических объявлений: UNPROCESSED — генерация объявлений не завершена; PROCESSED — объявления созданы; EMPTY\_RESULT — не удалось создать ни одного объявления. |
| DynamicTextFeedAdGroupSource | chr | Идентификатор фида. |
| DynamicTextFeedAdGroupSourceType | chr | Тип источника данных. В настоящее время доступно только значение RETAIL\_FEED. фида. |
| DynamicTextFeedAdGroupSourceProcessingStatus | chr | Статус генерации динамических объявлений: UNPROCESSED — генерация объявлений не завершена; PROCESSED — объявления созданы; EMPTY\_RESULT — не удалось создать ни одного объявления. |

#### Пример кода для получения списка групп объявлений:

```

#Подключаем пакет
library(ryandexdirect)
#Получаем API token
my_token &lt;- yadirGetToken()
#Получаем список рекламных кампаний
my_campaign &lt;- yadirGetCampaignList(login = &lt;ВАШ ЛОГИН&gt;,
token = my_token)
#Получаем данные по группам объявлений
my_adgroups &lt;- yadirGetAdGroups(CampaignIds = my_campaign$Id,
Login = &lt;ВАШ ЛОГИН&gt;,
Token = my_token)
```

## 

## yadirGetKeyWords

Функция возвращает дата фрейм со списком ключевых слов и некоторых их параметров по логину.

#### Аргументы:

**CampaignIds** – Вектор с ID рекламных кампаний, по которым необходимо загрузить список групп объявлений

**WithStats** – Логическое TRUE или FALSE, аргумент отвечает за загрузку статистики по показам и кликам, в случае если вы установите значение TRUE время работы функции будет значительно дольше.

**Login** – Логин на Яндексе

**Token** – Токен дотупа к API

#### Структура возвращаемого функцией `yadirGetKeyWords` дата фрейма:

|  |  |  |
| --- | --- | --- |
| Поле | Тип данных | Описание |
| Id | num | Идентификатор ключевой фразы. |
| Keyword | Factor | Ключевая фраза. Может содержать минус-слова. |
| AdGroupId | num | Идентификатор группы объявлений, к которой относится ключевая фраза. |
| CampaignId | int | Идентификатор кампании, к которой относится ключевая фраза. |
| ServingStatus | Factor | Статус возможности показов группы объявлений. Описание статусов см. в разделе [Статус возможности показов группы.](https://tech.yandex.ru/direct/doc/dg/objects/adgroup-docpage/#serving-status) |
| State | Factor | Состояние ключевой фразы. Описание состояний см. в разделе [Статус и состояние фразы.](https://tech.yandex.ru/direct/doc/dg/objects/keyword-docpage/#status) |
| Status | Factor | Статус ключевой фразы. Описание статусов см. в разделе [Статус и состояние фразы.](https://tech.yandex.ru/direct/doc/dg/objects/keyword-docpage/#status) |
| StrategyPriority | Factor | Приоритет фразы: LOW, NORMAL или HIGH. |
| StatisticsSearchImpressions | int | Количество показов всех объявлений группы в поиске по данной фразе. Рассчитывается за 28 дней от текущей даты. Для расчета отбираются дни, в течение которых был хотя бы один показ объявления по данной фразе. |
| StatisticsSearchClicks | int | Количество кликов по всем объявлениям группы в поиске, показанным по данной фразе. Рассчитывается за 28 дней от текущей даты. Для расчета отбираются дни, в течение которых был хотя бы один клик по объявлению. |
| StatisticsNetworkImpressions | int | Количество показов всех объявлений группы по данной фразе в сетях. Рассчитывается за 28 дней от текущей даты. Для расчета отбираются дни, в течение которых был хотя бы один показ объявления по данной фразе. |
| StatisticsNetworkClicks | int | Количество кликов по всем объявлениям группы, показанным по данной фразе в сетях. Рассчитывается за 28 дней от текущей даты. Для расчета отбираются дни, в течение которых был хотя бы один клик по объявлению. |
| UserParam1 | Factor | Значение [подстановочной переменной](https://tech.yandex.ru/direct/doc/dg/objects/keyword-docpage/#userparams) {param1}. Не более 255 символов. |
| UserParam2 | Factor | Значение [подстановочной переменной](https://tech.yandex.ru/direct/doc/dg/objects/keyword-docpage/#userparams) {param2}. Не более 255 символов. |
| Bid | num | Ставка на поиске. |
| ContextBid | num | Ставка в сетях. |

#### Пример кода для получения списка ключевых слов:

```

#Подключаем пакет
library(ryandexdirect)
#Получаем API token
my_token <- yadirGetToken()
#Получаем список рекламных кампаний
my_campaign <- yadirGetCampaignList(login = <ВАШ ЛОГИН>,
token = my_token)
#Получаем данные по ключевым словам
my_keywords <- yadirGetKeyWords(CampaignIds = my_campaign$Id,
WithStats = F,
Login = <ВАШ ЛОГИН>,
Token = my_token)
```

## yadirGetAds

Функция возвращает дата фрейм со списком объявлений и некоторых их параметров по логину.

#### Аргументы:

**CampaignIds** – Вектор с ID рекламных кампаний, по которым необходимо загрузить список групп объявлений

**Login** – Логин на Яндексе

**Token** – Токен дотупа к API

#### Структура возвращаемого функцией `yadirGetAds` дата фрейма:

|  |  |  |
| --- | --- | --- |
| Поле | Тип данных | Описание |
| Id | num | Идентификатор объявления. |
| AdGroupId | num | Идентификатор группы объявлений, к которой относится объявление. |
| CampaignId | int | Идентификатор кампании, к которой относится объявление. |
| Type | Factor | Тип объявления. См. [Тип объявления.](https://tech.yandex.ru/direct/doc/dg/objects/ad-docpage/#types) |
| Subtype | Factor | одтип объявления. Для объявлений с типом, отличным от IMAGE\_AD, возвращается значение NONE. |
| Status | Factor | Статус объявления. Описание статусов см. в разделе [Статус и состояние объявления.](https://tech.yandex.ru/direct/doc/dg/objects/ad-docpage/#status) |
| AgeLabel | chr | [Возрастная метка.](https://tech.yandex.ru/direct/doc/dg/objects/ad-docpage/#age) |
| State | int | Состояние объявления. Описание состояний см. в разделе [Статус и состояние объявления.](https://tech.yandex.ru/direct/doc/dg/objects/ad-docpage/#status) |
| TextAdTitle | Factor | Заголовок 1. Не более 35 символов без учета «узких» плюс не более 15 «узких» символов. Каждое слово не более 22 символов. В случае использования [шаблона](https://yandex.ru/support/direct/features/ad-templates.html) символы # не учитываются в длине). |
| TextAdTitle2 | chr | Заголовок 2. Не более 30 символов без учета «узких» плюс не более 15 «узких» символов. Каждое слово не более 22 символов. В случае использования [шаблона](https://yandex.ru/support/direct/features/ad-templates.html) символы # не учитываются в длине). |
| TextAdText | Factor | Текст объявления. Не более 81 символа без учета «узких» плюс не более 15 «узких» символов. Каждое слово не более 23 символов. В случае использования [шаблона](https://yandex.ru/support/direct/features/ad-templates.html) символы # не учитываются в длине). |
| TextAdHref | Factor | Ссылка на сайт рекламодателя. |
| TextAdDisplayDomain | Factor | Рекламируемый домен. Определяется автоматически на основе ссылки объявления. |
| TextAdMobile | Factor | Признак того, что объявление является мобильным: YES или NO. |
| TextImageAdHref | chr | Хэш изображения. Для текстово-графических объявлений подходят только изображения с типом REGULAR и WIDE. |

#### Пример кода для получения списка ключевых слов:

```

#Подключаем пакет
library(ryandexdirect)
#Получаем API token
my_token <- yadirGetToken()
#Получаем список рекламных кампаний
my_campaign <- yadirGetCampaignList(login = <ВАШ ЛОГИН>,
token = my_token)
#Получаем данные по ключевым словам
my_ads <- yadirGetAds(CampaignIds = my_campaign$Id,
Login = <ВАШ ЛОГИН>,
Token = my_token)
```
