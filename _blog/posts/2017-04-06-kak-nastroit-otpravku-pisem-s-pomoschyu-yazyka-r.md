---
title: Как настроить отправку писем с помощью языка R
date: '2017-04-06'
slug: kak-nastroit-otpravku-pisem-s-pomoschyu-yazyka-r
tags:
- Автоматизация
- R
categories:
- Программирование
- R
description: Хотите оперативно и своевременно узнавать о сбоях в работе скриптов R? Достаточно настроить оповещения на email. В этой статье я опишу, как настроить рассылку с помощью языка R и как избежать подводных камней.
original_url: https://alexeyseleznev.wordpress.com/2017/04/06/%d0%ba%d0%b0%d0%ba-%d0%bd%d0%b0%d1%81%d1%82%d1%80%d0%be%d0%b8%d1%82%d1%8c-%d0%be%d1%82%d0%bf%d1%80%d0%b0%d0%b2%d0%ba%d1%83-%d0%bf%d0%b8%d1%81%d0%b5%d0%bc-%d1%81-%d0%bf%d0%be%d0%bc%d0%be%d1%89%d1%8c/
wp_id: 715
draft: false
---

Хотите оперативно и своевременно узнавать о сбоях в работе скриптов R? Достаточно настроить оповещения на email. В этой статье я опишу, как настроить рассылку с помощью [языка R](https://netpeak.net/ru/blog/kak-nastroit-zapusk-r-skripta-po-raspisaniyu/) и как избежать подводных камней.

![Как выбрать пакет R для отправки email](../images/kak-nastroit-otpravku-pisem-s-pomosch-kak-vybrat-paket-r-dla-9799984a.webp)

Что можно отправлять в письмах:

- отчеты по результату работы скрипта на свою почту или по списку конкретных email-адресов;
- сообщения об ошибках, которые возникли в работе скриптов;
- файлы с локального диска, например, фотографию или CSV-документ.

Чтобы настроить отправку писем, потребуется:

- [язык R](https://cran.r-project.org/bin/windows/base/);
- интегрированная среда разработки [RStudio](https://www.rstudio.com/products/rstudio/download/).

## Как выбрать пакет R для отправки email?

Для отправки писем существует несколько пакетов. При выборе подходящего учитывайте:

- нужна ли аутентификация в почтовом сервисе;
- пользователям каких почтовых ящиков будете отправлять сообщения.

Рассмотрим подробнее плюсы и минусы пакетов «sendmailR» и «mailR».

### 1. Пакет «[sendmailR](https://cran.r-project.org/web/packages/sendmailR/index.html)»

Этот пакет не поддерживает процедуру аутентификации, а значит, можно отправлять письма не из всех почтовых сервисов. Более того, сервисы, позволяющие рассылать письма без аутентификации, накладывают определенные ограничения. К примеру, SMTP сервер для Gmail (ASPMX.L.GOOGLE.COM) не требует аутентификации, но отправлять сообщения можно только пользователям Gmail или G Suite.

Преимущество «sendmailR» в том, что этот пакет достаточно прост в установке, не требуется дополнительное программное обеспечение.

### 2. Пакет «[mailR](https://github.com/rpremraj/mailR)»

Пакет поддерживает аутентификацию, письма отправляются из любых почтовых сервисов.

Сложности могут возникнуть в связи с тем, что для работы пакета требуется установка Java.

Если нужно провести рассылку исключительно по пользователям Gmail или G Suite и при этом аутентификация необязательна — без особых раздумий пользуйтесь пакетом «**sendmailR»**, в противном случае — выбирайте «**mailR»*****.***

## Как установить пакет «sendmailR»?

1. Для установки пакета откройте RStudio и в области «Source» вставьте код:

```

#Установка пакета
install.packages("sendmailR")

#Подключение пакета
library(sendmailR)
```

Если вы впервыв запустили RStudio, воспользуйтесь сочетанием клавиш «Ctrl+«Alt+Shift+0», чтобы появилась панель «Source».

![Как установить пакет «sendmailR»](../images/kak-nastroit-otpravku-pisem-s-pomosch-kak-ustanovit-paket-se-4aec541c.webp)

2. Чтобы настроить отправку писем, подставьте ваши данные в код ниже:

```markup

```

```

from = "<sender@gmail.com>"
to = c("<recipient1@gmail.com>","<recipient2@gmail.com>")
subject <- “My first test letter”
body    <- (“It`s my first letter from R by sendmailR package!” ,mime_part(iris))
sendmail(from=from,to=to,subject=subject,msg=body,control=list(smtpServer="ASPMX.L.GOOGLE.COM"))
```

```markup

```

2.1. Вместо «sender@gmail.com» впишите адрес своей Gmail-почты, вместо «recipient1@gmail.com» и «recipient2@gmail.com» — адреса получателей. Помните, что с SMTP сервера ASPMX.L.GOOGLE.COM можно рассылать письма только пользователям Gmail и G Suite,

2.2. В «subject» впишите тему письма,

2.3. Объект «body» содержит тело письма. В теле письма может быть не только текст («It`s my first letter from R by sendmailR package!»), но и вложения, например, встроенная R-таблица «iris».

2.4. Команда «sendmail» отправляет письмо. При проверке почты в первую очередь посмотрите папку «Спам»: из-за того, что вы отправили email без аутентификации и предварительно не настроили фильтр на почте, письмо сначала, скорее всего, попадет в спам.

## Как установить пакет «mailR»?

1. Скачайте и установите версию Java, соответствующую разрядности на вашем компьютере.

Для 32-разрядной операционной системы скачайте Java по [ссылке](https://java.com/ru/download/).

Если у вас 64-разрядная ОС, рекомендую скачать нужную версию из [стороннего ресурса](http://softprime.net/razrabotchikam/278-java-runtime-environment-dlya-kompyutera.html). На официальном сайте указано, что 64-битную Java можно скачать только через 64-разрядную версию браузера — я пробовал этот способ и не получил нужный результат.

2. Далее нужно установить пакеты [«rJava»](https://cran.r-project.org/web/packages/rJava/index.html) и «mailR»:

```markup

```

```

#Установка пакета
install.packages("rJava")
install.packages("mailR")

#Подключение пакета
library(mailR)
```

```markup

```

При запуске кода может появиться следующая ошибка:

*Error: .onLoad failed in loadNamespace() for ‘rJava’, details: call: fun(libname, pkgname) error: JAVA\_HOME cannot be determined from the Registry*

Рассмотрим возможные причины:

2.1. Разрядность установленной Java не соответствует текущей версии Windows. Обычно подобная ошибка возникает, если у вас 64-разрядная ОС.

Как определить, какую версию Java вы используете? Проверьте системный диск Windows: для установки программного обеспечения по умолчанию используются две папки, расположенные в корне системного диска. Если папка «Java» появилась в «Program Files» — это 64-разрядная версия, а если в папке «Program Files (x86)» — 32-разрядная.

2.2. Вторая причина ошибки: в R не прописана или неверно прописана опция «JAVA\_HOME». Чтобы устранить ошибку, запустите в R команды:

- - для 32-разрядной ОС:

```markup

```

```

Sys.setenv(JAVA_HOME='C:\\Program Files (x86)\\Java\\jre1.8.0_102')
```

```markup

```

- - для 64-разрядной ОС:

```markup

```

```

Sys.setenv(JAVA_HOME='C:\\Program Files\\Java\\jre1.8.0_102')
```

```markup

```

Перед запуском команды замените **«jre1.8.0\_102»** на название файла Java, установленного на вашем клмпьютере. Файл можно найти в одноименной папке «Java», о которой я упоминал в предыдущем пункте.

3. Далее нужно определить, требует ли ваш SMTP-сервер прохождения аутентификации, и в зависимости от этого выбрать подходящий код для отправки писем.

3.1. Для отправки писем **без процедуры аутентификации** в код подставьте данные:

- тема и тело письма;
- отправитель и получатели;
- параметры SMTP-сервера.

```markup

```

```

library(mailR)
send.mail(from = "sender@gmail.com",
         to = c("Recipient 1 <recipient1@gmail.com>", "recipient2@gmail.com"),
         cc = c("CC Recipient <cc.recipient@gmail.com>"),
         bcc = c("BCC Recipient <bcc.recipient@gmail.com>"),
         subject = "Subject of the email",
         body = "Body of the email",
         smtp = list(host.name = "aspmx.l.google.com", port = 25),
         authenticate = FALSE,
         send = TRUE)
```

```markup

```

3.2. Чтобы отправить письмо через SMTP с прохождением аутентификации, используйте код:

```markup

```

```

library(mailR)
send.mail(from = "sender@gmail.com",
         to = c("recipient1@gmail.com", "Recipient 2 <recipient2@gmail.com>"),
         replyTo = c("Reply to someone else <someone.else@gmail.com>")
         subject = "Subject of the email",
         body = "Body of the email",
         smtp = list(host.name = "smtp.gmail.com", port = 465, user.name = "gmail_username", passwd = "password", ssl = TRUE),
         authenticate = TRUE,
         send = TRUE)
```

```markup

```

Аргумент «smtp» содержит все параметры SMTP сервера и в нем необходимо указать учетные данные.

## Как отправлять письма с текстом на русском языке?

Если вы используете пакет «mailR» и хотите, чтобы ваши письма содержали в теме или теле кириллические символы, воспользуйтесь аргументом «encoding» и укажите кодировку «utf-8».

```markup

```

```

library(mailR)
send.mail(from = "Sender Name <sender@gmail.com>",
                  to = "recipient@gmail.com",
                  subject = "Тема тестового письма на русском языке.",
                  body = "Русскоязычное тело письма!",
                  encoding = "utf-8",
                  smtp = list(host.name = "smtp.gmail.com", port = 465, user.name = "gmail_username", passwd = "password", ssl = T),
              authenticate = TRUE,
                  send = TRUE)
```

```markup

```

Для отправки русскоязычного текста с помощью пакета «sendmailR» необходимо предварительно дважды перекодировать этот текст в UTF-8.

```markup

```

```

library(sendmailR)
from = "<sender@gmail.com>"
to = c("<recipient1@gmail.com>","<recipient2@gmail.com>")
subject <- iconv(iconv('Тема письма',to = "UTF-8"),to = "UTF-8")
body    <- iconv(iconv('Тело письма',to = "UTF-8"),to = "UTF-8")
sendmail(from=from,to=to,subject=subject,msg=body,control=list(smtpServer="ASPMX.L.GOOGLE.COM"))
```

```markup

```

## Как отправлять письма в формате HTML?

Для отправки сообщений в HTML-формате с помощью пакета «mailR» достаточно воспользоваться аргументом «html»:

```markup

```

```

library(mailR)
send.mail(from = "sender@gmail.com",
         to = c("recipient1@gmail.com", "recipient2@gmail.com"),
         subject = "Subject of the email",
         body = "<span class="token tag"><span class="token tag"><span class="token punctuation"><</span>html</span><span class="token punctuation">></span></span>The apache logo - <img src=\"http://www.apache.org/images/asf_logo_wide.gif\"><span class="token tag"><span class="token tag"><span class="token punctuation"></</span>html</span><span class="token punctuation">></span></span>",
         html = TRUE,
         smtp = list(host.name = "smtp.gmail.com", port = 465, user.name = "gmail_username", passwd = "password", ssl = TRUE),
         authenticate = TRUE,
         send = TRUE)
```

```markup

```

Для отправки письма в HTML-формате с помощью пакета «sendmailR» используйте такой код:

```markup

```

```

library(sendmailR)
msg <- mime_part('<span class="token doctype"><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"></span>
<span class="token tag"><span class="token tag"><span class="token punctuation"><</span>html</span> <span class="token attr-name">xmlns</span><span class="token attr-value"><span class="token punctuation">=</span><span class="token punctuation">"</span>http://www.w3.org/1999/xhtml<span class="token punctuation">"</span></span><span class="token punctuation">></span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation"><</span>head</span><span class="token punctuation">></span></span>
 <span class="token tag"><span class="token tag"><span class="token punctuation"><</span>meta</span> <span class="token attr-name">http-equiv</span><span class="token attr-value"><span class="token punctuation">=</span><span class="token punctuation">"</span>Content-Type<span class="token punctuation">"</span></span> <span class="token attr-name">content</span><span class="token attr-value"><span class="token punctuation">=</span><span class="token punctuation">"</span>text/html; charset<span class="token punctuation">=</span>utf-8<span class="token punctuation">"</span></span> <span class="token punctuation">/></span></span>
 <span class="token tag"><span class="token tag"><span class="token punctuation"><</span>meta</span> <span class="token attr-name">name</span><span class="token attr-value"><span class="token punctuation">=</span><span class="token punctuation">"</span>viewport<span class="token punctuation">"</span></span> <span class="token attr-name">content</span><span class="token attr-value"><span class="token punctuation">=</span><span class="token punctuation">"</span>width<span class="token punctuation">=</span>device-width, initial-scale<span class="token punctuation">=</span>1.0<span class="token punctuation">"</span></span><span class="token punctuation">/></span></span>
 <span class="token tag"><span class="token tag"><span class="token punctuation"><</span>title</span><span class="token punctuation">></span></span>HTML demo<span class="token tag"><span class="token tag"><span class="token punctuation"></</span>title</span><span class="token punctuation">></span></span>
 <span class="token tag"><span class="token tag"><span class="token punctuation"><</span>style</span> <span class="token attr-name">type</span><span class="token attr-value"><span class="token punctuation">=</span><span class="token punctuation">"</span>text/css<span class="token punctuation">"</span></span><span class="token punctuation">></span></span>
 <span class="token tag"><span class="token tag"><span class="token punctuation"></</span>style</span><span class="token punctuation">></span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation"></</span>head</span><span class="token punctuation">></span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation"><</span>body</span><span class="token punctuation">></span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation"><</span>h1</span><span class="token punctuation">></span></span>HTML demo<span class="token tag"><span class="token tag"><span class="token punctuation"></</span>h1</span><span class="token punctuation">></span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation"></</span>body</span><span class="token punctuation">></span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation"></</span>html</span><span class="token punctuation">></span></span>')

msg[["headers"]][["Content-Type"]] <- "text/html"

from = "<sender@gmail.com>"
to = c("<recipient1@gmail.com>","<recipient2@gmail.com>")
subject <- "HTML test"
body    <- list(msg)
sendmail(from=from,to=to,subject=subject,msg=body,control=list(smtpServer="ASPMX.L.GOOGLE.COM"))
```

```markup

```

## Как отправить в теле письма HTML-таблицу?

Самый простой способ — использовать пакет «htmlTable». Приведу примеры преобразования встроенной в R-таблицы «iris» в HTML-формат и добавление ее в тело письма.

Код для пакета «mailR»:

```markup

```

```

iris_html <- htmlTable(iris)
library(mailR)
send.mail(from = "sender@gmail.com",
         to = c("recipient1@gmail.com", "recipient2@gmail.com"),
         subject = "Subject of the email",
         body = iris_html,
         html = TRUE,
         smtp = list(host.name = "smtp.gmail.com", port = 465, user.name = "gmail_username", passwd = "password", ssl = TRUE),
         authenticate = TRUE,
         send = TRUE)
```

```markup

```

Пример для «sendmailR»:

```markup

```

```

library(sendmailR)

iris_html <- htmlTable(iris)

msg <- mime_part(paste0('<span class="token doctype"><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0                 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"></span>
                <span class="token tag"><span class="token tag"><span class="token punctuation"><</span>html</span> <span class="token attr-name">xmlns</span><span class="token attr-value"><span class="token punctuation">=</span><span class="token punctuation">"</span>http://www.w3.org/1999/xhtml<span class="token punctuation">"</span></span><span class="token punctuation">></span></span>
                <span class="token tag"><span class="token tag"><span class="token punctuation"><</span>head</span><span class="token punctuation">></span></span>
                <span class="token tag"><span class="token tag"><span class="token punctuation"><</span>meta</span> <span class="token attr-name">http-equiv</span><span class="token attr-value"><span class="token punctuation">=</span><span class="token punctuation">"</span>Content-Type<span class="token punctuation">"</span></span> <span class="token attr-name">content</span><span class="token attr-value"><span class="token punctuation">=</span><span class="token punctuation">"</span>text/html; charset<span class="token punctuation">=</span>utf-8<span class="token punctuation">"</span></span> <span class="token punctuation">/></span></span>
                <span class="token tag"><span class="token tag"><span class="token punctuation"><</span>meta</span> <span class="token attr-name">name</span><span class="token attr-value"><span class="token punctuation">=</span><span class="token punctuation">"</span>viewport<span class="token punctuation">"</span></span> <span class="token attr-name">content</span><span class="token attr-value"><span class="token punctuation">=</span><span class="token punctuation">"</span>width<span class="token punctuation">=</span>device-width, initial-scale<span class="token punctuation">=</span>1.0<span class="token punctuation">"</span></span><span class="token punctuation">/></span></span>
                <span class="token tag"><span class="token tag"><span class="token punctuation"><</span>title</span><span class="token punctuation">></span></span>HTML table demo<span class="token tag"><span class="token tag"><span class="token punctuation"></</span>title</span><span class="token punctuation">></span></span>
                <span class="token tag"><span class="token tag"><span class="token punctuation"><</span>style</span> <span class="token attr-name">type</span><span class="token attr-value"><span class="token punctuation">=</span><span class="token punctuation">"</span>text/css<span class="token punctuation">"</span></span><span class="token punctuation">></span></span>
                <span class="token tag"><span class="token tag"><span class="token punctuation"></</span>style</span><span class="token punctuation">></span></span>
                <span class="token tag"><span class="token tag"><span class="token punctuation"></</span>head</span><span class="token punctuation">></span></span>
                <span class="token tag"><span class="token tag"><span class="token punctuation"><</span>body</span><span class="token punctuation">></span></span>
                <span class="token tag"><span class="token tag"><span class="token punctuation"><</span>h1</span><span class="token punctuation">></span></span>My table iris<span class="token tag"><span class="token tag"><span class="token punctuation"></</span>h1</span><span class="token punctuation">></span></span>',
                iris_html ,'
                <span class="token tag"><span class="token tag"><span class="token punctuation"></</span>body</span><span class="token punctuation">></span></span>
                <span class="token tag"><span class="token tag"><span class="token punctuation"></</span>html</span><span class="token punctuation">></span></span>'))

msg[["headers"]][["Content-Type"]] <- "text/html"

from = "<sender@gmail.com>"
to = c("<recipient1@gmail.com>","<recipient2@gmail.com>")
subject <- "HTML test"
body    <- list(msg)
sendmail(from=from,to=to,subject=subject,msg=body,control=list(smtpServer="ASPMX.L.GOOGLE.COM"))
```

```markup

```

Так же легко преобразовать любую таблицу из R в HTML-формат и отправлять ее в письме.

## Выводы

Язык R достаточно мощный, чтобы [автоматизировать](https://netpeak.net/ru/blog/kak-my-vnedrili-bi-analitiku-v-otdele-kontekstnoi-reklamy/) практически любой процесс работы с данными. Чтобы получать отчеты о работе скриптов или уведомления об ошибках, выберите подходящий пакет R и настройте рассылку.

1. Пакет «sendmailR» прост в установке, но не поддерживает процедуру аутентификации, и вы сможете отправлять письма только пользователям Gmail или G Suite.
2. Пакет «mailR» поддерживает аутентификацию, но в процессе его установки вам также придется инсталлировать Java.
3. С помощью языка R можно настроить не только отправку простых текстовых сообщений, но и письма:
   - с текстом на кириллице;
   - в формате HTML;
   - с HTML-таблицей в теле.

---

*[Оригинал публикации на блоге Netpeak.](https://netpeak.net/ru/blog/kak-nastroit-otpravku-pisem-s-pomoshch-yu-yazyka-r/)*
