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


<table>
    <tr>
      <td>
        <a href="https://selesnow.github.io/ryandexdirect/">ryandexdirect</a>
      </td>
      <td>
        <a href="https://selesnow.github.io/rfacebookstat/">rfacebookstat</a>
      </td>
      <td>
        <a href="https://selesnow.github.io/rvkstat/">rvkstat</a>
      </td>
      <td>
        <a href="https://selesnow.github.io/rmytarget/">rmytarget</a>
      </td>
      <td>
        <a href="https://selesnow.github.io/rmixpanel/">rmixpanel</a>
      </td>
      <td>
        <a href="https://selesnow.github.io/getProxy/">getProxy</a>
      </td>
      <td>
        <a href="https://selesnow.github.io/rGitHub/">rGitHub</a>
      </td>
      <td>
        <a href="https://selesnow.github.io/news/">NEWS</a>
      </td>
    </tr>
</table>

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

На этой странице собраны все статьи посвящённые работе с представленными на этом сайта пакетами функций расширяющих базовые возможности языка R.

Далее приведён  список статей с сопутсвующей информацией про автора, и пакеты о которых идёт речь в статье:

---
## [Облако минус слов для Яндекс Директ](https://esliklientov.net/articles/%D0%BA%D0%BE%D0%BD%D1%82%D0%B5%D0%BA%D1%81%D1%82%D0%BD%D0%B0%D1%8F-%D1%80%D0%B5%D0%BA%D0%BB%D0%B0%D0%BC%D0%B0/%D1%8F%D0%BD%D0%B4%D0%B5%D0%BA%D1%81-%D0%B4%D0%B8%D1%80%D0%B5%D0%BA%D1%82/%D0%BE%D0%B1%D0%BB%D0%B0%D0%BA%D0%BE-%D0%BC%D0%B8%D0%BD%D1%83%D1%81-%D1%81%D0%BB%D0%BE%D0%B2-%D0%B4%D0%BB%D1%8F-%D1%8F%D0%BD%D0%B4%D0%B5%D0%BA%D1%81-%D0%B4%D0%B8%D1%80%D0%B5%D0%BA%D1%82.html) <Br>
<b>Автор:</b> Андрей Москалец <Br>
<b>Впервые было опубликовано на:</b> [esliklientov.net](http://esliklientov.net) <Br>
<b>Дата публикации:</b> 20.06.2017 <Br>

<p align="center">
<img class="aligncenter" src="http://pm-partner.ru/upload/medialibrary/1cb/b234.png" align="middle" alt="Подключение Power BI к Yandex.Metrika" style="position: relative; width: 350px; margin-left: 50px; margin-top: 30px; margin-bottom: 30px;">
</p>

*Аналогично [скрипту на R для облака поисковых слов AdWords](https://esliklientov.net/articles/%D0%BA%D0%BE%D0%BD%D1%82%D0%B5%D0%BA%D1%81%D1%82%D0%BD%D0%B0%D1%8F-%D1%80%D0%B5%D0%BA%D0%BB%D0%B0%D0%BC%D0%B0/google-adwords/%D0%B1%D1%8B%D1%81%D1%82%D1%80%D0%B0%D1%8F-%D0%BE%D1%86%D0%B5%D0%BD%D0%BA%D0%B0-%D1%81%D0%BB%D0%BE%D0%B2-%D0%BD%D0%B5-%D0%BF%D1%80%D0%B8%D0%BD%D0%BE%D1%81%D1%8F%D1%89%D0%B8%D1%85-%D0%BA%D0%BE%D0%BD%D0%B2%D0%B5%D1%80%D1%81%D0%B8%D0%B8-%D0%B2-adwords-%D0%BF%D1%80%D0%B8-%D0%BF%D0%BE%D0%BC%D0%BE%D1%89%D0%B8-%D1%8F%D0%B7%D1%8B%D0%BA%D0%B0-r.html) сделал и для Директа, но добавил больше интерактивности, благодаря  Shiny можно его открыть любым браузером и все изменения в настройках сразу изменяют данные на странице. 
Скрипт скачивает поисковые запросы по всем кампаниям в аккаунте за последние 30 дней. 
Можно выбрать кампанию, указать анализируемый период внутри 30 дней (по умолчанию стоит последние 7 дней). *

*[Читать продолжение в первоисточнике.](https://esliklientov.net/articles/%D0%BA%D0%BE%D0%BD%D1%82%D0%B5%D0%BA%D1%81%D1%82%D0%BD%D0%B0%D1%8F-%D1%80%D0%B5%D0%BA%D0%BB%D0%B0%D0%BC%D0%B0/%D1%8F%D0%BD%D0%B4%D0%B5%D0%BA%D1%81-%D0%B4%D0%B8%D1%80%D0%B5%D0%BA%D1%82/%D0%BE%D0%B1%D0%BB%D0%B0%D0%BA%D0%BE-%D0%BC%D0%B8%D0%BD%D1%83%D1%81-%D1%81%D0%BB%D0%BE%D0%B2-%D0%B4%D0%BB%D1%8F-%D1%8F%D0%BD%D0%B4%D0%B5%D0%BA%D1%81-%D0%B4%D0%B8%D1%80%D0%B5%D0%BA%D1%82.html)*

---
## [Подключение Power BI к Yandex.Metrika](http://pm-partner.ru/articles/2017/podkluchenie-power-bi-yandex-metrika/) <Br>
<b>Автор:</b> Дмитрий Малых <Br>
<b>Впервые было опубликовано на:</b> [pm-partner](http://pm-partner.ru) <Br>
<b>Дата публикации:</b> 19.05.2017 <Br>

<p align="center">
<img class="aligncenter" src="http://pm-partner.ru/upload/medialibrary/1cb/b234.png" align="middle" alt="Подключение Power BI к Yandex.Metrika" style="position: relative; width: 350px; margin-left: 50px; margin-top: 30px; margin-bottom: 30px;">
</p>

*С тех пор, как мы начали работать с Microsoft Power BI, прошло значительное количество времени и, неожиданно было отмечено, что у нас осталась лишь одна область деятельности без визуализированных отчётов – Яндекс Метрика. 
Однако, тривиальная в общем-то задача, оказалась не настолько простой, как ожидалось.*

*[Читать продолжение в первоисточнике.](http://pm-partner.ru/articles/2017/podkluchenie-power-bi-yandex-metrika/)*

---
## [Как получить и обработать сырые данные из Яндекс.Метрики](https://netpeak.net/ru/blog/kak-poluchit-i-obrabotat-syrye-dannye-iz-yandeks-metriki/) <Br>
<b>Автор:</b> Алексей Селезнёв <Br>
<b>Впервые было опубликовано на:</b> [Блог Netpeak](https://netpeak.net/ru/blog/) <Br>
<b>Дата публикации:</b> 09.02.2017 <Br>

<p align="center">
<img class="aligncenter" src="https://images.netpeak.net/blog/kak-polucit-i-obrabotat-syrye-dannye-iz-andeksmetriki.jpg" align="middle" alt="Как получить и обработать сырые данные из  Яндекс.Метрики" style="position: relative; width: 350px; margin-left: 50px; margin-top: 30px; margin-bottom: 30px;">
</p>
  
*Хотите качественно анализировать статистику из Яндекс.Метрики? Отследить сложные воронки продаж, объединить данные из разных систем аналитики, контролировать расхождения в статистике, — «сырые» данные помогут вам эффективно решить все эти сложные задачи.*

*В 2016 году Яндекс заявили о публичном релизе программного интерфейса Logs API, который позволяет получить сырые данные из Яндекс.Метрики в файле формата TSV.*

*Однако в работе с API Яндекс.Метрики у вас могут возникнуть сложности:*

* *процедуру выгрузки придется повторять каждый раз, когда вы захотите получить новую статистику;*
* *для визуализации данных нужно вручную загружать TSV-файл в оболочку, предназначенную для построения графиков и таблиц.*
*В этой статье я расскажу, как автоматизировать выгрузку сырых данных из Яндекс.Метрики и работать с полученной статистикой.*

*[Читать продолжение в первоисточнике.](https://netpeak.net/ru/blog/kak-poluchit-i-obrabotat-syrye-dannye-iz-yandeks-metriki/)*

---
## [Как связать Яндекс.Директ с Microsoft Power BI](https://netpeak.net/ru/blog/kak-svyazat-yandeks-direkt-s-microsoft-power-bi/) <Br>
<b>Автор:</b> Алексей Селезнёв <Br>
<b>Впервые было опубликовано на:</b> [Блог Netpeak](https://netpeak.net/ru/blog/) <Br>
<b>Дата публикации:</b> 27.02.2017 <Br>

<p align="center">
<img class="aligncenter" src="https://images.netpeak.net/blog/card_facebook_kak-svyazat-yandeks-direkt-s-microsoft-power-bi.png" align="middle" alt="Как связать Яндекс.Директ с Microsoft Power BI" style="position: relative; width: 350px; margin-left: 50px; margin-top: 30px; margin-bottom: 30px;">
</p>

*Яндекс.Директ собирает много данных, но, к сожалению, в веб-интерфейсе доступно очень мало информации для анализа. В этой статье я подробно опишу, как получить статистику о рекламных кампаниях c помощью языка R для визуализации в Power BI.*

*[Читать продолжение в первоисточнике.](https://netpeak.net/ru/blog/kak-svyazat-yandeks-direkt-s-microsoft-power-bi/)*

---
