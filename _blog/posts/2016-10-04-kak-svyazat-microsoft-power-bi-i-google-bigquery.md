---
title: Как связать Microsoft Power BI и Google BigQuery
date: '2016-10-04'
slug: kak-svyazat-microsoft-power-bi-i-google-bigquery
tags:
- API
- BI
- Импорт данных
- BigQuery
- Power BI
- R
categories:
- BI
- Базы данных
- Программирование
description: Если вы храните данные в Google BigQuery, то наверняка захотите визуализировать их. В этой статье я расскажу, как загрузить данные из Google BigQuery в Microsoft Power BI с помощью скрипта на языке R.
original_url: https://alexeyseleznev.wordpress.com/2016/10/04/%d0%ba%d0%b0%d0%ba-%d1%81%d0%b2%d1%8f%d0%b7%d0%b0%d1%82%d1%8c-microsoft-power-bi-%d0%b8-google-bigquery/
wp_id: 538
draft: false
---

Если вы храните данные в Google BigQuery, то наверняка захотите визуализировать их. В этой статье я расскажу, как загрузить данные из Google BigQuery в Microsoft Power BI с помощью скрипта на языке R.

![Картинки по запросу Как связать Microsoft Power BI и Google BigQuery](../images/kak-svyazat-microsoft-power-bi-i-google-bigquery-kak-analizi-b77d7374.webp)

Интеграция Google BigQuery c BI-платформами и электронными таблицами

Ранее я уже рассказывал, как связывать Google BigQuery с различными инструментами визуализации, но интеграция Google BigQuery с Microsoft Power BI — отдельная тема.

Оба сервиса динамично развиваются, их возможности регулярно улучшаются, благодаря чему BigQuery и Power BI так популярны. При этом Google и Microsoft во многом конкурируют, поэтому, как правило, интеграции между их продуктами нет, и в ближайшем будущем не стоит ждать появления коннектора к Google BigQuery в программном интерфейсе Microsoft Power BI.

Как начать работу с BigData — загружаем данные в Google BigQuery

На самом деле есть несколько вариантов решения этой проблемы, в данной статье мы рассмотрим два способа загрузить данные из Google BigQuery в Microsoft Power BI:

- с помощью ODBC драйвера для Google BigQuery;
- с помощью R коннектора.

## Как связать Google BigQuery и Microsoft Power BI с помощью ODBC драйвера?

Первый способ стал доступен в ноябре 2016 года вместе с выходом [ODBC драйвера для Google BigQuery](https://cloud.google.com/bigquery/partners/simba-drivers/).

1. Скачайте и установите версию ODBC драйвера, соответствующую вашей операционной системе. Найти нужную версию можно, перейдя по [этой ссылке](https://cloud.google.com/bigquery/partners/simba-drivers/).

2. Создайте источник данных ODBC.

2.1. Перейдите в Панель управления / Все элементы панели управления / Администрирование / Источники данных ODBC (нужной разрядности).

![Создайте источник данных ODBC](../images/kak-svyazat-microsoft-power-bi-i-google-bigquery-sozdajte-is-f50490b1.webp)

2.2. В окне «Администратор источника данных ODBC» перейдите на вкладку «Пользовательский DSN» и нажмите «Добавить».

![В окне «Администратор источника данных ODBC» перейдите на вкладку «Пользовательский DSN» и нажмите «Добавить»](../images/kak-svyazat-microsoft-power-bi-i-google-bigquery-v-okne-admi-09907012.webp)

2.3. В окне «Создание нового источника данных» выбираете драйвер «Simba ODBC Driver for Google BigQuery» и нажимаете «Готово».

![В окне «Создание нового источника данных» выбираете драйвер «Simba ODBC Driver for Google BigQuery» и нажимаете «Готово»](../images/kak-svyazat-microsoft-power-bi-i-google-bigquery-v-okne-sozd-dbe30147.webp)

2.4. Далее откроется окно настройки ODBC подключения. Необходимо заполнить поле Data Source Name, выбрать из выпадающего списка OAuth mechanism и нажать Sign in для прохождения процесса аутентификации.

![Необходимо заполнить поле Data Source Name, выбрать из выпадающего списка OAuth mechanism и нажать Sign in для прохождения процесса аутентификации](../images/kak-svyazat-microsoft-power-bi-i-google-bigquery-neobhodimo-57df0f54.webp)

2.5. Выбираете Google аккаунт, у которого есть доступ к нужному проекту в Google BigQuery, и подтверждаете разрешение на получение автономного доступа.

![Выбираете Google аккаунт, у которого есть доступ к нужному проекту в Google BigQuery](../images/kak-svyazat-microsoft-power-bi-i-google-bigquery-vybiraete-g-15975420.webp)

![Выбираете Google аккаунт, у которого есть доступ к нужному проекту в Google BigQuery, и подтверждаете разрешение на получение автономного доступа](../images/kak-svyazat-microsoft-power-bi-i-google-bigquery-vybiraete-g-f65456aa.webp)

2.6. Далее вам будет предоставлен токен доступа, который необходимо скопировать и вставить в поле Confirmation code, после чего просто кликните по полю Refresh token для генерации токена обновления.

![Далее вам будет предоставлен токен доступа, который необходимо скопировать и вставить в поле Confirmation code](../images/kak-svyazat-microsoft-power-bi-i-google-bigquery-dalee-vam-b-05d71275.webp)

![просто кликните по полю Refresh token для генерации токена обновления](../images/kak-svyazat-microsoft-power-bi-i-google-bigquery-prosto-klik-8bfdfd58.webp)

2.7. Из выпадающего списка Catalog (Project) выберите нужный проект и нажмите Test.

![Из выпадающего списка Catalog (Project) выберите нужный проект и нажмите Test](../images/kak-svyazat-microsoft-power-bi-i-google-bigquery-iz-vypadaus-a56adc55.webp)

2.8. Драйвер сообщит, что тест соединения пройден успешно. После этого нажмите ОК в окне Test Result и повторно — в окне настройки драйвера.

![После этого нажмите ОК в окне Test Result и повторно — в окне настройки драйвера.](../images/kak-svyazat-microsoft-power-bi-i-google-bigquery-posle-etogo-bbfaec7b.webp)

3. Перейдите в Power BI и настройте подключение к созданному источнику данных.

3.1. На вкладке «Главная» основного меню Power BI нажмите «Получить данные», а в группе «Другое» выберите пункт ODBC.

![На вкладке «Главная» основного меню Power BI нажмите «Получить данные», а в группе «Другое» выберите пункт ODBC](../images/kak-svyazat-microsoft-power-bi-i-google-bigquery-na-vkladke-7c3d1485.webp)

3.2. В выпадающем списке «Имя источника данных (DSN)» выберите созданный в пункте 2 источник. В данном случае я его назвал BQ ODBC.

![В выпадающем списке «Имя источника данных (DSN)» выберите созданный в пункте 2 источник](../images/kak-svyazat-microsoft-power-bi-i-google-bigquery-v-vypadause-3318c2e9.webp)

3.3. В окне «Драйвер ODBC» выберите тип подключения «По умолчанию или пользовательский» и нажмите «Подключение».

![В окне «Драйвер ODBC» выберите тип подключения «По умолчанию или пользовательский» и нажмите «Подключение»](../images/kak-svyazat-microsoft-power-bi-i-google-bigquery-v-okne-draj-6a31356b.webp)

3.4. В окне «Навигатор» выбирайте нужные проекты, наборы данных и таблицы. Нажмите «Загрузить», после этого данные из Google BigQuery будут загружены в Power BI.

![В окне «Навигатор» выбирайте нужные проекты, наборы данных и таблицы. Нажмите «Загрузить», после этого данные из Google BigQuery будут загружены в Power BI](../images/kak-svyazat-microsoft-power-bi-i-google-bigquery-v-okne-navi-55e132ff.webp)

## Как связать Google BigQuery и Microsoft Power BI с помощью R коннектора?

В марте 2016 года [Microsoft объявил](https://powerbi.microsoft.com/en-us/blog/power-bi-desktop-march-update-feature-summary/), что поддержка R-скриптов для загрузки данных в Power BI вышла из бета-тестирования. Безусловно, это одно из наиболее значимых обновлений Power BI, так как с помощью языка R можно подгружать данные практически из любого источника, включая Google BigQuery.

### 1. Установите пакет «bigrquery»

1.1. Первое, что необходимо сделать, — скачать и установить [последнюю версию R](https://cran.r-project.org/bin/windows/base/). При установке не требуется задавать какие-то дополнительные параметры или настройки, в связи с чем затруднений возникнуть не должно.

1.2. Для более удобной работы Google BigQuery из R установите пакет «bigrquery». Для этого перейдите в папку «C:\Program Files\R\R-3.3.0\bin» и запустите файл «R.exe». Далее откроется консоль для работы с R.

![Установите пакет «bigrquery»](../images/kak-svyazat-microsoft-power-bi-i-google-bigquery-ustanovite-75c2112f.webp)  
В консоли установите нужный пакет с помощью команды «install.packages(“bigrquery”)».

![Установите нужный пакет с помощью команды «install.packages(](../images/kak-svyazat-microsoft-power-bi-i-google-bigquery-ustanovite-bd617118.webp)

1.3. На диске C создайте папку «BQ\_Integration», в ней мы будем сохранять учетные данные для доступа к API Google BigQuery.

![Создайте папку «BQ_Integration»](../images/kak-svyazat-microsoft-power-bi-i-google-bigquery-sozdajte-pa-1c85e64c.webp)

1.4. Далее в консоли R с помощью команды «setwd(“C:/BQ\_Integration”)» укажите, что созданную папку будем использовать в качестве рабочей директории. Если вы все сделали правильно, можете проверить установленную рабочую директорию с помощью команды «getwd()».

![Проверить установленную рабочую директорию ](../images/kak-svyazat-microsoft-power-bi-i-google-bigquery-proverit-us-458a323d.webp)

1.5. Далее подключаем пакет «bigrquery», установленный ранее с помощью «library(bigrquery)».

### 2. Предоставьте доступ к данным BigQuery

2.1. Для прохождения первой аутентификации запустите запрос к любой таблице BigQuery из консоли. Для этого воспользуйтесь следующим кодом:

```markup
projectID <- "XXXXXXX"  #Название проекта, получить его можно из URL
dataSetID <- "XXXXXXX" #Название набора данных, смотреть в интерфейсе BigQuery
tableID
```

2.2. Далее в консоли на вопрос «Use a local file .httr-oauth to cache OAuth access credentials between R sessions?» ответьте «Yes». К этому моменту в консоли должен быть следующий код:

![Предоставьте доступ к данным BigQuery](../images/kak-svyazat-microsoft-power-bi-i-google-bigquery-predostavte-2e5f3ea5.webp)

2.3. Далее выберите аккаунт Google и подтвердите разрешение на просмотр данных и управление ими в Google BigQuery, а также просмотр и изменение данных в сервисах Google облачной платформы.

![Выберите аккаунт Google](../images/kak-svyazat-microsoft-power-bi-i-google-bigquery-vyberite-ak-1844596a.webp)

![подтвердите разрешение на просмотр данных и управление ими в Google BigQuery](../images/kak-svyazat-microsoft-power-bi-i-google-bigquery-podtverdite-2d75d2ca.webp)

2.4. После этого вы получите подтверждение, что аутентификация прошла удачно.  
![аутентификация прошла удачно](../images/kak-svyazat-microsoft-power-bi-i-google-bigquery-autentifika-5a1765df.webp)

![Получите подтверждение](../images/kak-svyazat-microsoft-power-bi-i-google-bigquery-polucite-po-d4326d87.webp)

2.5. На этом этапе работа с консолью R завершена. В папке «BQ\_Integration», созданной на шаге 3, должен появится файл «.httr-oauth», который содержит ваши учётные данные.

### 3. Интеграция с Power BI

3.1. Перейдите в интерфейс Power BI и нажмите кнопку для получения данных. В группе «Другое» выберите коннектор «R-скрипт».

Скачать бесплатно последнюю версию Power BI можно по этой [ссылке](https://powerbi.microsoft.com/en-us/downloads/).

![Нажмите кнопку для получения данных](../images/kak-svyazat-microsoft-power-bi-i-google-bigquery-nazmite-kno-f50a2cca.webp)

3.2. Далее появится диалоговое окно «Выполнение сценария R». Подставьте в следующий код свои значения ID проекта, набора данных и [таблицы](https://netpeak.net/ru/blog/kak-obrabatyvat-dannie-iz-mnozhestva-tablits-v-google-bigquery/) и введите его в диалоговое окно.

```markup
library(bigrquery)
setwd("C:/BQ_Integration")
projectID <- "XXXXXXX"
dataSetID <- "XXXXXXXXX"
tableID <- "XXXXXXXX"

qry
```

![Выполнение сценария R](../images/kak-svyazat-microsoft-power-bi-i-google-bigquery-vypolnenie-6dea495b.webp)

Если вы знакомы с SQL, то в кавычках вместо «qry

Как работать с оконными функциями в Google BigQuery — подробное руководство

Читайте [об оконных функциях](https://netpeak.net/ru/blog/kak-rabotat-s-okonnymi-funktsiyami-v-google-bigquery-podrobnoe-rukovodstvo/)и принципах их работы в Google BigQuery.

3.3. По нажатию кнопки «ОК» начнется процесс загрузки данных, после чего появится окно «Навигатор» с загруженной таблицей и ее полями.

![окно «Навигатор» с загруженной таблицей и ее полями](../images/kak-svyazat-microsoft-power-bi-i-google-bigquery-okno-naviga-2edbc9b8.webp)

3.4. После нажатия кнопки «Загрузить», вы сможете строить визуализацию данных на основе загруженной таблицы в Microsoft Power BI.  
Данные будут обновляться каждый раз при нажатии кнопки «Обновить».

![Данные будут обновляться каждый раз при нажатии кнопки «Обновить»](../images/kak-svyazat-microsoft-power-bi-i-google-bigquery-dannye-budu-3e08adcd.webp)

Как работать с Microsoft Power BI — подробное руководство

Подробно узнать методы построения визуализации на основе загруженных в Power BI данных можно в статье [«Как работать с Microsoft Power BI — подробное руководство».](https://netpeak.net/ru/blog/kak-rabotat-s-microsoft-power-bi-podrobnoe-rukovodstvo/)

## Выводы

Три шага для связки Microsoft Power BI и Google BigQuery с помощью ODBC драйвера:

1. Скачайте и установите ODBC драйвер.
2. Создайте источник данных ODBC.
3. Перейдите в Power BI и настройте подключение к созданному источнику данных.

Три шага для связки Microsoft Power BI и Google BigQuery с помощью R коннектора:

1. Установить язык R и подключить пакет «bigrquery».
2. Предоставить доступ к данным BigQuery.
3. Загрузить данные в Power BI и построить визуализацию.

В следующих постах поделюсь фишками загрузки данных в Power BI из других источников, к которым нет встроенных коннекторов.

---

*[Оригинал публикации на блоге Netpeak.](https://netpeak.net/ru/blog/kak-svyazat-microsoft-power-bi-i-google-bigquery/)*
