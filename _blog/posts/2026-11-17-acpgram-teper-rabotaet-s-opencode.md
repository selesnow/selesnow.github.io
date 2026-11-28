---
title: 'AcpGram теперь работает с OpenCode: можно пользоваться бесплатно и подключать практически любую модель'
date: '2026-11-17'
slug: acpgram-teper-rabotaet-s-opencode
tags:
- AcpGram
- AI
- Telegram
- OpenCode
categories:
- AI
description: AcpGram 1.20.0 поддерживает OpenCode. Можно пользоваться бесплатно, без ключа и аккаунта, и подключать практически любую модель — через OpenRouter или ключи Anthropic, OpenAI, Gemini, Groq, DeepSeek и Mistral.
wp_id: 900003
draft: false
cover: ../images/covers/900003.webp
cover_generated: true
---

Для тех, кто ещё не в курсе, что такое [AcpGram](https://alexey-seleznev.pro/acpgram/). Это мост между Telegram и кодинг-агентами. Он устанавливается одной командой в консоли на любую машину: ноутбук, сервер или VPS. После этого вы работаете из Telegram с теми агентами, которые доступны на этой машине: Claude Code, Codex, Gemini CLI, Antigravity CLI. Пишете задачу в чат, агент читает файлы, запускает команды и правит код, а вы подтверждаете его действия кнопками. Подключить можно сколько угодно машин: для каждой отдельный бот.

## Что нового: поддержка OpenCode (AcpGram 1.20.0)

1. **Бесплатно.** В [OpenCode](https://opencode.ai/) есть бесплатные модели, которым не нужны ни ключ, ни аккаунт. Поэтому AcpGram теперь можно попробовать вообще без оплаты. Если на машине нет ни одного агента, мастер настройки сам предложит установить OpenCode.
2. **Практически любая модель.** Связка OpenCode и [OpenRouter](https://openrouter.ai/) даёт сотни моделей по одному ключу, так же можно подключить и ключи Anthropic, OpenAI, Gemini, Groq, DeepSeek, Mistral. Модель выбирается и меняется прямо в Telegram.

<div class="b-note"><i class="fa-solid fa-triangle-exclamation" aria-hidden="true"></i><div>Бесплатные модели могут использовать запросы для обучения, поэтому секреты и закрытый код в них лучше не отправлять. Платные модели через OpenRouter оплачиваются по факту использования.</div></div>

## Как установить и настроить

Записал видео, где показываю весь путь от установки до первого запуска (также доступно [на Facebook](https://www.facebook.com/share/v/1JC9AFdbwz/)):

{{video: https://youtube.com/shorts/OF82gVwjEUE}}

## Ответы на вопросы из комментариев

Спасибо всем, кто прочитал [прошлый пост в Facebook](https://www.facebook.com/share/p/1D7CmNSaEm/), пост за пару дней набрал более 10000 просмотров, отдельное спасибо всем, кто писал комментарии. Часть замечаний я учёл сразу, ниже отвечу на самые частые.

<div class="b-fb"><iframe src="https://www.facebook.com/plugins/post.php?href=https%3A%2F%2Fwww.facebook.com%2Fselesnow%2Fposts%2Fpfbid02fZBeh8WmvxfTbw3Nu4RqcSzmZnn3V6u1bKqJsQzXarLZk8UmEKWgvzHGMhPKE1sal&show_text=true&width=500" width="500" height="514" style="border:none;overflow:hidden" scrolling="no" frameborder="0" allowfullscreen="true" allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share" loading="lazy" title="Публикация в Facebook"></iframe></div>

<p class="b-q">«У Claude Code и Codex уже есть удалённое управление. Вы изобрели велосипед.»</p>

Есть, и если вам хватает одного агента, пользуйтесь им. Моя формулировка в прошлом посте была неточной: дело не в том, что другого способа нет, а в удобстве. У каждого агента своё приложение, а я работаю с несколькими на разных ноутбуках и серверах. У меня удалённый режим подходил не со всеми способами авторизации, а я работаю через API-ключи. Мне удобнее один бот в Telegram на каждую машину, внутри которого я переключаю агентов, модели, проекты и сессии.

<p class="b-q">«T3 Code, OpenClaw, Hermes, NanoClaw?»</p>

T3 Code я раньше не знал. Он решает близкую задачу, но как отдельное приложение, а не через Telegram, и с более широким выбором агентов. Спасибо Ивану и Богдану, что подсказали. OpenClaw, Hermes и NanoClaw это самостоятельные агенты, а AcpGram сам агентом не является, он управляет вашими кодинг-агентами.

<p class="b-q">«Зачем очередной костыль?»</p>

Это инструмент под мой сценарий. Я никого не прошу отказываться от родных приложений: если они вам удобны, они проще.
