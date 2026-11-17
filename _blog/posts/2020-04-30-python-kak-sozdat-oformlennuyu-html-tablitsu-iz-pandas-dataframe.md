---
title: 'Python: Как создать оформленную HTML таблицу из pandas DataFrame'
date: '2020-04-30'
slug: python-kak-sozdat-oformlennuyu-html-tablitsu-iz-pandas-dataframe
tags:
- Обработка данных
- Python
categories:
- Программирование
- Python
description: Как преобразовать pandas DataFrame в HTML таблицу для отправки электронном письме.
original_url: https://alexeyseleznev.wordpress.com/2020/04/30/python-%d0%ba%d0%b0%d0%ba-%d1%81%d0%be%d0%b7%d0%b4%d0%b0%d1%82%d1%8c-%d0%be%d1%84%d0%be%d1%80%d0%bc%d0%bb%d0%b5%d0%bd%d0%bd%d1%83%d1%8e-html-%d1%82%d0%b0%d0%b1%d0%bb%d0%b8%d1%86%d1%83-%d0%b8%d0%b7-pa/
wp_id: 1343
draft: false
cover: ../images/python-kak-sozdat-oformlennuyu-html-tablitsu-iz-pa-analytics-66323049.webp
---

Мы в Netpeak довольно активно используем дайджесты, это такие небольшие, информационные письма с таблицами и графиками которые помогают нам в общей массе информации контролировать основные показатели бизнеса, а каждому сотруднику выполнение его KPI.

Более подробно о том, что такое дайжесты и как мы их используем я уже рассказывал на GoAnalytics в 2019 году. Кому это интересно по [ссылке](https://youtu.be/fLP0gbsYF1k) доступна запись доклада.

В этой статье речь пойдёт о технической реализации таких писем на Python, а не о самих дайджестах.

Переводим pandas DataFrame в HTML таблицу с применением CSS стилей

По сути письмо – это HTML документ, и для того, что бы в него включить таблицу созданную с помощью `pandas`, её предварительно необходимо преобразовать в HTML формат. В `pandas` есть встроенный метод `to_html()` который выполняет эту операцию, но форматирование таблицы в таком виде оставляет желать лучшего.

## Метод `to_html()`

Для начала давайте создадим тестовый DataFrame, и воспользуемся стандартным методом, для конвертации его в HTML таблицу.

```

import pandas as pd

data = {'name': ['Alex', 'Nick', 'John', 'Tom'], 'val': [1024, 789, 1002, 987]}
df = pd.DataFrame.from_dict(data)

df.to_html()
```

Наш DataFrame при этом будет конвертирован вот в такую HTML таблицу.

![](https://i0.wp.com/img.netpeak.ua/alsey/158825692938_kiss_2kb.png)

Вроде и получилось то, что хотели, но выглядит мягко говоря так себе.

## Метод `style`

Есть внутренние возможности по приведению этой таблицы в порядок с помощью метода `style`, ознакомится с ними можно в [официальной документации](https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html). Но на самом деле его возможности ограничены, и он не очень удобен.

## Аргумент `classes`

Второй вариант прописывать CSS стили в отдельном файле, и использовать аргумент `classes` метода `to_html()`, пример реализации можно подсмотреть на [stackowerflof](https://stackoverflow.com/questions/50807744/apply-css-class-to-pandas-dataframe-using-to-html/50939211).

Если вкратце, вы создаёте файл с описанием CSS стилей, например такой:

```

/* includes alternating gray and white with on-hover color */

.mystyle {
    font-size: 11pt; 
    font-family: Arial;
    border-collapse: collapse; 
    border: 1px solid silver;

}

.mystyle td, th {
    padding: 5px;
}

.mystyle tr:nth-child(even) {
    background: #E0E0E0;
}

.mystyle tr:hover {
    background: silver;
    cursor: pointer;
}
```

Сохраняем этот CSS код в файл df\_style.css, в нашей рабочей директории.

Далее создаём каркас HTML страницы, в которую добавим наш DataFrame с применёнными CSS стилями.

```

html_string = '''
<html>
  <head><title>HTML Pandas Dataframe with CSS</title></head>
  <link rel="stylesheet" type="text/css" href="df_style.css"/>
  <body>
    {table}
  </body>
</html>
'''
```

Далее применяем к нашему DataFrame метод `to_html()` используя аргумент `classes`, и с помощью `format()` внедряем полученную HTML таблиц в созданный ранее каркас.

```

html_string.format(table=df.to_html(classes='mystyle'))
```

На выходе получим вот такую таблицу HTML таблицу:

![](https://i0.wp.com/img.netpeak.ua/alsey/158825695815_kiss_2kb.png)

Такая таблица выглядит уже значительно привлекательнее, но есть одна проблема, большинство почтовых сервисов, включая Gmail при отображении таблиц в письмах вырезают тег style, поэтому в письме всё равно ваша таблица будет выглядеть так же как и первый вариант, приведённый в статье в описании метода `to_html()`.

## Библиотека pretty-html-table

Мы уже рассмотрели несколько способов привести DataFrame в формат HTML таблицы, но все они к сожалению имеют ряд недостатков.

Наиболее удобным и универсальным способом превратить DataFrame в элементную HTML таблицу предоставляет библиотека `pretty-html-table`.

Для начала её надо установить, откройте командную строку, или терминал, в зависимости от вашей операционной системы и выполните следую команду.

```

pip install pretty-html-table
```

Далее возвращаемся в python, и используем метод `build_table()` для создания HTML таблицы.

```

pretty_html_table.build_table(df, 'blue_light')
```

В результате получим вот такую HTML таблицу:

![](https://i0.wp.com/img.netpeak.ua/alsey/158825699043_kiss_2kb.png)

Преимущество библиотеки `pretty-html-table` не только в том, что она создаёт более привлекательные таблицы, но и в том, что она применяет стили к каждому элементу таблицы. В этом случае все почтовые сервисы отображают ваши HTML таблиц корректно.

Как вы заметили аргумент `color` метода `build_table()` отвечает за цветовую схему вашей таблицы, на данный момент вы можете применять одну из следующих цветовых схем:

| Name | font style | Header | Rows |
| --- | --- | --- | --- |
| ‘blue\_light’ | Century Gothic | Bold: yes / Background color: white / Font color: dark blue | Odd background color: light blue / Even background color: white |
| blue\_dark’ | Century Gothic | Bold: yes / Background color: dark blue / Font color: white | Odd background color: light blue / Even background color: white |
| grey\_light’ | Century Gothic | Bold: yes / Background color: white / Font color: dark grey | Odd background color: light grey / Even background color: white |
| grey\_dark’ | Century Gothic | Bold: yes / Background color: dark grey / Font color: white | Odd background color: light grey / Even background color: white |
| orange\_light’ | Century Gothic | Bold: yes / Background color: white / Font color: dark orange | Odd background color: light orange / Even background color: white |
| orange\_dark’ | Century Gothic | Bold: yes / Background color: dark orange / Font color: white | Odd background color: light orange / Even background color: white |
| yellow\_light’ | Century Gothic | Bold: yes / Background color: white / Font color: dark yellow | Odd background color: light yellow / Even background color: white |
| yellow\_dark’ | Century Gothic | Bold: yes / Background color: dark yellow / Font color: white | Odd background color: light yellow / Even background color: white |
| green\_light’ | Century Gothic | Bold: yes / Background color: white / Font color: dark green | Odd background color: light green / Even background color: white |
| green\_dark’ | Century Gothic | Bold: yes / Background color: dark green / Font color: white | Odd background color: light green / Even background color: white |

Таблицы с описанием названий и CSS компонентов доступных стилей

Также есть некоторые дополнительные аргументы, которые помогут вам изменять стиль текста в таблице.

- `font_size` – размер текста, по умолчанию `'medium'`, возможные значения: xx-small, x-small, small, medium, large, x-large, xx-large;
- `font_family` – шрифт, по умолчанию `'Century Gothic'`;
- `text_align` – выравнивание текста, по умолчанию `'left'`.

## Отправляем отформатированную таблицу в письме

Полученную таблицу теперь не сложно добавить в текст письма:

```

import pandas as pd                             # работа с таблицами
import pretty_html_table                        # перевод DataFrame в HTML
import smtplib                                  # работа с SMTP сервером
from email.mime.multipart import MIMEMultipart  # создаём сообщение
from email.mime.text import MIMEText            # вёрстка письма

# создаём таблицу
data = {'name': ['Alex', 'Nick', 'John', 'Tom'], 'val': [1024, 789, 1002, 987]}
df = pd.DataFrame.from_dict(data)

# оформляем таблицу
html_table = pretty_html_table.build_table(df, 'blue_light')

# подключаемся к SMTP серверу
server = smtplib.SMTP('smtp.gmail.com')
server.login('email_login', 'email_password')

# создаём письмо
msg = MIMEMultipart('mixed')
msg['Subject'] = 'Письмо с текстом и таблицей'
msg['From'] = 'your_email@email.com'
msg['To'] = 'recipient@email.com'
      
#добавляем в письмо текст и таблицу
main_table = MIMEText('<h3>Ниже наша тестовая таблица</h3>', 'html')
html_table = MIMEText(html_table, 'html')

msg.attach(main_table)
msg.attach(html_table)

# отправляем письмо
server.send_message(msg)

# отключаемся от SMTP сервера
server.quit()
```

В приведённом примере кода подставьте свои значения вместо:

- **smtp.gmail.com** – адресс SMTP сервера Gmail, если используете другой почтовый сервер необходимо его заменить в коде
- **email\_login** – ваш логин в постовом сервере
- **email\_password** – пароль от почты
- **your\_email@email.com** – ваш адрес электронной почты
- **recipient@email.com** – электронный адрес получателей, можно через запятую перечислить несколько адресов

В результате выполнения кода вы отправите на указанные адреса следующее письмо:

![](https://i0.wp.com/img.netpeak.ua/alsey/158825731682_kiss_21kb.png)

Пример готового письма
