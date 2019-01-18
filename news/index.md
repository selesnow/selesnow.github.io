<p align="center">
<a href="https://selesnow.github.io/"><img src="https://alexeyseleznev.files.wordpress.com/2017/03/as.png" height="80"></a>
</p>

<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<script>
  (adsbygoogle = window.adsbygoogle || []).push({
    google_ad_client: "ca-pub-7009762262305396",
    enable_page_level_ads: true
  });
</script>
  
<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-114798296-1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'UA-114798296-1');
</script>

<style type="text/css">

ul.nm_ul {
  list-style: none; /*убираем маркеры списка*/
  margin: 0; /*убираем отступы*/
  padding-left: 0; /*убираем отступы*/
  margin-top:25px; /*делаем отступ сверху*/
  background:#DCDCDC; /*добавляем фон всему меню*/
  height: 30px; /*задаем высоту*/
}
a.nm_a {
  text-decoration: none; /*убираем подчеркивание текста ссылок*/
  background:#696969; /*добавляем фон к пункту меню*/
  color:#fff; /*меняем цвет ссылок*/
  padding:0px 7px; /*добавляем отступ*/
  font-family: arial; /*меняем шрифт*/
  line-height:30px; /*ровняем меню по вертикали*/
  display: block; 
  border-right: 1px solid #677B27; /*добавляем бордюр справа*/
  -moz-transition: all 0.3s 0.01s ease; /*делаем плавный переход*/
  -o-transition: all 0.3s 0.01s ease;
  -webkit-transition: all 0.3s 0.01s ease;
}
a.nm_a:hover {
  background:#FF8C00;/*добавляем эффект при наведении*/
}
li.nm_li {
  float:left; /*Размещаем список горизонтально для реализации меню*/
  position:relative; /*задаем позицию для позиционирования*/
}
     
    /*Стили для скрытого выпадающего меню*/
    li.nm_li > ul.nm_ul {
        position:absolute;
        top:5px;
        display:none;   
    }
     
    /*Делаем скрытую часть видимой*/
    li.nm_li:hover > ul.nm_ul {
        display:block; 
        width:280px;  /*Задаем ширину выпадающего меню*/      
    }
   li.nm_li:hover > ul.nm_ul > li.nm_li {
        float:none; /*Убираем горизонтальное позиционирование*/
    }
</style>

<h2>Menu:</h2>
<center>
<ul class="nm_ul">
    <li class="nm_li"><a href="/" class="nm_a">Main</a></li>
    <li class="nm_li"><a href="/" class="nm_a">R Packages</a>
        <ul class="nm_ul">
            <li class="nm_li"><a href="/ryandexdirect" class="nm_a">ryandexdirect</a></li>
            <li class="nm_li"><a href="/rym" class="nm_a">rym</a></li>
            <li class="nm_li"><a href="/rfacebookstat" class="nm_a">rfacebookstat</a></li>
			<li class="nm_li"><a href="/rvkstat" class="nm_a">rvkstat</a></li>
			<li class="nm_li"><a href="/rmytarget" class="nm_a">rmytarget</a></li>
			<li class="nm_li"><a href="/rmixpanel" class="nm_a">rmixpanel</a></li>
			<li class="nm_li"><a href="/rGitHub" class="nm_a">rGitHub</a></li>
			<li class="nm_li"><a href="/getProxy" class="nm_a">getProxy</a></li>
        </ul>
    </li>
	<li class="nm_li"><a href="#" class="nm_a">Онлайн Книги</a>
	    <ul class="nm_ul">
            <li class="nm_li"><a href="https://r-for-marketing.netpeak.net/" class="nm_a">Язык R в Интернет Маркетинге</a></li>
            <li class="nm_li"><a href="https://netpeak.net/files/whitepapers/10-fishek-web-analitiki.pdf" class="nm_a">10 фишек Google Analytics</a></li>
        </ul>
	</li>
	<li class="nm_li"><a href="#" class="nm_a">Онлайн Курсы</a>
	    <ul class="nm_ul">
            <li class="nm_li"><a href="https://learn.needfordata.ru/r" class="nm_a">Язык R в Интернет Маркетинге</a></li>
        </ul>
    </li>
    <li class="nm_li"><a href="/library" class="nm_a">Статьи</a></li>
    <li class="nm_li"><a href="https://alexeyseleznev.wordpress.com/" class="nm_a">Блог</a></li>
    <li class="nm_li"><a href="/news" class="nm_a">Новости</a></li>
    <li class="nm_li"><a href="/publications" class="nm_a">Архив</a></li>
</ul>
</center>
<Br>
<h2>Search:</h2>
<script>
  (function() {
    var cx = '002735389418227325972:fdikniadyig';
    var gcse = document.createElement('script');
    gcse.type = 'text/javascript';
    gcse.async = true;
    gcse.src = 'https://cse.google.com/cse.js?cx=' + cx;
    var s = document.getElementsByTagName('script')[0];
    s.parentNode.insertBefore(gcse, s);
  })();
</script>
<gcse:search></gcse:search>
  
# Последние новости репозиториев

---
### 2019-01-18| rvkstat & rym
За последние два дня было опубликовано сразу два релиза, первый кассается пакета `rvkstat`, второй `rym`.

В rvkstat была значительно улучшена функция `vkGetAdStatisctics`, подробнее можно узнать [тут](https://github.com/selesnow/rvkstat/releases/tag/2.5.4). 

В `rym` была добавлена функция `rym_get_direct_clients` которая возвращает данные о клиентах Яндекс.Директа, к кампаниям которых есть доступ у владельца счетчика Метрики, а так же исправлена ошибка с некорректной загрузкой ClientID из Logs API, подробности данного релиза можно найти [тут](https://github.com/selesnow/rym/releases/tag/0.5.1).

---
### 2018-12-18| ryandexdirect
Наконец добрались руки до [документации](/ryandexdirect/) по пакету ryandexdirect, теперь она полностью актульна. К тому же на страницу документации была дабавлена видео запись вебинара "Как маркетологу избавиться от рутины с помощью языка R", первые 28 минут которого посвящены работе с ryandexdirect.

---
### 2018-12-13| 
Сегодня две небольшие новости по проекту selesnow.github.io:
1. Книга "Язык R для интернет - маркетинга" сегодня была значительно доработана, и полностью переведена в формат академии, и вынесена на отдельный домен [r-for-marketing.netpeak.net](https://r-for-marketing.netpeak.net/). Книга по прежнему в свободном доступе, но теперь имеет удобный формат.
2. На стрницу документации пакета [rym](https://selesnow.github.io/rym/) добавлена видеозапись вебинара по работе с этим пакетом,это значительно упростит процес обучения.

---
### 2018-12-11| ryandexdirect
На стороне API Яндекс.Директ был полностью переработан справочник валют, о чём они [сообщили в своём блоге](https://yandex.ru/blog/ya-direct-api/otklyuchaem-podderzhku-u-e-v-spravochnike-valyut) 29 ноября, данные изменения затронули функции `yadirGetDictionary` и `yadirCurrencyRates` пакета ryandexdirect. Подробнее о внесённых изменениях можно узнать в описании [релиза на GitHub](https://github.com/selesnow/ryandexdirect/releases/tag/3.0.11.0).

---
### 2018-12-05| ryandexdirect
Полностью переписана функция `yadirGetClientList`, и переведена на API Яндекс.Директ версии 5. Синтаксис функции не изменился, но значительно расширился список полей который вы с её помошью можете получить. Все подробности можно узнать в релизе на [GitHub] (https://github.com/selesnow/ryandexdirect/releases/tag/3.0.10).

---
### 2018-11-26| безопасность
В связи с тем, что последнее время мне часто задают вопрос о безопасности использования моих пакетов, я написал по этой теме подробную статью на Хабру, "[Насколько безопасно использовать R пакеты для работы с API рекламных систем](https://habr.com/post/430888/)", в ближайшее время ссылка на неё появится в главном меню сайта.

---
### 2018-11-22| rmytarget
В связи с [сообщением](https://www.facebook.com/groups/targetmailapi/permalink/1954280624611261/) от поддержки API MyTarget о том, с 1 декабря прекращается поддержка API v1, я полностью переписал `rmytarget`. При этом его синтаксис практически не изменился, написанной на более ранних версиях пакета код будет работать, но появились новые возможности, и функции теперь возвращают больше данных. О всех подробностях можно узнать в описании [релиза на GitHub](https://github.com/selesnow/rmytarget/releases/tag/v2.0.1). 

---
### 2018-11-21| ryandexdirect
По [ссылке](https://www.youtube.com/watch?v=Kh-wyU-VXRU) доступна запись вебинара "Как маркетологу избавиться от рутины с помощью языка R и наконец то заняться маркетингом", в ходе которого я продемонстрировал как работать с пакетами ryandexdirect, RAdwords и RGA. 

[Презентация](https://www.slideshare.net/webpromoexperts/r-123628095)
[Примеры кода на GitHub](https://github.com/selesnow/publications/tree/master/code_example/webpromo_now_2018)

---
### 2018-11-01| телеграм канал - R4marketing
Ещё одна хорошая новость, сегодня стартует мой телеграм канал [R4marketing](https://t.me/r4marketing), канал создан для более удобного информорования о релизах пакетов, и о другой информации о применении языка R в решение задач интернет маркетинга, присоединяйтесь.

---
### 2018-10-29| интервью
Опубликовано интервь ["Язык R в веб-аналитике и интернет-маркетинге"](https://leadzavod.com/jazyk-r-v-veb-analitike-i-internet-marketinge/) для Лидзавода, в ходе интервью пообщались о том, как язык R помогает автоматизировать работу с данными в решении наших внутренних задач в Netpak. В конце интевью небольшой бонус, промокод со 10% скидкой на курс ["Язык R для интернет-маркетинга"](https://learn.needfordata.ru/r). 

---
### 2018-10-25
Сегодня у нас очень хорошая новость, 25 октября стартуют продажи моего первого онлайн курса ["Язык R для интернет-маркетинга"](https://learn.needfordata.ru/r). В курсе я собрал все накопленные за последние три года знания и наработки которые сам ежедневно использую в решении рабочих задач. 

От вас не трубется навыков программирования, главное понимание предметной области интернет-маркетинга. Курс начинается с озов программирования на R, далее вы научитесь работать с API интерфейсами всех популярных систем интернет рекламы и веб аналитики, после чего научитесь использовать собранные данные.

Вся дополнительная информация о цене, программе, и других деталях доступна по [ссылке](https://learn.needfordata.ru/r).

---
### 2018-10-24| ryandexdirect
В ryandexdirect реализован функционал, который был добавлен [8 июня в сервис Reports](https://yandex.ru/blog/ya-direct-api/modeli-atributsii-i-tseli-v-reports), а именно в функцию yadirGetReport добавлены аргументы Goals и AttributionModels с помощью которых вы можете запрашивать данные полей ConversionRate, Conversions, CostPerConversion, GoalsRoi и Revenue по каждой отдельной настроеной цели, к тому же получить расчёт по трём различнам моделям аттрибуции, подробности релиза и пример кода можно посмотреь на [GitHub](https://github.com/selesnow/ryandexdirect/releases/tag/3.0.8).

---
### 2018-10-09| rfacebookstat
rfacebookstat попал в [топ 40](https://rviews.rstudio.com/2018/09/26/august-2018-top-40-new-packages/) пакетов опубликованных на CRAN в августе 2018 года.

---
### 2018-10-05
Опубиковал [обзор R пакетов для интренет маркетинга](https://habr.com/post/425425/) на хабре.

---
### 2018-10-02| rym
Готова [официальная документация](https://selesnow.github.io/rym) к пакету rym.

---
### 2018-10-01| rym
Написал [статью](https://netpeak.net/ru/blog/kak-rabotat-s-api-yandeks-metriki-s-pomoshch-yu-yazyka-r/), о том, как с помощью пакета `rym` работать со всеми API Яндекс.Метрики.

---
### 2018-09-28| rmytarget
rmytarget, пакет предназначенный для работы с API платформы MyTarget был опубликован на CRAN, для установки еперь можно использовать стандартную команду `install.packages("rmytarget")`.

---
### 2018-09-03| rym
Новый пакет [rym](https://selesnow.gihub.io/rym), предназначенный для работы с API Яндекс.Метрики изначально был написан согласно всех правил репозитория CRAN и сразу был опубликован и на GitHub и на CRAN. 
Установка с CRAN: `install.packages("rym")`
Установка с GitHub: `devtools::install_github("selesnow/rym")`

---
### 2018-08-20| getProxy
Пакет getProxy прошел все проверки и был добавлен на CRAN.

---
### 2018-08-18| getProxy
В [документацию](https://selesnow.github.io/getProxy) пакета getProxy добавлен видео мануал по работе с пакетом.

---
### 2018-08-17| rmytarget
Пакет rmytarget получил доступ к схеме авторизации Authorization Code Grant, теперь для работы с API MyTarget через функции rmytarget вам не требуется запрашивать доступ к API MyTarget. Подробнее на [GitHub](https://github.com/selesnow/rmytarget/releases/tag/v1.1).

---
### 2018-08-14| rfacebookstat
Пакет rfacebookstat прошел все проверки и был загружен в основной репозиторий для хранения пакетов на R - CRAN (Comprehensive R Archive Network).

Для установки пакета из CRAN можно использовать следующую команду.

`install.packages("rfacebookstat")`

В ближайшее время можно будет установить пакет без явного указания репозитория т.е. просто `install.packages("rfacebookstat")`.

[Страница пакета](https://CRAN.R-project.org/package=rfacebookstat)()
[Документация по rfacebookstat на CRAN](https://cran.r-project.org/web/packages/rfacebookstat/rfacebookstat.pdf)

---
### 2018-08-08| rfacebookstat

Новая статья в нашей библиотеке, автор [Макс Гапчук](https://www.facebook.com/maks.hapchuk), рассказал как импортировать данные о расходах из Facebook в Google Analytics с помощью пакетов **rfacebookstat**, googleAnalyticsR и googleAuthR.

---
### 2018-08-08| rfacebookstat

Пакет rfacebookstat переведён на работу с версий API Facebook v3.1, рекомендую всем обновить пакет для избежания ошибок при отвправке запросов к API Facebook. [Подробности на GitHub](https://github.com/selesnow/rfacebookstat/releases/tag/1.8.2).

Для обновления пакета запустите следующую команду `devtools::install_github('selesnow/rfacebookstat')`.

---
### 2018-08-08| ryandexdirect

В сервис Reports, предназначеный для получения статистики с Яндекс Директ добавлены новые поля AvgTrafficVolume, WeightedCtr, WeightedImpressions. Соответсвенно теперь вы можете запрашивать данные поля при работе с функцией yadirGetReports. [Подробности в блоге Яндекс Директ](https://yandex.ru/blog/ya-direct-api?from=email).

---
### 2018-07-16| rfacebookstat

Релиз версии rfacebookstat 1.7.0, в которую было добавлено 4 новые функции, с помощью которых вы можете загружаьт список рекламных кампаний, групп объявлений, объявлений и контента объявлений, подробнее на [GitHub](https://github.com/selesnow/rfacebookstat/releases/tag/1.7.0).

---
### 2018-05-16| ryandexdirect

ryandexdirect был хначительно улучшен, подробнее с детальным описанием всех обновлений можно в [статье на блоге](https://alexeyseleznev.wordpress.com/2018/05/16/ryandexdirect-3-0-0-%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D1%91%D0%BD%D0%BD%D1%8B%D0%B9-r-%D0%BA%D0%BB%D0%B8%D0%B5%D0%BD%D1%82-%D0%B4%D0%BB%D1%8F-%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%8B-%D1%81-api/), или из [релиза на GitHub](https://github.com/selesnow/ryandexdirect/releases/tag/3.0.0).

К тому же была актуализирована и структурирована [официальная документация](https://selesnow.github.io/ryandexdirect/) по работе с пакетом ryandexdirect.

---
### 2018-05-07| ryandexdirect

ryandexdirect 2.6.0, в пакет добавлена функция `yadirGetSiteLinks`, с помощью которой вы можете получить список быстрых ссылок, другие подообности релиза доступны по [ссылке](https://github.com/selesnow/ryandexdirect/releases/tag/2.6.0).

---
### 2018-05-03| ryandexdirect

В сервис Repots, доступный в API Яндекс Диркта добален новый тип отчёта REACH_AND_FREQUENCY_PERFORMANCE_REPORT, в котором доступны новые поля AvgCpm (средняя стоимость тысячи показов), AvgImpressionFrequency (средняя частота показов одному пользователю) и ImpressionReach (охват по показам) и для поля CampaignType добавлено значение CPM_BANNER_CAMPAIGN.

Это значит что с помощью функции yadirGetReport теперь так же можно запрашивать эту информацию, [подробнее](https://yandex.ru/blog/ya-direct-api/ctatistika-dlya-mediynykh-kampaniy-v-reports).

---
### 2018-05-02| ryandexdirect

Доработана функция `yadirGetBalance`, запрашивающая остаток средств на счетах в аккаунтах Яндекс Директ, обновление касаются запроса остатков балансов по клиентах агентских аккаунтов, ранее можно было за раз запросить данные максимум по 50 аккаунтам, сейчас можно запрашивать данные по любому количеству клиентов, [подробнее](https://github.com/selesnow/ryandexdirect/issues/4#issuecomment-384208899).

---
### 2018-04-10| ryandexdirect

Написал статью о том как с помощью языка R получить данные из API Google AdWords и Яндекс Директ, с помощью пакетов RAdwords и ryandexdirect, с примерами кода, [ссылка на статью](https://www.owox.ru/blog/articles/r-language-and-api-of-ad-systems/).

---
### 2018-04-10| rvkstat 2.5.1

Исправлена ошибка в функции vkGetUserGroups, подробнее можно узнать из [тикета](https://github.com/selesnow/rvkstat/issues/11).

---
### 2018-04-03| rvkstat 2.5.0

Релиз rvkstat версии 2.5.0, в пакет добавлена возможность запрашивать подробную статистику о сообщенях на стене сообщества, подробности по [ссылке](https://github.com/selesnow/rvkstat/releases/tag/2.5.0).

---
### 2018-04-02| Интервью

Интервью для поортала посвящённого цифровым исследованиям "Цифровой Дискурс", пообщались на тему "Кто такие интернет-аналитики и какими инструментами они пользуются". Так же в ходе интервью речь зашла и про пакеты ryandexdirect, rvkstat, rfacebookstat, rmytarget, rmixpanel. Полный текст интервью доступен по [ссылке](https://discourse.digital/blogs/kto-takie-internet-analitiki-i-kakimi-instrumentami-oni-polzuyutsya/?utm_source=github&utm_medium=seleznev). 

---
### 2018-03-29| rfacebookstat

На страницу [документации пакета rfacebookstat](http://selesnow.github.io/rfacebookstat) добалвена форма для получения токена доступа к API Facebook.

---
### 2018-03-26| rvkstat

Доработана функция `vkGetUserWall`, теперь она помимо статистики по количеству комментариев, репостов и лайков возвращает количество просмотров сообщения, [подробности](https://github.com/selesnow/rvkstat/issues/4#issuecomment-376087748).

---
### 2018-03-21| ryandexdirect

Дмитрий Осиюк написал о том, как с помощью пакета ryandexdirect определить мошенничество CPA-сетей, [сылка на статью](https://iosiuk.blogspot.com/2018/03/cpa-logs-api-yandexmetrika-r.html).

---
### 2018-03-21| ryandexdirect

В пакете ryandexdirect исправлена ошибка, при использовании оператора IN при фильтрации данных в функции yadirGetReport. [подробности](https://github.com/selesnow/ryandexdirect/issues/1).

---
### 2018-03-20| rfacebookstat

В пакете rfacebookstat исправлена ошибка при работе с actions breakdowns, ранее задваивались строки с прочей статистикой т.к. API отдаёт данные по actions в виде отдельных списков, теперь каждое событие будет в отдельном столбце, количество строк никак от этого не изменится. [подробности](https://github.com/selesnow/rfacebookstat/issues/1).

---
### 2018-03-19| rvkstat

Исправлена ошибка в функции vkGetUserWall,теперь она корректно обращается как к старой версии API, т.е. до 5ой, так и с новой версией 5.x. [подробности](https://github.com/selesnow/rvkstat/issues/4).

---
### 2018-03-02| rvkstat

Добавлена возможность получения ключа доступа сообщества и списки диалогов Вконтакте, [релиз](https://github.com/selesnow/rvkstat/releases/tag/2.4.1).

---

### 2018-03-01

Собрал в одной [статье](https://alexeyseleznev.wordpress.com/2018/03/01/%D0%BF%D0%BE%D1%80%D1%86%D0%B8%D1%8F-%D0%B7%D0%B8%D0%BC%D0%BD%D0%B8%D1%85-%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B9-%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2-ryandexdirect-rfacebo/) все зимние обновления пакетов ryandexdirect, rfacebookstat, rvkstat.

---

### 2018-02-27| rvkstat

В пакет rvkstat добавлена функция vkGetAdsLayout, возвращающая описание внешнего вида рекламных объявлений, подробности [тут](https://github.com/selesnow/rvkstat/releases/tag/2.3.0).

---

### 2018-01-22| rvkstat, rfacebookstat

[Михаил Гусев](https://www.facebook.com/profile.php?id=100012364206491&fref=mentions) из eLama написал подробную [статью](https://ppc.world/articles/zagruzka-statistiki-iz-vkontakte-i-facebook-v-google-bigquery/) для [ppc.world](https://ppc.world/) о том, как с помощью пакета rvkstat и bigrquery загрузить данные из Вконтакте в Google BigQuery.

---
