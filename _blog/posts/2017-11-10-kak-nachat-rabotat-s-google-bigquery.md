---
title: Как начать работать с Google BigQuery
date: '2017-11-10'
slug: kak-nachat-rabotat-s-google-bigquery
tags:
- BigQuery
- Базы данных
- Обработка данных
- R
categories:
- Базы данных
description: Ранее я публиковал цикл материалов о работе с Google BigQuery. В этой статье расскажу о преимуществах и особенностях сервиса, а также о дополнительных инструментах для BigQuery. Google BigQuery — это облачная база данных с высочайшей скоростью обработки огромных массивов данных.
original_url: https://alexeyseleznev.wordpress.com/2017/11/10/%d0%ba%d0%b0%d0%ba-%d0%bd%d0%b0%d1%87%d0%b0%d1%82%d1%8c-%d1%80%d0%b0%d0%b1%d0%be%d1%82%d0%b0%d1%82%d1%8c-%d1%81-google-bigquery/
wp_id: 1053
draft: false
cover: ../images/covers/1053.webp
cover_generated: true
---

Ранее я публиковал цикл материалов о работе с Google BigQuery. В этой статье расскажу о преимуществах и особенностях сервиса, а также о дополнительных инструментах для BigQuery.

Google BigQuery — это облачная база данных с высочайшей скоростью обработки огромных массивов данных.

![Картинки по запросу картинки](https://i0.wp.com/minionomaniya.ru/wp-content/uploads/2016/01/miniony_kartinki_na_rabochi_stol_1920x1080.jpg)

## Как начать работу в Google BigQuery

Войдите в [Google Cloud Platform](https://console.cloud.google.com/?hl=ru). При первом запуске система предложит активировать бесплатный пробный период и получить кредит $300 на 12 месяцев. Честно говоря, чтобы потратить за год в BigQuery эту сумму, вам придется очень сильно постараться.

![Как активировать бесплатный пробный период BigQuery](../images/kak-nachat-rabotat-s-google-bigquery-kak-aktivirovat-besplat-adc18564.webp)

Для дальнейшей работы введите платежные данные.

![Как получить бесплатный триал в BigQuery](../images/kak-nachat-rabotat-s-google-bigquery-kak-polucit-besplatnyj-b3026c6e.webp)

Нажмите «Выбрать проект».

![Как выбрать проект в BigQuery](../images/kak-nachat-rabotat-s-google-bigquery-kak-sozdat-proekt-v-big-cdc7aced.webp)

Затем — «Создать проект».

![Как создать проект в BigQuery](../images/kak-nachat-rabotat-s-google-bigquery-s-cego-nacat-rabotu-v-b-8a18f751.webp)

Примите условия использования платформы.

![Условия использования BigQuery](../images/kak-nachat-rabotat-s-google-bigquery-uslovia-ispolzovania-bi-019369f4.webp)

Наконец назовите проект, задайте настройки уведомлений и еще раз согласитесь с условиями использования платформы.

![Как задать настройки уведомлений для BigQuery](../images/kak-nachat-rabotat-s-google-bigquery-kak-zadat-nastrojki-uve-ead16ff3.webp)

После подтверждения подождите несколько минут.

![Как создать свой первый проект в сервисе BigQuery](../images/kak-nachat-rabotat-s-google-bigquery-kak-sozdat-svoj-pervyj-321a4d21.webp)

Вскоре вы получите оповещение, что проект создан.

![Настройки оповещений при начале работы с BigQuery](../images/kak-nachat-rabotat-s-google-bigquery-nastrojki-opovesenij-pr-ecc4d119.webp)

Перейдите в раздел оплаты и привяжите платежный аккаунт.

![Как привязать платежный аккаунт BigQuery](../images/kak-nachat-rabotat-s-google-bigquery-kak-privazat-plateznyj-8868cd82.webp)

![Как правильно выбрать привязку платежного аккаунта BigQuery](../images/kak-nachat-rabotat-s-google-bigquery-kak-pravilno-vybrat-pri-eff94e64.webp)

Теперь проект привязан к только что созданному платежному аккаунту.

![Привязать проект к новому созданному аккаунту в BigQuery](../images/kak-nachat-rabotat-s-google-bigquery-privazat-proekt-k-novom-998dc7e5.webp)

Перейдите в [интерфейс Google BigQuery](https://bigquery.cloud.google.com/welcom) и напишите свой первый запрос.

Чтобы открыть редактор запросов, нажмите «Compose query» или сочетание клавиш «Ctrl + Space».

![Как написать запрос в BigQuery](../images/kak-nachat-rabotat-s-google-bigquery-kak-napisat-zapros-v-bi-7efb4330.webp)

Рассмотрим, как написать первый запрос на примере публичных данных в BigQuery. Возьмите первые 15 строк из таблицы project\_tycho\_reports, которая находится в наборе публичных данных lookerdata.

```markup
SELECT *
FROM [lookerdata:cdc.project_tycho_reports]
LIMIT 25
```

Запрос вернет результат:

![Как написать запрос на примере публичных данных в BigQuery](../images/kak-nachat-rabotat-s-google-bigquery-kak-napisat-zapros-na-p-67c3217a.webp)

Ранее я описывал самые простые [способы для загрузки собственных данных в Google BigQuery](https://netpeak.net/ru/blog/kak-nachat-rabotu-s-bigdata-zagruzhaem-dannie-v-google-bigquery/), а в этой статье далее расскажу, как загрузить данные с помощью языка R.

## Преимущества Google BigQuery

Скорость — это основное преимущество BigQuery, но не единственное. BigQuery — облачный сервис. При его использовании не понадобится арендовать сервер и оплачивать поддержку.

Стоимость BigQuery значительно ниже стоимости аренды самого примитивного сервера: даже если вы очень постараетесь и будете ежедневно записывать в эту базу данных миллионы строк, все равно вряд ли сможете потратить более $5.

Следующее преимущество — простота использования. В любой другой системе управления базами данных (СУБД) помимо знания SQL придется долго разбираться с тонкостями администрирования и настройками базы.

И если сам по себе SQL-диалект во всех базах данных очень похожий, то административная часть, как правило, везде устроена по-разному.

У BigQuery всю административную часть на себя взял Google. В этом сервисе нет никаких настроек, индексов, движков таблиц, тайм-аутов или внешних ключей. Реализована поддержка только одной кодировки UTF-8.

Для работы с BigQuery достаточно знать, как загрузить данные в BigQuery, и иметь базовые знания в SQL.

Несмотря на простоту, в BigQuery реализована поддержка практически всех функций СУБД:

- [оконные функции](https://netpeak.net/ru/blog/kak-rabotat-s-okonnymi-funktsiyami-v-google-bigquery-podrobnoe-rukovodstvo/);
- хранение данных в виде структур (нереляционные возможности);
- представления и табличные выражения (common table expression).

Правда, на момент публикации статьи сервис не поддерживает:

- рекурсивные запросы;
- создание хранимых процедур и функций;
- транзакции.

## Особенности SQL для Google BigQuery

BigQuery умеет переключаться между стандартным SQL и своим диалектами. Между ними также есть разница.

DML-операции INSERT, UPDATE и DELETE на данный момент поддерживаются только при использовании стандартного SQL.

Еще одно отличие между этими диалектами — способ вертикального объединения таблиц. В стандартном SQL для этого служит оператор UNION и ключевое слов ALL или DISTINCT:

```markup
SELECT 12 AS A, 32 AS B
UNION ALL
SELECT 2 AS A, 29 AS B
```

В собственном SQL-диалекте функционал для вертикального объединения таблиц значительно шире. Существует специальный набор функций подстановки таблиц ([Table Wildcard Functions](https://cloud.google.com/bigquery/docs/reference/legacy-sql#tablewildcardfunctions)).

Как обрабатывать данные из множества таблиц в Google BigQuery

Этот [способ объединения таблиц](https://netpeak.net/ru/blog/kak-obrabatyvat-dannie-iz-mnozhestva-tablits-v-google-bigquery/) я уже подробно описывал ранее.

Для простого объединения достаточно просто перечислить названия нужных таблиц или подзапросы через запятую. Объединение запросов из примера выше на внутреннем диалекте SQL в BigQuery будет выглядеть так:

```markup
SELECT *
FROM (SELECT 12 AS A, 32 AS B), (SELECT 2 AS A, 29 AS B)
```

Переключатель между SQL-диалектами в BigQuery находится в интерфейсе в блоке опций: нажмите кнопку Show options под редактором запросов.

![Переключаться между SQL диалектами в интерфейсе BigQuery](../images/kak-nachat-rabotat-s-google-bigquery-pereklucatsa-mezdu-sql-9c369505.webp)

С помощью галочки «SQL Dialect» переключитесь на нужный диалект.

![Как найти галочку «SQL Dialect» для переключения на нужный диалект](../images/kak-nachat-rabotat-s-google-bigquery-kak-najti-galocku-sql-d-35a058b7.webp)

## Инструменты для работы с BigQuery

Мы уже разобрались, как загружать данные в базу и как обращаться к данным SQL запросами. Но вряд ли вы хотите взаимодействовать с данными, ограничившись этими возможностями. Скорее всего, вы загружаете данные для построения дашбордов или чего-то подобного.

Как получить данные в различных BI платформах, я писал в статьях об интеграции с [электронными таблицами](https://netpeak.net/ru/blog/integratsiya-google-bigquery-c-bi-platformami-i-elektronnymi-tablitsami/) и [Microsoft Power BI.](https://netpeak.net/ru/blog/kak-svyazat-microsoft-power-bi-i-google-bigquery/)

Microsoft Power BI, как и большинство популярных  BI-систем и электронных таблиц, с июля 2017 года поддерживает интеграцию с Google BigQuery из коробки. У коннектора довольно скудные возможности: он не умеет обращаться к сохраненным представлениям или отправлять в BigQuery запросы. Пока что с помощью встроенного коннектора можно вытягивать только плоские таблицы.

### Simba Drivers

Если вам необходимо получить данные из Google BigQuery в электронной таблице или BI-системе, которая из коробки не поддерживает интеграцию, воспользуйтесь бесплатным [Simba Drivers](https://cloud.google.com/bigquery/partners/simba-drivers/).

Этот драйвер поддерживает все необходимые возможности, включая переключения SQL-диалектов. Подробности настройки ищите в моей статье о связке Microsoft Power BI и Google BigQuery.

### Язык R

Язык R — один из самых мощных инструментов для работы с данными. Он умеет как получать данные из Google BigQuery, так и записывать их. Для этого удобнее всего пакет [bigrquery](https://github.com/r-dbi/bigrquery).

Для начала [установите](https://cran.r-project.org/bin/windows/base/) язык R. Также для удобства работы с R я рекомендую [установить](https://www.rstudio.com/products/rstudio/download/) интегрированную среду разработки RStudio.

Запустите RStudio и с помощью сочетания клавиш «Ctrl + Alt + Shift + 0» откройте все доступные в ней панели. Чаще всего понадобятся панели Source и Console.

![Как запустить в RStudio панели Source и Console](../images/kak-nachat-rabotat-s-google-bigquery-kak-zapustit-v-rstudio-15b4a00c.webp)

Для установки develop-версии пакета bigrquery из репозитория на GitHub предварительно установите пакет devtools. Введите в окно Source код, затем выделите его (зажмите левой кнопки мыши) и нажмите «Ctrl + Enter» для выполнения команды:

```markup
install.packages("devtools")
```

Теперь установите пакет bigrquery:

```markup
devtools::install_github("rstats-db/bigrquery")
```

Чтобы в R были доступны функции пакета, после установки подключите их с помощью команды library или require. Например, подключим пакет bigrquery с помощью кода:

```markup
library(bigrquery)
```

Структура данных в Google BigQuery состоит из проекта с набором данных, содержащим таблицы. Проект вы уже создали, а теперь для передачи информации создайте набор данных. Выберите в интерфейсе из выпадающего меню «Create new dataset».

![BigQuery проект с набором данных, содержащим таблицы](../images/kak-nachat-rabotat-s-google-bigquery-bigquery-proekt-s-nabor-a1ea0460.webp)

Чтобы создать набор данных с помощью языка R, воспользуйтесь командой insert\_dataset. Команда требует всего 2 аргумента:

**project** — ID проекта (возьмите из URL в BigQuery).  
![Чтобы создать набор данных с помощью языка R, воспользуйтесь командой insert_dataset](../images/kak-nachat-rabotat-s-google-bigquery-ctoby-sozdat-nabor-dann-caf0e098.webp)

**dataset** — название нового набора данных.

Давайте создадим первый набор данных с названием myFirstDataSet. Введите в область Source приведенный ниже код, выделите команду с помощью мыши и нажмите «Ctrl+Enter» для выполнения.

```markup
insert_dataset(project = "myfirstproject-185308", dataset = "myFirstDataSet")
```

В окне Console в RStudio появится запрос о создании учетных данных, чтобы в дальнейшем не требовалась повторная аутентификация.

![Окно Console в RStudio, запрос о создании учетных данных](../images/kak-nachat-rabotat-s-google-bigquery-okno-console-v-rstudio-8f739e2e.webp)

Введите на запрос Selection в Console ответ Yes и нажмите Enter. Откроется браузер — разрешите доступ к данным и получите авторизационный код.

![Как на апрос Selection в Console разрешить доступа к данным и получить авторизационный код](../images/kak-nachat-rabotat-s-google-bigquery-kak-na-apros-selection-e785675f.webp)

![Авторизационный код в Bigquery](../images/kak-nachat-rabotat-s-google-bigquery-avtorizacionnyj-kod-v-b-aa1567c5.webp)

![Как сгенерированный код вставить в Console RStudio в ответ на запрос авторизационного кода](../images/kak-nachat-rabotat-s-google-bigquery-kak-sgenerirovannyj-kod-dc62e0b0.webp)

Скопируйте сгенерированный код. Затем вставьте его в Console RStudio в ответ на запрос авторизационного кода и нажмите Enter.

Отлично, вы создали набор данных.

![BigQuery и увидеть созданный dataset](../images/kak-nachat-rabotat-s-google-bigquery-bigquery-kak-uvidet-soz-b48c64d9.webp)

Теперь запишите встроенную в R таблицу mtcars в набор данных myFirstDataSet. Для передачи данных из R в BigQuery в пакете bigrquery есть функция insert\_upload\_job. Она принимает такие аргументы:

**project** — ID проекта (смотрите либо в URL проекта, либо в режиме переключения проектов).  
![Для передачи данных из R в BigQuery функция insert_upload_job](../images/kak-nachat-rabotat-s-google-bigquery-dla-peredaci-dannyh-iz-8097fee7.webp)

**dataset** — название набора данных, куда вы планируете отправить данные. В нашем случае myFirstDataSet.

**table** — название таблицы с записанными данными.

**values** — data frame (таблица данных) в R с данными для передачи в BigQuery.

**billing** = project аккаунта для оплаты операции. По умолчанию — платежный аккаунт, который привязан к проекту.

**create\_disposition** — опция для определения необходимых действий.  
Если в BigQuery нет таблицы с заданным в аргументе table названием, укажите “CREATE\_IF\_NEEDED” — система создаст новую таблицу.  
Если указать “CREATE\_NEVER” и таблица с заданным именем не найдется в наборе данных, будет возвращена соответствующая ошибка.

**write\_disposition** — опция для выбора добавления данных в существующую таблицу.  
“WRITE\_APPEND” — дописать данные в таблицу.  
“WRITE\_TRUNCATE” — перезаписать данные в таблице.  
“WRITE\_EMPTY” — записать данные для пустой таблицы.

Код для передачи в BigQuery встроенной в R таблицы mtcars:

```markup
insert_upload_job(project = "myfirstproject-185308",
                 dataset = "myFirstDataSet",
                 table = "mtcars_bigquery",
                 values = mtcars,
                 create_disposition = "CREATE_IF_NEEDED",
                 write_disposition = "WRITE_APPEND")
```

При успешном выполнении операции в консоли R появится дополнительная информация, а в интерфейсе BigQuery — созданная таблица mtcars\_bigquery.

![BigQuery таблица mtcars_bigquery](../images/kak-nachat-rabotat-s-google-bigquery-bigquery-tablica-mtcars-eba405b0.webp)

Для запроса данных из BigQuery в R в пакете bigrquery предназначена функция query\_exec. Основные аргументы:

**query** — текст SQL-запроса, результат которого вы хотите загрузить в R.

**project** — ID проекта для запроса данных.

**page\_size** — максимальный размер возвращаемого результата в строках (по умолчанию 10000).

**max\_pages** — максимальное количество страниц возврата запросом (по умолчанию 10).

**use\_legacy\_sql** — выбор SQL-диалекта для обработки запроса.  
По умолчанию задано значение TRUE с внутренним диалектом BigQuery.  
Для стандартного диалекта SQL задайте в этом аргументе значение FALSE.

Для обратного запроса данных, которые вы отправили в BigQuery в прошлом шаге, задайте команду:

```markup
bq_mtcars_table <- query_exec(query = "SELECT * FROM myFirstDataSet.mtcars_bigquery",
                             project = "myfirstproject-185308",
                             use_legacy_sql = TRUE)
```

В рабочем окружении (описание которого вы видите в окне Environment) появится новый объект bq\_mtcars\_table.

![Bigquery объект bq_mtcars_table](../images/kak-nachat-rabotat-s-google-bigquery-bigquery-obekt-bqmtcars-d8b1e623.webp)

## Выводы

Google BigQuery — простой в работе и в то же время мощнейший инструмент для хранения и обработки данных. Это облачная база данных с поддержкой большинства функций СУБД.

Сервис обходится значительно дешевле содержания, поддержки и администрирования сервера для бесплатных баз данных (MySQL или PostgreSQL).

Надеюсь, мой цикл инструкций для начала работы с Google BigQuery упростит ваши будни.

Успехов в работе с большими данными!

---

[Оригинал публикации в блоге Netpeak.](https://netpeak.net/ru/blog/google-bigquery-podrobnyy-obzor-funktsii/)
