---
title: Как работать с закладками (bookmarks) в Power BI — подробное руководство
date: '2017-12-28'
slug: kak-rabotat-s-zakladkami-bookmarks-v-power-bi-podrobnoe-rukovodstvo
tags:
- BI
- Power BI
- Визуализация данных
categories:
- BI
- Визуализация данных
description: Недавно вышла очередная, ежемесячная порция обновлений Power BI Desktop. Разработчики добавили множество новых функций и значительно доработали «Закладки» (Bookmarks), с помощью которых можно сделать дашборды более компактными и интерактивными. Создатели Power BI даже устроили конкурс Bookmark Report Contest на лучшее использование свежей фичи (проходит с 12 по 27 декабря). В этой статье я покажу пример использования закладок и […]
original_url: https://alexeyseleznev.wordpress.com/2017/12/28/%d0%ba%d0%b0%d0%ba-%d1%80%d0%b0%d0%b1%d0%be%d1%82%d0%b0%d1%82%d1%8c-%d1%81-%d0%b7%d0%b0%d0%ba%d0%bb%d0%b0%d0%b4%d0%ba%d0%b0%d0%bc%d0%b8-bookmarks-%d0%b2-power-bi-%d0%bf%d0%be%d0%b4%d1%80/
wp_id: 1082
draft: false
cover: ../images/covers/1082.webp
cover_generated: true
---

Недавно вышла очередная, ежемесячная порция [обновлений Power BI Desktop](https://powerbi.microsoft.com/en-us/blog/power-bi-desktop-december-feature-summary/#bookmarkFlexibility). Разработчики добавили множество новых функций и значительно доработали «Закладки» (Bookmarks), с помощью которых можно сделать дашборды более компактными и интерактивными. Создатели Power BI даже устроили конкурс [Bookmark Report Contest](https://powerbi.microsoft.com/en-us/blog/bookmarking-contest-dec-12th-dec-27th/) на лучшее использование свежей фичи (проходит с 12 по 27 декабря).

В этой статье я покажу пример использования закладок и пошагово разберу процесс их создания и применения для удобства визуализации данных.

## Как включить возможность работы с закладками в Power BI

Так как функция bookmarks пока что находится на стадии тестирования, для её включения необходимо перейти в меню «Файл» — «Опции и настройки» — «Опции»:

![«Файл» — «Опции и настройки» — «Опции»](../images/kak-rabotat-s-zakladkami-bookmarks-v-power-bi-podr-fajl-opci-4a047fba.webp)

В окне опций перейдите на вкладку подключения предварительных функций и поставьте галочку напротив пункта «Закладки»:

![В окне опций перейдите на вкладку подключения предварительных функций и поставьте галочку напротив пункта «Закладки»](../images/kak-rabotat-s-zakladkami-bookmarks-v-power-bi-podr-v-okne-op-05c0c214.webp)

Далее в основном меню Power BI переходим на вкладку «View» («Вид») и ставим галочку напротив «Bookmarks Pane» («Панель закладок»):

![Далее в основном меню Power BI переходим на вкладку «View» и ставим галочку напротив «Bookmarks Pane» («Панель закладок»)](../images/kak-rabotat-s-zakladkami-bookmarks-v-power-bi-podr-dalee-v-o-3fbfd97f.webp)

После этого к привычным панелям «Visualization» и «Fields», добавится «Bookmarks»:

![После этого к привычным панелям «Visualization» и «Fields», добавится «Bookmarks»](../images/kak-rabotat-s-zakladkami-bookmarks-v-power-bi-podr-posle-eto-8797ce64.webp)

## Как использовать закладки в Power BI

Закладки позволяют сохранить состояние дашборда, запоминая заданные в любой момент времени фильтры и добавленные на страницу визуальные элементы. А я еще использую закладки для переключения между визуальными элементами. В других источниках не встречал этот метод, поэтому опишу его подробно.

С помощью закладок можно переключаться:

1. Между параметрами таблиц, в данном случае Source/Medium:

![Между параметрами таблиц](../images/kak-rabotat-s-zakladkami-bookmarks-v-power-bi-podr-mezdu-par-2ba6d3ab.gif)

2. Между типами визуальных элементов (таблица/график):

![таблица-график](../images/kak-rabotat-s-zakladkami-bookmarks-v-power-bi-podr-tablica-g-47fbec96.gif)

## Как создать переключатель «таблица-график» с помощью закладок

Давайте по шагам разберем пример построения переключателя из табличного отображения информации в график.

Я подгрузил в BI таблицу с вымышленными данными о заказах и добавил на страницу Power BI два визуальных элемента:

1. Матрицу, в строки которой добавил поле «Дата» и оставил группировку по годам и месяцам, а в «Значения» подтянул количество уникальных номеров заказов:

![Матрицу, в строки которой добавил поле «Дата» и оставил группировку по годам и месяцам](../images/kak-rabotat-s-zakladkami-bookmarks-v-power-bi-podr-matricu-v-e62c2971.webp)

2. График. В шкалу добавил даты, а для «Значений» выбрал количество уникальных номеров заказов:

![В шкалу добавил даты, а для «Значений» выбрал количество уникальных номеров заказов](../images/kak-rabotat-s-zakladkami-bookmarks-v-power-bi-podr-v-skalu-d-e3e09b8d.webp)

На странице Power BI сейчас это выглядит так:

![На странице Power BI сейчас это выглядит](../images/kak-rabotat-s-zakladkami-bookmarks-v-power-bi-podr-na-strani-c64b1025.webp)

Далее я привел оба визуальных элемента к одинаковому размеру, перейдя в области «Формат» в блок «Общие»:

![Далее я привел оба визуальных элемента к одинаковому размеру, перейдя в области «Формат» в блок «Общие»](../images/kak-rabotat-s-zakladkami-bookmarks-v-power-bi-podr-dalee-a-p-1f03ed69.webp)

После этого следует создать кнопки-переключатели. Я просто нашел картинки в Google, аккуратно вырезал переключатель и добавил как изображение в Power BI.

Если что, скачать вырезанные изображения переключателя можно [здесь](https://drive.google.com/uc?authuser=0&id=1qAE2wRYnTqSvLlp7zz1Yi-qbzLuvBeFe&export=download).

![После этого следует создать кнопки-переключатели](../images/kak-rabotat-s-zakladkami-bookmarks-v-power-bi-podr-posle-eto-8d8b26ac.webp)

![Чтобы переключатель в обоих состояниях смотрелся как единый элемент, необходимо обе картинки привести к одному размеру](../images/kak-rabotat-s-zakladkami-bookmarks-v-power-bi-podr-ctoby-per-9ebde946.webp)

Чтобы переключатель в обоих состояниях смотрелся как единый элемент, необходимо обе картинки привести к одному размеру, так же, как мы это делали с таблицей и графиком.

После этого с помощью клавиши Ctrl и правой кнопки мыши необходимо выделить обе картинки, перейти на вкладку «Формат» в главном меню и выровнять элементы по горизонтали и вертикали. В результате они будут выглядеть как один переключатель:

![они будут выглядеть как один переключатель](../images/kak-rabotat-s-zakladkami-bookmarks-v-power-bi-podr-oni-budut-eee5730f.gif)

Так же выравниванием по вертикали и горизонтали и соединяем созданные ранее таблицу и график:

![выравниванием по вертикали и горизонтали и соединяем созданные ранее таблицу и график](../images/kak-rabotat-s-zakladkami-bookmarks-v-power-bi-podr-vyravniva-175902c1.gif)

Далее будем работать с панелью выбора и панелью закладок, поэтому перейдите на вкладку «View» основного меню и поставьте галочки напротив «Bookmark Pane» и «Selection Pane»:

![Далее будем работать с панелью выбора и панелью закладок](../images/kak-rabotat-s-zakladkami-bookmarks-v-power-bi-podr-dalee-bud-bb7a5fcb.webp)

Создаем две закладки. Для первой на панели «Selection» делаем невидимыми два из четырех визуальных элементов, убираем одно из положений переключателя и график, жмём на панели закладок («Bookmarks») кнопку «Add»:

![Для первой на панели «Selection» делаем невидимыми два из четырех визуальных элементов, убираем одно из положений переключателя и график, жмём на панели закладок («Bookmarks») кнопку «Add»](../images/kak-rabotat-s-zakladkami-bookmarks-v-power-bi-podr-dla-pervo-e610ce01.webp)

Для удобства вкладку можно переназвать в «TableView». Для этого нажимаем троеточие после названия «Bookmarks 1» и выбираем пункт «Rename».

На панели «Selection» убираем из видимости визуальные элементы, которые мы оставили для прошлой вкладки, и создаём вторую вкладку «ChartView»:

![На панели «Selection» убираем из видимости визуальные элементы, которые мы оставили для прошлой вкладки](../images/kak-rabotat-s-zakladkami-bookmarks-v-power-bi-podr-na-paneli-cd795001.webp)

Выделяем переключатель и в области форматирования изображения «Format image» в блоке «Links» создаём ссылку на вкладку «TableView»:

![создаём ссылку на вкладку «TableView»](../images/kak-rabotat-s-zakladkami-bookmarks-v-power-bi-podr-sozdaem-s-329b627b.gif)

То же повторяем, вернувшись на вкладку «TableView». Выделяем изображение переключателя и создаем ссылку на вкладку «ChartView».

Обратите внимание: когда вы создаете ссылку для изображения переключателя, которое отображается при включенной вкладке «TableView», вы указываете ссылку на вкладку «ChartView». И наоборот: когда создаете ссылку для изображения переключателя, которое остается видимым на вкладке «ChartView», ссылаетесь на вкладку «TableView».

Результат выглядит [так](https://app.powerbi.com/view?r=eyJrIjoiYmVmYzA1ZjQtM2M3Yy00ZmMxLWFiMGYtNzUwYzliNGI5NmYzIiwidCI6ImRlNjc1Y2JlLTlkNzMtNDhhMS04NGY3LWRiNDhiODVhYjUxOSIsImMiOjl9):

<https://app.powerbi.com/view?r=eyJrIjoiYmVmYzA1ZjQtM2M3Yy00ZmMxLWFiMGYtNzUwYzliNGI5NmYzIiwidCI6ImRlNjc1Y2JlLTlkNzMtNDhhMS04NGY3LWRiNDhiODVhYjUxOSIsImMiOjl9>

Для работы с переключателем в Power BI Desctop зажмит клавишу Ctrl. В онлайн-версии сервиса достаточно просто кликнуть по кнопке левой клавишей мышки.

Если остались вопросы, пишите в комментариях.

---

[Оригинал статьи на блоге Netpeak.](https://netpeak.net/ru/blog/kak-rabotat-s-zakladkami-v-power-bi-podrobnoye-rukovodstvo/)
