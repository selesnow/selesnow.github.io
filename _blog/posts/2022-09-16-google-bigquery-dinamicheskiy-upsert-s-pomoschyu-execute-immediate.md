---
title: 'Google BigQuery: Динамический UPSERT с помощью EXECUTE IMMEDIATE'
date: '2022-09-16'
slug: google-bigquery-dinamicheskiy-upsert-s-pomoschyu-execute-immediate
tags:
- BigQuery
- SQL
categories:
- Базы данных
description: Обычный паттерн обновления данных в BigQuery — добавление новых записей, даже если это означает дублирование данных. А затем обрабатывать дубликаты при чтении с помощью группировки или оконных функций, или удаление записей, и последующая повторная запись одних и тех же данных, но уже с новыми значениями. В любом случае все эти варианты не являются лучшей практикой. Иногда […]
original_url: https://alexeyseleznev.wordpress.com/2022/09/16/google-bigquery-%d0%b4%d0%b8%d0%bd%d0%b0%d0%bc%d0%b8%d1%87%d0%b5%d1%81%d0%ba%d0%b8%d0%b9-upsert-%d1%81-%d0%bf%d0%be%d0%bc%d0%be%d1%89%d1%8c%d1%8e-execute-immediate/
wp_id: 1577
draft: false
cover: ../images/covers/1577.webp
cover_generated: true
---

Обычный паттерн обновления данных в BigQuery — добавление новых записей, даже если это означает дублирование данных. А затем обрабатывать дубликаты при чтении с помощью группировки или оконных функций, или удаление записей, и последующая повторная запись одних и тех же данных, но уже с новыми значениями. В любом случае все эти варианты не являются лучшей практикой.

Иногда вам нужно выполнить UPSERT операцию (обновление или вставку) данных одним запросом. Возможно вы хотите «исправить» некоторые записи, или внести какие-то обновления в них (например обновить статусы транзакций), либо хотите сохранить чистую таблицу без дубликатов для своего коллеги-аналитика или специалиста по данным.

> UPDATE — **оператор языка SQL, позволяющий обновить значения в заданных столбцах таблицы**.

С недавних пор в BigQuery есть оператор MERGE, который мы можем использовать для реализации логики UPSERT. Как обсуждалось, например, в этой ветке [StackOverflow .](https://stackoverflow.com/questions/48177241/google-bq-how-to-upsert-existing-data-in-tables)

```

MERGE `project.merge_example.table_data` T
USING `project.merge_example.table_changes` S
ON T.id = S.id
WHEN MATCHED THEN
  UPDATE SET value = s.value
WHEN NOT MATCHED THEN
  INSERT (id, value) VALUES(id, value)
```

Данный запрос обновит значения поля value, в записях таблицы project.merge\_example.table\_data, которые будут найдены в таблице project.merge\_example.table\_changes по полю id. Записи, id которых есть в таблице project.merge\_example.table\_changes, но нет в project.merge\_example.table\_data, будут добавлены в таблицу project.merge\_example.table\_data.

Проблема тут в следующем, хорошо, когда необходимо обновить значение одного или нескольких полей, в нашем примере поля value, но, если вам надо обновить значения в сотне столбцов, то вам придётся перечислить каждое это поле в блоке UPDATE SET.

К счастью, мы можем превратить приведенный выше пример в динамический запрос UPSERT:

```

DECLARE fields STRING;
DECLARE updates STRING;
EXECUTE IMMEDIATE (
     "SELECT STRING_AGG(column_name) FROM `project.merge_example`.INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'table_data'"
  ) INTO fields;
EXECUTE IMMEDIATE (
    """WITH t AS (SELECT column_name FROM `project.merge_example`.INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'table_data')
       SELECT STRING_AGG("t."||column_name ||" = "|| "s."||column_name) from t join t as s using(column_name)"""
  ) INTO updates;
EXECUTE IMMEDIATE """
  MERGE `project.merge_example.table_data` T
  USING `project.merge_example.table_changes` S
    ON T.id = S.id
  WHEN MATCHED THEN 
    UPDATE SET """||updates||"""
  WHEN NOT MATCHED THEN
    INSERT ("""||fields||""") VALUES ("""||fields||""")"""
```

**Давайте разберём этот запрос:**

**DECLARE** создает переменные, которые мы позже заполняем значениями.

**EXECUTE IMMEDIATE позволяет нам динамически создавать SQL запрос и записывать** результат в объявленную переменную.

Чтобы получить разделенную запятыми **строку полей** в нашей таблице, мы запрашиваем метаданные набора данных:

```

SELECT STRING_AGG(column_name) FROM `project.merge_example`.INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'table_data'
```

**Чтобы получить строку со списком полей,** разделенных запятыми, для обновления, то есть `SET t.value1 = s.value1, t.value2 = s.value2` мы снова запрашиваем метаданные и добавляем некоторые конкатенации в функцию `STRING_AGG:SELECT STRING_AGG(“t.”||column_name ||” = “|| “s.”||column_name) from t join t as s using(column_name)`.

Наконец, мы создаем оператор UPSERT, **динамически заполняющий столбцы** для обновления и значения для вставки из переменных, объявленных выше:

```

EXECUTE IMMEDIATE """
  MERGE `project.merge_example.table_data` T
  USING `project.merge_example.table_changes` S
    ON T.id = S.id
  WHEN MATCHED THEN 
    UPDATE SET """||updates||"""
  WHEN NOT MATCHED THEN
    INSERT ("""||fields||""") VALUES ("""||fields||""")"""
```

Чтобы сделать этот пример еще более универсальным, мы можем завернуть описанный выше динамический запрос в **ХРАНИМУЮ ПРОЦЕДУРУ**, которая будет принимать имена таблиц в качестве аргументов и выполнять наш код UPSERT.

Код процедуры будет выглядеть примерно так:

```

CREATE OR REPLACE PROCEDURE `project.merge_example.upsert`(table_data STRING, table_changes STRING, project_dataset STRING)
BEGIN
DECLARE fields STRING;
DECLARE updates STRING;EXECUTE IMMEDIATE (
     "SELECT STRING_AGG(column_name) FROM `"||project_dataset||"`.INFORMATION_SCHEMA.COLUMNS WHERE table_name = '"||table_data||"'"
  ) INTO fields;EXECUTE IMMEDIATE (
    """WITH t AS (SELECT column_name FROM `"""||project_dataset||"""`.INFORMATION_SCHEMA.COLUMNS WHERE table_name = '"""||table_data||"""')
       SELECT STRING_AGG("t."||column_name ||" = "|| "s."||column_name) from t join t as s using(column_name)"""
  ) INTO updates;EXECUTE IMMEDIATE """
  MERGE `"""||project_dataset||"""."""||table_data||"""` T
  USING `"""||project_dataset||"""."""||table_changes||"""` S
    ON T.id = S.id
  WHEN MATCHED THEN 
    UPDATE SET """||updates||"""
  WHEN NOT MATCHED THEN
    INSERT ("""||fields||""") VALUES ("""||fields||""")""";
END;
```

Данная статья является свободным переводом статьи [“BigQuery dynamic UPSERT with EXECUTE IMMEDIATE”](https://medium.com/@chekanskiy/bigquery-upsert-with-execute-immediate-8399e9997753).
