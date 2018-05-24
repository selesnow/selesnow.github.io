<head>
  
<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-114798296-1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-114798296-1');
</script>

<style type="text/css">
 
</style>
ul {
  list-style: none; /*убираем маркеры списка*/
  margin: 0; /*убираем отступы*/
  padding-left: 0; /*убираем отступы*/
  margin-top:25px; /*делаем отступ сверху*/
  background:#FF4444; /*добавляем фон всему меню (заменив этот параметр, вы поменяете цвет всего меню)*/
  height: 50px; /*задаем высоту*/
}
a {
  text-decoration: none; /*убираем подчеркивание текста ссылок*/
  background:#FF4444; /*добавляем фон к пункту меню (заменив этот параметр, вы поменяете цвет всех пунктов меню)*/
  color:#fff; /*меняем цвет ссылок*/
  padding:0px 15px; /*добавляем отступ*/
  font-family: arial; /*меняем шрифт*/
  line-height:50px; /*ровняем меню по вертикали*/
  display: block; 
  border-right: 1px solid #F36262; /*добавляем бордюр справа*/
  -moz-transition: all 0.3s 0.01s ease; /*делаем плавный переход*/
  -o-transition: all 0.3s 0.01s ease;
  -webkit-transition: all 0.3s 0.01s ease;
}
a:hover {
  background:#D43737;/*добавляем эффект при наведении*/
}
li {
  float:left; /*Размещаем список горизонтально для реализации меню*/
}
</head>

<p align="center">
<a href="https://selesnow.github.io/"><img src="https://alexeyseleznev.files.wordpress.com/2017/03/as.png" height="80"></a>
</p>

<ul>
<li><a href="#">Главная</a></li>
<li><a href="#">Услуги</a></li>
<li><a href="#">Цены</a></li>
<li><a href="#">Контакты</a></li>
</ul>

# Обо мне
Меня зовут Алексей Селезнёв, на данный момент я возглавляю отдел аналитики в агентстве интернет маркетинга Netpeak. 
Более подробно обо мне можно узнать [на моём блоге](alexeyseleznev.wordpress.com).

<img class=" aligncenter" src="https://scontent.fods1-1.fna.fbcdn.net/v/t1.0-9/23519298_1723847460967555_7311750647506949501_n.jpg?oh=a88c93c1a1ea6600ee3268b3f8d74bd6&amp;oe=5B4B9D0E" alt="Фото Алексея Селезнёва.">


## Контакты
* email: selesnow@gmail.com
* facebook: [facebook.com/selesnow](https://www.facebook.com/selesnow)
* linkedin: [linkedin.com/in/selesnow](https://www.linkedin.com/in/selesnow)

Данный сайт содержит документацию к разработанным мной пакетам функций на языке R.

---

# Ссылки на репозитории
## ryandexdirect
*Пакет для работы с API системы контектсной рекламы Яндекс Директ, позволяет загружать статистику из рекламного аккаунта, останавливать и запускать показы на уровне объявлений, ключевых слов и рекламных кампаний, а так же получать данные из Яндекс.Метрики.*
* [Документация](https://selesnow.github.io/ryandexdirect/)
* [Отчёт об ошибках и доработках](https://github.com/selesnow/ryandexdirect/issues)
* [Список релизов](https://github.com/selesnow/ryandexdirect/releases)

---
## rfacebookstat
*Пакет для работы с API рекламного кабинета Facebook.*
* [Документация](https://selesnow.github.io/rfacebookstat/)
* [Отчёт об ошибках и доработках](https://github.com/selesnow/rfacebookstat/issues)
* [Список релизов](https://github.com/selesnow/rfacebookstat/releases)

---
## rvkstat
*Пакет для работы с API социальной сети Вконтакте, позволяет загружать справочную информацию, статистику сообществ, сообщения из стены сообщества и пользователей, списки друзей пользователей и статитику из рекламного кабинета.*
* [Документация](https://selesnow.github.io/rvkstat/)
* [Отчёт об ошибках и доработках](https://github.com/selesnow/rvkstat/issues)
* [Список релизов](https://github.com/selesnow/rvkstat/releases)

---
## rmytarget
*Пакет для загрузки статистики по рекламным кампаниям в системе MyTarget.*
* [Документация](https://selesnow.github.io/rmytarget/)
* [Отчёт об ошибках и доработках](https://github.com/selesnow/rmytarget/issues)
* [Список релизов](https://github.com/selesnow/rmytarget/releases)

---
## rmixpanel
*Пакет для загрузки данных из API платформы веб аналитики Mixpanel.*
* [Документация](https://selesnow.github.io/rmixpanel/)
* [Отчёт об ошибках и доработках](https://github.com/selesnow/rmixpanel/issues)
* [Список релизов](https://github.com/selesnow/rmixpanel/releases)

---
## rGitHub
*Загрузка данных о посещениях репозиториев на GitHub.*
* [Документация](https://selesnow.github.io/rGitHub/)
* [Отчёт об ошибках и доработках](https://github.com/selesnow/rGitHub/issues)
* [Список релизов](https://github.com/selesnow/rGitHub/releases)

---
## getProxy
*Перенаправления интернет соединения в R скриптах через бесплатные Proxy сервера.*
* [Документация](https://selesnow.github.io/getProxy/)
* [Отчёт об ошибках и доработках](https://github.com/selesnow/getProxy/issues)
* [Список релизов](https://github.com/selesnow/getProxy/releases)
---

# Последние новости репозиториев
---
### 2018-02-27| rvkstat

В пакет rvkstat добавлена функция vkGetAdsLayout, возвращающая описание внешнего вида рекламных объявлений, подробности [тут](https://github.com/selesnow/rvkstat/releases/tag/2.3.0).

---
