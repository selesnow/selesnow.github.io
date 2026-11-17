---
title: 'Пишем telegram бота на языке R (часть 3): Как добавить боту поддержку клавиатуры'
date: '2021-06-01'
slug: pishem-telegram-bota-na-yazyke-r-chast-3-kak-dobavit-botu-podderzhku-k
tags:
- API
- Telegram
- R
categories:
- Программирование
- R
description: Это третья статья из серии “Пишем telegram бота на языке R”. В предыдущих публикациях мы научились создавать телеграм бота, отправлять через него сообщения, добавили боту команды и фильтры сообщений. Поэтому перед тем как приступить к чтению данной статьи я крайне рекомендую ознакомиться с предыдущими, т.к. тут я уже не буду останавливать на описанных ранее основах ботостроения. […]
original_url: https://alexeyseleznev.wordpress.com/2021/06/01/%d0%bf%d0%b8%d1%88%d0%b5%d0%bc-telegram-%d0%b1%d0%be%d1%82%d0%b0-%d0%bd%d0%b0-%d1%8f%d0%b7%d1%8b%d0%ba%d0%b5-r-%d1%87%d0%b0%d1%81%d1%82%d1%8c-3-%d0%ba%d0%b0%d0%ba-%d0%b4%d0%be%d0%b1%d0%b0%d0%b2/
wp_id: 1497
draft: false
---

Это третья статья из серии “Пишем telegram бота на языке R”. В предыдущих публикациях мы научились создавать телеграм бота, отправлять через него сообщения, добавили боту команды и фильтры сообщений. Поэтому перед тем как приступить к чтению данной статьи я крайне рекомендую ознакомиться с [предыдущими](https://habr.com/ru/post/516908/#vse-stati-iz-serii-pishem-telegram-bota-na-yazyke-r), т.к. тут я уже не буду останавливать на описанных ранее основах ботостроения.

В этой статье мы повысим юзабилити нашего бота за счёт добавления клавиатуры, которая сделает интерфейс бота интуитивно понятным, и простым в использовании.

![](../images/pishem-telegram-bota-na-yazyke-r-chast-3-kak-dobav-xvxzt04r-2cf02d84.webp)

# Все статьи из серии “Пишем telegram бота на языке R”

1. [Создаём бота, и отправляем с его помощью сообщения в telegram](https://habr.com/ru/post/511222/)
2. [Добавляем боту поддержку команд и фильтры сообщений](https://habr.com/ru/post/515148/)
3. [Как добавить боту поддержку клавиатуры](https://habr.com/ru/post/516908/)
4. [Построение последовательного, логического диалога с ботом](https://habr.com/ru/post/518470/)
5. [Управление правами пользователей бота](https://habr.com/ru/post/520208/)

# Содержание

*Если вы интересуетесь анализом данных возможно вам будут интересны мои [telegram](https://t.me/R4marketing) и [youtube](https://www.youtube.com/R4marketing/?sub_confirmation=1) каналы. Большая часть контента которых посвящены языку R.*

1. Какие типы клавиатур поддерживает телеграм бот
2. Reply клавиатура
3. Inline клавиатура  
   3.1. Пример простейшего бота с поддержкой InLine кнопок  
   3.2. Пример бота, который сообщает текущую погоду по выбранному городу  
   3.3. Пример бота, который выводит список самых свежих статей со ссылками по-указанному Хабу из habr.com
4. Заключение

# Какие типы клавиатур поддерживает телеграм бот

На момент написания статьи `telegram.bot` позволяет вам создать клавиатуры двух типов:

- Reply — Основная, обычная клавиатура, которая находится под панелью ввода текста сообщения. Такая клавиатура просто отправляет боту текстовое сообщение, и в качестве текста отправит тот текст, который написан на самой кнопке.
- Inline — Клавиатура привязанная к конкретному сообщению бота. Данная клавиатура отправляет боту данные, привязанные к нажатой кнопке, эти данные могут отличаться от текста, написанного на самой кнопке. И обрабатываются такие кнопки через **CallbackQueryHandler**.

Для того, что бы бот открыл клавиатуру необходимо при отправке сообщения через метод `sendMessage()`, передать созданную ранее клавиатуру в аргумент `reply_markup`.

Ниже мы разберём несколько примеров.

# Reply клавиатура

Как я уже писал выше, это основная клавиатура управления ботом.  
**Пример создания Reply клавиатуры из официальной справки**

```
bot <- Bot(token = "TOKEN")
chat_id <- "CHAT_ID"

# Create Custom Keyboard
text <- "Aren't those custom keyboards cool?"
RKM <- ReplyKeyboardMarkup(
  keyboard = list(
    list(KeyboardButton("Yes, they certainly are!")),
    list(KeyboardButton("I'm not quite sure")),
    list(KeyboardButton("No..."))
  ),
  resize_keyboard = FALSE,
  one_time_keyboard = TRUE
)

# Send Custom Keyboard
bot$sendMessage(chat_id, text, reply_markup = RKM)
```

Выше приведён пример из официальной справки пакета `telegram.bot`. Для создания клавиатуры используется функция `ReplyKeyboardMarkup()`, которая в свою очередь принимает список списков кнопок, которые создаются функцией `KeyboardButton()`.

Почему в `ReplyKeyboardMarkup()` необходимо передавать не просто список, а список списков? Дело в том, что вы передаёте основной список, и в нём отдельными списками вы задаёте каждый ряд кнопок, т.к. в один ряд можно расположить несколько кнопок.

Аргумент `resize_keyboard` позволяет автоматически подбирать оптимальный размер кнопок клавиатуры, а аргумент `one_time_keyboard` позволяет скрывать клавиатуру после каждого нажатия на кнопку.

Давайте напишем простейшего бота, у которого будет 3 кнопки:

- Чат ID — Запросить чат ID диалога с ботом
- Моё имя — Запросить своё имя
- Мой логин — Запросить своё имя пользователя в телеграм

**Код 1: Простой бот с Reply клавиатурой**

```
library(telegram.bot)

# создаём экземпляр класса Updater
updater <- Updater('ТОКЕН ВАШЕГО БОТА')

# создаём методы
## метод для запуска клавиатуры
start <- function(bot, update) {

  # создаём клавиатуру
  RKM <- ReplyKeyboardMarkup(
    keyboard = list(
      list(KeyboardButton("Чат ID")),
      list(KeyboardButton("Моё имя")),
      list(KeyboardButton("Мой логин"))
    ),
    resize_keyboard = FALSE,
    one_time_keyboard = TRUE
  )

  # отправляем клавиатуру
  bot$sendMessage(update$message$chat_id,
                  text = 'Выберите команду', 
                  reply_markup = RKM)

}

## метод возвразающий id чата
chat_id <- function(bot, update) {

  bot$sendMessage(update$message$chat_id, 
                  text = paste0("Чат id этого диалога: ", update$message$chat_id),
                  parse_mode = "Markdown")

}

## метод возвращающий имя
my_name <- function(bot, update) {

  bot$sendMessage(update$message$chat_id, 
                  text = paste0("Вас зовут ", update$message$from$first_name),
                  parse_mode = "Markdown")

}

## метод возвращающий логин
my_username <- function(bot, update) {

  bot$sendMessage(update$message$chat_id, 
                  text = paste0("Ваш логин ", update$message$from$username),
                  parse_mode = "Markdown")

}

# создаём фильтры
## сообщения с текстом Чат ID
MessageFilters$chat_id <- BaseFilter(function(message) {

  # проверяем текст сообщения
  message$text == "Чат ID"

}
)

## сообщения с текстом Моё имя
MessageFilters$name <- BaseFilter(function(message) {

  # проверяем текст сообщения
  message$text == "Моё имя"

}
)

## сообщения с текстом Мой логин
MessageFilters$username <- BaseFilter(function(message) {

  # проверяем текст сообщения
  message$text == "Мой логин"
)

# создаём обработчики
h_start    <- CommandHandler('start', start)
h_chat_id  <- MessageHandler(chat_id, filters = MessageFilters$chat_id)
h_name     <- MessageHandler(my_name, filters = MessageFilters$name)
h_username <- MessageHandler(my_username, filters = MessageFilters$username)

# добавляем обработчики в диспетчер
updater <- updater + 
            h_start +
            h_chat_id +
            h_name +
            h_username

# запускаем бота 
updater$start_polling()
```

> Запустите приведённый выше пример кода, предварительно заменив ‘ТОКЕН ВАШЕГО БОТА’ на реальный токен, который вы получили при создании бота через *BotFather* (о создании бота я рассказывал в [первой статье](https://habr.com/ru/post/511222/#sozdanie-telegram-bota)).

После запуска задайте боту команду `/start`, т.к. именно её мы определили для запуска клавиатуры.

![](../images/pishem-telegram-bota-na-yazyke-r-chast-3-kak-dobav-eac355de2-d56c6c72.webp)

Если на данный момент вам сложно разобрать приведённый пример кода, с созданием методов, фильтров и обработчиков, то следует вернуться к предыдущей [статье](https://habr.com/ru/post/515148/), в которой я подробно всё это описал.

Мы создали 4 метода:

- start — Запуск клавиатуры
- chat\_id — Запрос идентификатора чата
- my\_name — Запрос своего имени
- my\_username — Запрос своего логина

В объект *MessageFilters* добавили 3 фильтра сообщений, по их тексту:

- chat\_id — Сообщения с текстом `"Чат ID"`
- name — Сообщения с текстом `"Моё имя"`
- username — Сообщения с текстом `"Мой логин"`

И создали 4 обработчика, которые по заданным командам и фильтрам будут выполнять указанные методы.

```
# создаём обработчики
h_start    <- CommandHandler('start', start)
h_chat_id  <- MessageHandler(chat_id, filters = MessageFilters$chat_id)
h_name     <- MessageHandler(my_name, filters = MessageFilters$name)
h_username <- MessageHandler(my_username, filters = MessageFilters$username)
```

Сама клавиатура создаётся внутри метода `start()` командой `ReplyKeyboardMarkup()`.

```
RKM <- ReplyKeyboardMarkup(
    keyboard = list(
      list(KeyboardButton("Чат ID")),
      list(KeyboardButton("Моё имя")),
      list(KeyboardButton("Мой логин"))
    ),
    resize_keyboard = FALSE,
    one_time_keyboard = TRUE
)
```

В нашем случае все кнопки мы расположили друг под другом, но мы можем расположить их в один ряд, внеся изменения в список списков кнопок. Т.к. один ряд внутри клавиатуры создаётся через вложенный список кнопок, то для того, что бы вывести наши кнопки в один ряд надо переписать часть кода по построению клавиатуры вот так:

```
RKM <- ReplyKeyboardMarkup(
    keyboard = list(
      list(
          KeyboardButton("Чат ID"),
          KeyboardButton("Моё имя"),
          KeyboardButton("Мой логин")
     )
    ),
    resize_keyboard = FALSE,
    one_time_keyboard = TRUE
)
```

![](../images/pishem-telegram-bota-na-yazyke-r-chast-3-kak-dobav-65127916c-c925cff0.webp)

Отправляется клавиатура в чат методом `sendMessage()`, в аргументе `reply_markup`.

```
  bot$sendMessage(update$message$chat_id,
                  text = 'Выберите команду', 
                  reply_markup = RKM)
```

# Inline клавиатура

Как я уже писал выше, Inline клавиатура привязана к конкретному сообщению. С ней работать несколько сложнее чем с основной клавиатурой.

Изначально вам необходимо добавить боту метод, для вызова Inline клавиатуры.

Для ответа на нажатие Inline кнопки также можно использовать метод бота `answerCallbackQuery()`, который может вывести уведомление в интерфейсе telegram, пользователю нажавшему Inline кнопку.

Данные отправленные с Inline кнопки не являются текстом, поэтому для их обработки необходимо создать специальный обработчик с помощью команды `CallbackQueryHandler()`.

Код построения Inline клавиатуры который приводится в официальной справке пакета `telegram.bot`.  
**Код построения Inline клавиатуры из официальной справки**

```
# Initialize bot
bot <- Bot(token = "TOKEN")
chat_id <- "CHAT_ID"

# Create Inline Keyboard
text <- "Could you type their phone number, please?"
IKM <- InlineKeyboardMarkup(
  inline_keyboard = list(
    list(
      InlineKeyboardButton(1),
      InlineKeyboardButton(2),
      InlineKeyboardButton(3)
    ),
    list(
      InlineKeyboardButton(4),
      InlineKeyboardButton(5),
      InlineKeyboardButton(6)
    ),
    list(
      InlineKeyboardButton(7),
      InlineKeyboardButton(8),
      InlineKeyboardButton(9)
    ),
    list(
      InlineKeyboardButton("*"),
      InlineKeyboardButton(0),
      InlineKeyboardButton("#")
    )
  )
)

# Send Inline Keyboard
bot$sendMessage(chat_id, text, reply_markup = IKM)
```

Строить Inline клавиатуру необходимо с помощью команды `InlineKeyboardMarkup()`, по такому же принципу, как и Reply клавиатуру. В `InlineKeyboardMarkup()` необходимо передать список, списков Inline кнопок, каждая отдельная кнопка создаётся функцией `InlineKeyboardButton()`.

Inline кнопка может либо передавать боту какие-то данные с помощью аргумента `callback_data`, либо открывать какую-либо HTML страницу, заданную с помощью аргумента `url`.

В результате будет список, в котором каждый элемент так же является списком Inline кнопок, которые необходимо объединить в один ряд.

Далее мы рассмотрим несколько примеров ботов с Inline кнопками.

### Пример простейшего бота с поддержкой InLine кнопок

Для начала мы напишем бота для экспресс тестирования на covid-19. По команде `/test`, он будет отправлять вам клавиатуру с двумя кнопками, в зависимости от нажатой кнопки он будет присылать вам сообщение с результатами вашего тестирования.  
**Код 2: Простейший бот с Inline клавиатурой**

```
library(telegram.bot)

# создаём экземпляр класса Updater
updater <- Updater('ТОКЕН ВАШЕГО БОТА')

# метод для отправки InLine клавиатуры
test <- function(bot, update) {

  # создаём InLine клавиатуру
  IKM <- InlineKeyboardMarkup(
    inline_keyboard = list(
      list(
        InlineKeyboardButton("Да", callback_data = 'yes'),
        InlineKeyboardButton("Нет", callback_data = 'no')
      )
    )
  )

  # Отправляем клавиатуру в чат
  bot$sendMessage(update$message$chat_id, 
                  text = "Вы болете коронавирусом?", 
                  reply_markup = IKM)
}

# метод для обработки нажатия кнопки
answer_cb <- function(bot, update) {

  # полученные данные с кнопки
  data <- update$callback_query$data

  # получаем имя пользователя, нажавшего кнопку
  uname <- update$effective_user()$first_name

  # обработка результата
  if ( data == 'no' ) {

    msg <- paste0(uname, ", поздравляю, ваш тест на covid-19 отрицательный.")

  } else {

    msg <- paste0(uname, ", к сожалени ваш тест на covid-19 положительный.")

  }

  # Отправка сообщения
  bot$sendMessage(chat_id = update$from_chat_id(),
                  text = msg)

  # сообщаем боту, что запрос с кнопки принят
  bot$answerCallbackQuery(callback_query_id = update$callback_query$id) 
}

# создаём обработчики
inline_h      <- CommandHandler('test', test)
query_handler <- CallbackQueryHandler(answer_cb)

# добавляем обработчики в диспетчер
updater <- updater + inline_h + query_handler

# запускаем бота
updater$start_polling()
```

> Запустите приведённый выше пример кода, предварительно заменив ‘ТОКЕН ВАШЕГО БОТА’ на реальный токен, который вы получили при создании бота через *BotFather* (о создании бота я рассказывал в [первой статье](https://habr.com/ru/post/511222/#sozdanie-telegram-bota)).

Результат:  
![](../images/pishem-telegram-bota-na-yazyke-r-chast-3-kak-dobav-a8a74645a-b391229c.webp)

Мы создали два метода:

- *test* — Для отправки в чат Inline клавиатуры
- *answer\_cb* — Для обработки отправленных с клавиатуры данных.

Данные, которые будут отправлены с каждой кнопки задаются в аргументе `callback_data`, при создании кнопки. Получить отправленные с кнопки данные можно с помощью конструкции `update$callback_query$data`, внутри метода *answer\_cb*.

Что бы бот реагировал на Inline клавиатуру, метод *answer\_cb* обрабатывается специальным обработчиком: `CallbackQueryHandler(answer_cb)`. Который запускает указанный метод по нажатию Inline кнопки. Обработчик **CallbackQueryHandler** принимает два аргумента:

- `callback` — Метод который необходимо запустить
- `pattern` — Фильтр по данным, которые привязаны к кнопке с помощью аргумента `callback_data`.

Соответвенно с помощью аргумента `pattern` мы можем под нажатие каждой кнопки написать отдельный метод:  
**Код 3: Разделяем методы под каждую Inline кнопку**

```
library(telegram.bot)

# создаём экземпляр класса Updater
updater <- Updater('ТОКЕН ВАШЕГО БОТА')

# метод для отправки InLine клавиатуры
test <- function(bot, update) {  

  # создаём InLine клавиатуру
  IKM <- InlineKeyboardMarkup(
    inline_keyboard = list(
      list(
        InlineKeyboardButton("Да", callback_data = 'yes'),
        InlineKeyboardButton("Нет", callback_data = 'no')
      )
    )
  )

  # Отправляем клавиатуру в чат
  bot$sendMessage(update$message$chat_id, 
                  text = "Вы болете коронавирусом?", 
                  reply_markup = IKM)
}

# метод для обработки нажатия кнопки Да
answer_cb_yes <- function(bot, update) {

  # получаем имя пользователя, нажавшего кнопку
  uname <- update$effective_user()$first_name

  # обработка результата
  msg <- paste0(uname, ", к сожалени ваш текст на covid-19 положительный.")

  # Отправка сообщения
  bot$sendMessage(chat_id = update$from_chat_id(),
                  text = msg)

  # сообщаем боту, что запрос с кнопки принят
  bot$answerCallbackQuery(callback_query_id = update$callback_query$id) 
}

# метод для обработки нажатия кнопки Нет
answer_cb_no <- function(bot, update) {

  # получаем имя пользователя, нажавшего кнопку
  uname <- update$effective_user()$first_name

  msg <- paste0(uname, ", поздравляю, ваш текст на covid-19 отрицательный.")

  # Отправка сообщения
  bot$sendMessage(chat_id = update$from_chat_id(),
                  text = msg)

  # сообщаем боту, что запрос с кнопки принят
  bot$answerCallbackQuery(callback_query_id = update$callback_query$id) 
}

# создаём обработчики
inline_h          <- CommandHandler('test', test)
query_handler_yes <- CallbackQueryHandler(answer_cb_yes, pattern = 'yes')
query_handler_no  <- CallbackQueryHandler(answer_cb_no, pattern = 'no')

# добавляем обработчики в диспетчер
updater <- updater + 
            inline_h + 
            query_handler_yes +
            query_handler_no

# запускаем бота
updater$start_polling()
```

> Запустите приведённый выше пример кода, предварительно заменив ‘ТОКЕН ВАШЕГО БОТА’ на реальный токен, который вы получили при создании бота через *BotFather* (о создании бота я рассказывал в [первой статье](https://habr.com/ru/post/511222/#sozdanie-telegram-bota)).

Теперь мы написали 2 отдельных метода, т.е. по одному методу, под нажатие каждой кнопки, и использовали аргумент `pattern`, при создании их обработчиков:

```

query_handler_yes <- CallbackQueryHandler(answer_cb_yes, pattern = 'yes')
query_handler_no  <- CallbackQueryHandler(answer_cb_no, pattern = 'no')
```

Заканчивается код метода *answer\_cb* командой `bot$answerCallbackQuery(callback_query_id = update$callback_query$id)`, которая сообщает боту, что данные с inline клавиатуры получены.

### Пример бота, который сообщает текущую погоду по выбранному городу

Давайте попробуем написать бота, который запрашивает данные о погоде.

Логика его работы будет следующая. Изначально командой `/start` вы вызываете основную клавиатуру, в которой присутствует всего одна кнопка “Погода”. Нажав на эту кнопку вы получаете сообщение с Inline клавиатурой, для выбора города, по которому требуется узнать текущую погоду. Выбираете один из городов, и получаете текущую погоду.

В этом примере кода мы будем использовать несколько дополнительных пакетов:

- `httr` — пакет для работы с HTTP запросами, на основе которых построена работа с любым API. В нашем случае мы будем использовать бесплатный API [openweathermap.org](https://openweathermap.org/api).
- `stringr` — пакет для работы с текстом, в нашем случае мы будем его использовать для формирования сообщения о погоде в выбранном городе.

**Код 4: Бот, который сообщает текущую погоду по выбранному городу**

```
library(telegram.bot)
library(httr)
library(stringr)

# создаём экземпляр класса Updater
updater <- Updater('ТОКЕН ВАШЕГО БОТА')

# создаём методы
## метод для запуска основной клавиатуры
start <- function(bot, update) {

  # создаём клавиатуру
  RKM <- ReplyKeyboardMarkup(
    keyboard = list(
      list(
        KeyboardButton("Погода")
      )
    ),
    resize_keyboard = TRUE,
    one_time_keyboard = TRUE
  )

  # отправляем клавиатуру
  bot$sendMessage(update$message$chat_id,
                  text = 'Выберите команду', 
                  reply_markup = RKM)

}

## Метод вызова Inine клавиатуры
weather <- function(bot, update) {

  IKM <- InlineKeyboardMarkup(
    inline_keyboard = list(
      list(
        InlineKeyboardButton(text = 'Москва', callback_data = 'New York,us'),
        InlineKeyboardButton(text = 'Санкт-Петербург', callback_data = 'Saint Petersburg'),
        InlineKeyboardButton(text = 'Нью-Йорк', callback_data = 'New York')
      ),
      list(
        InlineKeyboardButton(text = 'Екатеринбург', callback_data = 'Yekaterinburg,ru'),
        InlineKeyboardButton(text = 'Берлин', callback_data = 'Berlin,de'),
        InlineKeyboardButton(text = 'Париж', callback_data = 'Paris,fr')
      ),
      list(
        InlineKeyboardButton(text = 'Рим', callback_data = 'Rome,it'),
        InlineKeyboardButton(text = 'Одесса', callback_data = 'Odessa,ua'),
        InlineKeyboardButton(text = 'Киев', callback_data = 'Kyiv,fr')
      ),
      list(
        InlineKeyboardButton(text = 'Токио', callback_data = 'Tokyo'),
        InlineKeyboardButton(text = 'Амстердам', callback_data = 'Amsterdam,nl'),
        InlineKeyboardButton(text = 'Вашингтон', callback_data = 'Washington,us')
      )
    )
  )

  # Send Inline Keyboard
  bot$sendMessage(chat_id = update$message$chat_id, 
                  text = "Выберите город", 
                  reply_markup = IKM)
}

# метод для сообщения погоды
answer_cb <- function(bot, update) {

  # получаем из сообщения город
  city <- update$callback_query$data

  # отправляем запрос
  ans <- GET('https://api.openweathermap.org/data/2.5/weather', 
             query = list(q     = city,
                          lang  = 'ru',
                          units = 'metric',
                          appid = '4776568ccea136ffe4cda9f1969af340')) 

  # парсим ответ
  result <- content(ans)

  # формируем сообщение
  msg <- str_glue("{result$name} погода:\n",
                  "Текущая температура: {result$main$temp}\n",
                  "Скорость ветра: {result$wind$speed}\n",
                  "Описание: {result$weather[[1]]$description}")

  # отправляем информацию о погоде
  bot$sendMessage(chat_id = update$from_chat_id(),
                  text    = msg)

  bot$answerCallbackQuery(callback_query_id = update$callback_query$id) 
}

# создаём фильтры
## сообщения с текстом Погода
MessageFilters$weather <- BaseFilter(function(message) {

  # проверяем текст сообщения
  message$text == "Погода"

}
)

# создаём обработчики
h_start         <- CommandHandler('start', start)
h_weather       <- MessageHandler(weather, filters = MessageFilters$weather)
h_query_handler <- CallbackQueryHandler(answer_cb)

# добавляем обработчики в диспетчер
updater <- updater + 
              h_start +
              h_weather +
              h_query_handler

# запускаем бота
updater$start_polling()
```

> Запустите приведённый выше пример кода, предварительно заменив ‘ТОКЕН ВАШЕГО БОТА’ на реальный токен, который вы получили при создании бота через *BotFather* (о создании бота я рассказывал в [первой статье](https://habr.com/ru/post/511222/#sozdanie-telegram-bota)).

В результате наш бот будет работать примерно так:  
![](../images/pishem-telegram-bota-na-yazyke-r-chast-3-kak-dobav-9de4a83c4-a32f89e2.webp)

Схематически данного бота можно изобрать вот так:  
![](../images/pishem-telegram-bota-na-yazyke-r-chast-3-kak-dobav-757ad9c8a-436afd61.webp)

Мы создали 3 метода, доступные внутри нашего погодного бота:

- *start* — Запуск основной клавиатуры бота
- *weather* — Запуск Inline клавиатуры для выбора города
- *answer\_cb* — Основной метод, который по заданному городу запрашивает в API погоду, и отправляет её в чат.

Метод *start* у нас запускается командой `/start`, что реализовано обработчиком `CommandHandler('start', start)`.

Для запуска метода *weather* мы создали одноимённый фильтр:

```
# создаём фильтры
## сообщения с текстом Погода
MessageFilters$weather <- BaseFilter(function(message) {

  # проверяем текст сообщения
  message$text == "Погода"

}
)
```

И вызываем этот метод следующим обработчиком сообщений: `MessageHandler(weather, filters = MessageFilters$weather)`.

И в конце концов, основной наш метод *answer\_cb* реагирует на нажатие Inline кнопок, что реализовано специальным обработчиком: `CallbackQueryHandler(answer_cb)`.

Внутри метода *answer\_cb*, мы считываем отправленные с клавиатуры данные и записываем их в переменную `city`: `city <- update$callback_query$data`. После чего запрашиваем из API данные о погоде, формируем и отправляем сообщение, и в конце концов используем метод `answerCallbackQuery` для того, что бы сообщить боту, о том, что мы обработали нажатие Inline кнопки.

### Пример бота, который выводит список самых свежих статей со ссылками по-указанному Хабу из [habr.com](https://habr.com/).

Данного бота я привожу для того, что бы показать вам, как вывести Inline кнопки которые ведут на веб страницы.

Логика данного бота схожа с предыдущим, изначально мы запускаем основную клавиатуру командой `/start`. Далее бот даёт нам на выбор список из 6 хабов, мы выбираем интересующий нас хаб, и получаем 5 самых свежих публикаций из выбранного Хаба.

Как вы понимаете, в данном случае нам необходимо получить список статей, и для этого мы будем использовать специальный пакет `habR`, который позволяет запрашивать из хабры статьи и некоторую статистику по ним в R.

Установить пакет `habR` можно только из github, для чего вам понадобится дополнительный пакет `devtools`. Для установки воспользуйтесь приведённым ниже кодом.

```

install.packages('devtools')
devtools::install_github('selesnow/habR')
```

Теперь рассмотрим код построения описанного выше бота:  
**Код 5: Бот который выводит список наиболее свежих статей по выбранному Хабу**

```
library(telegram.bot)
library(habR)

# создаём экземпляр класса Updater
updater <- Updater('ТОКЕН ВАШЕГО БОТА')

# создаём методы
## метод для запуска основной клавиатуры
start <- function(bot, update) {

  # создаём клавиатуру
  RKM <- ReplyKeyboardMarkup(
    keyboard = list(
      list(
        KeyboardButton("Список статей")
      )
    ),
    resize_keyboard = TRUE,
    one_time_keyboard = TRUE
  )

  # отправляем клавиатуру
  bot$sendMessage(update$message$chat_id,
                  text = 'Выберите команду', 
                  reply_markup = RKM)

}

## Метод вызова Inine клавиатуры
habs <- function(bot, update) {

  IKM <- InlineKeyboardMarkup(
    inline_keyboard = list(
      list(
        InlineKeyboardButton(text = 'R', callback_data = 'R'),
        InlineKeyboardButton(text = 'Data Mining', callback_data = 'data_mining'),
        InlineKeyboardButton(text = 'Data Engineering', callback_data = 'data_engineering')
      ),
      list(
        InlineKeyboardButton(text = 'Big Data', callback_data = 'bigdata'),
        InlineKeyboardButton(text = 'Python', callback_data = 'python'),
        InlineKeyboardButton(text = 'Визуализация данных', callback_data = 'data_visualization')
      )
    )
  )

  # Send Inline Keyboard
  bot$sendMessage(chat_id = update$message$chat_id, 
                  text = "Выберите Хаб", 
                  reply_markup = IKM)
}

# метод для сообщения погоды
answer_cb <- function(bot, update) {

  # получаем из сообщения город
  hub <- update$callback_query$data

  # сообщение о том, что данные по кнопке получены
  bot$answerCallbackQuery(callback_query_id = update$callback_query$id, 
                          text = 'Подождите несколько минут, запрос обрабатывается') 

  # сообщение о том, что надо подождать пока бот получит данные
  mid <- bot$sendMessage(chat_id = update$from_chat_id(),
                         text    = "Подождите несколько минут пока, я соберу данные по выбранному Хабу")

  # парсим Хабр
  posts <- head(habr_hub_posts(hub, 1), 5)

  # удаляем сообщение о том, что надо подождать
  bot$deleteMessage(update$from_chat_id(), mid$message_id) 

  # формируем список кнопок
  keys <- lapply(1:5, function(x) list(InlineKeyboardButton(posts$title[x], url = posts$link[x])))

  # формируем клавиатуру
  IKM <- InlineKeyboardMarkup(
    inline_keyboard =  keys 
    )

  # отправляем информацию о погоде
  bot$sendMessage(chat_id = update$from_chat_id(),
                  text    = paste0("5 наиболее свежих статей из Хаба ", hub),
                  reply_markup = IKM)

}

# создаём фильтры
## сообщения с текстом Погода
MessageFilters$hubs <- BaseFilter(function(message) {

  # проверяем текст сообщения
  message$text == "Список статей"

}
)

# создаём обработчики
h_start         <- CommandHandler('start', start)
h_hubs          <- MessageHandler(habs, filters = MessageFilters$hubs)
h_query_handler <- CallbackQueryHandler(answer_cb)

# добавляем обработчики в диспетчер
updater <- updater + 
  h_start +
  h_hubs  +
  h_query_handler

# запускаем бота
updater$start_polling()
```

> Запустите приведённый выше пример кода, предварительно заменив ‘ТОКЕН ВАШЕГО БОТА’ на реальный токен, который вы получили при создании бота через *BotFather* (о создании бота я рассказывал в [первой статье](https://habr.com/ru/post/511222/#sozdanie-telegram-bota)).

В итоге мы получим вот такой результат:  
![](../images/pishem-telegram-bota-na-yazyke-r-chast-3-kak-dobav-9c9ada0e5-ecdfd951.webp)

Список доступных для выбора Хабов мы вбили хардкодом, в методе `habs`:

```
## Метод вызова Inine клавиатуры
habs <- function(bot, update) {

  IKM <- InlineKeyboardMarkup(
    inline_keyboard = list(
      list(
        InlineKeyboardButton(text = 'R', callback_data = 'r'),
        InlineKeyboardButton(text = 'Data Mining', callback_data = 'data_mining'),
        InlineKeyboardButton(text = 'Data Engineering', callback_data = 'data_engineering')
      ),
      list(
        InlineKeyboardButton(text = 'Big Data', callback_data = 'bigdata'),
        InlineKeyboardButton(text = 'Python', callback_data = 'python'),
        InlineKeyboardButton(text = 'Визуализация данных', callback_data = 'data_visualization')
      )
    )
  )

  # Send Inline Keyboard
  bot$sendMessage(chat_id = update$message$chat_id, 
                  text = "Выберите Хаб", 
                  reply_markup = IKM)
}
```

Список статей из указанного Хаба мы получаем командой `habr_hub_posts()`, из пакета `habR`. При этом указываем, что нам не требуется список статей за всё время, а только первая страница на которой располагаются 20 статей. Из полученной таблицы с помощью команды `head()` оставляем только 5 самых верхних, которые и являются самыми свежими статьями.

```
  # парсим Хабр
  posts <- head(habr_hub_posts(hub, 1), 5)
```

Логика очень схожа с предыдущим ботом, но в данном случае Inline клавиатуру со списком статей мы генерируем динамически с помощью функции `lapply()`.

```
  # формируем список кнопок
  keys <- lapply(1:5, function(x) list(InlineKeyboardButton(posts$title[x], url = posts$link[x])))

  # формируем клавиатуру
  IKM <- InlineKeyboardMarkup(
    inline_keyboard =  keys 
    )
```

В текст кнопки мы подставляем название статьи `posts$title[x]`, а в аргумент `url` ссылку на статью: `url = posts$link[x]`.

Далее, создаём фильтр, обработчики и запускаем нашего бота.

# Заключение

Теперь написанные вами боты будут значительно удобней в работе, за счёт того, что управление ими будет осуществляться с клавиатуры, а не вводом команд. Как минимум при взаимодействии с ботом через смартфон клавиатура ощутимо упростит процесс его использования.

В [следующей статье](https://habr.com/ru/post/518470/) мы разберёмся как строить логический диалог с ботом, и работать с базами данных.
