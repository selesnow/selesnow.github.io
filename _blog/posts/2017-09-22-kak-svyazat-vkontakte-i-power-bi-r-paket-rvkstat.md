---
title: Как связать ВКонтакте и Power BI, R пакет rvkstat.
date: '2017-09-22'
slug: kak-svyazat-vkontakte-i-power-bi-r-paket-rvkstat
tags:
- API
- BI
- R
- ВКонтакте
categories:
- BI
- Программирование
- R
description: 'Несмотря на недавнюю блокировку соцсети в Индии, ВКонтакте продолжает оставаться огромным источником полезной информации и статистики. В этой статье я расскажу, как с помощью написанного мной программного пакета rvkstat и коннектора  R получить данные из API ВКонтакте в Microsoft Power BI. Как использовать прокси в скриптах R: обходим блокировку API Яндекса, Mail.ru и ВКонтакте Причем получить эти […]'
original_url: https://alexeyseleznev.wordpress.com/2017/09/22/%d0%ba%d0%b0%d0%ba-%d0%bf%d0%b5%d1%80%d0%b5%d0%bd%d0%b5%d1%81%d1%82%d0%b8-%d0%b4%d0%b0%d0%bd%d0%bd%d1%8b%d0%b5-%d0%b8%d0%b7-%d0%b2%d0%ba%d0%be%d0%bd%d1%82%d0%b0%d0%ba%d1%82%d0%b5-%d0%b2-power-bi/
wp_id: 1003
draft: false
---

Несмотря на недавнюю блокировку соцсети в Индии, ВКонтакте продолжает оставаться огромным источником полезной информации и статистики. В этой статье я расскажу, как с помощью написанного мной программного пакета [rvkstat](https://selesnow.github.io/rvkstat/) и коннектора  R получить данные из API ВКонтакте в Microsoft Power BI.

Как использовать прокси в скриптах R: обходим блокировку API Яндекса, Mail.ru и ВКонтакте

Причем получить эти данные можно даже в странах, где сама соцсеть официально [заблокирована](https://netpeak.net/ru/blog/kak-ispol-zovat-proksi-v-skriptakh-r-obkhodim-blokirovku-api-yandeksa-mail-ru-i-vkontakte/).

## 

## Установка необходимого программного обеспечения

Скачайте и установите актуальную версию [языка R](https://cran.r-project.org/bin/windows/base/) и [Power BI](https://powerbi.microsoft.com/ru-ru/desktop/). Это, пожалуй, самая простая часть работы, как R так и Power BI при установке не требуют от вас никаких дополнительных манипуляций и настройки — просто кликайте по кнопкам Next и Ok.

## Как создать Standalone-приложение ВКонтакте

Для работы с API Вконтакте необходимо создать Standalone-приложение, непосредственно в интерфейсе социальной сети.

Для создания приложения перейдите по этой [ссылке](https://vk.com/editapp?act=create) и выберите Standalone-приложение.

![Для создания приложения перейдите по этой ссылке и выберите Standalone-приложение](../images/kak-perenesti-dannye-iz-vkontakte-v-power-bi-dla-sozdania-pr-7344a7a1.webp)

Перейдите в настройки только что созданного приложения и заполните следующие поля следующим образом:

**Адрес сайта**: <https://selesnow.github.io/rvkstat/getCode/get_code.html>  
**Базовый домен**: selesnow.github.io  
**Доверенные redirect URI**: <https://selesnow.github.io/rvkstat/getCode/get_code.html>  
<https://selesnow.github.io/rvkstat/getCode/get_token.html>

Далее для получения токена разработчика вам понадобится ID и засекреченный ключ приложения.

![Доверенные редирект URL](../images/kak-perenesti-dannye-iz-vkontakte-v-power-bi-doverennye-redi-6ba2ae54.webp)

## Устанавливаем пакет rvkstat

Пакет rvkstat является R-клиентом для работы с API ВКонтакте. Его можно установить из [моего репозитория на GitHub](https://github.com/selesnow) с помощью приведенного ниже кода в R.

```markup
if(!"devtools" %in% installed.packages()[,1]){install.packages("devtools")}
devtools::install_github('selesnow/rvkstat')
```

Если на данном этапе вы всё сделали правильно, в R-консоли увидите сообщение о том, что пакет rvkstat успешно установлен:

![Если на данном этапе вы всё сделали правильно, в R-консоли увидите сообщение о том, что пакет rvkstat успешно установлен](../images/kak-perenesti-dannye-iz-vkontakte-v-power-bi-esli-na-dannom-34db9b36.webp)

## Получаем токен разработчика

Следующий шаг — получение токена доступа к API ВКонтакте. Для этого необходимо подключить пакет rvkstat и с помощью функции vkAuth получить токен разработчика.

Для этого вставьте в R-консоль следующий код:

```markup
myCredential <- vkAuth(app_id = <ID Вашего Приложения>, app_secret = <Защищённый Ключ Вашего Приложения>)
```

После запуска функции откроется окно браузера, в котором необходимо предоставить приложению все необходимые для работы разрешения:

![Нажмите «Разрешить»](../images/kak-perenesti-dannye-iz-vkontakte-v-power-bi-nazmite-razresi-35b0ec93.webp)

Затем откроется окно браузера, в котором будет ваш код доступа. Вам необходимо скопировать его и вставить в R-консоль в ответ на запрос «Enter code from URL:».

![После чего откроется окно браузера, в котором будет ваш код доступа](../images/kak-perenesti-dannye-iz-vkontakte-v-power-bi-posle-cego-otkr-d945e44e.webp)

![Вам необходимо скопировать его и вставить в R-консоль в ответ на запрос](../images/kak-perenesti-dannye-iz-vkontakte-v-power-bi-vam-neobhodimo-45ab8147.webp)

После этого в вашем рабочем окружении будет создан объект myCredential, именно в нём теперь хранится токен доступа к API.

Посмотреть его можно с помощью кода:

```markup
myCredential$access_token
```

Для удобства скопируйте из консоли полученный токен в блокнот.

![Для удобства скопируйте из консоли полученный токен в блокнот](../images/kak-perenesti-dannye-iz-vkontakte-v-power-bi-dla-udobstva-sk-35dd3b41.webp)

## Как получить данные из рекламного кабинета ВКонтакте в Power BI

На этом шаге можно смело закрывать R-консоль и открывать Power BI. Для загрузки данных жмите на «Get Data».

![На этом шаге можно смело закрывать R-консоль и открывать Power BI. Для загрузки данных жмите на «Get Data»](../images/kak-perenesti-dannye-iz-vkontakte-v-power-bi-na-etom-sage-mo-6e4514b8.webp)

В открывшемся диалоговом окне переходим в группу коннекторов «Other», выбирайте «R script» и нажимайте «Connect».

![В открывшемся диалоговом окне переходим в группу коннекторов «Other», выбирайте «R script» и нажимайте «Connect»](../images/kak-perenesti-dannye-iz-vkontakte-v-power-bi-v-otkryvsemsa-d-1db20a8f.webp)

Далее в диалоговое окно «R Script» вставьте R-код, подставив в аргументы функций свои значения.

```markup
#Подключаем пакет
library(rvkstat)

##Получаем список рекламных кампаний
camp <- vkGetAdCampaigns(account_id = <id вашего рекламного кабинета>,
                        access_token = <токен разработчика, полученный на прошлом шаге>)

##Получаем статистику по рекламным кампаниям по дням
vk_stat_by_campaign <- vkGetAdStatistics(account_id = <id вашего рекламного кабинета>,
                                        ids_type = "campaign",
                                        ids = camp$id ,
                                        period = "day",
                                        date_from = "2010-01-01",
                                        date_to =Sys.Date(),
                                        access_token = <токен разработчика, полученный на прошлом шаге>)
```

![Далее в диалоговое окно «R Script» вставьте R-код, подставив в аргументы функций свои значения](../images/kak-perenesti-dannye-iz-vkontakte-v-power-bi-dalee-v-dialogo-699bde91.webp)

Если вы верно указали значения для всех аргументов функций, откроется диалоговое окно «Navigator», в котором можно выбрать две таблицы:

- **camp** — справочник рекламных кампаний;
- **vk\_stat\_by\_camp** — статистика по рекламным кампаниям.

![Если вы верно указали значения для всех аргументов функций, откроется диалоговое окно «Navigator», в котором можно выбрать две таблицы](../images/kak-perenesti-dannye-iz-vkontakte-v-power-bi-esli-vy-verno-u-6085457e.webp)

После этого в Power BI будут загружены обе таблицы, и между таблицами будет установлена связь *camp.id = vk\_stat\_by\_camp.id*.

Чтобы получить статистику в разрезе рекламных объявлений, необходимо в аргументе *ids\_type* указать значение «ad» и в аргумент ids передать номера объявлений.

Например, можете воспользоваться следующим кодом:

```markup
##Подключаем пакет
library(rvkstat)
## Получаем список рекламных кампаний
ads <- vkGetAds(account_id = account_id, access_token = my_tok$access_token)
## Получаем статистику по объявлениям
vk_stat_by_ads <- vkGetAdStatistics(account_id = 1,
                                   ids_type = "ad",
                                   ids = ads$id ,
                                   period = "month",
                                   date_from = "2010-01-01",
                                   date_to =Sys.Date(),
                                   access_token = <токен разработчика полученный на прошлом шаге>))
```

Для загрузки общей статистики по рекламному кабинету необходимо передать в аргумент ids\_type значение «office», а в аргумент ids передать номер рекламного кабинета.

По указанному выше примеру можно получить и другую статистику из рекламного кабинета и сообществ ВКонтакте.

Ловите список доступных функций для загрузки статистики из рекламного кабинета:

- [vkGetAdCategories](https://github.com/selesnow/rvkstat#%D0%9F%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D0%B2%D0%BE%D0%B7%D0%BC%D0%BE%D0%B6%D0%BD%D1%8B%D1%85-%D1%82%D0%B5%D0%BC%D0%B0%D1%82%D0%B8%D0%BA-%D1%80%D0%B5%D0%BA%D0%BB%D0%B0%D0%BC%D0%BD%D1%8B%D1%85-%D0%BE%D0%B1%D1%8A%D1%8F%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B9-%D0%B8-%D0%B8%D1%85-%D0%BF%D0%BE%D0%B4%D1%80%D0%B0%D0%B7%D0%B4%D0%B5%D0%BB%D0%BE%D0%B2) — возможные тематики рекламных объявлений и их категорий;
- [vkGetAdAccounts](https://github.com/selesnow/rvkstat#%D0%9F%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D0%B4%D0%BE%D1%81%D1%83%D0%BF%D0%BD%D1%8B%D1%85-%D1%80%D0%B5%D0%BA%D0%BB%D0%B0%D0%BC%D0%BD%D1%8B%D1%85-%D0%BA%D0%B0%D0%B1%D0%B8%D0%BD%D0%B5%D1%82%D0%BE%D0%B2-%D0%92%D0%BA%D0%BE%D0%BD%D1%82%D0%B0%D0%BA%D1%82%D0%B5) — список доступных рекламных кабинетов;
- [vkGetAdClients](https://github.com/selesnow/rvkstat/blob/master/README.md#%D0%9F%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D0%BA%D0%BB%D0%B8%D0%B5%D0%BD%D1%82%D0%BE%D0%B2-%D0%B8%D0%B7-%D0%B0%D0%B3%D0%B5%D0%BD%D1%82%D1%81%D0%BA%D0%BE%D0%B3%D0%BE-%D0%B0%D0%BA%D0%BA%D0%B0%D1%83%D0%BD%D1%82%D0%B0-%D0%92%D0%BA%D0%BE%D0%BD%D1%82%D0%B0%D0%BA%D1%82%D0%B5) — список клиентов из агентского аккаунта;
- [vkGetAds](https://github.com/selesnow/rvkstat#%D0%9F%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D0%BE%D0%B1%D1%8A%D1%8F%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B9-%D0%B8%D0%B7-%D1%80%D0%B5%D0%BA%D0%BB%D0%B0%D0%BC%D0%BD%D0%BE%D0%B3%D0%BE-%D0%BA%D0%B0%D0%B1%D0%B8%D0%BD%D0%B5%D1%82%D0%B0-%D0%B2%D0%BA%D0%BE%D0%BD%D1%82%D0%B0%D0%BA%D1%82%D0%B5) — список объявлений;
- [vkGetAdCampaigns](https://github.com/selesnow/rvkstat/blob/master/README.md#%D0%9F%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D1%80%D0%B5%D0%BA%D0%BB%D0%B0%D0%BC%D0%BD%D1%8B%D1%85-%D0%BA%D0%B0%D0%BC%D0%BF%D0%B0%D0%BD%D0%B8%D0%B9-%D0%B8%D0%B7-%D1%80%D0%B5%D0%BA%D0%BB%D0%B0%D0%BC%D0%BD%D0%BE%D0%B3%D0%BE-%D0%BA%D0%B0%D0%B1%D0%B8%D0%BD%D0%B5%D1%82%D0%B0-%D0%B2%D0%BA%D0%BE%D0%BD%D1%82%D0%B0%D0%BA%D1%82%D0%B5) — список рекламных кампаний;
- [vkGetAdStatistics](https://github.com/selesnow/rvkstat/blob/master/README.md#%D0%9F%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D1%81%D1%82%D0%B0%D1%82%D0%B8%D1%81%D1%82%D0%B8%D0%BA%D1%83-%D0%BF%D0%BE%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D0%B5%D0%BB%D0%B5%D0%B9-%D1%8D%D1%84%D1%84%D0%B5%D0%BA%D1%82%D0%B8%D0%B2%D0%BD%D0%BE%D1%81%D1%82%D0%B8-%D0%BF%D0%BE-%D1%80%D0%B5%D0%BA%D0%BB%D0%B0%D0%BC%D0%BD%D1%8B%D0%BC-%D0%BE%D0%B1%D1%8A%D1%8F%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F%D0%BC-%D0%BA%D0%B0%D0%BC%D0%BF%D0%B0%D0%BD%D0%B8%D1%8F%D0%BC-%D0%BA%D0%BB%D0%B8%D0%B5%D0%BD%D1%82%D0%B0%D0%BC-%D0%B8%D0%BB%D0%B8-%D0%B2%D1%81%D0%B5%D0%BC%D1%83-%D0%BA%D0%B0%D0%B1%D0%B8%D0%BD%D0%B5%D1%82%D1%83) — статистика показателей эффективности по рекламным объявлениям, кампаниям, клиентам или всему кабинету;
- [vkGetAdCityStats](https://github.com/selesnow/rvkstat/blob/master/README.md#%D0%9F%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D1%81%D1%82%D0%B0%D1%82%D0%B8%D1%81%D1%82%D0%B8%D0%BA%D1%83-%D0%BF%D0%BE-%D0%BE%D1%85%D0%B2%D0%B0%D1%82%D1%83-%D0%B0%D1%83%D0%B4%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%B8-%D0%BF%D0%BE-%D1%80%D0%B5%D0%BA%D0%BB%D0%B0%D0%BC%D0%BD%D1%8B%D0%BC-%D0%BA%D0%B0%D0%BC%D0%BF%D0%B0%D0%BD%D0%B8%D0%BC-%D0%B8%D0%BB%D0%B8-%D0%BE%D0%B1%D1%8A%D1%8F%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B2-%D1%80%D0%B0%D0%B7%D1%80%D0%B5%D0%B7%D0%B5-%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%BE%D0%B2) — статистика охвата аудитории по рекламным кампаниям или объявления в разрезе городов;
- [vkGetAdGenderStats](https://github.com/selesnow/rvkstat/blob/master/README.md#%D0%9F%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D1%81%D1%82%D0%B0%D1%82%D0%B8%D1%81%D1%82%D0%B8%D0%BA%D1%83-%D0%BF%D0%BE-%D0%BE%D1%85%D0%B2%D0%B0%D1%82%D1%83-%D0%B0%D1%83%D0%B4%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%B8-%D0%BF%D0%BE-%D1%80%D0%B5%D0%BA%D0%BB%D0%B0%D0%BC%D0%BD%D1%8B%D0%BC-%D0%BA%D0%B0%D0%BC%D0%BF%D0%B0%D0%BD%D0%B8%D0%BC-%D0%B8%D0%BB%D0%B8-%D0%BE%D0%B1%D1%8A%D1%8F%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B2-%D1%80%D0%B0%D0%B7%D1%80%D0%B5%D0%B7%D0%B5-%D0%BF%D0%BE%D0%BB%D0%B0) — статистика охвата аудитории по рекламным кампаниям или объявления в разрезе пола;
- [vkGetAdAgeStats](https://github.com/selesnow/rvkstat/blob/master/README.md#%D0%9F%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D1%81%D1%82%D0%B0%D1%82%D0%B8%D1%81%D1%82%D0%B8%D0%BA%D1%83-%D0%BF%D0%BE-%D0%BE%D1%85%D0%B2%D0%B0%D1%82%D1%83-%D0%B0%D1%83%D0%B4%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%B8-%D0%BF%D0%BE-%D1%80%D0%B5%D0%BA%D0%BB%D0%B0%D0%BC%D0%BD%D1%8B%D0%BC-%D0%BA%D0%B0%D0%BC%D0%BF%D0%B0%D0%BD%D0%B8%D0%BC-%D0%B8%D0%BB%D0%B8-%D0%BE%D0%B1%D1%8A%D1%8F%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B2-%D1%80%D0%B0%D0%B7%D1%80%D0%B5%D0%B7%D0%B5-%D0%B2%D0%BE%D0%B7%D1%80%D0%B0%D1%81%D1%82%D0%B0) — статистика охвата аудитории по рекламным кампаниям или объявлениям в разрезе возраста;
- [vkGetAdGenderAgeStats](https://github.com/selesnow/rvkstat/blob/master/README.md#%D0%9F%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D1%81%D1%82%D0%B0%D1%82%D0%B8%D1%81%D1%82%D0%B8%D0%BA%D1%83-%D0%BF%D0%BE-%D0%BE%D1%85%D0%B2%D0%B0%D1%82%D1%83-%D0%B0%D1%83%D0%B4%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%B8-%D0%BF%D0%BE-%D1%80%D0%B5%D0%BA%D0%BB%D0%B0%D0%BC%D0%BD%D1%8B%D0%BC-%D0%BA%D0%B0%D0%BC%D0%BF%D0%B0%D0%BD%D0%B8%D0%BC-%D0%B8%D0%BB%D0%B8-%D0%BE%D0%B1%D1%8A%D1%8F%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B2-%D1%80%D0%B0%D0%B7%D1%80%D0%B5%D0%B7%D0%B5-%D0%BF%D0%BE%D0%BB%D0%B0-%D0%B8-%D0%B2%D0%BE%D0%B7%D1%80%D0%B0%D1%81%D1%82%D0%B0) — статистика охвата аудитории по рекламным кампаниям или объявлениям в разрезе пола и возраста;
- [vkGetAdBudget](https://github.com/selesnow/rvkstat/blob/master/README.md#%D0%9F%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D0%BE%D1%81%D1%82%D0%B0%D1%82%D0%BE%D0%BA-%D1%81%D1%80%D0%B5%D0%B4%D1%81%D1%82%D0%B2-%D0%B8%D0%B7-%D1%80%D0%B5%D0%BA%D0%BB%D0%B0%D0%BC%D0%BD%D0%BE%D0%B3%D0%BE-%D0%BA%D0%B0%D0%B1%D0%B8%D0%BD%D0%B5%D1%82%D0%B0) — остаток средств из рекламного кабинета;
- [vkGetAdPostsReach](https://github.com/selesnow/rvkstat/blob/master/README.md#%D0%9F%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D0%BF%D0%BE%D0%B4%D1%80%D0%BE%D0%B1%D0%BD%D1%83%D1%8E-%D1%81%D1%82%D0%B0%D1%82%D0%B8%D1%81%D1%82%D0%B8%D0%BA%D1%83-%D0%BF%D0%BE-%D0%BE%D1%85%D0%B2%D0%B0%D1%82%D1%83-%D1%80%D0%B5%D0%BA%D0%BB%D0%B0%D0%BC%D0%BD%D1%8B%D1%85-%D0%B7%D0%B0%D0%BF%D0%B8%D1%81%D0%B5%D0%B9-%D0%B8%D0%B7-%D0%BE%D0%B1%D1%8A%D1%8F%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B9-%D0%B8-%D0%BA%D0%B0%D0%BC%D0%BF%D0%B0%D0%BD%D0%B8%D0%B9-%D0%B4%D0%BB%D1%8F-%D0%BF%D1%80%D0%BE%D0%B4%D0%B2%D0%B8%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B7%D0%B0%D0%BF%D0%B8%D1%81%D0%B5%D0%B9-%D1%81%D0%BE%D0%BE%D0%B1%D1%89%D0%B5%D1%81%D1%82%D0%B2%D0%B0) — подробная статистика по охвату рекламных записей из объявлений и кампаний для продвижения записей сообщества.

Подробную справку с примерами кода и полным описанием полей, которые будут загружены в результате работы функции в пакете rvkstat, можно получить с помощью команды help в R-консоли:

```markup
help("vkGetAdStatistics")
```

Полный список функций можно получить с помощью команды *help(package  = “rvkstat”)*, либо перейдя в ReadMe репозитория пакета по [ссылке](https://selesnow.github.io/rvkstat/).

## Как построить визуализацию в Power BI

После загрузки данных в Power BI будет создано две таблицы:

- **camp** — справочник рекламных кампаний;
- **vk\_stat\_by\_campaign** — статистика по рекламным кампаниям.

Между кампаниями будет автоматически создана связь по полям id.

![На данном шаге данные уже загружены в Power BI, вам остаётся только построить нужные графики и таблицы](../images/kak-perenesti-dannye-iz-vkontakte-v-power-bi-na-dannom-sage-3d7b802b.webp)

Остаётся только построить нужные графики и таблицы.

![остаётся только построить нужные графики и таблицы](../images/kak-perenesti-dannye-iz-vkontakte-v-power-bi-ostaetsa-tolko-0df455df.webp)

## Выводы

ВКонтакте — одна из самых популярных социальных сетей в СНГ, а Power BI одна из самых популярных в мире BI-платформ. Связав эти инструменты, вы легко построите удобные дашборды и проанализируете свои рекламные кампании и объявления.

Что для этого нужно:

1. Скачать и установить актуальную версию [языка R](https://cran.r-project.org/bin/windows/base/).
2. Скачать и установить актуальную версию [Microsoft Power BI](https://powerbi.microsoft.com/ru-ru/desktop/).
3. Создать Standalone-приложение ВКонтакте.
4. Установить пакет [rvkstat](https://selesnow.github.io/rvkstat/).
5. Получить токен для доступа к API ВКонтакте.
6. С помощью функций доступных в пакете rvkstat написать код для загрузки данных в Power BI.
7. Построить удобный и информативный dashboard.

---

*[Оригинал публикации на блоге Netpeak.](https://netpeak.net/ru/blog/kak-perenesti-dannyye-iz-vkontakte-v-power-bi/)*
