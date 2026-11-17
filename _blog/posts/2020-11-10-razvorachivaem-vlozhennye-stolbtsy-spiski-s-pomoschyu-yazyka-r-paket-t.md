---
title: Разворачиваем вложенные столбцы — списки с помощью языка R (пакет tidyr и функции семейства unnest)
date: '2020-11-10'
slug: razvorachivaem-vlozhennye-stolbtsy-spiski-s-pomoschyu-yazyka-r-paket-t
tags:
- R
- Обработка данных
- tidyverse
categories:
- Программирование
- R
description: 'В большинстве случаев при работе с ответом полученным от API, или с любыми другими данными которые имеют сложную древовидную структуру, вы сталкиваетесь с форматами JSON и XML. Эти форматы имеют множество преимуществ: они достаточно компактно хранят данные и позволяют избежать излишнего дублирования информации. Минусом данных форматов является сложность их обработки и анализа. Неструктурированные данные невозможно […]'
original_url: https://alexeyseleznev.wordpress.com/2020/11/10/%d1%80%d0%b0%d0%b7%d0%b2%d0%be%d1%80%d0%b0%d1%87%d0%b8%d0%b2%d0%b0%d0%b5%d0%bc-%d0%b2%d0%bb%d0%be%d0%b6%d0%b5%d0%bd%d0%bd%d1%8b%d0%b5-%d1%81%d1%82%d0%be%d0%bb%d0%b1%d1%86%d1%8b-%d1%81%d0%bf/
wp_id: 1428
draft: false
---

В большинстве случаев при работе с ответом полученным от API, или с любыми другими данными которые имеют сложную древовидную структуру, вы сталкиваетесь с форматами JSON и XML.

Эти форматы имеют множество преимуществ: они достаточно компактно хранят данные и позволяют избежать излишнего дублирования информации.

Минусом данных форматов является сложность их обработки и анализа. Неструктурированные данные невозможно использовать в вычислениях и нельзя строить на их основе визуализацию.

![](../images/razvorachivaem-vlozhennye-stolbtsy-sp-7syfgrnpyegv-ihhcguupz-9349286e.webp)

Данная статья является логическим продолжением публикации [“R пакет tidyr и его новые функции pivot\_longer и pivot\_wider”](https://habr.com/ru/post/444622/). Она поможет вам привести неструктурированные конструкции данных к привычному, и пригодному для анализа табличному виду с помощью пакета `tidyr`, входящего в ядро библиотеки `tidyverse`, и его функций семейства `unnest_*()`.

# Содержание

*Если вы интересуетесь анализом данных возможно вам будут интересны мои [telegram](https://t.me/R4marketing) и [youtube](https://www.youtube.com/R4marketing/?sub_confirmation=1) каналы. Большая часть контента которых посвящены языку R.*

1. Введение
2. Пользователи GitHub
3. Репозитории Github
4. Персонажи Игры Престолов
5. Геокодирование с помощью Google
6. Дискография Шарлы Гельфанд
7. Заключение

> Изначально статья была написана для Хабры
>
> <https://habr.com/ru/post/491726/>

# Введение

**Rectangling** *(прим. переводчика, не нашел адекватных вариантов перевода этого термина, поэтому оставим его как есть.)* — это процесс приведения не структурированных данных с вложенными массивами к двухмерной таблице, состоящей из привычных нам строк и столбцов. В `tidyr` есть несколько функций, которые помогут вам развернуть вложенные столбцы-списки и привести данные к прямоугольной, табличной форме:

- `unnest_longer()` берет каждый элемент списка-столбца и создает новую строку.
- `unnest_wider()` берет каждый элемент списка-столбца и создает новый столбец.
- `unnest_auto()` автоматически определяет какую из функций лучше использовать  
  `unnest_longer()` или `unnest_wider()`.
- `hoist()` похожа на `unnest_wider()` но отбирает только указанные компоненты и позволяет работать с несколькими уровнями вложенности.

Большинство проблем связанных с приведением не структурированных данных с несколькими уровнями вложенности к двухмерной таблице можно решить, комбинируя перечисленные функции с dplyr.

Для демонстрации этих приемов, мы будем использовать пакет `repurrrsive`, который предоставляет несколько сложных, многоуровневых списков, полученных из веб-API.

```

library(tidyr)
library(dplyr)
library(repurrrsive)
```

# Пользователи GitHub

Начнем с *gh\_users*, списка, который содержит информацию о шести пользователях GitHub. Для начала преобразуем список *gh\_users* в *tibble* фрейм.:

```

users <-   tibble( user = gh_users )
```

Это кажется немного нелогичным: зачем приводить список *gh\_users*, к более сложной структуре данных? Но у дата фрейма есть большое преимущество: он объединяет несколько векторов, так что все отслеживается в одном объекте.

Каждый элемент объекта `users` представляет собой именованный список, в котором каждый элемент представляет столбец.

```

names(users$user[[1]])
#>  [1] "login"               "id"                  "avatar_url"         
#>  [4] "gravatar_id"         "url"                 "html_url"           
#>  [7] "followers_url"       "following_url"       "gists_url"          
#> [10] "starred_url"         "subscriptions_url"   "organizations_url"  
#> [13] "repos_url"           "events_url"          "received_events_url"
#> [16] "type"                "site_admin"          "name"               
#> [19] "company"             "blog"                "location"           
#> [22] "email"               "hireable"            "bio"                
#> [25] "public_repos"        "public_gists"        "followers"          
#> [28] "following"           "created_at"          "updated_at"
```

Есть два способа превратить компоненты списка в столбцы. `unnest_wider()` берет каждый компонент и создает новый столбец:

```

users %>% unnest_wider(user)
#> # A tibble: 6 x 30
#>   login     id avatar_url gravatar_id url   html_url followers_url
#>   <chr>  <int> <chr>      <chr>       <chr> <chr>    <chr>        
#> 1 gabo… 6.60e5 https://a… ""          http… https:/… https://api.…
#> 2 jenn… 5.99e5 https://a… ""          http… https:/… https://api.…
#> 3 jtle… 1.57e6 https://a… ""          http… https:/… https://api.…
#> 4 juli… 1.25e7 https://a… ""          http… https:/… https://api.…
#> 5 leep… 3.51e6 https://a… ""          http… https:/… https://api.…
#> 6 masa… 8.36e6 https://a… ""          http… https:/… https://api.…
#> # … with 23 more variables: following_url <chr>, gists_url <chr>,
#> #   starred_url <chr>, subscriptions_url <chr>, organizations_url <chr>,
#> #   repos_url <chr>, events_url <chr>, received_events_url <chr>,
#> #   type <chr>, site_admin <lgl>, name <chr>, company <chr>, blog <chr>,
#> #   location <chr>, email <chr>, public_repos <int>, public_gists <int>,
#> #   followers <int>, following <int>, created_at <chr>, updated_at <chr>,
#> #   bio <chr>, hireable <lgl>
```

В этом случае мы получили таблицу состоящую из 30 столбцов, и большинство из них нам не понадобятся, поэтому мы можем вместо `unnest_wider()` использовать `hoist()`. `hoist()` позволяет нам извлекать выбранные компоненты, используя тот же синтаксис, что и `purrr::pluck()`:

```

users %>% hoist(user, 
  followers = "followers", 
  login = "login", 
  url = "html_url"
)
#> # A tibble: 6 x 4
#>   followers login       url                            user             
#>       <int> <chr>       <chr>                          <list>           
#> 1       303 gaborcsardi https://github.com/gaborcsardi <named list [27]>
#> 2       780 jennybc     https://github.com/jennybc     <named list [27]>
#> 3      3958 jtleek      https://github.com/jtleek      <named list [27]>
#> 4       115 juliasilge  https://github.com/juliasilge  <named list [27]>
#> 5       213 leeper      https://github.com/leeper      <named list [27]>
#> 6        34 masalmon    https://github.com/masalmon    <named list [27]>
```

`hoist()` удаляет указанные именованные компоненты из списка-столбца *user*, поэтому вы можете рассматривать `hoist()` как перемещение компонентов из внутреннего списка дата фрейма к его верхнему уровню.

# Репозитории Github

Выравнивание списка `gh_repos` мы начинаем аналогично, преобразуя его в `tibble`:

```

repos <- tibble(repo = gh_repos)
repos
#> # A tibble: 6 x 1
#>   repo       
#>   <list>     
#> 1 <list [30]>
#> 2 <list [30]>
#> 3 <list [30]>
#> 4 <list [26]>
#> 5 <list [30]>
#> 6 <list [30]>
```

На этот раз элементы *user* представляют собой список репозиториев, принадлежащих этому пользователю. Каждый репозиторий является отдельным наблюдением, поэтому согласно концепции аккуратных данных *(прим. tidy data)* они должны стать новыми строками, в связи с чем мы используем `unnest_longer()` а не `unnest_wider()`:

```

repos <- repos %>% unnest_longer(repo)
repos
#> # A tibble: 176 x 1
#>    repo             
#>    <list>           
#>  1 <named list [68]>
#>  2 <named list [68]>
#>  3 <named list [68]>
#>  4 <named list [68]>
#>  5 <named list [68]>
#>  6 <named list [68]>
#>  7 <named list [68]>
#>  8 <named list [68]>
#>  9 <named list [68]>
#> 10 <named list [68]>
#> # … with 166 more rows
```

Теперь мы можем использовать `unnest_wider()` или `hoist()` :

```

repos %>% hoist(repo, 
  login = c("owner", "login"), 
  name = "name",
  homepage = "homepage",
  watchers = "watchers_count"
)
#> # A tibble: 176 x 5
#>    login       name        homepage watchers repo             
#>    <chr>       <chr>       <chr>       <int> <list>           
#>  1 gaborcsardi after       <NA>            5 <named list [65]>
#>  2 gaborcsardi argufy      <NA>           19 <named list [65]>
#>  3 gaborcsardi ask         <NA>            5 <named list [65]>
#>  4 gaborcsardi baseimports <NA>            0 <named list [65]>
#>  5 gaborcsardi citest      <NA>            0 <named list [65]>
#>  6 gaborcsardi clisymbols  ""             18 <named list [65]>
#>  7 gaborcsardi cmaker      <NA>            0 <named list [65]>
#>  8 gaborcsardi cmark       <NA>            0 <named list [65]>
#>  9 gaborcsardi conditions  <NA>            0 <named list [65]>
#> 10 gaborcsardi crayon      <NA>           52 <named list [65]>
#> # … with 166 more rows
```

Обратите внимание на использование `c("owner", "login")`: это позволяет нам получить значение второго уровня из вложенного списка `owner`. Альтернативный подход состоит в том, чтобы получить весь список `owner` и затем с помощью функции `unnest_wider()` поместить каждый его элемент в столбец:

```

repos %>% 
  hoist(repo, owner = "owner") %>% 
  unnest_wider(owner)
#> # A tibble: 176 x 18
#>    login     id avatar_url gravatar_id url   html_url followers_url
#>    <chr>  <int> <chr>      <chr>       <chr> <chr>    <chr>        
#>  1 gabo… 660288 https://a… ""          http… https:/… https://api.…
#>  2 gabo… 660288 https://a… ""          http… https:/… https://api.…
#>  3 gabo… 660288 https://a… ""          http… https:/… https://api.…
#>  4 gabo… 660288 https://a… ""          http… https:/… https://api.…
#>  5 gabo… 660288 https://a… ""          http… https:/… https://api.…
#>  6 gabo… 660288 https://a… ""          http… https:/… https://api.…
#>  7 gabo… 660288 https://a… ""          http… https:/… https://api.…
#>  8 gabo… 660288 https://a… ""          http… https:/… https://api.…
#>  9 gabo… 660288 https://a… ""          http… https:/… https://api.…
#> 10 gabo… 660288 https://a… ""          http… https:/… https://api.…
#> # … with 166 more rows, and 11 more variables: following_url <chr>,
#> #   gists_url <chr>, starred_url <chr>, subscriptions_url <chr>,
#> #   organizations_url <chr>, repos_url <chr>, events_url <chr>,
#> #   received_events_url <chr>, type <chr>, site_admin <lgl>, repo <list>
```

Вместо того, что бы размышлять над выбором нужной функции `unnest_longer()` или `unnest_wider()` вы можете использовать `unnest_auto()`. Эта функция использует несколько эвристических методов для подбора наиболее подходящей функции для трансформации данных, и выводит сообщение о выбранном способе.

```

tibble(repo = gh_repos) %>% 
  unnest_auto(repo) %>% 
  unnest_auto(repo)
#> Using `unnest_longer(repo)`; no element has names
#> Using `unnest_wider(repo)`; elements have 68 names in common
#> # A tibble: 176 x 67
#>        id name  full_name owner private html_url description fork  url  
#>     <int> <chr> <chr>     <lis> <lgl>   <chr>    <chr>       <lgl> <chr>
#>  1 6.12e7 after gaborcsa… <nam… FALSE   https:/… Run Code i… FALSE http…
#>  2 4.05e7 argu… gaborcsa… <nam… FALSE   https:/… Declarativ… FALSE http…
#>  3 3.64e7 ask   gaborcsa… <nam… FALSE   https:/… Friendly C… FALSE http…
#>  4 3.49e7 base… gaborcsa… <nam… FALSE   https:/… Do we get … FALSE http…
#>  5 6.16e7 cite… gaborcsa… <nam… FALSE   https:/… Test R pac… TRUE  http…
#>  6 3.39e7 clis… gaborcsa… <nam… FALSE   https:/… Unicode sy… FALSE http…
#>  7 3.72e7 cmak… gaborcsa… <nam… FALSE   https:/… port of cm… TRUE  http…
#>  8 6.80e7 cmark gaborcsa… <nam… FALSE   https:/… CommonMark… TRUE  http…
#>  9 6.32e7 cond… gaborcsa… <nam… FALSE   https:/… <NA>        TRUE  http…
#> 10 2.43e7 cray… gaborcsa… <nam… FALSE   https:/… R package … FALSE http…
#> # … with 166 more rows, and 58 more variables: forks_url <chr>,
#> #   keys_url <chr>, collaborators_url <chr>, teams_url <chr>,
#> #   hooks_url <chr>, issue_events_url <chr>, events_url <chr>,
#> #   assignees_url <chr>, branches_url <chr>, tags_url <chr>,
#> #   blobs_url <chr>, git_tags_url <chr>, git_refs_url <chr>,
#> #   trees_url <chr>, statuses_url <chr>, languages_url <chr>,
#> #   stargazers_url <chr>, contributors_url <chr>, subscribers_url <chr>,
#> #   subscription_url <chr>, commits_url <chr>, git_commits_url <chr>,
#> #   comments_url <chr>, issue_comment_url <chr>, contents_url <chr>,
#> #   compare_url <chr>, merges_url <chr>, archive_url <chr>,
#> #   downloads_url <chr>, issues_url <chr>, pulls_url <chr>,
#> #   milestones_url <chr>, notifications_url <chr>, labels_url <chr>,
#> #   releases_url <chr>, deployments_url <chr>, created_at <chr>,
#> #   updated_at <chr>, pushed_at <chr>, git_url <chr>, ssh_url <chr>,
#> #   clone_url <chr>, svn_url <chr>, size <int>, stargazers_count <int>,
#> #   watchers_count <int>, language <chr>, has_issues <lgl>,
#> #   has_downloads <lgl>, has_wiki <lgl>, has_pages <lgl>,
#> #   forks_count <int>, open_issues_count <int>, forks <int>,
#> #   open_issues <int>, watchers <int>, default_branch <chr>,
#> #   homepage <chr>
```

# Персонажи Игры Престолов

`got_chars` имеет идентичную структуру с `gh_users`: это набор именованных списков, где каждый элемент внутреннего списка описывает некоторый атрибут персонажа Игры Престолов. Приведение `got_chars` к табличному виду мы начинаем с создания дата фрейма, так же как и в приведённых ранее примерах, а затем переведём каждый элемент в отдельный столбец:

```

chars <- tibble(char = got_chars)
chars
#> # A tibble: 30 x 1
#>    char             
#>    <list>           
#>  1 <named list [18]>
#>  2 <named list [18]>
#>  3 <named list [18]>
#>  4 <named list [18]>
#>  5 <named list [18]>
#>  6 <named list [18]>
#>  7 <named list [18]>
#>  8 <named list [18]>
#>  9 <named list [18]>
#> 10 <named list [18]>
#> # … with 20 more rows

chars2 <- chars %>% unnest_wider(char)
chars2
#> # A tibble: 30 x 18
#>    url      id name  gender culture born  died  alive titles aliases father
#>    <chr> <int> <chr> <chr>  <chr>   <chr> <chr> <lgl> <list> <list>  <chr> 
#>  1 http…  1022 Theo… Male   Ironbo… In 2… ""    TRUE  <chr … <chr [… ""    
#>  2 http…  1052 Tyri… Male   ""      In 2… ""    TRUE  <chr … <chr [… ""    
#>  3 http…  1074 Vict… Male   Ironbo… In 2… ""    TRUE  <chr … <chr [… ""    
#>  4 http…  1109 Will  Male   ""      ""    In 2… FALSE <chr … <chr [… ""    
#>  5 http…  1166 Areo… Male   Norvos… In 2… ""    TRUE  <chr … <chr [… ""    
#>  6 http…  1267 Chett Male   ""      At H… In 2… FALSE <chr … <chr [… ""    
#>  7 http…  1295 Cres… Male   ""      In 2… In 2… FALSE <chr … <chr [… ""    
#>  8 http…   130 Aria… Female Dornish In 2… ""    TRUE  <chr … <chr [… ""    
#>  9 http…  1303 Daen… Female Valyri… In 2… ""    TRUE  <chr … <chr [… ""    
#> 10 http…  1319 Davo… Male   Wester… In 2… ""    TRUE  <chr … <chr [… ""    
#> # … with 20 more rows, and 7 more variables: mother <chr>, spouse <chr>,
#> #   allegiances <list>, books <list>, povBooks <list>, tvSeries <list>,
#> #   playedBy <list>
```

Структура `got_chars` несколько сложнее, чем `gh_users`, т.к. некоторые компоненты списка `char` сами по себе являются списком, в результате мы получаем столбы — списки:

```

chars2 %>% select_if(is.list)
#> # A tibble: 30 x 7
#>    titles    aliases    allegiances books     povBooks  tvSeries  playedBy 
#>    <list>    <list>     <list>      <list>    <list>    <list>    <list>   
#>  1 <chr [3]> <chr [4]>  <chr [1]>   <chr [3]> <chr [2]> <chr [6]> <chr [1]>
#>  2 <chr [2]> <chr [11]> <chr [1]>   <chr [2]> <chr [4]> <chr [6]> <chr [1]>
#>  3 <chr [2]> <chr [1]>  <chr [1]>   <chr [3]> <chr [2]> <chr [1]> <chr [1]>
#>  4 <chr [1]> <chr [1]>  <???>       <chr [1]> <chr [1]> <chr [1]> <chr [1]>
#>  5 <chr [1]> <chr [1]>  <chr [1]>   <chr [3]> <chr [2]> <chr [2]> <chr [1]>
#>  6 <chr [1]> <chr [1]>  <???>       <chr [2]> <chr [1]> <chr [1]> <chr [1]>
#>  7 <chr [1]> <chr [1]>  <???>       <chr [2]> <chr [1]> <chr [1]> <chr [1]>
#>  8 <chr [1]> <chr [1]>  <chr [1]>   <chr [4]> <chr [1]> <chr [1]> <chr [1]>
#>  9 <chr [5]> <chr [11]> <chr [1]>   <chr [1]> <chr [4]> <chr [6]> <chr [1]>
#> 10 <chr [4]> <chr [5]>  <chr [2]>   <chr [1]> <chr [3]> <chr [5]> <chr [1]>
#> # … with 20 more rows
```

Ваши дальнейшие действия зависят от целей анализа. Возможно, вам необходимо поместить в строки информацию по каждой книге и сериале, в котором появляется персонаж:

```

chars2 %>% 
  select(name, books, tvSeries) %>% 
  pivot_longer(c(books, tvSeries), names_to = "media", values_to = "value") %>% 
  unnest_longer(value)
#> # A tibble: 180 x 3
#>    name             media    value            
#>    <chr>            <chr>    <chr>            
#>  1 Theon Greyjoy    books    A Game of Thrones
#>  2 Theon Greyjoy    books    A Storm of Swords
#>  3 Theon Greyjoy    books    A Feast for Crows
#>  4 Theon Greyjoy    tvSeries Season 1         
#>  5 Theon Greyjoy    tvSeries Season 2         
#>  6 Theon Greyjoy    tvSeries Season 3         
#>  7 Theon Greyjoy    tvSeries Season 4         
#>  8 Theon Greyjoy    tvSeries Season 5         
#>  9 Theon Greyjoy    tvSeries Season 6         
#> 10 Tyrion Lannister books    A Feast for Crows
#> # … with 170 more rows
```

Или, может быть, вы хотите создать таблицу, которая позволит вам сопоставить персонажа и произведение:

```

chars2 %>% 
  select(name, title = titles) %>% 
  unnest_longer(title)
#> # A tibble: 60 x 2
#>    name              title                                               
#>    <chr>             <chr>                                               
#>  1 Theon Greyjoy     Prince of Winterfell                                
#>  2 Theon Greyjoy     Captain of Sea Bitch                                
#>  3 Theon Greyjoy     Lord of the Iron Islands (by law of the green lands)
#>  4 Tyrion Lannister  Acting Hand of the King (former)                    
#>  5 Tyrion Lannister  Master of Coin (former)                             
#>  6 Victarion Greyjoy Lord Captain of the Iron Fleet                      
#>  7 Victarion Greyjoy Master of the Iron Victory                          
#>  8 Will              ""                                                  
#>  9 Areo Hotah        Captain of the Guard at Sunspear                    
#> 10 Chett             ""                                                  
#> # … with 50 more rows
```

(Обратите внимание, на пустые значения `""` в поле `title`, это связано с ошибками допущенными при вводе данных в `got_chars`: на самом деле персонажи для которых нет соответствующих заголовков книг и сериалов в поле `title` должны иметь вектор длины 0, а не вектор длины 1, содержащий пустую строку.)

Мы можем переписать приведённый выше пример используя функцию `unnest_auto()`. Этот подход удобен для разового анализа, но не стоит полагаться на `unnest_auto()` для использования на регулярной основе. Дело в том, что если ваша структура данных изменится `unnest_auto()` может поменять выбранный механизм преобразования данных, если изначально он разворачивал столбцы-списки в строки используя `unnest_longer()`, то при изменении структуры входящих данных логика может быть изменена в пользу `unnest_wider()`, и использование такого подхода на постоянной основе может привести к непредвиденным ошибкам.

```

tibble(char = got_chars) %>% 
  unnest_auto(char) %>% 
  select(name, title = titles) %>% 
  unnest_auto(title)
#> Using `unnest_wider(char)`; elements have 18 names in common
#> Using `unnest_longer(title)`; no element has names
#> # A tibble: 60 x 2
#>    name              title                                               
#>    <chr>             <chr>                                               
#>  1 Theon Greyjoy     Prince of Winterfell                                
#>  2 Theon Greyjoy     Captain of Sea Bitch                                
#>  3 Theon Greyjoy     Lord of the Iron Islands (by law of the green lands)
#>  4 Tyrion Lannister  Acting Hand of the King (former)                    
#>  5 Tyrion Lannister  Master of Coin (former)                             
#>  6 Victarion Greyjoy Lord Captain of the Iron Fleet                      
#>  7 Victarion Greyjoy Master of the Iron Victory                          
#>  8 Will              ""                                                  
#>  9 Areo Hotah        Captain of the Guard at Sunspear                    
#> 10 Chett             ""                                                  
#> # … with 50 more rows
```

# Геокодирование с помощью Google

Далее мы рассмотрим более сложную структуру данных, получаемых от службы геокодирования Google. Кэширование учётных данных противоречит условиям работы с API Google maps, поэтому я сначала напишу простую оболочку к API. Которая основана на хранении ключа API Google карт в переменной среды; если в переменных среды у вас не сохранён ключ для работы с API Google Maps, фрагменты кода представленные в этом разделе выполняться не будут.

```

has_key <- !identical(Sys.getenv("GOOGLE_MAPS_API_KEY"), "")
if (!has_key) {
  message("No Google Maps API key found; code chunks will not be run")
}

# https://developers.google.com/maps/documentation/geocoding
geocode <- function(address, api_key = Sys.getenv("GOOGLE_MAPS_API_KEY")) {
  url <- "https://maps.googleapis.com/maps/api/geocode/json"
  url <- paste0(url, "?address=", URLencode(address), "&key=", api_key)

  jsonlite::read_json(url)
}
```

Список, который возвращает эта функция, довольно сложен:

```

houston <- geocode("Houston TX")
str(houston)
#> List of 2
#>  $ results:List of 1
#>   ..$ :List of 5
#>   .. ..$ address_components:List of 4
#>   .. .. ..$ :List of 3
#>   .. .. .. ..$ long_name : chr "Houston"
#>   .. .. .. ..$ short_name: chr "Houston"
#>   .. .. .. ..$ types     :List of 2
#>   .. .. .. .. ..$ : chr "locality"
#>   .. .. .. .. ..$ : chr "political"
#>   .. .. ..$ :List of 3
#>   .. .. .. ..$ long_name : chr "Harris County"
#>   .. .. .. ..$ short_name: chr "Harris County"
#>   .. .. .. ..$ types     :List of 2
#>   .. .. .. .. ..$ : chr "administrative_area_level_2"
#>   .. .. .. .. ..$ : chr "political"
#>   .. .. ..$ :List of 3
#>   .. .. .. ..$ long_name : chr "Texas"
#>   .. .. .. ..$ short_name: chr "TX"
#>   .. .. .. ..$ types     :List of 2
#>   .. .. .. .. ..$ : chr "administrative_area_level_1"
#>   .. .. .. .. ..$ : chr "political"
#>   .. .. ..$ :List of 3
#>   .. .. .. ..$ long_name : chr "United States"
#>   .. .. .. ..$ short_name: chr "US"
#>   .. .. .. ..$ types     :List of 2
#>   .. .. .. .. ..$ : chr "country"
#>   .. .. .. .. ..$ : chr "political"
#>   .. ..$ formatted_address : chr "Houston, TX, USA"
#>   .. ..$ geometry          :List of 4
#>   .. .. ..$ bounds       :List of 2
#>   .. .. .. ..$ northeast:List of 2
#>   .. .. .. .. ..$ lat: num 30.1
#>   .. .. .. .. ..$ lng: num -95
#>   .. .. .. ..$ southwest:List of 2
#>   .. .. .. .. ..$ lat: num 29.5
#>   .. .. .. .. ..$ lng: num -95.8
#>   .. .. ..$ location     :List of 2
#>   .. .. .. ..$ lat: num 29.8
#>   .. .. .. ..$ lng: num -95.4
#>   .. .. ..$ location_type: chr "APPROXIMATE"
#>   .. .. ..$ viewport     :List of 2
#>   .. .. .. ..$ northeast:List of 2
#>   .. .. .. .. ..$ lat: num 30.1
#>   .. .. .. .. ..$ lng: num -95
#>   .. .. .. ..$ southwest:List of 2
#>   .. .. .. .. ..$ lat: num 29.5
#>   .. .. .. .. ..$ lng: num -95.8
#>   .. ..$ place_id          : chr "ChIJAYWNSLS4QIYROwVl894CDco"
#>   .. ..$ types             :List of 2
#>   .. .. ..$ : chr "locality"
#>   .. .. ..$ : chr "political"
#>  $ status : chr "OK"
```

К счастью, мы можем пошагово решить проблему преобразования этих данных в табличный вид с помощью функций `tidyr`. Чтобы сделать задачу немного сложнее и реалистичнее, я начну с геокодирования нескольких городов:

```

  city <-   c ( "Houston" , "LA" , "New York" , "Chicago" , "Springfield" )  city_geo <-   purrr::map (city, geocode)
```

Полученный результат я преобразую в `tibble`, для удобства добавлю столбец с соответствующим названием города.

```

loc <- tibble(city = city, json = city_geo)
loc
#> # A tibble: 5 x 2
#>   city        json            
#>   <chr>       <list>          
#> 1 Houston     <named list [2]>
#> 2 LA          <named list [2]>
#> 3 New York    <named list [2]>
#> 4 Chicago     <named list [2]>
#> 5 Springfield <named list [2]>
```

Первый уровень содержит компоненты `status` и `result`, который мы можем развернуть с помощью `unnest_wider()` :

```

loc %>%
  unnest_wider(json)
#> # A tibble: 5 x 3
#>   city        results    status
#>   <chr>       <list>     <chr> 
#> 1 Houston     <list [1]> OK    
#> 2 LA          <list [1]> OK    
#> 3 New York    <list [1]> OK    
#> 4 Chicago     <list [1]> OK    
#> 5 Springfield <list [1]> OK
```

Обратите внимание, что `results` является многоуровневым списком. У большинства городов есть 1 элемент (представляющий уникальное значение, соответствующее API геокодирования), но у Спрингфилда их два. Мы можем вытащить их в отдельные строки с помощью `unnest_longer()` :

```

loc %>%
  unnest_wider(json) %>% 
  unnest_longer(results)
#> # A tibble: 5 x 3
#>   city        results          status
#>   <chr>       <list>           <chr> 
#> 1 Houston     <named list [5]> OK    
#> 2 LA          <named list [5]> OK    
#> 3 New York    <named list [5]> OK    
#> 4 Chicago     <named list [5]> OK    
#> 5 Springfield <named list [5]> OK
```

Теперь все они имеют одинаковые компоненты, в чём можно убедиться с помощью `unnest_wider()`:

```

loc %>%
  unnest_wider(json) %>% 
  unnest_longer(results) %>% 
  unnest_wider(results)
#> # A tibble: 5 x 7
#>   city   address_componen… formatted_addre… geometry place_id  types status
#>   <chr>  <list>            <chr>            <list>   <chr>     <lis> <chr> 
#> 1 Houst… <list [4]>        Houston, TX, USA <named … ChIJAYWN… <lis… OK    
#> 2 LA     <list [4]>        Los Angeles, CA… <named … ChIJE9on… <lis… OK    
#> 3 New Y… <list [3]>        New York, NY, U… <named … ChIJOwg_… <lis… OK    
#> 4 Chica… <list [4]>        Chicago, IL, USA <named … ChIJ7cv0… <lis… OK    
#> 5 Sprin… <list [5]>        Springfield, MO… <named … ChIJP5jI… <lis… OK
```

Мы можем найти координаты широты и долготы каждого города развернув список `geometry`:

```

loc %>%
  unnest_wider(json) %>% 
  unnest_longer(results) %>% 
  unnest_wider(results) %>% 
  unnest_wider(geometry)
#> # A tibble: 5 x 10
#>   city  address_compone… formatted_addre… bounds location location_type
#>   <chr> <list>           <chr>            <list> <list>   <chr>        
#> 1 Hous… <list [4]>       Houston, TX, USA <name… <named … APPROXIMATE  
#> 2 LA    <list [4]>       Los Angeles, CA… <name… <named … APPROXIMATE  
#> 3 New … <list [3]>       New York, NY, U… <name… <named … APPROXIMATE  
#> 4 Chic… <list [4]>       Chicago, IL, USA <name… <named … APPROXIMATE  
#> 5 Spri… <list [5]>       Springfield, MO… <name… <named … APPROXIMATE  
#> # … with 4 more variables: viewport <list>, place_id <chr>, types <list>,
#> #   status <chr>
```

А затем местоположение, для чего требуется развернуть `location`:

```

loc %>%
  unnest_wider(json) %>%
  unnest_longer(results) %>%
  unnest_wider(results) %>%
  unnest_wider(geometry) %>%
  unnest_wider(location)
#> # A tibble: 5 x 11
#>   city  address_compone… formatted_addre… bounds   lat    lng location_type
#>   <chr> <list>           <chr>            <list> <dbl>  <dbl> <chr>        
#> 1 Hous… <list [4]>       Houston, TX, USA <name…  29.8  -95.4 APPROXIMATE  
#> 2 LA    <list [4]>       Los Angeles, CA… <name…  34.1 -118.  APPROXIMATE  
#> 3 New … <list [3]>       New York, NY, U… <name…  40.7  -74.0 APPROXIMATE  
#> 4 Chic… <list [4]>       Chicago, IL, USA <name…  41.9  -87.6 APPROXIMATE  
#> 5 Spri… <list [5]>       Springfield, MO… <name…  37.2  -93.3 APPROXIMATE  
#> # … with 4 more variables: viewport <list>, place_id <chr>, types <list>,
#> #   status <chr>
```

Опять же, `unnest_auto()` упрощает описанную операцию с некоторыми рисками, которые могут быть вызваны изменением структуры входящих данных:

```

loc %>%
  unnest_auto(json) %>%
  unnest_auto(results) %>%
  unnest_auto(results) %>%
  unnest_auto(geometry) %>%
  unnest_auto(location)
#> Using `unnest_wider(json)`; elements have 2 names in common
#> Using `unnest_longer(results)`; no element has names
#> Using `unnest_wider(results)`; elements have 5 names in common
#> Using `unnest_wider(geometry)`; elements have 4 names in common
#> Using `unnest_wider(location)`; elements have 2 names in common
#> # A tibble: 5 x 11
#>   city  address_compone… formatted_addre… bounds   lat    lng location_type
#>   <chr> <list>           <chr>            <list> <dbl>  <dbl> <chr>        
#> 1 Hous… <list [4]>       Houston, TX, USA <name…  29.8  -95.4 APPROXIMATE  
#> 2 LA    <list [4]>       Los Angeles, CA… <name…  34.1 -118.  APPROXIMATE  
#> 3 New … <list [3]>       New York, NY, U… <name…  40.7  -74.0 APPROXIMATE  
#> 4 Chic… <list [4]>       Chicago, IL, USA <name…  41.9  -87.6 APPROXIMATE  
#> 5 Spri… <list [5]>       Springfield, MO… <name…  37.2  -93.3 APPROXIMATE  
#> # … with 4 more variables: viewport <list>, place_id <chr>, types <list>,
#> #   status <chr>
```

Мы также можем просто посмотреть на первый адрес для каждого города:

```

loc %>%
  unnest_wider(json) %>%
  hoist(results, first_result = 1) %>%
  unnest_wider(first_result) %>%
  unnest_wider(geometry) %>%
  unnest_wider(location)
#> # A tibble: 5 x 11
#>   city  address_compone… formatted_addre… bounds   lat    lng location_type
#>   <chr> <list>           <chr>            <list> <dbl>  <dbl> <chr>        
#> 1 Hous… <list [4]>       Houston, TX, USA <name…  29.8  -95.4 APPROXIMATE  
#> 2 LA    <list [4]>       Los Angeles, CA… <name…  34.1 -118.  APPROXIMATE  
#> 3 New … <list [3]>       New York, NY, U… <name…  40.7  -74.0 APPROXIMATE  
#> 4 Chic… <list [4]>       Chicago, IL, USA <name…  41.9  -87.6 APPROXIMATE  
#> 5 Spri… <list [5]>       Springfield, MO… <name…  37.2  -93.3 APPROXIMATE  
#> # … with 4 more variables: viewport <list>, place_id <chr>, types <list>,
#> #   status <chr>
```

Или использовать `hoist()` для многоуровневого погружения, чтобы перейти непосредственно к `lat` и `lng`.

```

loc %>%
  hoist(json,
    lat = list("results", 1, "geometry", "location", "lat"),
    lng = list("results", 1, "geometry", "location", "lng")
  )
#> # A tibble: 5 x 4
#>   city          lat    lng json            
#>   <chr>       <dbl>  <dbl> <list>          
#> 1 Houston      29.8  -95.4 <named list [2]>
#> 2 LA           34.1 -118.  <named list [2]>
#> 3 New York     40.7  -74.0 <named list [2]>
#> 4 Chicago      41.9  -87.6 <named list [2]>
#> 5 Springfield  37.2  -93.3 <named list [2]>
```

# Дискография Шарлы Гельфанд

В завершении мы рассмотрим самую сложную конструкцию — дискографию Шарлы Гельфанд. Как и в приведённых выше примерах, мы начинаем с конвертации списка в дата фрейм с одним столбцом, а затем расширим его, чтобы каждый компонент был отдельным столбцом. Также я преобразую столбец `date_added` в соответствующий формат даты и времени в R.

```

discs <- tibble(disc = discog) %>% 
  unnest_wider(disc) %>% 
  mutate(date_added = as.POSIXct(strptime(date_added, "%Y-%m-%dT%H:%M:%S"))) 
discs
#> # A tibble: 155 x 5
#>    instance_id date_added          basic_information       id rating
#>          <int> <dttm>              <list>               <int>  <int>
#>  1   354823933 2019-02-16 17:48:59 <named list [11]>  7496378      0
#>  2   354092601 2019-02-13 14:13:11 <named list [11]>  4490852      0
#>  3   354091476 2019-02-13 14:07:23 <named list [11]>  9827276      0
#>  4   351244906 2019-02-02 11:39:58 <named list [11]>  9769203      0
#>  5   351244801 2019-02-02 11:39:37 <named list [11]>  7237138      0
#>  6   351052065 2019-02-01 20:40:53 <named list [11]> 13117042      0
#>  7   350315345 2019-01-29 15:48:37 <named list [11]>  7113575      0
#>  8   350315103 2019-01-29 15:47:22 <named list [11]> 10540713      0
#>  9   350314507 2019-01-29 15:44:08 <named list [11]> 11260950      0
#> 10   350314047 2019-01-29 15:41:35 <named list [11]> 11726853      0
#> # … with 145 more rows
```

На этом уровне мы получили информацию о том, когда каждый диск был добавлен в дискографию Шарлы, но при этом не видим никаких данных об этих дисках. Для этого нам нужно расширить столбец `basic_information`:

```

discs %>% unnest_wider(basic_information)
#> Column name `id` must not be duplicated.
#> Use .name_repair to specify repair.
```

К сожалению мы получим ошибку, т.к. внутри списка `basic_information` есть одноимённый столбец `basic_information`. При возникновении подобной ошибки, для того, что бы быстро определить её причину можно использовать `names_repair = "unique"`:

```

discs %>% unnest_wider(basic_information, names_repair = "unique")
#> New names:
#> * id -> id...6
#> * id -> id...14
#> # A tibble: 155 x 15
#>    instance_id date_added          labels  year artists id...6 thumb title
#>          <int> <dttm>              <list> <int> <list>   <int> <chr> <chr>
#>  1   354823933 2019-02-16 17:48:59 <list…  2015 <list … 7.50e6 http… Demo 
#>  2   354092601 2019-02-13 14:13:11 <list…  2013 <list … 4.49e6 http… Obse…
#>  3   354091476 2019-02-13 14:07:23 <list…  2017 <list … 9.83e6 http… I    
#>  4   351244906 2019-02-02 11:39:58 <list…  2017 <list … 9.77e6 http… Oído…
#>  5   351244801 2019-02-02 11:39:37 <list…  2015 <list … 7.24e6 http… A Ca…
#>  6   351052065 2019-02-01 20:40:53 <list…  2019 <list … 1.31e7 http… Tash…
#>  7   350315345 2019-01-29 15:48:37 <list…  2014 <list … 7.11e6 http… Demo 
#>  8   350315103 2019-01-29 15:47:22 <list…  2015 <list … 1.05e7 http… Let …
#>  9   350314507 2019-01-29 15:44:08 <list…  2017 <list … 1.13e7 ""    Sub …
#> 10   350314047 2019-01-29 15:41:35 <list…  2017 <list … 1.17e7 http… Demo 
#> # … with 145 more rows, and 7 more variables: formats <list>,
#> #   cover_image <chr>, resource_url <chr>, master_id <int>,
#> #   master_url <chr>, id...14 <int>, rating <int>
```

Проблема в том, что `basic_information` повторяет столбец id который также хранится на верхнем уровне, поэтому мы можем просто удалить его:

```

discs %>% 
  select(-id) %>% 
  unnest_wider(basic_information)
#> # A tibble: 155 x 14
#>    instance_id date_added          labels  year artists     id thumb title
#>          <int> <dttm>              <list> <int> <list>   <int> <chr> <chr>
#>  1   354823933 2019-02-16 17:48:59 <list…  2015 <list … 7.50e6 http… Demo 
#>  2   354092601 2019-02-13 14:13:11 <list…  2013 <list … 4.49e6 http… Obse…
#>  3   354091476 2019-02-13 14:07:23 <list…  2017 <list … 9.83e6 http… I    
#>  4   351244906 2019-02-02 11:39:58 <list…  2017 <list … 9.77e6 http… Oído…
#>  5   351244801 2019-02-02 11:39:37 <list…  2015 <list … 7.24e6 http… A Ca…
#>  6   351052065 2019-02-01 20:40:53 <list…  2019 <list … 1.31e7 http… Tash…
#>  7   350315345 2019-01-29 15:48:37 <list…  2014 <list … 7.11e6 http… Demo 
#>  8   350315103 2019-01-29 15:47:22 <list…  2015 <list … 1.05e7 http… Let …
#>  9   350314507 2019-01-29 15:44:08 <list…  2017 <list … 1.13e7 ""    Sub …
#> 10   350314047 2019-01-29 15:41:35 <list…  2017 <list … 1.17e7 http… Demo 
#> # … with 145 more rows, and 6 more variables: formats <list>,
#> #   cover_image <chr>, resource_url <chr>, master_id <int>,
#> #   master_url <chr>, rating <int>
```

В качестве альтернативы, мы могли бы использовать `hoist()`:

```

discs %>% 
  hoist(basic_information,
    title = "title",
    year = "year",
    label = list("labels", 1, "name"),
    artist = list("artists", 1, "name")
  )
#> # A tibble: 155 x 9
#>    instance_id date_added          title  year label artist
#>          <int> <dttm>              <chr> <int> <chr> <chr> 
#>  1   354823933 2019-02-16 17:48:59 Demo   2015 Tobi… Mollot
#>  2   354092601 2019-02-13 14:13:11 Obse…  2013 La V… Una B…
#>  3   354091476 2019-02-13 14:07:23 I      2017 La V… S.H.I…
#>  4   351244906 2019-02-02 11:39:58 Oído…  2017 La V… Rata …
#>  5   351244801 2019-02-02 11:39:37 A Ca…  2015 Kato… Ivy (…
#>  6   351052065 2019-02-01 20:40:53 Tash…  2019 High… Tashme
#>  7   350315345 2019-01-29 15:48:37 Demo   2014 Mind… Desgr…
#>  8   350315103 2019-01-29 15:47:22 Let …  2015 Not … Phant…
#>  9   350314507 2019-01-29 15:44:08 Sub …  2017 Not … Sub S…
#> 10   350314047 2019-01-29 15:41:35 Demo   2017 Pres… Small…
#> # … with 145 more rows, and 3 more variables: basic_information <list>,
#> #   id <int>, rating <int>
```

Здесь я быстро извлекаю имя первого лейбла и исполнителя по индексу, погрузившись во вложенный список.

Более систематический подход заключается в создании отдельных таблиц для исполнителя и лейбла:

```

discs %>% 
  hoist(basic_information, artist = "artists") %>% 
  select(disc_id = id, artist) %>% 
  unnest_longer(artist) %>% 
  unnest_wider(artist)
#> # A tibble: 167 x 8
#>     disc_id join  name        anv   tracks role  resource_url            id
#>       <int> <chr> <chr>       <chr> <chr>  <chr> <chr>                <int>
#>  1  7496378 ""    Mollot      ""    ""     ""    https://api.discog… 4.62e6
#>  2  4490852 ""    Una Bèstia… ""    ""     ""    https://api.discog… 3.19e6
#>  3  9827276 ""    S.H.I.T. (… ""    ""     ""    https://api.discog… 2.77e6
#>  4  9769203 ""    Rata Negra  ""    ""     ""    https://api.discog… 4.28e6
#>  5  7237138 ""    Ivy (18)    ""    ""     ""    https://api.discog… 3.60e6
#>  6 13117042 ""    Tashme      ""    ""     ""    https://api.discog… 5.21e6
#>  7  7113575 ""    Desgraciad… ""    ""     ""    https://api.discog… 4.45e6
#>  8 10540713 ""    Phantom He… ""    ""     ""    https://api.discog… 4.27e6
#>  9 11260950 ""    Sub Space … ""    ""     ""    https://api.discog… 5.69e6
#> 10 11726853 ""    Small Man … ""    ""     ""    https://api.discog… 6.37e6
#> # … with 157 more rows

discs %>% 
  hoist(basic_information, format = "formats") %>% 
  select(disc_id = id, format) %>% 
  unnest_longer(format) %>% 
  unnest_wider(format) %>% 
  unnest_longer(descriptions)
#> # A tibble: 280 x 5
#>     disc_id descriptions text  name     qty  
#>       <int> <chr>        <chr> <chr>    <chr>
#>  1  7496378 Numbered     Black Cassette 1    
#>  2  4490852 LP           <NA>  Vinyl    1    
#>  3  9827276 "7\""        <NA>  Vinyl    1    
#>  4  9827276 45 RPM       <NA>  Vinyl    1    
#>  5  9827276 EP           <NA>  Vinyl    1    
#>  6  9769203 LP           <NA>  Vinyl    1    
#>  7  9769203 Album        <NA>  Vinyl    1    
#>  8  7237138 "7\""        <NA>  Vinyl    1    
#>  9  7237138 45 RPM       <NA>  Vinyl    1    
#> 10 13117042 "7\""        <NA>  Vinyl    1    
#> # … with 270 more rows
```

Затем вы можете присоединить их обратно к исходному набору данных по мере необходимости.

# Заключение

В ядро библиотеки `tidyverse` входят множество полезных пакетов объединённые общей философией обработки данных.

В этой статье мы разобрали семейство функций `unnest_*()`, которые направлены на работу с извлечением элементов из вложенных списков. Данный пакет содержит множество других полезных функций, которые упрощают преобразование данных согласно концепции *Tidy Data*
