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
 ul.menu {
  list-style: none; /*убираем маркеры списка*/
  margin: 0; /*убираем отступы*/
  padding-left: 0; /*убираем отступы*/
  margin-top:25px; /*делаем отступ сверху*/
  background:#C0C0C0; /*добавляем фон всему меню (заменив этот параметр, вы поменяете цвет всего меню)*/
  height: 40px; /*задаем высоту*/
}
a.amenu {
  text-decoration: none; /*убираем подчеркивание текста ссылок*/
  background: #C0C0C0; /*добавляем фон к пункту меню (заменив этот параметр, вы поменяете цвет всех пунктов меню)*/
  color: #000000; /*меняем цвет ссылок*/
  padding:0px 10px; /*добавляем отступ*/
  font-family: sans-serif; /*меняем шрифт*/
  font-size: 9pt;
  line-height:40px; /*ровняем меню по вертикали*/
  display: block; 
  border-right: 1px solid #808080; /*добавляем бордюр справа*/
  -moz-transition: all 0.3s 0.01s ease; /*делаем плавный переход*/
  -o-transition: all 0.3s 0.01s ease;
  -webkit-transition: all 0.3s 0.01s ease;
}
a:hover {
  background:#808080;/*добавляем эффект при наведении*/
}
li.menu {
  float:left; /*Размещаем список горизонтально для реализации меню*/
}
</style>

<h2>Menu:</h2>
<center>
<ul class="menu">
  <li class="menu"><a href="https://selesnow.github.io/ryandexdirect" class="amenu">ryandexdirect</a></li>
  <li class="menu"><a href="https://selesnow.github.io/rmytarget" class="amenu">rvkstat</a></li>
  <li class="menu"><a href="https://selesnow.github.io/rfacebookstat" class="amenu">rfacebookstat</a></li>
  <li class="menu"><a href="https://selesnow.github.io/rmytarget" class="amenu">rmytarget</a></li>
  <li class="menu"><a href="https://selesnow.github.io/rmixpanel" class="amenu">rmixpanel</a></li>
  <li class="menu"><a href="https://selesnow.github.io/rgithub" class="amenu">rGitHub</a></li>
  <li class="menu"><a href="https://selesnow.github.io/getproxy" class="amenu">getProxy</a></li>
  <li class="menu"><a href="https://selesnow.github.io/news" class="amenu">NEWS</a></li>
  <li class="menu"><a href="https://selesnow.github.io/library" class="amenu">Статьи</a></li>
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
