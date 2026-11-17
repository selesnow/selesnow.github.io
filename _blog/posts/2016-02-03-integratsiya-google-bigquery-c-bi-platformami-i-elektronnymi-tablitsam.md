---
title: Интеграция Google BigQuery c BI-платформами и электронными таблицами
date: '2016-02-03'
slug: integratsiya-google-bigquery-c-bi-platformami-i-elektronnymi-tablitsam
tags:
- BI
- Импорт данных
- Google Таблицы
- Excel
categories:
- BI
- Базы данных
- Таблицы
description: С каждым годом количество данных в различных базах растет в геометрической прогрессии — этот фактор определяет интенсивный рост интереса к Big Data. Сегодня облачная база данных Google BigQuery — один из наиболее востребованных инструментов, решающих проблему хранения и быстрой обработки больших массивов данных. Мы выяснили способы соединения хранящихся в Google BigQuery данных с различными инструментами […]
original_url: https://alexeyseleznev.wordpress.com/2016/02/03/%d0%b8%d0%bd%d1%82%d0%b5%d0%b3%d1%80%d0%b0%d1%86%d0%b8%d1%8f-google-bigquery-c-bi-%d0%bf%d0%bb%d0%b0%d1%82%d1%84%d0%be%d1%80%d0%bc%d0%b0%d0%bc%d0%b8-%d0%b8-%d1%8d%d0%bb%d0%b5%d0%ba%d1%82%d1%80%d0%be/
wp_id: 194
draft: false
cover: ../images/covers/194.webp
cover_generated: true
---

С каждым годом количество данных в различных базах растет в геометрической прогрессии — этот фактор определяет интенсивный рост интереса к Big Data. Сегодня облачная база данных Google BigQuery — один из наиболее востребованных инструментов, решающих проблему хранения и быстрой обработки больших массивов данных. Мы выяснили способы соединения хранящихся в Google BigQuery данных с различными инструментами визуализации и составили подробный мануал по настройке их интеграции.

![Картинки по запросу Интеграция](https://utmagazine.ru/uploads/content/WK_2.jpg)

## Как интегрировать BigQuery с Google Таблицами

Сначала необходимо установить дополнение к Google Таблицам [OWOX BI BigQuery Reports](https://chrome.google.com/webstore/detail/owox-bi-bigquery-reports/fepofngogkjnejgcbdmmkddnpeojbbin). В меню «Дополнения» выбираем пункт «Установить дополнение». В поиске вводим название «OWOX BI BigQuery Reports», затем нажимаем кнопку «+ Бесплатно».

![Установка дополнения](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-usta-2392d29c.webp)

Даем все необходимые разрешения установленному дополнению — кнопка «Разрешить».

![Даем все необходимые разрешения установленному дополнению](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-daem-e2911efb.webp)

В списке установленных дополнений появится «OWOX BI BigQuery Reports»:

![В списке установленных дополнений появится OWOX BI BigQuery Reports](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-v-sp-8ed65138.webp)

Выбираем пункт «Add a new report», затем — нужный проект в появившемся SideBar. После чего выбираем пункт «Add new query».

![выбираем пункт Add new query](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-vybi-e1dce690.webp)

В появившемся диалоговом окне «Add new query» вводим текст SQL запроса и жмем на кнопку «Save & Run».

![В появившемся диалоговом окне Add new query вводим текст SQL запроса](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-v-po-a607dc43.webp)

В вашей Google Таблице будет создан новый лист, название которого будет совпадать с названием запроса. На этот лист импортируется результат работы вашего запроса. С помощью пункта меню «Schedule reports» описанного дополнения можно задать настройки автоматического обновления результатов запроса через определенный интервал времени.

![С помощью пункта меню Schedule reports описанного дополнения можно задать настройки автоматического обновления результатов запроса через определенный интервал времени](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-s-po-fe0faab5.webp)

## Как интегрировать BigQuery с Excel

Для начала необходимо [скачать IQY файл](https://bigquery-connector.appspot.com/), который и является коннектором между BigQuery и Excel. Затем указываете аккаунт Google, к которому привязан нужный вам проект в BigQuery. Перейдя по указанной ссылке, нажмите на «Click here to download IQY file».

![Нажмите на Click here to download IQY file](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-nazh-3c3901bd.webp)

Далее вам необходимо создать ключ доступа. Переместитесь вниз по странице загрузки IQY файла к пункту «Creating a new key», установите время действия созданного ключа доступа. Максимально возможное время — 30 дней.

![Установите время действия созданного ключа доступа](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-usta-35866fc7.webp)

Далее следует опять подняться к началу страницы и скопировать сгенерированный ключ в буфер обмена.

![Далее следует опять подняться к началу страницы и скопировать сгенерированный ключ в буфер обмена](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-dale-dc432c16.webp)

После этого открываем Excel и подписываем ячейки на новом листе:

- ProjectID;
- Key;
- Query.

Напротив ячейки ProjectID требуется указать ID нужного вам проекта. Его можно вытянуть из URL проекта в BigQuery.

![Напротив ячейки ProjectID требуется указать ID нужного вам проекта](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-napr-1caee956.webp)

Напротив ячейки «Key» вводим скопированный раннее в буфер обмена ключ доступа. Напротив ячейки «Query» вводим текст SQL запроса, но в 1 ячейку можно ввести не более 256 символов. Для ввода более длинного запроса вы можете просто разместить разные части запроса в разных ячейках. В результате созданный вами лист будет выглядеть так:

![В результате созданный вами лист будет выглядеть так](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-v-re-5034b17b.webp)

Как видно на скриншоте, текст запроса растянут на четыре ячейки в диапазоне B3:E3 (потому что в одной ячейке можно вместить не более 256 символов).

> То, как вы разделите запрос, никакой роли не играет — он в любом случае будет работать.

Переходим на вкладку «Данные» и в группе «Получение внешних данных» выбираем пункт «Существующие подключения».

![Существующие подключения](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-sush-82aa2714.webp)

В открывшемся диалоговом окне жмем кнопку «Найти другие».

![Это не те подключения, которые вы ищете](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-eto-6c10a970.webp)

Далее выбираем скачанный ранее IQY файл и жмем «Открыть».

![Открываем файл IQY](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-otkr-e1d44d81.webp)

Теперь необходимо указать, куда следует поместить результат выполнения SQL запроса.

![Необходимо указать, куда следует поместить результат выполнения SQL запроса](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-neob-3434ad1d.webp)

Далее указываем ячейки, в которых расположен текст SQL запроса. В нашем случае он располагается в четырех ячейках B3:E3.

![Указываем ячейки, в которых расположен текст SQL запроса](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-ukaz-9bde9f69.webp)

Указываем ячейку, в которой введен ID проекта.

![Указываем ячейку, в которой введен ID проекта](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-ukaz-b1078fd8.webp)

Указываем ячейку, в которой хранится ключ доступа.

![Указываем ячейку, в которой хранится ключ доступа](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-ukaz-277354e4.webp)

После нажатия ОК результат SQL вашего запроса будет загружен на новый лист.

> К сожалению, на момент написания статьи нет коннектора, который мог бы импортировать данные из BigQuery напрямую в модель данных Excel.

## Как интегрировать BigQuery с QlikView

Для интеграции между Google BigQuery и QlikView нам необходим [специальный коннектор](http://market.qlik.com/qlikview-connector-for-google-bigquery.html). Сам коннектор бесплатный, но доступ предоставляется только пользователям, которые пользуются платными лицензиями QlikView. После скачивания и установки коннектора необходимо создать ClientID. Для этого заходим в левое меню [консоли Google Cloud](https://console.developers.google.com/), выбираем пункт «Credentials» из группы «APIs & auth». Жмем «Add credential» и выбираем «OAuth 2.0 client ID».

![OAuth 2.0 client ID](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-oaut-68c3d2a3.webp)

Потом выбираем тип приложения «Other», задаем имя «ClientID» и нажимаем кнопку «Create».

![выбираем тип приложения Other](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-vybi-bceda609.webp)

Создаем ClientID и ключ доступа к нему.

![Создаем ClientID и ключ доступа к нему](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-sozd-88524484.webp)

Теперь можно открыть редактор скриптов в QlikView и настроить подключение. В списке возможных коннекторов теперь есть «BigQuery». Выбираем его и жмем кнопку «Соед…».

![Теперь можно открыть редактор скриптов в QlikView и настроить подключение](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-tepe-51a814f1.webp)

Вводим необходимую для подключения информацию. Заполняем поля Client ID и Client secret и жмем Authorize.

![Вводим информацию, необходимую для подключения](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-vvod-88aab334.webp)

Даем разрешение на доступ коннектора к данным, хранящимся в BigQuery.

![Даем разрешение на доступ коннектора к данным, хранящимся в BigQuery](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-daem-4a303e6e.webp)

После авторизации будет заполнена информация по существующим в аккаунте проектам и наборам данных, вам остается выбрать нужный набор данных и нажать ОК.

![После авторизации будет заполнена информация по существующим в аккаунте проектам и наборам данных](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-posl-e488bb29.webp)

В редакторе скриптов будет сгенерирована строка подключения к Google BigQuery.

![В редакторе скриптов будет сгенерирована строка подключения к Google BigQuery](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-v-re-30493f2a.webp)

Остается только добавить текст нужного SQL запроса под строкой подключения и загрузить данные.

![Остается только добавить текст нужного SQL запроса под строкой подключения и загрузить данные](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-osta-ba992b90.webp)

После этого вы получите подтверждение загрузки в модель данных QlikView.

![После этого вы получите подтверждение загрузки в модель данных QlikView](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-posl-dc13a94d.webp)

## Как интегрировать Google BigQuery с Tableau

В Tableau существует встроенный коннектор к BigQuery, поэтому дополнительно скачивать ничего не потребуется.

> На данный момент коннектор, соединяющий Tableau и Google BigQuery, доступен только в версии Tableau Desktop Professional Edition.

Чтобы загрузить данные из Google BigQuery, выберите в группе «To a server» пункт «More Servers». В меню появится «Google BigQuery».

![Загрузите данные из Google BigQuery](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-zagr-14fec7d2.webp)

Заходим в аккаунт Google.

![Заходим в аккаунт Google](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-zaho-e91a4476.webp)

Выбираем нужный проект и набор данных из выпадающего списка.

![Выбираем нужный проект и набор данных из выпадающего списка](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-vybi-ffc6357f.webp)

Далее можем выбрать любую таблицу, либо ввести текст нужного нам SQL запроса, нажав кнопку «New Custom SQL».

![Далее можем выбрать любую таблицу, либо ввести текст нужного нам SQL запроса](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-dale-cd77bf80.webp)

После нажатия OK ваш запрос появится в рабочей области.

![После нажатия OK ваш запрос появится в рабочей области](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-posl-db55da49.webp)

Теперь вы можете строить любую визуализацию, создав новый рабочий лист.

![Теперь вы можете строить любую визуализацию, создав новый рабочий лист](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-tepe-401817d8.webp)

## Как интегрировать Google BigQuery с BIME Analytics

При первом запуске BIME сразу предлагает выбрать нужный коннектор. Для интеграции выбираем из списка Google BigQuery.

![Для интеграции выбираем из списка Google BigQuery](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-dlya-e2d2eaff.webp)

Жмем «Аутентификация через Google».

![Аутентификация через Google](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-aute-20ee8ab4.webp)

Даем разрешение BIME на автономный доступ к данным, хранящимся в BigQuery.

![Даем разрешение BIME на автономный доступ к данным, хранящимся в BigQuery](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-daem-c2825a08.webp)

Теперь у нас есть возможность выбрать нужный проект и набор данных, а также выбрать один из трех возможных способов интеграции:

1. **Single** — выбор одной конкретной таблицы из набора данных.
2. **Union** — выбор ряда таблиц из набора данных, все таблицы должны иметь одинаковую структуру.
3. **Custom** дает возможность ввести текст SQL запроса к данным.

![Custom дает возможность ввести текст SQL запроса к данным](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-cust-12b5ca6d.webp)

В данном случае нас интересует загрузка результата запроса. Вводим текст нашего SQL запроса и жмем «Test». Если тестирование запроса не выявило никаких ошибок, нажимаем «Next».

![Нас интересует загрузка результата запроса](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-nas-6ff1662b.webp)

Начнется процесс загрузки данных в BIME для дальнейшего построения нужной вам визуализации.

![Начнется процесс загрузки данных в BIME для дальнейшего построения нужной вам визуализации](../images/integratsiya-google-bigquery-c-bi-platformami-i-elektro-nach-c009f441.webp)

## Подведем итог

Теперь вы знаете, как подключать различные инструменты, начиная от бесплатных (Google таблицы) и заканчивая довольно дорогими (Tableau) к облачной базе данных Google BigQuery. Честно говоря, Google BigQuery хороша всем, кроме одного: новичку понадобятся недели, а может, и месяцы, чтобы разобраться в ней. Например, в Украине тех, кто умеет работать с QlikView, Tableau и BIME можно пересчитать на пальцах. Небольшое сравнение, насколько хорошо и удобно работать с данными из BigQuery в упомянутых BI-платформах.

Таблица баллов основывается только на моем субъективном мнении.

|  |  |  |  |
| --- | --- | --- | --- |
| **BI-платформы / электронные таблицы** | **Удобство интеграции с BigQuery** | **Удобство работы с данными** | **Стоимость** |
| **Google Spreadsheets** | Легко подключаемый и довольно простой в понимании коннектор от OWOX. **4 балла** | В Google Таблицах неудобно работать с загруженными данными в связи с тем, что в принципе отсутствует понятие модели данных. Поэтому данные можно загрузить только непосредственно на рабочий лист. При этом в Google SpreadSheets имеется ограничение в 2 млн. ячеек на один документ, то есть загрузить данные можно в рамках этого предела.**2 балла** | Бесплатно |
| **Microsoft Excel** | Не очень удобный коннектор, ключ доступа предоставляется максимум на 30 дней. Из-за этого придется часто генерировать новый ключ для обновления данных. **3 балла** | Сама по себе работа с данными в Excel очень удобна, но коннектор, написанный для интеграции Excel с Google BigQuery, оставляет желать лучшего и не имеет возможности загрузить данные непосредственно в модель данных а не на рабочий лист. В связи с чем при интеграции с BigQuery вы сталкиваетесь с ограничением в 1048576 строк, при этом размер файла будет очень большим. <**4 балла** | ~100 USD |
| **QlikView** | Достаточно простой в обращении коннектор, но, к сожалению, идет отдельно от самой платформы и для интеграции необходимо создавать в Google аккаунте Client ID. **3 балла** | QlikView очень удобен в работе с загруженными из BigQuery данными, доступен весь инструментарий визуализации данных. **5 баллов** | Бесплатная персональная версия, полный функционал от 1010 EUR |
| **Tableau** | Встроенные и интуитивно понятный коннектор. **5 баллов** | Работа по визуализация в Tableau уступает по удобству Microsoft Excel и QlikView, но тем не менее имеет достаточно мощный функционал. Что касается данных, загруженных из BigQuery, никаких ограничений в работе нет, доступен весь функционал. **4 балла** | Работа с BigQuery доступна только в Professional Edition стоимостью 1999 USD |
| **BIME** | Встроенный и интуитивно понятный понятный коннектор к BigQuery. **5 баллов** | BIME имеет довольно обширный инструментарий в работе с визуализацией данных, интуитивно понятный интерфейс позволяет быстро и удобно строить дашборды любой сложности, никаких ограничений при работе с данными загруженными из BigQuery нет. **5 баллов** | Работа с BigQuery доступна в тарифном плане «Big data» стоимостью 690 USD / месяц. |

Также я сравнил перечисленные BI-платформы по удобству интеграции и работы с Google BigQuery:

|  |  |  |
| --- | --- | --- |
| **BI-платформы / электронные таблицы** | **Удобство интеграции с BigQuery** | **Удобство работы с данными** |
| Google Spreadsheets | 4 | 2 |
| Microsoft Excel | 3 | 4 |
| QlikView | 3 | 5 |
| Tableau | 5 | 4 |
| BIME | 5 | 5 |

Надеюсь, эта инструкция сделает работу с облачными базами данных проще. Но если до сих пор непонятно, готов разъяснить сложные моменты в комментариях. А за комплексной помощью в настройке визуализации данных обращайтесь к нам в Netpeak — [мы поможем](http://netpeak.net/ru/blog/kak-my-sdelali-instrument-veb-analitiki-dlya-sayta-ecommerce/).

---

*[Оригинал публикации на блоге Netpeak.](https://netpeak.net/ru/blog/integratsiya-google-bigquery-c-bi-platformami-i-elektronnymi-tablitsami/)*

*[Упоминание о статье на конференции “Data Driven SEO – 1”.](https://www.youtube.com/watch?v=zgxFDMdCZZU&feature=youtu.be&t=2h6m17s)*
