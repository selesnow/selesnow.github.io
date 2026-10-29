# Скрипт автоматического создания Custom Dimensions в Google Analytics 4 через GA4 Admin API
# Требуются пакеты: googleAnalyticsR, googleAuthR, httr, jsonlite

suppressPackageStartupMessages({
  library(googleAnalyticsR)
  library(googleAuthR)
  library(httr)
  library(jsonlite)
})

options(rlang_interactive = TRUE)
options(gargle_oob_default = FALSE)

message("\n=== Авторизация в Google Analytics ===")
# Загружаем сохранённый токен из кеша gargle
tok_file <- "C:/Users/User/AppData/Local/gargle/gargle/Cache/9b80f6a79b3080c58c5dd1e54bf00a07_selesnow@gmail.com"
if (!file.exists(tok_file)) {
  # Поиск по шаблону
  tok_file <- list.files("C:/Users/User/AppData/Local/gargle/gargle/Cache", pattern = "9b80f6", full.names = TRUE)[1]
}
tok <- readRDS(tok_file)
tok$refresh()
token_str <- tok$credentials$access_token

property_id <- "282495698"
message(sprintf("Выбран ресурс Property ID: %s", property_id))

# Получаем уже существующие параметры
url_base <- sprintf("https://analyticsadmin.googleapis.com/v1beta/properties/%s/customDimensions", property_id)
resp <- GET(url_base, add_headers(Authorization = paste("Bearer", token_str)))

existing_params <- character(0)
if (status_code(resp) == 200) {
  content_data <- fromJSON(content(resp, as = "text", encoding = "UTF-8"))
  if (!is.null(content_data$customDimensions) && length(content_data$customDimensions$parameterName) > 0) {
    existing_params <- content_data$customDimensions$parameterName
  }
} else {
  message(sprintf("Предупреждение при получении списка (%d): %s", status_code(resp), content(resp, as = "text")))
}

message(sprintf("Уже создано параметров в ресурсе: %d", length(existing_params)))

# Список всех необходимых параметров сайта
dims <- list(
  list(param = "contact_type", name = "Тип контакта", desc = "telegram, email"),
  list(param = "placement", name = "Место размещения", desc = "hero, contacts_section, footer, nav, landing_slider"),
  list(param = "platform", name = "Платформа", desc = "telegram, youtube, habr, blog"),
  list(param = "course_id", name = "ID курса", desc = "Идентификатор курса (r4excel, dplyr и др.)"),
  list(param = "course_name", name = "Название курса", desc = "Название курса"),
  list(param = "course_level", name = "Уровень курса", desc = "beginner, middle, advanced, new"),
  list(param = "target_type", name = "Тип цели перехода", desc = "site, book, youtube_playlist"),
  list(param = "resource_type", name = "Тип ресурса курса", desc = "playlist, materials, article"),
  list(param = "package_name", name = "Имя R пакета", desc = "Имя пакета (rgoogleads, rym и др.)"),
  list(param = "action_type", name = "Действие по пакету", desc = "github, cran, docs, video, article"),
  list(param = "video_id", name = "ID видео YouTube", desc = "Идентификатор видео на YouTube"),
  list(param = "video_title", name = "Заголовок видео", desc = "Название доклада или видеоурока"),
  list(param = "content_title", name = "Заголовок контента", desc = "Название статьи, доклада или интервью"),
  list(param = "content_type", name = "Тип контента", desc = "article, interview, conference_materials, playlist"),
  list(param = "section", name = "Раздел сайта", desc = "Раздел сайта"),
  list(param = "search_section", name = "Раздел поиска", desc = "Раздел, где производился поиск"),
  list(param = "results_count", name = "Результатов поиска", desc = "Количество найденных карточек"),
  list(param = "filter_group", name = "Группа фильтра", desc = "Группа фильтра (cat, type, speaking, topic)"),
  list(param = "filter_value", name = "Значение фильтра", desc = "Выбранное значение фильтра"),
  list(param = "selected_language", name = "Выбранный язык", desc = "en, ru, ua"),
  list(param = "previous_language", name = "Предыдущий язык", desc = "Язык до переключения"),
  list(param = "direction", name = "Направление слайдера", desc = "left, right"),
  list(param = "service_name", name = "Имя сервиса статистики рекламы", desc = "TGStat, Telemetr"),
  list(param = "poll_id", name = "ID опроса рекламы", desc = "geo, cities, income и др."),
  list(param = "exchange_name", name = "Биржа рекламы", desc = "Название биржи")
)

message("\n=== Создание параметров ===")
created_count <- 0
skipped_count <- 0

for (d in dims) {
  if (d$param %in% existing_params) {
    message(sprintf("  [ПРОПУСК] Уже существует: %s (%s)", d$param, d$name))
    skipped_count <- skipped_count + 1
    next
  }

  body <- list(
    parameterName = d$param,
    displayName = d$name,
    description = d$desc,
    scope = "EVENT"
  )

  post_resp <- POST(
    url_base,
    add_headers(
      Authorization = paste("Bearer", token_str),
      "Content-Type" = "application/json; charset=utf-8"
    ),
    body = toJSON(body, auto_unbox = TRUE)
  )

  if (status_code(post_resp) %in% c(200, 201)) {
    message(sprintf("  [СОЗДАН] %s (%s)", d$param, d$name))
    created_count <- created_count + 1
  } else {
    err_msg <- content(post_resp, as = "text", encoding = "UTF-8")
    message(sprintf("  [ОШИБКА] %s: %s", d$param, err_msg))
  }
  Sys.sleep(0.3)
}

message(sprintf("\nГотово! Создано новых: %d, пропущено существующих: %d\n", created_count, skipped_count))
