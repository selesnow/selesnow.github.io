---
title: 'Пишем telegram бота на языке R (часть 5): Управление правами пользователей бота'
date: '2022-06-02'
slug: pishem-telegram-bota-na-yazyke-r-chast-5-upravlenie-pravami-polzovatel
tags:
- API
- R
- Telegram
categories:
- Программирование
- R
description: В предыдущих статьях мы достаточно подробно разобрали тему ботостроения, от отправки первого сообщения до программирования логического диалога с ботом. Это последняя статья из данной серии, в которой мы разберёмся с тем, как управлять правами использования отдельных методов бота на различных уровнях.
original_url: https://alexeyseleznev.wordpress.com/2022/06/02/%d0%bf%d0%b8%d1%88%d0%b5%d0%bc-telegram-%d0%b1%d0%be%d1%82%d0%b0-%d0%bd%d0%b0-%d1%8f%d0%b7%d1%8b%d0%ba%d0%b5-r-%d1%87%d0%b0%d1%81%d1%82%d1%8c-5-%d1%83%d0%bf%d1%80%d0%b0%d0%b2%d0%bb%d0%b5%d0%bd/
wp_id: 1560
draft: false
---

В предыдущих статьях мы достаточно подробно разобрали тему ботостроения, от отправки первого сообщения до программирования логического диалога с ботом.

Это последняя статья из данной серии, в которой мы разберёмся с тем, как управлять правами использования отдельных методов бота на различных уровнях.

![](../images/pishem-telegram-bota-na-yazyke-r-chast-5-upravlen-zx1mk2dp30-2c7a0a1d.webp)

# Все статьи из серии “Пишем telegram бота на языке R”

1. [Создаём бота, и отправляем с его помощью сообщения в telegram](/blog/pishem-telegram-bota-na-yazyke-r-chast-1-sozdaem-bota-i-otpravlyaem-s/)
2. [Добавляем боту поддержку команд и фильтры сообщений](/blog/pishem-telegram-bota-na-yazyke-r-chast-2-dobavlyaem-botu-podderzhku-ko/)
3. [Как добавить боту поддержку клавиатуры](/blog/pishem-telegram-bota-na-yazyke-r-chast-3-kak-dobavit-botu-podderzhku-k/)
4. [Построение последовательного, логического диалога с ботом](/blog/pishem-telegram-bota-na-yazyke-r-chast-2-dobavlyaem-botu-podderzhku-ko/)
5. Управление правами пользователей бота

# Содержание

*Если вы интересуетесь анализом данных возможно вам будут интересны мои [telegram](https://t.me/R4marketing) и [youtube](https://www.youtube.com/R4marketing/?sub_confirmation=1) каналы. Большая часть контента которых посвящены языку R.*

1. Введение
2. Ограничиваем права пользователя с помощью фильтров сообщений  
   2.1. Ограничиваем права на уровне имени пользователя  
   2.2. Ограничиваем права на уровне чата
3. Ограничиваем права пользователя внутри кода методов  
   3.1. Ограничиваем права на уровне имени пользователя  
   3.2. Ограничиваем права на уровне чата
4. Заключение

# Введение

Ваш бот может выполнять совершенно любые задачи, и автоматизировать как некоторые внутренние процессы, так и наладить коммуникации с клиентами.

Т.е. бот может использоваться в многопользовательском режиме. При этом, вам может понадобиться разграничить права на использование бота. Например, некоторые пользователи смогут использовать абсолютно все возможности бота, а некоторым вы предоставите ограниченные права.

Ограничить права можно не только на уровне пользователя, но и на уровне отдельных чатов.

Мы создадим простейшего бота, у которого в арсенале будет всего 2 метода:

- `say_hello` — команда приветствия
- `what_time` — команда, по которой бот сообщает текущую дату и время

**Базовый код бота**

```

library(telegram.bot)

# создаём экземпляр класса Updater
updater <- Updater('ТОКЕН ВАШЕГО БОТА')

# Пишем метод для приветсвия
## команда приветствия
say_hello <- function(bot, update) {

  # Имя пользователя с которым надо поздароваться
  user_name <- update$message$from$first_name

  # Отправка сообщения
  bot$sendMessage(update$message$chat_id, 
                  text = paste0("Моё почтение, ", user_name, "!"),
                  parse_mode = "Markdown",
                  reply_to_message_id = update$message$message_id)

}

## команда по которой бот возвращает системную дату и время
what_time <- function(bot, update) {

  # Запрашиваем текущее время
  cur_time <- as.character(Sys.time())

  # Отправка сообщения
  bot$sendMessage(update$message$chat_id, 
                  text = paste0("Текущее время, ", cur_time),
                                parse_mode = "Markdown",
                                reply_to_message_id = update$message$message_id)

}

# обработчики
h_hello <- CommandHandler('say_hello', say_hello)
h_time  <- CommandHandler('what_time', what_time)

# добавляем обработчики в диспетчер
updater <- updater + h_hello + h_time

# запускаем бота 
updater$start_polling()
```

> Запустите приведённый выше пример кода, предварительно заменив ‘ТОКЕН ВАШЕГО БОТА’ на реальный токен, который вы получили при создании бота через *BotFather* (о создании бота я рассказывал в [первой статье](https://habr.com/ru/post/511222/#sozdanie-telegram-bota)).

В статье мы разберёмся с тем, как разными способами, и на разных уровнях ограничить использование методов этого бота.

# Ограничиваем права пользователя с помощью фильтров сообщений

Из предыдущих публикаций мы уже разобрались с тем, что такое фильтры сообщений. Но ранее мы использовали их в основном для, того, что бы вызывать какие-то методы бота через обычное сообщение, а не команду и для прослушиваний сообщений в определённом состоянии чата.

В этот раз мы научимся с помощью фильтров ограничивать возможности по использованию методов бота, на разных уровнях.

### Ограничиваем права на уровне имени пользователя

Для создания собственных фильтров вам необходимо с помощью функции `BaseFilter()` добавить новый элемент в объект `MessageFilters`. Более подробно об этом я рассказывал во [второй статье](https://habr.com/ru/post/515148/) из данной серии.

В анонимную функцию, которую вы прописываете внутри `BaseFilter()` передаётся всего один аргумент — `message`. Это сообщение которое вы, или другой пользователей отправляет боту, со всеми его метаданными. Данный объект имеет следующую структуру:

```

$message_id
[1] 1174

$from
$from$id
[1] 194336771

$from$is_bot
[1] FALSE

$from$first_name
[1] "Alexey"

$from$last_name
[1] "Seleznev"

$from$username
[1] "AlexeySeleznev"

$from$language_code
[1] "ru"

$chat
$chat$id
[1] 194336771

$chat$first_name
[1] "Alexey"

$chat$last_name
[1] "Seleznev"

$chat$username
[1] "AlexeySeleznev"

$chat$type
[1] "private"

$date
[1] 1601295189

$text
[1] "отправленный пользователем текст"

$chat_id
[1] 194336771

$from_user
[1] 194336771
```

Соответственно вы можете разделять права пользователей бота, и его методов используя любую, отправляемую с сообщением информацию. Для того, что бы ограничить круг пользователей которые могут использовать методы вашего бота достаточно создать фильтр:

```

## список пользователей, с полными правами
MessageFilters$admins <- BaseFilter(
  function(message) {

    # проверяем от кого отправлено сообщение
    message$from$username %in% c('AlexeySeleznev', 'user1', 'user2')

 }
)
```

Где `c('AlexeySeleznev', 'user1', 'user2')` — вектор, с именами пользователей, которые могут использовать все функции бота. Далее этот фильтр мы используем при создании обработчиков.

```

## фильтр для вызова команды say_hello
MessageFilters$say_hello <- BaseFilter(
  function(message) {

    # проверяем от кого отправлено сообщение
    message$text == '/say_hallo'

  }
)

## фильтр для вызова команды what_time
MessageFilters$what_time <- BaseFilter(
  function(message) {

    # проверяем от кого отправлено сообщение
    message$text == '/what_time'

  }
)

# обработчики
h_hello <- MessageHandler(say_hello, MessageFilters$admins & MessageFilters$say_hello)
h_time  <- MessageHandler(what_time, MessageFilters$admins & MessageFilters$what_time)
```

Теперь нашего бота могут использовать пользователи с логинами AlexeySeleznev, user1, user2. На сообщения отправленные боту другими пользователями он никак не будет реагировать.

Изменённый код нашего бота на данный момент выглядит вот так:

**Код бота, в котором с помощью фильтров был ограничен круг пользователей**

```

library(telegram.bot)

# создаём экземпляр класса Updater
updater <- Updater('ТОКЕН ВАШЕГО БОТА')

# Пишем метод для приветсвия
## команда приветствия
say_hello <- function(bot, update) {

  # Имя пользователя с которым надо поздароваться
  user_name <- update$message$from$first_name

  # Отправка сообщения
  bot$sendMessage(update$message$chat_id, 
                  text = paste0("Моё почтение, ", user_name, "!"),
                  parse_mode = "Markdown",
                  reply_to_message_id = update$message$message_id)

}

## команда по которой бот возвращает системную дату и время
what_time <- function(bot, update) {

  # Запрашиваем текущее время
  cur_time <- as.character(Sys.time())

  # Отправка сообщения
  bot$sendMessage(update$message$chat_id, 
                  text = paste0("Текущее время, ", cur_time),
                                parse_mode = "Markdown",
                                reply_to_message_id = update$message$message_id)

}

# фильтры
## список пользователей, с полными правами
MessageFilters$admins <- BaseFilter(
  function(message) {

    # проверяем от кого отправлено сообщение
    message$from$username %in% c('AlexeySeleznev', 'user1', 'user2')

 }
)

## фильтр для вызова команды say_hello
MessageFilters$say_hello <- BaseFilter(
  function(message) {

    # проверяем от кого отправлено сообщение
    message$text == '/say_hallo'

  }
)

## фильтр для вызова команды what_time
MessageFilters$what_time <- BaseFilter(
  function(message) {

    # проверяем от кого отправлено сообщение
    message$text == '/what_time'

  }
)

# обработчики
h_hello <- MessageHandler(say_hello, MessageFilters$admins & MessageFilters$say_hello)
h_time  <- MessageHandler(what_time, MessageFilters$admins & MessageFilters$what_time)

# добавляем обработчики в диспетчер
updater <- updater + h_hello + h_time

# запускаем бота 
updater$start_polling()
```

### Ограничиваем права на уровне чата

Тем же способом мы можем создать фильтр не только по списку пользователей, но и по конкретному чату. Для этого достаточно создать ещё один фильтр:

```

## список чатов в которых разрешено использовать бота
MessageFilters$chats <- BaseFilter(
  function(message) {

    # проверяем от кого отправлено сообщение
    message$chat_id %in% c(194336771, 0, 1)

  }
)

## фильтр для вызова команды say_hello
MessageFilters$say_hello <- BaseFilter(
  function(message) {

    # проверяем от кого отправлено сообщение
    message$text == '/say_hallo'

  }
)

## фильтр для вызова команды what_time
MessageFilters$what_time <- BaseFilter(
  function(message) {

    # проверяем от кого отправлено сообщение
    message$text == '/what_time'

  }
)

# обработчики
h_hello <- MessageHandler(say_hello, MessageFilters$admins & MessageFilters$chats & MessageFilters$say_hello)
h_time  <- MessageHandler(what_time, MessageFilters$admins & MessageFilters$chats & MessageFilters$what_time)
```

# Ограничиваем права пользователя внутри кода методов

Так же вы можете ограничить использование методов не прибегая к созданию дополнительных фильтров, а прописав все условия внутри каждого метода.

### Ограничиваем права на уровне имени пользователя

Давайте создадим функцию, которая будет принимать данные для проверки имени пользователя.

```

# функция для проверки прав пользователя
bot_check_usernames <- 
  function(admins, username) {

   username %in% admins 

}
```

В аргумент `admins` далее нам надо передавать список пользователей, которым разрешено использовать данный метод, а в аргумент `username` имя пользователя, которого надо проверить в списке.

Далее в каждый метод, который мы хотим защитить с помощью конструкции `IF` добавляем проверку, разрешено пользователю использовать данный метод или нет. В случае если у пользователя нет таких прав бот будет сообщать об этом в чате.

Давайте, для примера, я исключу себя из списка пользователей, которым разрешено использовать метод `what_time`.

**Код бота, в котором ограничены права пользователя внутри кода методов**

```

library(telegram.bot)

# создаём экземпляр класса Updater
updater <- Updater('ТОКЕН ВАШЕГО БОТА')

# Пишем метод для приветсвия
## команда приветствия
say_hello <- function(bot, update) {

  # Имя пользователя с которым надо поздароваться
  user_name <- update$message$from$username

  # проверяем разрешено ли использовать данному пользователю этот метод
  if ( bot_check_usernames(c('AlexeySeleznev', 'user1', 'user2'), user_name) ) {

    # Отправка сообщения
    bot$sendMessage(update$message$chat_id, 
                    text = paste0("Моё почтение, ", user_name, "!"),
                    parse_mode = "Markdown",
                    reply_to_message_id = update$message$message_id)

  } else {

    # Отправка сообщения
    bot$sendMessage(update$message$chat_id, 
                    text = paste0("У вас нет прав для использования этого метода!"),
                    parse_mode = "Markdown",
                    reply_to_message_id = update$message$message_id)

  }

}

## команда по которой бот возвращает системную дату и время
what_time <- function(bot, update) {

  # проверяем разрешено ли использовать данному пользователю этот метод
  if ( bot_check_usernames(c('user1', 'user2'), update$message$from$username) ) {

    # Запрашиваем текущее время
    cur_time <- as.character(Sys.time())

    # Отправка сообщения о том что у пользователя не достаточно прав
    bot$sendMessage(update$message$chat_id, 
                    text = paste0("Текущее время, ", cur_time),
                                  parse_mode = "Markdown",
                                  reply_to_message_id = update$message$message_id)
  } else {

    # Отправка сообщения о том что у пользователя не достаточно прав
    bot$sendMessage(update$message$chat_id, 
                    text = paste0("У вас нет прав для использования этого метода!"),
                    parse_mode = "Markdown",
                    reply_to_message_id = update$message$message_id)

  }

}

# обработчики
h_hello <- CommandHandler('say_hello', say_hello)
h_time  <- CommandHandler('what_time', what_time)

# добавляем обработчики в диспетчер
updater <- updater + h_hello + h_time

# запускаем бота 
updater$start_polling()
```

Результат будет следующим:

![](../images/pishem-telegram-bota-na-yazyke-r-chast-5-upravlen-09f25341b9-31575561.webp)

Теперь бот не просто игнорирует сообщения от обычных пользователей, а сообщает им, что у них недостаточно прав использовать какой либо метод.

### Ограничиваем права на уровне чата

Думаю у вас уже не возникнет трудностей при доработке ваших методов, таким образом, что бы их можно было использовать только в определённых чатах, тем не менее приведу пример.

Напишем функцию, которая будет проверять входит ли текущий чат в список разрешенных.

```

bot_check_chat_id <- 
  function(allowed_chats, current_chat) {

     current_chat %in% allowed_chats 

}
```

Далее используем эту функции внутри наших методов:

**Код бота с распределением прав пользователя на уровне пользователей и чатов**

```

library(telegram.bot)

# создаём экземпляр класса Updater
updater <- Updater('ТОКЕН ВАШЕГО БОТА')

# Пишем метод для приветсвия
## команда приветствия
say_hello <- function(bot, update) {

  # Имя пользователя с которым надо поздароваться
  user_name <- update$message$from$username

  # проверяем разрешено ли использовать данному пользователю этот метод
  if ( bot_check_usernames(c('AlexeySeleznev', 'user1', 'user2'), user_name) 
       &
       bot_check_chat_id(c(194336771, 1, 2), update$message$chat_id)) {

    # Отправка сообщения
    bot$sendMessage(update$message$chat_id, 
                    text = paste0("Моё почтение, ", user_name, "!"),
                    parse_mode = "Markdown",
                    reply_to_message_id = update$message$message_id)

  } else {

    # Отправка сообщения
    bot$sendMessage(update$message$chat_id, 
                    text = paste0("У вас нет прав для использования этого метода!"),
                    parse_mode = "Markdown",
                    reply_to_message_id = update$message$message_id)

  }

}

## команда по которой бот возвращает системную дату и время
what_time <- function(bot, update) {

  # проверяем разрешено ли использовать данному пользователю этот метод
  if ( bot_check_usernames(c('AlexeySeleznev', 'user1', 'user2'), update$message$from$username)
       &
       bot_check_chat_id(c(194336771, 1, 2), update$message$chat_id)) {

    # Запрашиваем текущее время
    cur_time <- as.character(Sys.time())

    # Отправка сообщения о том что у пользователя не достаточно прав
    bot$sendMessage(update$message$chat_id, 
                    text = paste0("Текущее время, ", cur_time),
                                  parse_mode = "Markdown",
                                  reply_to_message_id = update$message$message_id)
  } else {

    # Отправка сообщения о том что у пользователя не достаточно прав
    bot$sendMessage(update$message$chat_id, 
                    text = paste0("У вас нет прав для использования этого метода!"),
                    parse_mode = "Markdown",
                    reply_to_message_id = update$message$message_id)

  }

}

# обработчики
h_hello <- CommandHandler('say_hello', say_hello)
h_time  <- CommandHandler('what_time', what_time)

# добавляем обработчики в диспетчер
updater <- updater + h_hello + h_time

# запускаем бота 
updater$start_polling()
```

# Заключение

На этом серия статей о построении telegram ботов завершается. Я старался структурировать и подавать материал достаточно сжато, убрав всю воду, но при этом сделать так, что бы материал был вам понятен. Очень надеюсь на то, что мне это удалось.

Успехов вам в ботостроении. В комментариях можете написать примеры ваших ботов, и как вы их на практике используете.
