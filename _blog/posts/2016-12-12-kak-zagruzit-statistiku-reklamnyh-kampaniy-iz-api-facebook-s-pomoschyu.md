---
title: Как загрузить статистику рекламных кампаний из API Facebook с помощью языка R
date: '2016-12-12'
slug: kak-zagruzit-statistiku-reklamnyh-kampaniy-iz-api-facebook-s-pomoschyu
tags:
- API
- Автоматизация
- Импорт данных
- Facebook
- R
categories:
- Реклама
- Программирование
- R
description: Популярность Facebook как рекламной площадки стремительно растет, но анализировать статистику в рекламном кабинете неудобно. Один из альтернативных способов — загрузить статистику в R и визуализировать ее. В этой статье я подробно расскажу, как получить данные из API Facebook и работать с ними в R. R — язык программирования для статистической обработки данных и работы с графикой, а также […]
original_url: https://alexeyseleznev.wordpress.com/2016/12/12/%d0%ba%d0%b0%d0%ba-%d0%b7%d0%b0%d0%b3%d1%80%d1%83%d0%b7%d0%b8%d1%82%d1%8c-%d1%81%d1%82%d0%b0%d1%82%d0%b8%d1%81%d1%82%d0%b8%d0%ba%d1%83-%d1%80%d0%b5%d0%ba%d0%bb%d0%b0%d0%bc%d0%bd%d1%8b%d1%85-%d0%ba/
wp_id: 581
draft: false
cover: ../images/covers/581.webp
cover_generated: true
---

Популярность Facebook как рекламной площадки стремительно растет, но анализировать статистику в рекламном кабинете неудобно. Один из альтернативных способов — загрузить статистику в R и [визуализировать](https://netpeak.net/ru/blog/kak-vizualizirovat-pokazatel-kachestva-klyuchevyh-slov-retsept-skripta-na-yazyke-r/) ее. В этой статье я подробно расскажу, как получить данные из API Facebook и работать с ними в R.

R — язык программирования для статистической обработки данных и работы с графикой, а также свободная программная среда вычислений с открытым исходным кодом в рамках проекта GNU. Пользователи ежедневно выкладывают в свободный доступ новые полезные пакеты, поэтому библиотека пакетов R богатая и значительно расширяет базовые возможности языка.

Я написал ряд функций для работы с API Facebook и их собрал в пакет [rfacebookstat](https://github.com/selesnow/rfacebookstat), доступный на [GitHub](https://github.com/) и [CRAN](https://cran.r-project.org/package=rfacebookstat).

## 1. Создайте приложение в Facebook

1.1. Чтобы начать работу с API Facebook, нужно создать новое приложение. Для этого перейдите по этой [ссылке](https://developers.facebook.com/apps/), или найдите пункт «Управление приложениями» в левом меню.

![Создайте приложение в Facebook](../images/kak-zagruzit-statistiku-reklamnyh-k-sozdajte-prilozenie-v-fa-30d4892d.webp)

1.2. В кабинете разработчика нажмите кнопку «+ Добавить новое приложение».

![Добавляем новое приложение в кабинете разработчика](../images/kak-zagruzit-statistiku-reklamnyh-k-dobavlaem-novoe-prilozen-e95c5e90.webp)

Заполните поля «Отображаемое название приложения»,«Эл. адрес для связи», «Категория» и нажмите «Создайте ID приложения».

1.3. Далее вы попадете в меню «Установка и настройка продукта». Кликните на кнопку «Начать» напротив пункта «Вход через Facebook».

![кнопка Начать напротив Входа через Facebook](../images/kak-zagruzit-statistiku-reklamnyh-k-knopka-nacat-naprotiv-vh-fb584a3b.webp)

1.4. Выберите платформу веб.

![Выбираем платформу веб](../images/kak-zagruzit-statistiku-reklamnyh-k-vybiraem-platformu-veb-2f9d08ed.webp)

1.5. Вводим [https://selesnow.githun.io](https://selesnow.githun.io/) в поле «URL сайта» и жмём Save — Продолжить — Далее…

![Указываем урл сайта](../images/kak-zagruzit-statistiku-reklamnyh-k-ukazyvaem-url-sajta-ca321cb1.webp)

1.6. В меню приложения перейдите в раздел «Вход через Facebook». В поле «Действительные URL-адреса для перенаправления OAuth» введите «https://selesnow.github.io/rfacebookstat/getToken/get\_token.html».

![Что делаем в меню приложения](../images/kak-zagruzit-statistiku-reklamnyh-k-cto-delaem-v-menu-priloz-585ad956.webp)

1.7. Подключаем ещё один продукт — «API Marketing»

![Подключаем API Marketing](../images/kak-zagruzit-statistiku-reklamnyh-k-podklucaem-api-marketing-514de796.webp)

На этом создание и настройка приложения завершены. Перейдите в меню Настройка — Основное и скопируйте идентификатор и секрет приложения.

![Копируем идентификатор и секрет приложения](../images/kak-zagruzit-statistiku-reklamnyh-k-kopiruem-identifikator-i-c99e0ede.webp)

Эти данные нам понадобятся для авторизации.

**Важно**: многие ошибочно выводят своё приложения из статуса «В разработке», и при попытке авторизации получают ошибку, так как для публикации приложения необходимо пройти серьёзные проверки со стороны Facebook. К счастью, если вы регистрируете приложение для своих личных нужд то выводить его из разработки не требуется.

![если вы регистрируете приложение для своих личных нужд то не нужно выводить его из разработки](../images/kak-zagruzit-statistiku-reklamnyh-k-esli-vy-registriruete-pr-1d6b2b37.webp)

## 2. Установите пакет rfacebookstat

Пакет rfacebookstat доступен для установки из CRAN и GitHub.

2.1. Для установки пакетов с CRAN используйте стандартную команду install.packages().

```

install.packages("rfacebookstat")
```

2.2. Подключите пакет rfacebookstat.

Пакет можно рассматривать как отдельное программное обеспечение, поэтому, как и любую программу его необходимо сначала установить, и при каждой необходимости – запускать. В R подключение пакетов осуществляется функцией library().

```

library(rfacebookstat)
```

## 3. Получите токен для работы с API Facebook

Для начала работы с API Facebook осталось пройти авторизацию. Воспользуйтесь функцией fbAuth() в пакете rfacebookstat.

3.1. На вкладке «Настройки» —> «Основное» скопируйте ID и секрет вашего приложения и введите их в соответствующие аргументы функций.

```

fbAuth(app_id     = 00000000000000,
      app_secret = "xxxxxxxxxxxxx", 
      username   = "ваш логин")
```

В аргумент username передайте ваш логин на Facebook.

3.2. Возможно, впервые получая токен, вы попадете на страницу с предупреждением, что некоторые разрешения еще не одобрены для использования Facebook. Пропустите это предупреждение с помощью кнопки «Продолжить как, …».

Подтвердите вход через Facebook.

![Входим через ФБ](../images/kak-zagruzit-statistiku-reklamnyh-k-vhodim-cerez-fb-90d7067a.webp)

Далее вы будете перенаправлены на страницу сайта моих пакетов <https://selesnow.github.io>, где для вас будет сгенерирован краткосрочный авторизационный токен.

В своё время меня часто спрашивали о безопасности использования разработанных мной пакетов. Многих беспокоил именно процесс авторизации через мой сайт. Поэтому я написал о безопасности использования пакетов подробную статью  [«Насколько безопасно использовать R пакеты для работы с API рекламных систем»](https://habr.com/ru/post/430888/).

Если у вас включён JavaScript, то токен автоматически будет скопирован в буфер обмена,  и через 30 секунд вы будете перенаправлены на страницу с официальной справкой к пакету. Если вы отключили выполнение JavaScript, то самостоятельно скопируйте токен.

3.3. Полученный токен необходимо ввести в R консоль.

![Необходимый токен](../images/kak-zagruzit-statistiku-reklamnyh-k-neobhodimyj-token-85575760.webp)

3.4. Далее ваш краткосрочный токен автоматически будет заменён на долгосрочный, и вы увидите в консоли сообщение:

```

Token changed to long time successfully
Do you want save your access token into rds file C:/Users/Username/Documents/blog_login.rfb_auth.rds for use it between R sessions ? 
y / n (recmedation y) ?:
```

Первая строка сообщения говорит о том, что ваш краткосрочный токен был успешно заменён долгосрочным токеном. После, пакет спрашивает вас, хотите ли вы сохранить полученные учётные данные, что бы использовать в разных сессиях работы в R. Я крайне рекомендую вам отвечать на этот вопрос y, это избавить вас от необходимости постоянно проходить авторизацию через браузер.

3.5. Проверить, что авторизация была успешно пройдена можно запросив список доступных аккаунтов.

```

fbGetAdAccounts(username = "ваш логин")
```

Если вы получите список аккаунтов – значит авторизация пройдена успешно, если получите ошибку — то скорее всего вы неправильно настроили приложение.

## 4. Получите статистику по рекламным аккаунтам в Facebook

Мы завершили подготовительный этап и можем перейти непосредственно к импорту данных.

Основная функция пакета rfacebookstat — fbGetMarketingStat(). Рассмотрим подробнее работу с этой функцией, потому что с ее помощью можно получить любые данные об эффективности рекламного аккаунта.

### 4.1. Синтаксис

```

stat <- fbGetMarketingStat(accounts_id  = "act_0000000000",
                           sorting      = NULL,
                           level        = "account",
                           breakdowns   = NULL,
                           fields       = "account_id, 
                                           campaign_name,
                                           impressions, 
                                           clicks, 
                                           reach, 
                                           spend",
                           filtering    = NULL,
                           date_start   = Sys.Date() - 30,
                           date_stop    = Sys.Date(),
                           username     = getOption("rfacebookstat.username"),
                           token_path = fbTokenPath())
```

В приведённом выше коде представлены значения большинства аргументов функции fbGetMarketingStat() принятые по умолчанию.

### 4.2. Аргументы функции

***4.2.1. accounts\_id****—*ID рекламного аккаунта. Это обязательный аргумент. Вы можете получить его из URL, если перейдете в нужный рекламный аккаунт Facebook.

![accounts_id](../images/kak-zagruzit-statistiku-reklamnyh-k-accountsid-57396b44.webp)

Так как указывать id рекламного аккаунта вам необходимо при каждом обращении к API, вы можете избежать дублирования этой информации, передав в начале скрипта список нужных аккаунтов в опцию rfacebookstat.accounts\_id.

```

options( rfacebookstat.accounts_id = c("47725506", "361373151") )
```

После чего, каждая функция пакета rfacebookstat автоматически будет подтягивать указанные в опции rfacebookstat.accounts\_id аккаунты.

***4.2.2. sorting —***cортировка данных. Необязательный аргумент. На входе принимает список полей и направление сортировки (по возрастанию или по убыванию). Пример: reach\_descending, impressions\_ascending.

***4.2.3. level***— основной уровень детализации данных. Обязательный аргумент. Принимает значения ad, adset, campaign, account. Пример — level = “account”.

***4.2.4. fields***— список полей, по которым вы планируете получить данные. Обязательный аргумент. Пример: fields = “account\_id,account\_name,campaign\_name,impressions,unique\_impressions,clicks,unique\_clicks,reach,spend”.

Список доступных полей в версии API 2.8. смотрите в таблице ниже или [официальной документации](https://developers.facebook.com/docs/marketing-api/insights/fields/v2.8).

|  |  |
| --- | --- |
| **Поле** | **Описание** |
| account\_idnumeric string | Идентификатор рекламного аккаунта, с которым связана ваша рекламная деятельность. Рекламный аккаунт включает кампании, объявления и биллинг.[По умолчанию](https://developers.facebook.com/docs/graph-api/using-graph-api/#fields) |
| account\_namestring | Имя рекламного аккаунта, в котором сосредоточена ваша рекламная деятельность. Ваш рекламный аккаунт содержит кампании, объявления и биллинг. |
| action\_values[list<AdsActionStats>](https://developers.facebook.com/docs/marketing-api/reference/ads-action-stats/) | Общая стоимость всех конверсий в результате просмотра рекламы. |
| actions[list<AdsActionStats>](https://developers.facebook.com/docs/marketing-api/reference/ads-action-stats/) | Общее количество действий, которые люди выполняют после просмотра рекламы. Действия могут включать вовлеченность, клики или конверсии. |
| ad\_idnumeric string | Уникальный идентификатор объявления, который вы видите в отчете.[По умолчанию](https://developers.facebook.com/docs/graph-api/using-graph-api/#fields) |
| ad\_namestring | Уникальный ID объявления, который вы видите в отчете. |
| adset\_idnumeric string | Уникальный идентификатор группы объявлений, который вы видите в отчете. Группа объявлений — это набор объявлений с одинаковыми настройками бюджета, графика показа, оптимизации и целевой аудитории.[По умолчанию](https://developers.facebook.com/docs/graph-api/using-graph-api/#fields) |
| adset\_namestring | Название группы объявлений, которое вы видите в отчете. |
| app\_store\_clicksnumeric string | Количество кликов по ссылкам на магазин приложений в вашей рекламе. |
| buying\_typestring | Способы оплаты, таргетинга и измерения результатов рекламы в кампаниях: динамические ставки, фиксированные ставки или покупка охвата и частоты. |
| call\_to\_action\_clicksnumeric string | Метрика указывает, сколько раз люди нажали кнопку с призывом к действию в рекламе. |
| campaign\_idnumeric string | Уникальный ID рекламной кампании, который вы видите в отчете. Кампания включает группы объявлений и отдельные рекламные объявления.[По умолчанию](https://developers.facebook.com/docs/graph-api/using-graph-api/#fields) |
| campaign\_namestring | Название рекламной кампании в отчетах. Кампания включает группы объявлений и отдельные рекламные объявления. |
| canvas\_avg\_view\_percentnumeric string | Среднее число просмотров Холста (в процентах). Холст — это экран, который открывается на мобильном устройстве после того, как человек нажимает ссылку Холста в вашей рекламе. Он может включать интерактивные или мультимедийные компоненты, такие как видео, изображения, каталоги продуктов и так далее. |
| canvas\_avg\_view\_timenumeric string | Среднее время (в секундах), в течение которого люди просматривали Холст Facebook. Холст — это экран, который открывается на мобильном устройстве после того, как человек нажимает ссылку Холста в вашей рекламе. Он может включать интерактивные или мультимедийные компоненты, такие как видео, изображения, каталоги продуктов и так далее. |
| clicksnumeric string | Общее число нажатий вашего объявления. В это число могут входить сторонние клики на веб-сайт, отметки «Нравится» Страницы, комментарии к публикациям, ответы на приглашения или установки приложения |
| cost\_per\_10\_sec\_video\_view[list<AdsActionStats>](https://developers.facebook.com/docs/marketing-api/reference/ads-action-stats/) | Средняя цена за каждый 10-секундный просмотр видео. |
| cost\_per\_action\_type[list<AdsActionStats>](https://developers.facebook.com/docs/marketing-api/reference/ads-action-stats/) | Средняя цена за актуальное действие. |
| cost\_per\_estimated\_ad\_recallersnumeric string | Средняя цена за приблизительный прирост запоминаемости рекламы на человека. |
| cost\_per\_inline\_link\_clicknumeric string | Средняя стоимость клика по каждой встроенной ссылке. |
| cost\_per\_inline\_post\_engagementnumeric string | Средняя стоимость вовлеченности для каждой встроенной публикации. |
| cost\_per\_total\_actionnumeric string | Средняя цена за актуальное действие. |
| cost\_per\_unique\_action\_type[list<AdsActionStats>](https://developers.facebook.com/docs/marketing-api/reference/ads-action-stats/) | Средняя цена каждого уникального действия. |
| cost\_per\_unique\_clicknumeric string | Средняя цена за каждый уникальный клик по ссылке (все), полученный в результате вашей рекламы. |
| cost\_per\_unique\_inline\_link\_clicknumeric string | Средняя цена каждого уникального клика по встроенной ссылке. |
| cpcnumeric string | Средняя цена за каждый клик в результате просмотра вашей рекламы. |
| cpmnumeric string | Средняя цена за 1 000 показов. |
| cppnumeric string | Средняя стоимость охвата 1 000 пользователей. |
| ctrnumeric string | Кликабельность для всех кликов. Общее количество полученных кликов (например, сторонние клики, отметки «Нравится», ответы на приглашения), деленное на количество показов. |
| date\_startstring | Дата начала учета ваших данных. Эта метрика основана на диапазоне данных, который вы выбрали для своего представления отчетности.[По умолчанию](https://developers.facebook.com/docs/graph-api/using-graph-api/#fields) |
| date\_stopstring | Дата окончания учета ваших данных. Эта метрика основана на диапазоне данных, который вы выбрали для своего представления отчетности.[По умолчанию](https://developers.facebook.com/docs/graph-api/using-graph-api/#fields) |
| deeplink\_clicksnumeric string | Количество кликов по ссылкам на определенные части приложения. |
| estimated\_ad\_recall\_ratenumeric string | Доля участников опроса (в процентах), которые вспомнили вашу рекламу в течение двух дней после просмотра. |
| estimated\_ad\_recallersnumeric string | Примерное количество людей, которые через два дня после просмотра могут вспомнить вашу рекламу, если их о ней спросят. Эта метрика показывает результативность рекламы с целями «Узнаваемость бренда», «Просмотры видео» и «Вовлеченность для публикации Страницы». |
| frequencynumeric string | Среднее количество просмотров рекламы каждым человеком. |
| impressionsnumeric string | Количество просмотров рекламы.[По умолчанию](https://developers.facebook.com/docs/graph-api/using-graph-api/#fields) |
| inline\_link\_click\_ctrnumeric string | Процентное отношение просмотров вашей рекламы к кликам по встроенной ссылке. |
| inline\_link\_clicksnumeric string | Количество кликов по ссылкам на выбранные адреса, входящие или не входящие в состав объектов монетизации Facebook. Для кликов по встроенным ссылкам используется фиксированное окно атрибуции «1 день после клика». |
| inline\_post\_engagementnumeric string | Общее количество действий, выполненных людьми с вашей рекламой (или, в некоторых случаях, все публикации). Для вовлеченности от встроенных публикаций используется фиксированное окно атрибуции «один день после клика». |
| newsfeed\_avg\_positionnumeric string | Средняя позиция, где ваша реклама была вставлена в ленты новостей на мобильных устройствах и ПК. Первая позиция находится наверху ленты новостей. |
| newsfeed\_clicksnumeric string | Общее количество кликов на вашу рекламу в лентах новостей пользователей на мобильных устройствах и ПК. |
| newsfeed\_impressionsnumeric string | Общее количество вставок вашей рекламы в ленты новостей пользователей на мобильных устройствах и ПК. |
| objectivestring | Цель, которую вы выбрали для кампании. Цель отражает, чего вы хотите добиться с помощью рекламы. |
| reachnumeric string | Количество людей, которые хотя бы раз увидели вашу рекламу. Отличие охвата от показов заключается в том, что последние могут включать просмотры рекламы одним и тем же человеком. |
| relevance\_scoreAdgroupRelevanceScore | Оценка от 1 до 10, обозначающая уровень реагирования целевой аудитории на вашу рекламу. Данный показатель отображается после 500 показов и только для объявлений (не отображается для групп объявлений и кампаний). |
| social\_clicksnumeric string | Количество всех кликов, полученных рекламой (например, отметки «Нравится», ответы на приглашения, клики с других сайтов) при отображении с социальной информацией (например, Алине Ивановой это нравится). |
| social\_impressionsnumeric string | Количество просмотров вашей рекламы с упоминанием того, что кто-то из друзей на Facebook взаимодействовал с вашей Страницей Facebook или рекламой. |
| social\_reachnumeric string | Количество людей, которые увидели вашу рекламу с упоминанием того, что один из их друзей на Facebook взаимодействовал с вашей Страницей Facebook или рекламой. |
| social\_spendnumeric string | Общая сумма, которую вы уже потратили на свою рекламу, которая дополняется социальной информацией (например, Петру Соколову это нравится). |
| spendnumeric string | Общая сумма, которую вы потратили на кампанию, группу объявлений или рекламу в период показа.[По умолчанию](https://developers.facebook.com/docs/graph-api/using-graph-api/#fields) |
| total\_action\_valuenumeric string | Общая стоимость всех конверсий в результате просмотра рекламы. |
| total\_actionsnumeric string | Общее количество действий, которые люди выполняют после просмотра рекламы. Действия могут включать вовлеченность, клики или конверсии. |
| total\_unique\_actionsnumeric string | Количество людей, которые выполнили действие после просмотра рекламы. |
| unique\_actions[list<AdsActionStats>](https://developers.facebook.com/docs/marketing-api/reference/ads-action-stats/) | Количество людей, которые выполнили действие после просмотра рекламы. |
| unique\_clicksnumeric string | Общее количество уникальных пользователей, нажавших на ссылку вашего рекламного объявления. Например, если три человека нажали одно и то же объявление пять раз, число уникальных кликов — три. |
| unique\_ctrnumeric string | Уникальная кликабельность для всех кликов. Количество людей, нажавших рекламу в любом месте, разделенное на количество охваченных людей. Например, вы получили 20 уникальных кликов, а реклама была показана 1 000 уникальным пользователям. Значит, соотношение кликов к показам составляет 2%. |
| unique\_impressionsnumeric string | Количество людей, видевших рекламу как минимум раз. |
| unique\_inline\_link\_click\_ctrnumeric string | Отношение количества просмотров рекламы к кликам по ссылке. Для кликабельности встроенных элементов используется фиксированное окно атрибуции «1 день после клика». |
| unique\_inline\_link\_clicksnumeric string | Количество человек, выполнивших клик по встроенной ссылке. |
| unique\_link\_clicks\_ctrnumeric string | Доля людей, которые посмотрели вашу рекламу и нажали ссылку. |
| unique\_social\_clicksnumeric string | Количество людей, которые нажали эту рекламу (например, отметки «Нравится», ответы на приглашения, клики с других сайтов), пока она отображалась с социальной информацией (например, Алине Ивановой это нравится). |
| unique\_social\_impressionsnumeric string | Количество людей, которым было показано объявление в контекстной рекламе. |
| video\_10\_sec\_watched\_actions[list<AdsActionStats>](https://developers.facebook.com/docs/marketing-api/reference/ads-action-stats/) | Количество просмотров видео в течение как минимум 10 секунд или почти полностью (в зависимости от того, что произошло раньше). |
| video\_15\_sec\_watched\_actions[list<AdsActionStats>](https://developers.facebook.com/docs/marketing-api/reference/ads-action-stats/) | Количество просмотров вашего видео в течение как минимум 15 секунд или почти полностью в зависимости от того, что наступило раньше. |
| video\_30\_sec\_watched\_actions[list<AdsActionStats>](https://developers.facebook.com/docs/marketing-api/reference/ads-action-stats/) | Количество просмотров вашего видео в течение как минимум 30 секунд или почти полностью в зависимости от того, что наступило раньше. |
| video\_avg\_pct\_watched\_actions[list<AdsActionStats>](https://developers.facebook.com/docs/marketing-api/reference/ads-action-stats/) | (Использование данной метрики будет скоро прекращено, используйте video\_avg\_percent\_watched\_actions). Это общее время просмотра видео, разделенное на количество просмотров видео в течение всей его продолжительности. Метрика недоступна для прямых эфиров. |
| video\_avg\_percent\_watched\_actions[list<AdsActionStats>](https://developers.facebook.com/docs/marketing-api/reference/ads-action-stats/) | Среднее время просмотра видео (в процентах). |
| video\_avg\_sec\_watched\_actions[list<AdsActionStats>](https://developers.facebook.com/docs/marketing-api/reference/ads-action-stats/) | (Использование данной метрики будет скоро прекращено, используйте video\_avg\_time\_watched\_actions). Это общее время просмотра видео, разделенное на общее количество просмотров видео. |
| video\_avg\_time\_watched\_actions[list<AdsActionStats>](https://developers.facebook.com/docs/marketing-api/reference/ads-action-stats/) | Среднее время, в течение которого люди смотрели видео. |
| video\_complete\_watched\_actions[list<AdsActionStats>](https://developers.facebook.com/docs/marketing-api/reference/ads-action-stats/) | Количество просмотров видео в течение как минимум 30 секунд или почти полностью (в зависимости от того, что произошло раньше). |
| video\_p100\_watched\_actions[list<AdsActionStats>](https://developers.facebook.com/docs/marketing-api/reference/ads-action-stats/) | Количество раз, когда ваше видео было просмотрено в точке 100%, включая просмотры, когда человек прокрутил видео до этого момента. |
| video\_p25\_watched\_actions[list<AdsActionStats>](https://developers.facebook.com/docs/marketing-api/reference/ads-action-stats/) | Количество раз, когда ваше видео было просмотрено в точке 25%, включая просмотры, когда человек прокрутил видео до этого момента. |
| video\_p50\_watched\_actions[list<AdsActionStats>](https://developers.facebook.com/docs/marketing-api/reference/ads-action-stats/) | Количество раз, когда ваше видео было просмотрено в точке 50%, включая просмотры, когда человек прокрутил видео до этого момента. |
| video\_p75\_watched\_actions[list<AdsActionStats>](https://developers.facebook.com/docs/marketing-api/reference/ads-action-stats/) | Количество раз, когда ваше видео было просмотрено в точке 75%, включая просмотры, когда человек прокрутил видео до этого момента. |
| video\_p95\_watched\_actions[list<AdsActionStats>](https://developers.facebook.com/docs/marketing-api/reference/ads-action-stats/) | Количество раз, когда ваше видео было просмотрено в точке 95%, включая просмотры, когда человек прокрутил видео до этого момента. |
| website\_clicksnumeric string | Количество кликов по ссылкам на сайт в вашей рекламе. |
| website\_ctr[list<AdsActionStats>](https://developers.facebook.com/docs/marketing-api/reference/ads-action-stats/) | Процентное отношение просмотров вашей рекламы к кликам по сайту. |

***4.2.5. breakdowns*** — аргумент, с помощью которого можно получить данные в разбивке на различные сегменты. Можно разбивать информацию по следующим срезам:

- age;
- country;
- gender;
- frequency\_value;
- hourly\_stats\_aggregated\_by\_advertiser\_time\_zone;
- hourly\_stats\_aggregated\_by\_audience\_time\_zone;
- impression\_device;
- place\_page\_id;
- placement;
- device\_platform;
- product\_id;
- region;
- actions;
- publisher\_platform;
- platform\_position;
- impression\_device.

В одном запросе можно комбинировать несколько срезов. На данный момент доступны следующие комбинации:

Поля, отмеченные звездочкой «\*», могут запрашиваться вместе с *action\_type, action\_target\_id* и *action\_destination*.

- action\_type \*;
- action\_target\_id \*;
- action\_device \*;
- action\_device, placement \*;
- action\_device, placement, impression\_device \*;
- action\_device, publisher\_platform \*;
- action\_device, publisher\_platform, impression\_device \*;
- action\_device, publisher\_platform, platform\_position \*;
- action\_device, publisher\_platform, platform\_position, impression\_device \*;
- action\_reaction;
- action\_type, action\_reaction;
- age \*;
- gender \*;
- age, gender \*;
- country \*;
- region \*;
- placement \*;
- placement, impression\_device \*;
- publisher\_platform \*;
- publisher\_platform, impression\_device \*;
- publisher\_platform, platform\_position \*;
- publisher\_platform, platform\_position, impression\_device \*;
- product\_id \*;
- hourly\_stats\_aggregated\_by\_advertiser\_time\_zone \*;
- hourly\_stats\_aggregated\_by\_audience\_time\_zone \*;
- action\_carousel\_card\_id / action\_carousel\_card\_name;
- action\_carousel\_card\_id / action\_carousel\_card\_name, placement;
- action\_carousel\_card\_id / action\_carousel\_card\_name, placement, impression\_device;
- action\_carousel\_card\_id / action\_carousel\_card\_name, country;
- action\_carousel\_card\_id / action\_carousel\_card\_name, age;
- action\_carousel\_card\_id / action\_carousel\_card\_name, gender;
- action\_carousel\_card\_id / action\_carousel\_card\_name, age, gender.

Пример: breakdowns = “region”

***4.2.6. filtering*** — фильтр данных. Необязательный аргумент. Фильтры задаются в виде JSON объектов «ключ:значение». Необходимо прописать три свойства:

- field — поле, по которому будет осуществляться фильтрация;
- operator — оператор логического значения (‘EQUAL’, ‘NOT\_EQUAL’, ‘GREATER\_THAN’, ‘GREATER\_THAN\_OR\_EQUAL’, ‘LESS\_THAN’, ‘LESS\_THAN\_OR\_EQUAL’, ‘IN\_RANGE’, ‘NOT\_IN\_RANGE’, ‘CONTAIN’, ‘NOT\_CONTAIN’, ‘IN’, ‘NOT\_IN’, ‘ANY’, ‘ALL’, ‘NONE’);
- value — значения, по которому будет фильтроваться указанное поле.

Пример:   filtering = “impressions LESS\_THAN 5000”

***4.2.7. date\_start*** — начальная дата отчетного периода в формате YYYY-MM-DDD.

***4.2.8. date\_stop*** — конечная дата отчетного периода в формате YYYY-MM-DDD.

***4.2.9. api\_version*** — версия API Facebook.

***4.2.10. access\_token*** — токен доступа.

## 5. Примеры использования функции fbGetMarketingStat

5.1. Перед тем как запускать описанные ниже примеры, сгенерируйте API-токен и сохраните его в виде файла, с помощью функции fbAuth().

```

fbAuth(app_id     = 00000000000000,
       app_secret = "xxxxxxxxxxxxx", 
       username   = "ваш логин")
```

5.2. Чтобы получить статистику о количестве показов, кликов и затрат на рекламу на уровне аккаунта и в  разрезе регионов, введите следующий код:

```

AccStat <- fbGetMarketingStat( 
                      accounts_id = «act_0000000000»,
                      level = "account",
                      fields = "account_id,
                                account_name,
                                impressions,
                                clicks,
                                spend",
                      breakdowns = "region",
                      date_start = "2020-03-01",
                      date_stop = "2020-03-30",
                      username   = "ваш логин")
```

5.3. Получите статистику по количеству уникальных показов и уникальных кликов, с фильтром по возрастным группам «18-24», «25-34» и сортировкой данных в порядке убывания количества уникальных показов (поле reach).

```

CampStat <-     fbGetMarketingStat(accounts_id = "act_0000000000",
                          level = "campaign",
                          fields = "campaign_name,
                                    reach,
                                    unique_clicks",
                          breakdowns = "age",
                          sorting = "reach_descending",
                          filtering  = "age IN 18-24,25-34",
                          date_start = "2020-03-01",
                          date_stop  = "2020-03-30",
                          username   = "ваш логин")
```

## 6. Официальные учебные материалы

Пакет rfacebookstat имеет хорошую русскоязычную документацию. В этом разделе приведу ряд ссылок, которые позволят вам максимально подробно разобраться со всеми его возможностями и особенностями синтаксиса.

### Официальные ссылки:

1. Виньетки:
   - [авторизация в API facebook](https://cran.r-project.org/web/packages/rfacebookstat/vignettes/rfacebookstat-authorization.html);
   - [загрузки статистики из рекламных аккаунтов Facebook](https://cran.r-project.org/web/packages/rfacebookstat/vignettes/rfacebookstat-get-statistics.html);
2. [Страница документации](https://selesnow.github.io/rfacebookstat).
3. [Плейлист с видеоуроками](https://www.youtube.com/watch?v=SgcxDqZ-5Qg&list=PLD2LDq8edf4pItOb-vZTG5AXZK2niJ8_R).
4. [Страница пакета на CRAN](https://cran.r-project.org/package=rfacebookstat).
5. [Страница проекта на GitHub](https://github.com/selesnow/rfacebookstat/).

## Выводы

Используя API Facebook и пакет функций на языке R rfacebookstat, вы сможете:

- получить данные по своим рекламным аккаунтам, кампаниям, объявлениям и так далее во множестве различных разрезов.
- строить на основе полученных данных любые визуализации, используя всю мощь языка R.
- передавать полученные данные в любую базу данных или сохранять в виде CSV-файла.

---

*[Оригинал публикации на блоге Netpeka.](https://netpeak.net/ru/blog/kak-zagruzit-statistiku-reklamnykh-kampanii-iz-api-facebook-s-pomoshch-yu-yazyka-r/)*
