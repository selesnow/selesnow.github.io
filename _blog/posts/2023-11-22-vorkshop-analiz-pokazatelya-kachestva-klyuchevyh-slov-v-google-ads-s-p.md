---
title: 'Воркшоп: Анализ показателя качества ключевых слов в Google Ads с помощью языка R и пакета rgoogleads'
date: '2023-11-22'
slug: vorkshop-analiz-pokazatelya-kachestva-klyuchevyh-slov-v-google-ads-s-p
tags:
- Google Ads
categories:
- Выступления
- Google Ads
- Реклама
description: Воркшоп по работе с Google Ads API с помощью языка R и пакета rgoogleads. В ходе которого мы с нуля разберёмся как пройти авторизацию, запрашивать отчёты из Google Ads, и проанализируем показатель качества ключевых слов рекламного аккаунта.
original_url: https://alexeyseleznev.wordpress.com/2023/11/22/%d0%b2%d0%be%d1%80%d0%ba%d1%88%d0%be%d0%bf-%d0%b0%d0%bd%d0%b0%d0%bb%d0%b8%d0%b7-%d0%bf%d0%be%d0%ba%d0%b0%d0%b7%d0%b0%d1%82%d0%b5%d0%bb%d1%8f-%d0%ba%d0%b0%d1%87%d0%b5%d1%81%d1%82%d0%b2%d0%b0-%d0%ba/
wp_id: 1594
draft: false
cover: ../images/covers/1594.webp
cover_generated: true
---

Воркшоп по работе с Google Ads API с помощью языка R и пакета rgoogleads. В ходе которого мы с нуля разберёмся как пройти авторизацию, запрашивать отчёты из Google Ads, и проанализируем показатель качества ключевых слов рекламного аккаунта.

## Видео

{{video: https://www.youtube.com/embed/EnImByySQEE?version=3&rel=1&showsearch=0&showinfo=1&iv\_load\_policy=1&fs=1&hl=en&autohide=2&wmode=transparent}}

### Тайм коды:

- 00:00:00 Приветствие
- 00:01:12 О спикере
- 00:03:43 Программа воркшопа
- 00:04:14 Что такое контекстная реклама и сервис Google Ads
- 00:06:34 Варианты авторизации в пакете rgoogleads
- 00:07:24 Авторизация в Google Ads с помощью дефолтных параметров пакета rgoogleads
- 00:10:00 Создание собственных учётных данных для авторизации
- 00:21:12 Авторизация в Google Ads с помощью собственных учётных данных
- 00:23:00 Иерархия аккаунтов в Google Ads API
- 00:24:53 Ограничения при использовании собственных учётных данных
- 00:25:54 Автоматизация процесса авторизации с помощью переменных среды
- 00:26:43 Опции пакеа rgoogleads
- 00:27:34 Запрос отчётов из Google Ads API
- 00:30:49 GAQL QueryBuilder
- 00:34:52 Пример запроса отчётов из Google Ads API
- 00:39:54 Аргументы функции gads\_get\_report()
- 00:41:13 Загрузка отчётов из Google Ads API в многопоточном режиме
- 00:44:34 Запрос объектов рекламного кабинета Google Ads
- 00:45:49 Что такое показатель качества ключевых слов и как проходит аукцион среди рекламодателей в Google Ads
- 00:47:47 Что влияет на показатель качества ключевых слов Google Ads
- 00:48:29 На что влияет показатель качества Google Ads
- 00:49:16 Пример анализа качества ключевых слов
- 01:03:36 Ответы на вопросы

## Презентация

{{video: https://www.slideshare.net/slideshow/embed\_code/key/3vdHb3FFOzT8mv}}

{{video: https://www.slideshare.net/slideshow/embed\_code/key/3vdHb3FFOzT8mv}}

from **[Алексей Селезнёв](https://www.slideshare.net/ssuser459d25)**

## Материалы к воркшопу

### Скрипт 1-google-ads-auth.R

```

library(rgoogleads)

# простейший способ авторизации
gads_auth('a.seleznev@netpeak.group')

# учётные данные кешируются в файл
gads_auth_cache_path()
gads_open_auth_cache_folder()

# настройка конфигурации авторизации
gads_auth_configure(
  path = 'auth/gads.client.json'
    )

gads_auth('a.seleznow@netpeak.group')

# иерархия аккаунтов
top_accounts <- gads_get_accessible_customers()

# опции
gads_set_login_customer_id(1754107253)

# запрос все иерархии аккаунтов
account_hie <- gads_get_account_hierarchy()
```

### Скрипт 2-google-ads-reporting.R

```

library(rgoogleads)

# ####################################
# авторизация
gads_auth('a.seleznev@netpeak.group')

# ####################################
# установка клиентского и упраляющего аккаунта
gads_set_login_customer_id("175-410-7253")
gads_set_customer_id("896-697-8643")

# ####################################
# запрос данных используя текст GAQL запроса
## Текст запроса
campaign_query <- "
SELECT 
  campaign.id, 
  campaign.name, 
  segments.date, 
  metrics.clicks, 
  metrics.impressions 
FROM campaign 
WHERE 
  segments.date DURING THIS_MONTH AND metrics.clicks > 0
"

## Запрос данных
campaign_data <- gads_get_report(gaql_query = campaign_query) 

# ####################################
# метаданные и информация о ресурсах
resources <- gads_get_metadata("RESOURCE")
metadata  <- gads_get_metadata("ALL")

fields    <- gads_get_fields("campaign")

# ####################################
# Задаём параметры запроса внутри gads_get_report()
## Повторяем используемый ранее запрос, но через параметры функции
campaign_data_2 <- gads_get_report(
  resource = "campaign", 
  fields   = c("campaign.id", 
               "campaign.name",
               "segments.date", 
               "metrics.clicks",
               "metrics.impressions"), 
  during = "THIS_MONTH",
  where  = "metrics.clicks > 0") 

# Статичные даты
campaign_data_3 <- gads_get_report(
  resource = "campaign", 
  fields   = c("campaign.id", 
    "campaign.name",
    "segments.date", 
    "metrics.clicks",
    "metrics.impressions"), 
  date_from = "2022-04-01", date_to = "2022-04-19",
  where  = "metrics.clicks > 0") 

# ####################################
# Использование многопоточности
## задаём список клиентских аккаунтов
client_ids <- c(
  "896-697-8643", 
  "201-949-5809", 
  "263-160-7978", 
  "793-293-9250", 
  "927-254-7535")

gads_set_login_customer_id("175-410-7253")
gads_set_customer_id(client_ids)

## создаём кластер
cl <- parallel::makeCluster(4)

## выполняем запрос в многопоточном режиме
tictoc::tic("Loading in parallel")

multi_account_data <- gads_get_report(
  resource = "campaign", 
  fields   = c("campaign.id", 
    "campaign.name",
    "segments.date", 
    "metrics.clicks",
    "metrics.impressions"), 
  during = "THIS_MONTH",
  where  = "metrics.clicks > 0", 
  cl     = cl) 

tictoc::toc()

## останавливаем кластер
parallel::stopCluster(cl)

## запускаем тот же запрос в последовательном режиме
tictoc::tic("Loading in sequences")

multi_account_data <- gads_get_report(
  resource = "campaign", 
  fields   = c("campaign.id", 
    "campaign.name",
    "segments.date", 
    "metrics.clicks",
    "metrics.impressions"), 
  during = "THIS_MONTH",
  where  = "metrics.clicks > 0") 

tictoc::toc()

# ####################################
## Забираем списки объектов
gads_set_customer_id("927-254-7535")

campaigns <- gads_get_campaigns()
ad_groups <- gads_get_ad_groups()
ads       <- gads_get_ads()
keywords  <- gads_get_keywords(limit = 100)
```

### 3-google\_ads\_quality\_score\_analisys.R

```

# подключение пакетов
library(rgoogleads)
library(dplyr)
library(forcats)
library(ggplot2)

# авторизация
gads_auth('a.seleznev@netpeak.group')

# аккаунты
## управляющий аккаунт
gads_set_login_customer_id('175-410-7253')
## рекламный аккаунт
gads_set_customer_id('474-944-7568')

# запрос данных из Google Ads
ads_data <- gads_get_report(
  resource = 'keyword_view', 
  fields = c('customer.descriptive_name', 
             'ad_group_criterion.criterion_id', 
             'ad_group_criterion.final_urls',
             'ad_group_criterion.status',
             'ad_group.id', 
             'ad_group.name',
             'ad_group.status',
             'campaign.id',
             'campaign.name',
             'campaign.status',
             'metrics.impressions',
             'metrics.clicks',
             'metrics.cost_micros',
             'metrics.ctr',
             'metrics.search_top_impression_share',
             'ad_group_criterion.quality_info.creative_quality_score',
             'ad_group_criterion.quality_info.post_click_quality_score',
             'ad_group_criterion.quality_info.search_predicted_ctr', 
             'ad_group_criterion.quality_info.quality_score'),
  where     = c('metrics.impressions > 0', 
                'ad_group_criterion.quality_info.creative_quality_score IN ("ABOVE_AVERAGE", "AVERAGE", "BELOW_AVERAGE")'),
  during    = 'LAST_30_DAYS'
)

# Определяем группу показателя качества для каждого ключевого слова
ads_data <- mutate(ads_data, 
                   qiality_score_group = case_when(
                     ad_group_criterion_quality_info_quality_score <= 4           ~ 'Low',
                     between(ad_group_criterion_quality_info_quality_score, 5, 7) ~ 'Middle',
                     ad_group_criterion_quality_info_quality_score >= 8           ~ 'High'
                   )
)

# Визуализация среднего показателя качества в разрезе кампаний
ads_data %>% 
  group_by(campaign_name) %>% 
  summarise(avg_qs = mean(ad_group_criterion_quality_info_quality_score, na.rm = TRUE)) %>% 
  ggplot(aes(x = fct_reorder(.f = campaign_name, .x = avg_qs, .fun = median), y = avg_qs, fill = avg_qs)) +  
  geom_bar(stat = "identity", position = "dodge") +
  theme(axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5, size = 9)) + 
  scale_fill_gradient(low = hcl(15,100,75), high = hcl(195,100,75)) +
  ggtitle("Average Quality Score by Campaign") +
  xlab('Campaign') +
  ylab('Average Quality Score')

# Визуализация по группированному показателю качества
ads_data %>% 
  group_by(campaign_name, qiality_score_group) %>% 
  summarise(keywords_count = n_distinct(ad_group_criterion_criterion_id)) %>% 
  ggplot(aes(x = campaign_name, y = keywords_count,fill = qiality_score_group))+  
  geom_col(stat = "count", position = "fill") +  
  scale_fill_manual(breaks=c("High","Middle","Low"),
                    values=c(High = "forestgreen", 
                             Middle = "tan1" , 
                             Low = "firebrick1"))+  
  theme(axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5, size = 9))+  
  ggtitle("Number of keywords by Quality Score Group") +
  xlab('Campaign') +
  ylab('Kweywords number')

# Визуализация по релевантности объявления
ggplot(ads_data, aes(x = campaign_name, fill = ad_group_criterion_quality_info_creative_quality_score))+  
  geom_bar(stat = "count", position = "fill")+   
  scale_fill_manual(values=c("forestgreen", "tan1" , "firebrick1","grey" ))+  
  theme(axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5, size = 9), 
        legend.position = 'bottom')+  
  ggtitle("Landing page experience by Campaign") +
  xlab('Campaign') +
  ylab('Kweywords number')

# Визуализация по качеству целевой страницы
ggplot(ads_data, aes(x = campaign_name, fill = ad_group_criterion_quality_info_post_click_quality_score))+  
  geom_bar(stat = "count", position = "fill")+   
  scale_fill_manual(values=c("forestgreen", "tan1" , "firebrick1","grey" ))+  
  theme(axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5, size = 9), 
        legend.position = 'bottom')+  
  ggtitle("AdRelevance by Campaign") +
  xlab('Campaign') +
  ylab('Kweywords number')

# Визуализация по ожидаемому значению CTR
ggplot(ads_data, aes(x = campaign_name, fill = ad_group_criterion_quality_info_search_predicted_ctr))+  
  geom_bar(stat = "count", position = "fill")+   
  scale_fill_manual(values=c("forestgreen", "tan1" , "firebrick1","grey" ))+  
  theme(axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5, size = 9), 
        legend.position = 'bottom')+  
  ggtitle("Expected CTR by Campaign") +
  xlab('Campaign') +
  ylab('Kweywords number')

# оценка % показа над результатами поиска
ads_data %>% 
  group_by(qiality_score_group) %>% 
  mutate(med_impression_share = median(search_top_impression_share)) %>% 
  ggplot(aes(x = fct_relevel(qiality_score_group, "Low", "Middle", "High"), y = search_top_impression_share, fill = med_impression_share))+
  geom_boxplot(outlier.color = "grey", outlier.stroke = F) +
  scale_fill_gradient(high = hcl(15,100,75), low = hcl(195,100,75)) +
  scale_y_continuous(labels = scales::percent_format()) +
  theme(legend.position = 'none') +
  ggtitle("Search Top Impression Share by Quality Score Group") +
  xlab('Quality Score Group') +
  ylab('Search Top Impression Share, %')

# CTR в зависимости от группы показателя качества
ads_data %>% 
  group_by(qiality_score_group) %>% 
  mutate(med_ctr = median(ctr)) %>% 
  ggplot(aes(x = fct_relevel(qiality_score_group, "Low", "Middle", "High"), y = ctr, fill = med_ctr))+
  geom_boxplot(outlier.color = "grey", outlier.stroke = F) +
  scale_fill_gradient(high = hcl(15,100,75), low = hcl(195,100,75)) +
  scale_y_continuous(labels = scales::percent_format()) +
  theme(legend.position = 'none') +
  ggtitle("Search Top Impression Share by Quality Score Group") +
  xlab('Quality Score Group') +
  ylab('Search Top Impression Share, %')
```
