---
title: 'Как использовать прокси в скриптах R: обходим блокировку API Яндекса, Mail.ru и ВКонтакте'
date: '2017-05-30'
slug: kak-ispolzovat-proksi-v-skriptah-r-obhodim-blokirovku-api-yandeksa-mai
tags:
- API
- Яндекс Метрика
- Яндекс Директ
- Автоматизация
- R
categories:
- Программирование
- R
description: Если вы из Украины и до 16 мая использовали API Яндекса, Mail.Ru и ВКонтакте, то после этой даты, очевидно, столкнулись с определенными трудностями. В этой статье я расскажу, как обойти блокировку API запрещенных сервисов в скриптах R и продолжать использовать пакеты ryandexdirect, rvkstat или rmytarget.
original_url: https://alexeyseleznev.wordpress.com/2017/05/30/%d0%ba%d0%b0%d0%ba-%d0%b8%d1%81%d0%bf%d0%be%d0%bb%d1%8c%d0%b7%d0%be%d0%b2%d0%b0%d1%82%d1%8c-%d0%bf%d1%80%d0%be%d0%ba%d1%81%d0%b8-%d0%b2-%d1%81%d0%ba%d1%80%d0%b8%d0%bf%d1%82%d0%b0%d1%85-r-%d0%be%d0%b1/
wp_id: 791
draft: false
---

Если вы из Украины и до 16 мая использовали API Яндекса, Mail.Ru и ВКонтакте, то после этой даты, очевидно, столкнулись с определенными трудностями. В этой статье я расскажу, как обойти блокировку API запрещенных сервисов в скриптах R и продолжать использовать пакеты [ryandexdirect](https://github.com/selesnow/ryandexdirect), [rvkstat](https://github.com/selesnow/rvkstat) или [rmytarget](https://github.com/selesnow/rmytarget).

![](https://700700.ru/images/stories/razdel/vzlom_zamok_1435653.jpg)

## Обход блокировки в полуавтоматическом режиме

1. Найдите любой сервис, генерирующий списки доступных прокси (например, <https://hidemy.name/ru/proxy-list/>).

2. Выберите в фильтре тип прокси, поддерживающий HTTPS.

![Выберите в фильтре тип прокси, поддерживающий HTTPS](../images/kak-ispolzovat-proksi-v-skriptah-r-ob-vyberite-v-filtre-tip-5bb1dd5c.webp)

3. Сформируйте список доступных прокси-серверов.

4. Далее понадобятся только IP-адрес и порт прокси сервера (обычно использую сервера с портом 3128):

![Далее понадобятся только IP-адрес и порт прокси сервера (обычно использую сервера с портом 3128)](../images/kak-ispolzovat-proksi-v-skriptah-r-ob-dalee-ponadobatsa-tolk-cef9c000.webp)

5. Например, возьмем американский сервер, который из третьей строки списка IP 104.37.212.5, порт 3128. В код R необходимо направить интернет-соединение через прокси-сервер, для этого добавляем в код строку:

```markup
Sys.setenv(https_proxy="http://104.37.212.5:3128")
```

6. Пишем код обращения к API (пример — чуть дальше).

7. Добавляем строку для отключения интернет-соединения от прокси-сервера:

```markup
Sys.unsetenv("https_proxy")
```

8. Если прокси-сервер требует прохождения аутентификации, можете указать имя пользователя и пароль:

```markup
Sys.setenv(https_proxy="http://user:password@proxy_server:port")
```

9. Проверьте, установлена ли настройка соединения — введите в R консоль команду:

```markup
Sys.getenv("https_proxy")
```

В ответ на эту команду в консоли появится запись:

```markup
[1] "http://104.37.212.5:3128"
```

Это значит, что соединение через прокси установлено успешно.

### Обращение к API Яндекс. Директ через прокси-сервер

Перед использованием приведенного ниже кода необходимо установить пакеты devtools и ryandexditrect:

```markup
install.packages("devtools")
library(devtools)
install_github('selesnow/ryandexdirect')
```

Для получения API токена необходимо установить одно из расширений для браузера, которое позволяет обойти блокировку сайтов. Можете установить [Proxy for Chrome](https://chrome.google.com/webstore/detail/proxy-for-chrome/iilpibhiihokecnbdkaminemnmecjfed?hl=ru), например.

Теперь можно использовать следующий код на языке R, подставляя в аргументы функций свои значения:

```markup
#Подключаем пакет ryandexdirect
library(ryandexdirect)

#Получаем API токен
myToken <- yadirGetToken()

#Направляем интернет-соединение через прокси-сервер, IP и порт которого мы получили на предыдущем шаге
Sys.setenv(https_proxy="http://104.37.212.5:3128")

#Обращаемся к API Яндекс.Директ
My_report <- yadirGetReport(ReportType = "CAMPAIGN_PERFORMANCE_REPORT", 
                           DateRangeType = "CUSTOM_DATE", 
                           DateFrom = '2017-01-01', 
                           DateTo = '2017-01-31', 
                           Login = <YourLogin>, 
                           Token = myToken)

#Отключаемся от прокси-сервера
Sys.unsetenv("https_proxy")
```

## Как автоматизировать получение IP и порта прокси-сервера?

Если установить ещё несколько пакетов и немного дописать код, процесс получения IP-адреса и порта бесплатного прокси-сервера можно полностью автоматизировать.

Дело в том, что сервис GimmeProxy API предоставляет возможность загрузки IP адреса и порта с помощью API.

Во-первых, необходимо установить пакеты RCurl и jsonlite:

```markup
#Установка пакетов
if(!"RCurl" %in% installed.packages()[,1]){install.packages("RCurl")}
if(!"jsonlite" %in% installed.packages()[,1]){install.packages("jsonlite")}

#Подключаем пакеты
library(RCurl)
library(jsonlite)
library(ryandexdirect)

#Запрашиваем IP-адрес и порт
proxy_list_raw <- getURL("https://gimmeproxy.com/api/getProxy?supportsHttps=true&port=3128")

#Сохраняем IP-адрес и порт в переменную для использования в коде
proxy_ip_port <- fromJSON(proxy_list_raw)$ipPort

#Направляем интернет-соединение через прокси-сервер
Sys.setenv(https_proxy=proxy_ip_port)

#Получаем API токен
myToken <- yadirGetToken()

#Обращаемся к API Яндекс.Директ
My_report <- yadirGetReport(ReportType = "CAMPAIGN_PERFORMANCE_REPORT", 
                           DateRangeType = "CUSTOM_DATE", 
                           DateFrom = '2017-01-01', 
                           DateTo = '2017-01-31', 
                           FieldNames = c("CampaignName","Impressions","Clicks"), 
                           Login = <YourLogin>, 
                           Token = myToken)

#Отключаемся от прокси-сервера
Sys.unsetenv("https_proxy")
```

Вначале по API мы запрашиваем IP-адрес и порт прокси-сервера с помощью функции *getURL* из пакета Curl, далее конвертируем её в объект-лист с помощью функции *fromJSON,* доступной в пакете jsonlite, и, наконец, сохраняем IP-адрес и порт в переменную *proxy\_ip\_port*. Затем эту переменную используем в коде в качестве аргумента функции *Sys.setenv*.

Как вы понимаете, все бесплатное работает не так стабильно, как хотелось бы, поэтому в качестве недорогой но стабильно работающей и значительно более гибкой в настройках альтернативы рекомендую купить доступ к API у [HideMy.name](http://hidemy.name/). Запросите доступ к API в этой [форме](https://hidemy.name/ru/feedback/).

Актуальную стоимость доступа к API можно узнать по этой [ссылке](https://hidemy.name/ru/order/vpn/).

## Как автоматизировать получение IP-адреса, порта прокси-сервера и запуск необходимых настроек с помощью пакета getProxy

Код из предыдущего пункта — рабочий, он полезен для понимания, как использовать любое API, с помощью которого можно получить IP и порт прокси-сервера.

Чтобы упростить работу с бесплатными сервисами, предоставляющими IP и порт прокси-серверов, я написал пакет [getProxy](https://github.com/selesnow/getProxy). С его помощью вы в одной строке кода можете автоматически запрашивать IP-адрес и порт прокси, применять к запросу фильтры по порту, странам и типу прокси-сервера, а также сразу внедрять полученные настройки.

На  данный момент пакет содержит всего одну функцию getProxy. Функция использует два бесплатных API-сервиса: gimmeproxy.com и getproxylist.com, обращаясь к ним за IP и портом публично доступных и бесплатных прокси-серверов.

### Установка пакета getProxy

Установите пакет из репозитория GitHub:

```markup
if(!"devtools" %in% installed.packages()[,1]){install.packages("devtools")}
library(devtools)
install_github("selesnow/getProxy")
```

### Аргументы функции getProxy

- **country** — код страны в формате ISO 3166-1 alpha-2. Коды всех стран можно найти [здесь](https://en.wikipedia.org/wiki/ISO_3166-1#Current_codes).
- **notCountry** — код страны, по которой не надо запрашивать настройки прокси-сервера, в формате ISO 3166-1 alpha-2.
- **supportsHttps** — логическое значение TRUE или FALSE, используется для фильтрации прокси-серверов по поддержке протокола https.
- **port** — номер порта для фильтрации прокси-серверов.
- **type** — тип протокола прокси-сервера, поддерживает возможные значения «http», «socks4», «socks5».
- **action** — действие, которое необходимо выполнить: *start*, чтобы получить и сразу направить интернет-соединение через прокси-сервер, *get* — если хотите получить IP-адрес и порт прокси-сервера, но не применять эти настройки, *stop* — если хотите отключиться от прокси-сервера.

### Пример использования функции getProxy

Чтобы автоматизировать процесс получения IP-адреса и порта прокси-сервера и сохранения его в объект без перенаправления интернет-соединения, достаточно в аргументе *action* установить значение *get*.

```markup
prox_ip_and_port <- getProxy(port = "3128", country = "RU", action = "get")
```

Если хотите получить IP-адрес и порт прокси-сервера, а также одновременно применить полученные настройки, в аргумент *action* передайте значение *start*.

```markup
prox_ip_and_port <- getProxy(port = "3128", country = "RU", supportsHttps = TRUE, action = "start")
```

Если необходимо отключиться от прокси-сервера, достаточно передать в аргумент *action* значение *stop*.

```markup
getProxy(action = "stop")
```

### Пример обращения к API Яндекс. Директ через прокси-сервер с помощью пакета getProxy

Перед запуском приведенного ниже кода у вас уже должны быть установлены пакеты ryandexdirect и getProxy.

```markup
#Подключаем пакеты
library(ryandexdirect)
library(getProxy)

#Запрашиваем IP-адрес и порт и применяем полученные настройки
getProxy(port = "3128", country = "RU", supportsHttps = TRUE, action = "start")

#Получаем API токен
myToken <- yadirGetToken()

#Обращаемся к API Яндекс.Директ
My_report <- yadirGetReport(ReportType = "CAMPAIGN_PERFORMANCE_REPORT", 
                           DateRangeType = "CUSTOM_DATE", 
                           DateFrom = '2017-01-01', 
                           DateTo = '2017-01-31', 
                           FieldNames = c("CampaignName","Impressions","Clicks"), 
                           Login = <YourLogin>, 
                           Token = myToken)

#Отключаемся от прокси-сервера
getProxy(action = "stop")
```

Этот код при каждом запуске будет автоматически запрашивать настройки доступного прокси-сервера и применять их.

## Выводы

Для обхода блокировки доступа к API в ваши скрипты на языке R достаточно добавить всего две строки и использовать функции Sys.setenv и Sys.unsetenv.

Немного дописав скрипт, вы сможете беспрепятственно получать данные из API Яндекс. Директ, Яндекс. Метрики, ВКонтакте и Mail.ru. В большинстве случаев будет достаточно бесплатных API-сервисов, для работы с которыми я написал пакет getProxy.

Читайте также о методах использования языка R [в интернет-маркетинге](https://netpeak.net/ru/blog/yazyk-r-v-internet-marketinge-daidzhest-poleznykh-publikatsii/).

---

[Оригинал публикации на блоге Netpeak.](https://netpeak.net/ru/blog/kak-ispol-zovat-proksi-v-skriptakh-r-obkhodim-blokirovku-api-yandeksa-mail-ru-i-vkontakte/)
