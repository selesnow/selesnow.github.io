---
title: Как связать Яндекс.Директ с Microsoft Power BI.
date: '2017-02-27'
slug: kak-svyazat-yandeks-direkt-s-microsoft-power-bi
tags:
- API
- Яндекс Директ
- BI
- Автоматизация
- Импорт данных
- Power BI
- PPC
- R
categories:
- BI
- Яндекс
- Реклама
description: Яндекс.Директ собирает много данных, но, к сожалению, в веб-интерфейсе доступно очень мало информации для анализа. В этой статье я подробно опишу, как получить статистику о рекламных кампаниях c помощью языка R для визуализации в Power BI.
original_url: https://alexeyseleznev.wordpress.com/2017/02/27/%d0%ba%d0%b0%d0%ba-%d1%81%d0%b2%d1%8f%d0%b7%d0%b0%d1%82%d1%8c-%d1%8f%d0%bd%d0%b4%d0%b5%d0%ba%d1%81-%d0%b4%d0%b8%d1%80%d0%b5%d0%ba%d1%82-%d1%81-microsoft-power-bi/
wp_id: 694
draft: false
---

Яндекс. Директ собирает много данных, но, к сожалению, в веб-интерфейсе доступно очень мало информации для анализа. В этой статье я подробно опишу, как получить статистику о рекламных кампаниях c помощью языка R для визуализации в Power BI.

![Картинки по запросу connect](https://i0.wp.com/kingofwallpapers.com/connect/connect-002.jpg)

[Microsoft Power BI](https://netpeak.net/ru/blog/kak-rabotat-s-microsoft-power-bi-podrobnoe-rukovodstvo/) — один из лидеров BI-индустрии. Бесплатной базовой версии вполне достаточно для решения большинства задач, благодаря этому инструмент довольно быстро стал очень популярным среди аналитиков и маркетологов.

## 1. Установите язык R и необходимые пакеты функций

1.1. Скачайте и установите [актуальную версию R](https://cran.r-project.org/bin/windows/base/), а также интегрированную среду разработки [R Studio](https://www.rstudio.com/products/rstudio/download/#download), в которой вам будет удобнее работать.

1.2. В R Studio откройте все доступные панели с помощью сочетания клавиш Ctrl+Alt+Shift+0. В область Source вставьте код.

```markup

```

```

if(!"devtools" %in% installed.packages()[,1]){install.packages("devtools")}
library(devtools)
install_github('selesnow/ryandexdirect')
```

```markup

```

Чтобы запустить процесс установки пакетов, выделите код с помощью мыши и запустите его нажатием Ctrl+Enter.

![Установите язык R и необходимые пакеты функций](../images/kak-svyazat-yandeks-direkt-s-microsoft-power-bi-ustanovite-a-3bad2fbf.webp)

## 2. Получите токен доступа к API Яндекс. Директ

2.1. Для получения токена доступа к API Директа воспользуйтесь кодом:

```markup

```

```

library(ryandexdirect)
ya_token <- ya_token <- yadirGetToken()
```

```markup

```

Для запуска также необходимо вставить код в область «Source» в R Studio, выделить с помощью мыши и запустить сочетанием клавиш Ctrl+Enter.

2.2. В открывшемся окне браузера предоставьте пакету «ryandexdirect» доступ к данным — нажмите кнопку «Разрешить». После этого откроется страница со сгенерированным токеном доступа к API.

![Получите токен доступа к API Яндекс. Директ](../images/kak-svyazat-yandeks-direkt-s-microsoft-power-bi-polucite-tok-96dce157.webp)

Токен доступа еще понадобится, поэтому скопируйте его в любой текстовый документ и смело можете закрывать R Studio.

## 3. Загрузите данные в Microsoft Power BI

Чтобы обрабатывать данные из Яндекс. Директ в Power BI, необходимо настроить импорт. Рассмотрим два способа настройки: с помощью сценария на языке R и готового документа Power BI .

### 3.1. С помощью сценария на языке R

3.1.1. Откройте [Power BI](https://powerbi.microsoft.com/en-us/), нажмите «Получить данные» и выберите коннектор R-скрипт.

В диалоговое окно «Выполнить сценарий R» вставьте следующий код:

```markup

```

```

#Подключаем пакет
library(ryandexdirect)

#Получаем список кампаний
campList <- yadirGetCampaignList(logins = "<span class="token tag"><span class="token tag"><span class="token punctuation"><</span>ВАШ</span> <span class="token attr-name">ЛОГИН</span> <span class="token attr-name">НА</span> <span class="token attr-name">ЯНДЕКСЕ</span><span class="token punctuation">></span></span>", token = "<span class="token tag"><span class="token tag"><span class="token punctuation"><</span>ВАШ</span> <span class="token attr-name">ТОКЕН</span> <span class="token attr-name">В</span> <span class="token attr-name">ВИДЕ</span> <span class="token attr-name">СТОКИ</span><span class="token punctuation">></span></span>")

#Получаем статистику по кампаниям
Stat <- yadirGetSummaryStat(campaignIDS = campList$Id,
                           dateStart = Sys.Date() - 90,
                           dateEnd = Sys.Date(),
                           token = "<span class="token tag"><span class="token tag"><span class="token punctuation"><</span>ВАШ</span> <span class="token attr-name">ТОКЕН</span> <span class="token attr-name">В</span> <span class="token attr-name">ВИДЕ</span> <span class="token attr-name">СТОКИ</span><span class="token punctuation">></span></span>")
```

```markup

```

В код подставьте ваш логин Яндекс. Директ и токен доступа к API, полученный на втором шаге. Значения необходимо в кавычках.

![С помощью сценария на языке R](../images/kak-svyazat-yandeks-direkt-s-microsoft-power-bi-31-s-pomosu-7db5cc2b.webp)

3.1.2. Нажмите «ОК», и начнется процесс загрузки данных.

![начнется процесс загрузки данных](../images/kak-svyazat-yandeks-direkt-s-microsoft-power-bi-nacnetsa-pro-512b0885.webp)

В результате получите в Power BI две таблицы:

- **campList** — со списком рекламных кампаний;
- **Stat** — со статистикой по кампаниям.

Все денежные данные будут возвращены в условных единицах Яндекса. Текущий курс всегда можете найти [в справке](https://tech.yandex.ru/direct/doc/dg-v4/concepts/multicurrency_const-docpage/#currency-rates).

![денежные данные будут возвращены в условных единицах](../images/kak-svyazat-yandeks-direkt-s-microsoft-power-bi-deneznye-dan-73383332.webp)

3.1.3. Связь между таблицами можете настроить непосредственно в Power BI по полям **Id** из таблицы campList и **CampaignID** из таблицы Stat.

![По полям Id из таблицы campList](../images/kak-svyazat-yandeks-direkt-s-microsoft-power-bi-po-polam-id-1f3996e2.webp)

### 3.2. С помощью файла Power BI с коннектором к Яндекс. Директ

Второй способ более простой, потому что я уже создал документ Power BI и настроил отправку запроса к Яндекс. Директ через пользовательские параметры.

3.2.1. Скачайте [файл с коннектором](https://drive.google.com/file/d/0B1rgddqnM9XJb2xFVGxrb2JRczg/view?usp=sharing). В интерфейсе Power BI откройте выпадающее меню «Изменить запросы» и выберите команду «Изменить параметры».

![выбираем команду «Изменить параметры»](../images/kak-svyazat-yandeks-direkt-s-microsoft-power-bi-vybiraem-kom-72accb07.webp)

3.2.2. Введите свой логин в Яндексе и API-токен, полученный на втором шаге. Нажмите «ОК».

![Введите полученный логин](../images/kak-svyazat-yandeks-direkt-s-microsoft-power-bi-vvedite-polu-497cb573.webp)

## Выводы

На основе данных, импортированных из Яндекс. Директ в Microsoft Power BI, сможете создавать понятные отчеты и обновлять их в режиме реального времени. Подытожим основные шаги:

1. Установите актуальную версию языка R и R Studio. Инсталлируйте пакет «devtools» и «ryandexdirect».
2. Получите токен доступа к API Яндекс. Директ и сохраните его.
3. Загрузите данные в Power BI:
   - с помощью сценария на языке R;
   - с помощью документа Power BI с коннектором к Яндекс. Директ.

На этом все. Если у вас что-либо не получится — пишите комментарии, постараюсь помочь.

---

[Оригинал публикации на блоге Netpeak](https://netpeak.net/ru/blog/kak-svyazat-yandeks-direkt-s-microsoft-power-bi/)
