<head>
<link rel="shortcut icon" type="image/x-icon" href="as.ico">
<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-114798296-1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'UA-114798296-1');
</script>
</head>

<table>
    <tr>
      <td>
        <a href="https://selesnow.github.io/ryandexdirect/">ryandexdirect</a>
      </td>
      <td>
        <a href="https://selesnow.github.io/rfacebookstat/">rfacebookstat</a>
      </td>
      <td>
        <a href="https://selesnow.github.io/rvkstat/">rvkstat</a>
      </td>
      <td>
        <a href="https://selesnow.github.io/rmytarget/">rmytarget</a>
      </td>
      <td>
        <a href="https://selesnow.github.io/rmixpanel/">rmixpanel</a>
      </td>
      <td>
        <a href="https://selesnow.github.io/getProxy/">getProxy</a>
      </td>
    </tr>
</table>

# Выберите язык описания пакета | Chose language of package description
<table align="center">
  <tr>
    <td><a href="https://github.com/selesnow/rmixpanel/blob/master/ReadMe_EN.MD"><img src="http://img.freeflagicons.com/thumb/round_icon/united_kingdom/united_kingdom_640.png" height="80"></img></a></td>
    <td><a href="https://github.com/selesnow/rmixpanel/blob/master/ReadMe.md"><img src="http://izgranita.in.ua/img/ru_flag.ico" height="80"></img></a></td>
  </tr>
  <tr>
  <td align="center"><a href="https://github.com/selesnow/rmixpanel/blob/master/ReadMe_EN.MD">English</a></td> 
  <td align="center"><a href="https://github.com/selesnow/rmixpanel/blob/master/ReadMe.md">Русский</a></td> 
  </tr>
</table>

# Contents of rmixpanel read me.
* [Description of rmixpanel](https://github.com/selesnow/rmixpanel/blob/master/ReadMe_EN.MD#description-of-rmixpanel)
* [Instalation rmixpanel](https://github.com/selesnow/rmixpanel/blob/master/ReadMe_EN.MD#install-rmixpanel)
* [How get API Secret for work with API Mixpanel](https://github.com/selesnow/rmixpanel/blob/master/ReadMe_EN.MD#how-get-api_secret-для-работы-с-api-mixpanel)
* [Function of rmixpanel](https://github.com/selesnow/rmixpanel/blob/master/ReadMe_EN.MD#rmixpanel-functions)
  * [MP.getEvents](https://github.com/selesnow/rmixpanel/blob/master/ReadMe_EN.MD#mpgetevents---get-unique-total-or-average-data-for-a-set-of-events-over-n-days-weeks-or-months) - Get unique, total, or average data for a set of events over N days, weeks, or months.
  * [MP.getEventsProperty](https://github.com/selesnow/rmixpanel/blob/master/ReadMe_EN.MD#mpgeteventsproperty---get-unique-total-or-average-data-for-of-a-single-event-and-property-over-days-weeks-or-months) - Get unique, total, or average data for of a single event and property over days, weeks, or months.
  * [MP.getRetention](https://github.com/selesnow/rmixpanel/blob/master/ReadMe_EN.MD#mpgetretention----get-cohort-analysis) - Get cohort analysis.
  * [MP.getRawData](https://github.com/selesnow/rmixpanel/blob/master/ReadMe_EN.MD#mpgetrawdata----get-a-raw-dump-of-tracked-events-over-a-time-period) - Get a "raw dump" of tracked events over a time period.
* [About Author](https://github.com/selesnow/rmixpanel/blob/master/ReadMe_EN.MD#author-alexey-seleznev-head-of-analytics-dept-at-netpeak)

# Description of rmixpanel
rmixpanel is the R client for Mixpanel API, use this tool if you need load data from Mixpanel API into R.

For convenience of searching functions of rmixpanel, each function have prefix "MP.".

You can get detailed help about each of package function by `help ` command, for example if you need help about `MP.getRawData` function you can run `help("MP.getRawData")`.

In order to get list of all available rmixpanel fuction use `help(package = "rmixpanel")`.

# Install rmixpanel
You can instal rmixpanel from GitHub repository, for this run next code in R console.

```
if(!"rmixpanel" %in% installed.packages()[,1]){install.packages("devtools")}
devtools::install_github("selesnow/rmixpanel")
```

# How get api_secret для работы с API mixpanel
You can be found your api secret by clicking on your name in the upper righthand corner under Project Settings.

API Secret is a require argument of each rmixpanel functions.

1. Sing in mixpanel using your login and password.
![](http://img.netpeak.ua/alsey/150634204879_kiss_71kb.png)
2. Chose "Accounts" in main menu.
![](http://img.netpeak.ua/alsey/150634211597_kiss_33kb.png)
3. Go to tab "Projects", and copy API Secret of your project.
![](http://img.netpeak.ua/alsey/150634217727_kiss_57kb.png)

# rmixpanel functions
<table>
  <tr>
    <td>Name</td><td>Description</td>
  </tr>
  <tr>
    <td>MP.getEvents</td><td>Get unique, total, or average data for a set of events over N days, weeks, or months.</td>
  </tr>
    <tr>
    <td>MP.getEventsProperty</td><td>Get unique, total, or average data for of a single event and property over days, weeks, or months.</td>
  </tr>
    <tr>
     <td>MP.getRetention</td><td>Get cohort analysis.</td>
  </tr>
    <tr>
     <td>MP.getRawData</td><td>Get a "raw dump" of tracked events over a time period.</td>
  </tr>
</table>

## MP.getEvents - Get unique, total, or average data for a set of events over N days, weeks, or months.
### Arguments

* api_secret	- Your API Mixpanel secret, you can find hin in mixpanel web interface: Account (http://img.netpeak.ua/alsey/150600941068_kiss_10kb.png) > Projects (http://img.netpeak.ua/alsey/150600948369_kiss_46kb.png).
* event	- Character vector, the event or events that you wish to get data for, example c("play song", "log in", "add playlist").
* type	- The analysis type you would like to get data for - such as general, unique, or average events. Valid values:
  * "general" - Total events number
  * "unique" - Number of unique users commit event
  * "average" - Average events number on user
* unit	- It determines the level of granularity of the data you get back. Note that you cannot get hourly uniques, Valid values:
  * "minute" - Group by minutes
  * "hour" - Group by hours
  * "day" - Group by date
  * "week" - Group by week
  * "month" - Group by month
* interval	- The number of "units" to return data for - minutes, hours, days, weeks, or months. 1 will return data for the current unit (minute, hour, day, week or month). 2 will return the current and previous units, and so on. Specify either interval or from_date and to_date.
* from_date	- The first date to return data for, in yyyy-mm-dd format. This date is inclusive. Specify either interval or from_date and to_date.
* to_date		- The last date to return data for, in yyyy-mm-dd format. This date is inclusive. Specify either interval or from_date and to_date.

### Example
*Get total number of event "posting_success","emu","session_start","$custom_event:585946" from 1 june of 2017 till 25 july of 2017, with group by day.*
```
MP_events_day <- MP.getEvents(api_secret = "hgf7fi437nhdsad7863y98ryn988h8",
                              event = c("posting_success","emu","session_start","$custom_event:585946"),
                              type = "general",
                              unit = "day",
                              from_date = "2017-07-01",
                              to_date = "2017-07-25")
```
*Get average events number of event "session_start" and "$custom_event:585946" in the last two weeks, with group by month.*
```
MP_events_month <- MP.getEvents(api_secret = "hgf7fi437nhdsad7863y98ryn988h8",
                                event = c("session_start","$custom_event:585946"),
                                interval = 2,
                                type = "average",
                                unit = "month")
```

## MP.getEventsProperty - Get unique, total, or average data for of a single event and property over days, weeks, or months.
### Arguments
* api_secret	- Your API Mixpanel secret, you can find hin in mixpanel web interface: Account (http://img.netpeak.ua/alsey/150600941068_kiss_10kb.png) > Projects (http://img.netpeak.ua/alsey/150600948369_kiss_46kb.png).
* event	- Character vector, the event or events that you wish to get data, for example c("posting_success","emu","session_start","$custom_event:585946".
* property - The name of the property you would like to get data for. For example  "mp_country_code".
* values - The specific property values that you would like to get data for Example: If you have a property "gender" you may have values "male", "female" and "unknown". If you just want data for female and unknown users, you can include a values property that looks like "["female", "unknown"]".
* type	- The analysis type you would like to get data for - such as general, unique, or average events. Valid values:
  * "general" - Total events number
  * "unique" - Number of unique users commit event
  * "average" - Average events number on user
* unit	- It determines the level of granularity of the data you get back. Note that you cannot get hourly uniques, Valid values:
  * "minute" - Group by minutes
  * "hour" - Group by hours
  * "day" - Group by date
  * "week" - Group by week
  * "month" - Group by month
* interval	- The number of "units" to return data for - minutes, hours, days, weeks, or months. 1 will return data for the current unit (minute, hour, day, week or month). 2 will return the current and previous units, and so on. Specify either interval or from_date and to_date.
* tidy - Logical, if TRUE apply [tidy data](http://biostat-r.blogspot.com/2016/01/tidy-data.html) format, if FALSE apply report data format.
* from_date	- The first date to return data for, in yyyy-mm-dd format. This date is inclusive. Specify either interval or from_date and to_date.
* to_date		- The last date to return data for, in yyyy-mm-dd format. This date is inclusive. Specify either interval or from_date and to_date.
* limit - The maximum number of values to return.

### Example 
*Get total umber of event "$custom_event:585946" from 1 june of 2017 till 25 july of 2017, with group by day and property mp_country_code.*
```
MP_event_prop <- MP.getEventsProperty(api_secret = "hgf7fi437nhdsad7863y98ryn988h8",
                                      event = c("$custom_event:585946"),
                                      property = "mp_country_code",
                                      type = "general",
                                      unit = "day",
                                      from_date = "2017-07-01",
                                      to_date = "2017-07-25")
```
*Get total umber of event "$custom_event:585946" in current and previous month, with group by month and property mp_country_code.*
```
MP_event_prop_month <- MP.getEventsProperty(api_secret = "hgf7fi437nhdsad7863y98ryn988h8",
                                            event = c("$custom_event:585946"),
                                            property = "mp_country_code",
                                            type = "general",
                                            interval = 2,
                                            unit = "month")
```

## MP.getRetention  - Get cohort analysis.
### Arguments
* api_secret	- Your API Mixpanel secret, you can find hin in mixpanel web interface: Account (http://img.netpeak.ua/alsey/150600941068_kiss_10kb.png) > Projects (http://img.netpeak.ua/alsey/150600948369_kiss_46kb.png).
* event	- Character vector, the event or events that you wish to get data, for example c("posting_success","emu","session_start","$custom_event:585946".
* retention_type - Must be either "birth" or "compounded". Defaults to "birth". For example "compounded".
* born_event - The first event a user must do to be counted in a birth retention cohort. Required when retention_type is "birth"; ignored otherwise.
* born_where - An expression to filter the returning events by. For example 'properties["utm_source"]=="AdWords" and "Brand" in properties["utm_campaign"]', For more information go [link](https://mixpanel.com/help/reference/data-export-api#segmentation-expressions).
* where - An expression to filter the returning events by. For example 'properties["utm_source"]=="AdWords" and "Brand" in properties["utm_campaign"]', For more information go [link](https://mixpanel.com/help/reference/data-export-api#segmentation-expressions).
* unit	- It determines the level of granularity of the data you get back. Note that you cannot get hourly uniques, Valid values:
  * "minute" - Group by minutes
  * "hour" - Group by hours
  * "day" - Group by date
  * "week" - Group by week
  * "month" - Group by month
* interval	- The number of "units" to return data for - minutes, hours, days, weeks, or months. 1 will return data for the current unit (minute, hour, day, week or month). 2 will return the current and previous units, and so on. Specify either interval or from_date and to_date.
* interval_count - The number of intervals you want; defaults to 1. Note that we include a "0th" interval for events which take place less than one interval after the initial event.
* on - The property expression to segment the second event on. See the expressions [section above]( https://mixpanel.com/help/reference/data-export-api#segmentation-expressions), for example 'properties["utm_source"]'.
* tidy - Logical, if TRUE apply [tidy data](http://biostat-r.blogspot.com/2016/01/tidy-data.html) format, if FALSE apply report data format.
* from_date	- The first date to return data for, in yyyy-mm-dd format. This date is inclusive. Specify either interval or from_date and to_date.
* to_date		- The last date to return data for, in yyyy-mm-dd format. This date is inclusive. Specify either interval or from_date and to_date.

### Example
*Get cohort analisys by event "$custom_event:585946" from 1 june of 2017 till 25 july of 2017, with week steps*
```
retension <- MP.getRetention(api_secret = "hgf7fi437nhdsad7863y98ryn988h8",
                             event = "emu",
                             retention_type = "birth",
                             unit = "week",
                             born_event = "session_start",
                             where = 'properties["utm_source"]=="AdWords" and "Brand" in properties["utm_campaign"]',
                             interval_count = 4,
                             from_date = "2017-08-01",
                             to_date = "2017-09-25")
```
*Get cohort analisys by week, in last four weeks from 1 august of 2017, and segmentation cohort by propery utm_source.*
```
retension_property <- MP.getRetention(api_secret = "hgf7fi437nhdsad7863y98ryn988h8",
                                      event = "emu",
                                      retention_type = "birth",
                                      unit = "week",
                                      born_event = "session_start",
                                      on = 'properties["utm_source"]',
                                      interval_count = 4,
                                      from_date = "2017-08-01",
                                      to_date = "2017-09-25")
```

## MP.getRawData  - Get a "raw dump" of tracked events over a time period..
*Work duration of this function is too long and use him only if you can't get data using another functions.*

### Example usage cases
* If you receive a spike of 10K events but notice that only a few users contributed to it and would like to dive deeper into the data.
* If you are buying mobile ads and would like to dive deeper into the exact UDIDs and see who you really can attribute to the install.
* If you are doing some very custom analysis Mixpanel cannot currently do. If this is the case, please email support@mixpanel.com so we can either improve our product or possibly show you how you can do it with us.

### Arguments
* api_secret	- Your API Mixpanel secret, you can find hin in mixpanel web interface: Account (http://img.netpeak.ua/alsey/150600941068_kiss_10kb.png) > Projects (http://img.netpeak.ua/alsey/150600948369_kiss_46kb.png).
* event	- Character vector, the event or events that you wish to get data, for example c("posting_success","emu","session_start","$custom_event:585946".
* where - An expression to filter the returning events by. For example 'properties["utm_source"]=="AdWords" and "Brand" in properties["utm_campaign"]', For more information go [link](https://mixpanel.com/help/reference/data-export-api#segmentation-expressions).
* from_date	- The first date to return data for, in yyyy-mm-dd format. This date is inclusive. Specify either interval or from_date and to_date.
* to_date		- The last date to return data for, in yyyy-mm-dd format. This date is inclusive. Specify either interval or from_date and to_date.

### Example
*Get all events emu with all his properties from 10 july 2017 года, only by utm_source is AdWords, and campaign name constain "Brand".*
```
MixPanel.RawData <- MP.getRawData(api_secret = "hgf7fi437nhdsad7863y98ryn988h8",
                                  event = "emu",
                                  where = 'properties["utm_source"]=="AdWords" and "Brand" in properties["utm_campaign"]',
                                  from_date = "2017-07-10",
                                  to_date = "2017-07-10")
```

*Get all events with all properties from 1 september 2017 till 10 september 2017.*
```
MixPanel.RawData <- MP.getRawData(api_secret = "hgf7fi437nhdsad7863y98ryn988h8",
                                  from_date = "2017-09-01",
                                  to_date = "2017-09-10")
```
## *Author: Alexey Seleznev, Head of Analytics Dept. at Netpeak*
 <p align="center">
<img src="https://lh3.googleusercontent.com/R-0jgJSxIIhpag2L6YCIhJVIcIWx6-Jt5UCTRJjWzJewo47u2QBnik5CRF2dNB79jmsN_BFRjVOAYfvCqFcn3UNS_thGbbxF-99c9lwBWWlFI7JCWE43K5Yk9HnIW8i8YpTDx3l28IuYswaI-qc9QosHT1lPCsVilTfXTyV2empF4S74daOJ6x5QHYRWumT_2MhUS0hPqUsKVtOoveqDnGf3cF_VsN-RfOAwG9uCeGOgNRgv_fhSr41rw4LBND4gf05nO8zMp4TZMrrcUjKvvx6qNgYDor5LFOHiRmfKISYRVkWYe4wLyGO1FgkgTDjg0300lcur2t3txVwZUgROLZdaxOLx4owa8Rc8B8VKwd3vHxjov_aVfNPT4xf9jSFBBEOI-mfYpa55ejKDw-rqTQ6miFRFWpp_hjrk9KbGyB-Z6iZvYL-2dZ6mzgpUfs2I0tEAGsV07yTzboJ0RNCByC2-U-ZVjWdp2_9Au3FFoUcdQUAmPYOVqOv4r3oLbkkJKLj2A5jp7vf4IAoExLIfJuqEf7XN7fFcv4geib029qJjBt28wnqSO6TKEwB2fesR3uPHvGB6_6NHD70UDH-aCRCK4UBeoajtU0Y8Ks8Vwxo0oZBwmoEu8gudTFBF6mDT7GjLoGLDeNxE-TG7OtWUdxsJk7yzXGW3hE-VxsMD9g=s351-no?w=300" data-canonical-src="https://alexeyseleznev.files.wordpress.com/2017/03/as.png?w=300" style="max-width:100%;">
</p>

### Контакты:
<nav class="jetpack-social-navigation jetpack-social-navigation-svg">
<div class="menu-%d1%81%d0%be%d1%86%d0%b8%d0%b0%d0%bb%d1%8c%d0%bd%d1%8b%d0%b5-%d1%81%d0%b5%d1%82%d0%b8-container">
<ul id="menu-%d1%81%d0%be%d1%86%d0%b8%d0%b0%d0%bb%d1%8c%d0%bd%d1%8b%d0%b5-%d1%81%d0%b5%d1%82%d0%b8" class="menu">
<li id="menu-item-13" class="menu-item menu-item-type-custom menu-item-object-custom menu-item-13"><a href="http://www.facebook.com/selesnow" target="_blank"><span class="screen-reader-text">Facebook</span></a></li>
<li id="menu-item-14" class="menu-item menu-item-type-custom menu-item-object-custom menu-item-14"><a href="https://www.linkedin.com/in/selesnow/" target="_blank"><span class="screen-reader-text">LinkedIn</span></a></li>
<li id="menu-item-15" class="menu-item menu-item-type-custom menu-item-object-custom menu-item-15"><a href="http://www.vk.com/selesnow" target="_blank"><span class="screen-reader-text">Vkontakte</span></a></li>
<li id="menu-item-16" class="menu-item menu-item-type-custom menu-item-object-custom menu-item-16"><a href="https://github.com/selesnow"><span class="screen-reader-text">GitHub</span></a></li>
<li class="menu-item menu-item-type-custom menu-item-object-custom menu-item-16"><a href="https://alexeyseleznev.wordpress.com/">Blog</a></li>
</ul>
</div>
</nav>
  
<p align="center">
<img src="https://alexeyseleznev.files.wordpress.com/2017/03/as.png?w=300" data-canonical-src="https://alexeyseleznev.files.wordpress.com/2017/03/as.png?w=300" style="max-width:100%;">
</p>

