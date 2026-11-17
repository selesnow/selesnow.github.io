---
title: Ошибка SSL certificate problem при работе с пакетами RAdwords и RCurl
date: '2017-12-13'
slug: oshibka-ssl-certificate-problem-pri-rabote-s-paketami-radwords-i-rcurl
tags:
- R
- Обработка ошибок
- Google Ads
categories:
- Программирование
- R
description: Уже несколько раз при работе с пакетом RAdwords я сталкивался с ошибкой SSL certificate problem, это означает что у вас какая то проблема с SSL сертификатами.
original_url: https://alexeyseleznev.wordpress.com/2017/12/13/%d0%be%d1%88%d0%b8%d0%b1%d0%ba%d0%b0-ssl-certificate-problem-%d0%bf%d1%80%d0%b8-%d1%80%d0%b0%d0%b1%d0%be%d1%82%d0%b5-%d1%81-%d0%bf%d0%b0%d0%ba%d0%b5%d1%82%d0%b0%d0%bc%d0%b8-radwords-%d0%b8-rcurl/
wp_id: 1071
draft: false
cover: ../images/covers/1071.webp
cover_generated: true
---

Уже несколько раз при работе с пакетом RAdwords я сталкивался с ошибкой SSL certificate problem, это означает что у вас какая то проблема с SSL сертификатами.

![Картинки по запросу fix](../images/oshibka-ssl-certificate-problem-pri-rabote-s-paketami-radwor-2bd783f7.gif)

*Сообщение об ошибке:*

```
Error in function (type, msg, asError = TRUE)  : 
  SSL certificate problem: unable to get local issuer certificate
```

На самом деле проблема не в RAdwords, а в пакете RCurl и его функции getURL.

Первое, что стоит попробовать это переустановить пакет RCurl.

`install.packages("RCurl")`

Если переустановка RCurl не помогла то далее можно решить эту проблему двумя способами, исправлением кода функции в пакете RAdwords, или починить сертификаты, в этой статье я расскажу как привести в порядок SSL сертификат.

Решение я нашёл на [stackowerflow](https://stackoverflow.com/questions/6736895/using-rcurl-with-https).

Алгоритм решения проблемы следующий:

- Скачиваем сертификаты [Download “OpenSSL for Windows” version 0.9.8k](http://code.google.com/p/openssl-for-windows/downloads/detail?name=openssl-0.9.8k_WIN32.zip&can=2&q=)
- Распаковываем их и копируем файлы “libeay32.dll” и “ssleay32.dll” из папки “bin” которая будет находиться в папках распакованных сертификатов в  R\library\RCurl\libs\i386.

*Я распаковал все сертификаты во временную папку Cert.*

![](https://i0.wp.com/img.netpeak.ua/alsey/151317336838_kiss_21kb.png)

![](https://i0.wp.com/img.netpeak.ua/alsey/151317341493_kiss_21kb.png)

*Вставляем скопированные файлы файлы libeay32.dll” и “ssleay32.dll” в папку i386 пакета RCurl.*

![](https://i0.wp.com/img.netpeak.ua/alsey/151317361444_kiss_38kb.png)

- Также вы можете скопировать его в каталог где находится файл R.exe, у меня по умолчанию он находится по пути C:\Program Files\R\R-3.4.3\bin.
- Затем скачайте [этот файл](http://curl.haxx.se/ca/cacert.pem), переименуйте его в ca-bundle.crt, и установите новый набор файлов учетных данных запустив скачанный файл.

![](https://i0.wp.com/img.netpeak.ua/alsey/151318206279_kiss_38kb.png)

![](https://i0.wp.com/img.netpeak.ua/alsey/151318217314_kiss_18kb.png)

- Замените файл ca-bundle.crt в папке C:\Users\Alsey\Documents\R\win-library\3.4\RCurl\CurlSSL на скачанный.

![](https://i0.wp.com/img.netpeak.ua/alsey/151318223193_kiss_25kb.png)
