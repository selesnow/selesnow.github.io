# Выгрузка плейлиста курса «Язык R для интернет-маркетинга» в _build/data/rcourse_playlist.csv.
# Запуск из корня репозитория:  Rscript _build/rcourse_fetch_playlist.R
# Нужна авторизация rytstat (ryt_auth) в аккаунте с доступом к каналу R4marketing.
suppressPackageStartupMessages(library(rytstat))
ryt_auth(Sys.getenv("RYT_EMAIL", "r4marketing-6832@pages.plusgoogle.com"))

items <- ryt_get_playlist_items("PLD2LDq8edf4o6dSZ4BIr7J08gT97nimH_")
dur <- vapply(items$video_id, function(id) {
  v <- tryCatch(ryt_get_video_details(id, part = "contentDetails"), error = function(e) NULL)
  if (is.null(v) || nrow(v) == 0) NA_character_ else as.character(v$duration[1])
}, character(1))

d <- data.frame(
  position     = items$position,
  video_id     = items$video_id,
  title        = items$title,
  duration     = unname(dur),
  published_at = items$video_published_at,
  description  = items$description,
  stringsAsFactors = FALSE
)
con <- file("_build/data/rcourse_playlist.csv", "w", encoding = "UTF-8")
write.csv(d, con, row.names = FALSE)
close(con)
cat("Сохранено видео:", nrow(d), "\n")
