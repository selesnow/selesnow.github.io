"""Product landing. Uses the site's shared header/footer, CSS and language switcher.

Content principle: first screen answers "what is it and why", the middle answers
"is it for me", the install section gives one short default path; everything rare
(npm, source, Docker, service management) is folded into <details>.
Facts come only from the AcpGram README and code (see _build/ACPGRAM.md).
"""
import json
import re
from pathlib import Path
from build import T, esc, head, nav, footer, tail, ROOT

REPO = 'https://github.com/selesnow/acpgram'
NPM = 'https://www.npmjs.com/package/acpgram'
CHANNEL = 'https://t.me/R4marketing'
BOTFATHER = 'https://t.me/BotFather'


def text(ru, ua, en):
    return T(esc(ru), esc(ua), esc(en))


def p(ru, ua, en, cls=''):
    return f'<p class="{cls}">{text(ru, ua, en)}</p>'


def link(href, label, primary=False, icon='arrow-up-right-from-square'):
    return f'<a class="ap-button {"ap-primary" if primary else ""}" href="{href}"><i aria-hidden="true" class="fa-solid fa-{icon}"></i>{label}</a>'


def code(value):
    return f'''<div class="ap-code"><pre><code>{esc(value)}</code></pre><button type="button" class="ap-copy" aria-label="Copy command">{text('Копировать', 'Копіювати', 'Copy')}</button></div>'''


def card(title, desc, icon):
    return f'<article class="bento-glass ap-card ap-reveal"><div class="bento-content"><i aria-hidden="true" class="ap-icon fa-solid fa-{icon}"></i><h3>{text(*title)}</h3>{p(*desc)}</div></article>'


def section(id, title, content, intro=None):
    return f'''<section id="{id}" class="ap-section"><div class="ap-section-heading ap-reveal"><h2>{text(*title)}</h2>{p(*intro, cls='ap-lead') if intro else ''}</div>{content}</section>'''


def h5(value):
    return f'<h5>{value}</h5>'


def tabs(group, label, items):
    """Accessible tab set. Without JS the tab row is hidden and every panel is shown with its own title."""
    buttons = ''.join(
        f'<button type="button" role="tab" id="tab-{group}-{id}" aria-controls="panel-{group}-{id}" aria-selected="{str(i == 0).lower()}" tabindex="{0 if i == 0 else -1}">{name}</button>'
        for i, (id, name, _) in enumerate(items))
    panels = ''.join(
        f'<div class="ap-service-panel" role="tabpanel" id="panel-{group}-{id}" aria-labelledby="tab-{group}-{id}"><h4 class="ap-panel-title">{name}</h4>{body}</div>'
        for id, name, body in items)
    return f'<div class="ap-tabset" data-label="{esc(label)}"><div class="ap-tabs" role="tablist" aria-label="{esc(label)}">{buttons}</div>{panels}</div>'


def more(summary, body):
    return f'<details class="ap-more"><summary>{summary}<span aria-hidden="true">+</span></summary><div class="ap-more-body">{body}</div></details>'


# ---------- Install: step 1, per agent ----------

def agent_panels():
    node = p('Для npm-команд нужен Node.js 24 с npm.', 'Для npm-команд потрібен Node.js 24 з npm.', 'npm commands need Node.js 24 with npm.', 'ap-small') + '<a class="ap-text-link" href="https://nodejs.org/en/download">Node.js ↗</a>'

    claude = p('Уже работаете в Claude Code? Тогда достаточно поставить мост, через который AcpGram с ним общается:',
               'Уже працюєте в Claude Code? Тоді достатньо встановити міст, через який AcpGram із ним спілкується:',
               'Already using Claude Code? Then you only need the bridge AcpGram uses to talk to it:')
    claude += code('npm install -g @agentclientprotocol/claude-agent-acp')
    claude += more(text('Claude Code ещё не установлен', 'Claude Code ще не встановлено', 'Claude Code is not installed yet'),
                   code('npm install -g @anthropic-ai/claude-code@latest')
                   + p('Затем запустите claude и войдите в аккаунт. Вместо входа можно указать ключ ANTHROPIC_API_KEY в мастере AcpGram. На Windows пригодится Git for Windows.',
                       'Потім запустіть claude і увійдіть в акаунт. Замість входу можна вказати ключ ANTHROPIC_API_KEY у майстрі AcpGram. На Windows знадобиться Git for Windows.',
                       'Then run claude and sign in. Instead of signing in you can enter an ANTHROPIC_API_KEY in the AcpGram wizard. On Windows, install Git for Windows.')
                   + code('claude') + node
                   + '<a class="ap-text-link" href="https://code.claude.com/docs/en/setup">' + text('Документация Claude Code', 'Документація Claude Code', 'Claude Code docs') + ' ↗</a>')

    codex = p('Уже работаете в Codex CLI? Поставьте мост, через который AcpGram с ним общается:',
              'Уже працюєте в Codex CLI? Встановіть міст, через який AcpGram із ним спілкується:',
              'Already using Codex CLI? Install the bridge AcpGram uses to talk to it:')
    codex += code('npm install -g @agentclientprotocol/codex-acp')
    codex += more(text('Codex CLI ещё не установлен', 'Codex CLI ще не встановлено', 'Codex CLI is not installed yet'),
                  code('npm install -g @openai/codex') + code('codex login')
                  + p('Вместо входа можно указать ключ OPENAI_API_KEY в мастере AcpGram. На Windows режимам read-only и workspace-write нужен работающий sandbox Codex.',
                      'Замість входу можна вказати ключ OPENAI_API_KEY у майстрі AcpGram. На Windows режимам read-only і workspace-write потрібен робочий sandbox Codex.',
                      'Instead of signing in you can enter an OPENAI_API_KEY in the AcpGram wizard. On Windows, read-only and workspace-write modes need a working Codex sandbox.')
                  + node + '<a class="ap-text-link" href="https://github.com/openai/codex#quickstart">' + text('Документация Codex CLI', 'Документація Codex CLI', 'Codex CLI docs') + ' ↗</a>')

    gemini = p('Уже работаете в Gemini CLI? Ничего ставить не нужно: AcpGram подключается к нему напрямую. Переходите к шагу 2.',
               'Уже працюєте в Gemini CLI? Нічого встановлювати не потрібно: AcpGram підключається до нього напряму. Переходьте до кроку 2.',
               'Already using Gemini CLI? Nothing to install: AcpGram connects to it directly. Go to step 2.')
    gemini += more(text('Gemini CLI ещё не установлен', 'Gemini CLI ще не встановлено', 'Gemini CLI is not installed yet'),
                   code('npm install -g @google/gemini-cli')
                   + p('Затем запустите gemini и авторизуйтесь или укажите ключ GEMINI_API_KEY в мастере AcpGram.',
                       'Потім запустіть gemini й авторизуйтеся або вкажіть ключ GEMINI_API_KEY у майстрі AcpGram.',
                       'Then run gemini and sign in, or enter a GEMINI_API_KEY in the AcpGram wizard.')
                   + code('gemini') + node
                   + '<a class="ap-text-link" href="https://github.com/google-gemini/gemini-cli#readme">' + text('Документация Gemini CLI', 'Документація Gemini CLI', 'Gemini CLI docs') + ' ↗</a>')

    agy = p('Нужна версия 1.5 или новее. Мост не нужен — достаточно один раз войти через Google:',
            'Потрібна версія 1.5 або новіша. Міст не потрібен — достатньо один раз увійти через Google:',
            'Version 1.5 or newer is required. No bridge needed — just sign in with Google once:')
    agy += code('agy acp --login')
    agy += more(text('Antigravity CLI ещё не установлен', 'Antigravity CLI ще не встановлено', 'Antigravity CLI is not installed yet'),
                h5('Windows (PowerShell)') + code('irm https://antigravity.google/cli/install.ps1 | iex')
                + h5('Linux / macOS') + code('curl -fsSL https://antigravity.google/cli/install.sh | bash')
                + p('Откройте новый терминал и проверьте версию:', 'Відкрийте новий термінал і перевірте версію:', 'Open a new terminal and check the version:')
                + code('agy --version')
                + '<a class="ap-text-link" href="https://antigravity.google/docs/getting-started?tab=cli">' + text('Документация Antigravity CLI', 'Документація Antigravity CLI', 'Antigravity CLI docs') + ' ↗</a>')

    return tabs('agent', 'Agent', [('claude', 'Claude Code', claude), ('codex', 'Codex', codex),
                                   ('gemini', 'Gemini CLI', gemini), ('agy', 'Antigravity CLI', agy)])


def os_panels():
    note = p('Установщик скачает AcpGram, при необходимости сам поставит Node.js 24 (без прав администратора) и сразу запустит мастер настройки.',
             'Інсталятор завантажить AcpGram, за потреби сам встановить Node.js 24 (без прав адміністратора) і одразу запустить майстер налаштування.',
             'The installer downloads AcpGram, installs Node.js 24 if needed (no admin rights) and launches the setup wizard right away.', 'ap-small')
    return tabs('os', 'OS', [
        ('win', 'Windows', p('Выполните в PowerShell:', 'Виконайте в PowerShell:', 'Run in PowerShell:') + code('irm https://raw.githubusercontent.com/selesnow/acpgram/main/install.ps1 | iex') + note),
        ('unix', 'Linux / macOS', p('Выполните в терминале:', 'Виконайте в терміналі:', 'Run in a terminal:') + code('curl -fsSL https://raw.githubusercontent.com/selesnow/acpgram/main/install.sh | bash') + note),
    ])


def install_content():
    steps = [
        (('Подготовьте своего агента', 'Підготуйте свого агента', 'Prepare your agent'),
         p('Выберите агента, которым пользуетесь. Достаточно одного, остальные можно добавить позже.',
           'Виберіть агента, яким користуєтеся. Достатньо одного, інших можна додати пізніше.',
           'Pick the agent you use. One is enough; you can add others later.') + agent_panels()),
        (('Создайте Telegram-бота', 'Створіть Telegram-бота', 'Create a Telegram bot'),
         p('Откройте @BotFather, отправьте /newbot, придумайте имя — и скопируйте токен, который он пришлёт. Это займёт минуту.',
           'Відкрийте @BotFather, надішліть /newbot, придумайте ім’я — і скопіюйте токен, який він надішле. Це займе хвилину.',
           'Open @BotFather, send /newbot, pick a name and copy the token it sends you. Takes a minute.')
         + f'<a class="ap-text-link" href="{BOTFATHER}">{text("Открыть @BotFather", "Відкрити @BotFather", "Open @BotFather")} ↗</a>'),
        (('Установите AcpGram одной командой', 'Встановіть AcpGram однією командою', 'Install AcpGram with one command'),
         os_panels()),
        (('Ответьте на вопросы мастера', 'Дайте відповідь на запитання майстра', 'Answer the wizard'),
         '<ul class="ap-checklist">'
         + ''.join(f'<li>{text(*item)}</li>' for item in [
             ('вставьте токен бота;', 'вставте токен бота;', 'paste the bot token;'),
             ('напишите своему боту любое сообщение — мастер запомнит вас как администратора;', 'напишіть своєму боту будь-яке повідомлення — майстер запам’ятає вас як адміністратора;', 'send your bot any message — the wizard registers you as the admin;'),
             ('выберите агента по умолчанию и, если нужно, укажите API-ключ;', 'виберіть агента за замовчуванням і, якщо потрібно, вкажіть API-ключ;', 'choose the default agent and enter an API key if you need one;'),
             ('согласитесь установить сервис — бот будет запускаться вместе с системой.', 'погодьтеся встановити сервіс — бот запускатиметься разом із системою.', 'accept the service install — the bot will start with your system.'),
         ]) + '</ul>'),
        (('Напишите боту задачу', 'Напишіть боту завдання', 'Send your bot a task'),
         p('В Telegram: /start → выберите папку проекта через /project → напишите, что сделать. Готово.',
           'У Telegram: /start → виберіть папку проєкту через /project → напишіть, що зробити. Готово.',
           'In Telegram: /start → pick the project folder with /project → write what to do. Done.')
         + '<div class="ap-command-tags"><code>/start</code><code>/project</code><code>/engine</code><code>/model</code><code>/new</code><code>/stop</code></div>'),
    ]
    content = '<ol class="ap-start-steps">' + ''.join(
        f'<li class="bento-glass ap-reveal"><span class="ap-start-number">{i+1}</span><div class="bento-content"><h3>{text(*title)}</h3>{body}</div></li>'
        for i, (title, body) in enumerate(steps)) + '</ol>'

    # Everything below is optional and folded.
    npm = (p('Нужен Node.js 22.13+ с npm. После установки запустите мастер.', 'Потрібен Node.js 22.13+ з npm. Після встановлення запустіть майстер.', 'Requires Node.js 22.13+ with npm. Run the wizard after installing.')
           + code('npm install -g acpgram') + code('acpgram setup')
           + p('Настройки и база хранятся в ~/.acpgram (или ACPGRAM_HOME) и не теряются при обновлении.', 'Налаштування й база зберігаються в ~/.acpgram (або ACPGRAM_HOME) і не губляться під час оновлення.', 'Settings and the database live in ~/.acpgram (or ACPGRAM_HOME) and survive updates.', 'ap-small'))
    source = (p('Нужны Git и Node.js 24+. Зависимости npm самому AcpGram не нужны.', 'Потрібні Git і Node.js 24+. Залежності npm самому AcpGram не потрібні.', 'Requires Git and Node.js 24+. AcpGram itself has no npm dependencies.')
              + code('git clone https://github.com/selesnow/acpgram.git\ncd acpgram\nnpm run setup')
              + p('Если отказались от сервиса, бот запускается командой:', 'Якщо відмовилися від сервісу, бот запускається командою:', 'If you skipped the service, start the bot with:') + code('npm start'))
    docker = (p('Нужны Git и Docker с Docker Compose. Все четыре агента и мосты уже внутри образа — на хост ничего ставить не нужно, мастер тоже не нужен.',
                'Потрібні Git і Docker із Docker Compose. Усі чотири агенти й мости вже всередині образу — на хост нічого встановлювати не потрібно, майстер теж не потрібен.',
                'Requires Git and Docker with Docker Compose. All four agents and bridges ship in the image — nothing to install on the host, no wizard needed.')
              + code('git clone https://github.com/selesnow/acpgram.git\ncd acpgram\ncp .env.example .env')
              + p('Заполните в .env токен бота, свой Telegram ID, ключ агента и папку с проектами. Например, для Gemini CLI:',
                  'Заповніть у .env токен бота, свій Telegram ID, ключ агента й папку з проєктами. Наприклад, для Gemini CLI:',
                  'Fill in .env with the bot token, your Telegram ID, the agent key and the projects folder. For example, for Gemini CLI:')
              + code('TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN\nALLOWED_USER_ID=YOUR_TELEGRAM_ID\nDEFAULT_ENGINE=gemini\nGEMINI_API_KEY=YOUR_API_KEY\nPROJECTS_DIR=./projects')
              + code('docker compose up -d --build')
              + p('Для Claude Code — ANTHROPIC_API_KEY, для Codex — OPENAI_API_KEY. Antigravity CLI: после запуска один раз выполните docker compose exec -it bot agy acp --login. В контейнере агент видит только папку проектов. На Windows вместо cp используйте Copy-Item.',
                  'Для Claude Code — ANTHROPIC_API_KEY, для Codex — OPENAI_API_KEY. Antigravity CLI: після запуску один раз виконайте docker compose exec -it bot agy acp --login. У контейнері агент бачить лише папку проєктів. На Windows замість cp використовуйте Copy-Item.',
                  'Claude Code uses ANTHROPIC_API_KEY, Codex uses OPENAI_API_KEY. Antigravity CLI: after start, run docker compose exec -it bot agy acp --login once. Inside the container the agent sees only the projects folder. On Windows use Copy-Item instead of cp.', 'ap-small'))
    service = (p('Обычно сервис ставит мастер. Управлять им можно так:', 'Зазвичай сервіс встановлює майстер. Керувати ним можна так:', 'The wizard normally installs the service. To manage it:')
               + code('acpgram service install\nacpgram service status\nacpgram service restart\nacpgram service uninstall')
               + p('Windows: сервис ставится через NSSM из терминала администратора и просит пароль вашей учётной записи (для аккаунта Microsoft — его пароль, не PIN). Linux: systemd --user; чтобы бот работал без входа в систему, выполните sudo loginctl enable-linger $USER. macOS: LaunchAgent.',
                   'Windows: сервіс встановлюється через NSSM із термінала адміністратора й просить пароль вашого облікового запису (для акаунта Microsoft — його пароль, не PIN). Linux: systemd --user; щоб бот працював без входу в систему, виконайте sudo loginctl enable-linger $USER. macOS: LaunchAgent.',
                   'Windows: the service is installed via NSSM from an administrator terminal and asks for your account password (for a Microsoft account, its password, not the PIN). Linux: systemd --user; to keep it running without a login session, run sudo loginctl enable-linger $USER. macOS: LaunchAgent.', 'ap-small')
               + h5(text('Обновление', 'Оновлення', 'Updating'))
               + p('Установили одной командой — обновляйтесь так, затем перезапустите сервис:', 'Встановили однією командою — оновлюйтеся так, потім перезапустіть сервіс:', 'Installed with the one-line installer? Update like this, then restart the service:')
               + code('acpgram update\nacpgram service restart')
               + p('Установили через npm:', 'Встановили через npm:', 'Installed with npm:') + code('npm install -g acpgram@latest\nacpgram service restart')
               + p('Настройки и история сохраняются.', 'Налаштування та історія зберігаються.', 'Settings and history are kept.', 'ap-small'))

    content += '<div class="ap-more-list ap-reveal"><h3>' + text('Другие способы и подробности', 'Інші способи й подробиці', 'Other options and details') + '</h3>'
    content += more(text('Установка через npm', 'Встановлення через npm', 'Install with npm'), npm)
    content += more(text('Запуск из исходников', 'Запуск із вихідного коду', 'Run from source'), source)
    content += more('Docker', docker)
    content += more(text('Сервис, автозапуск и обновление', 'Сервіс, автозапуск і оновлення', 'Service, autostart and updates'), service)
    content += f'<a class="ap-text-link" href="{REPO}#readme">{text("Полная документация на GitHub", "Повна документація на GitHub", "Full documentation on GitHub")} ↗</a></div>'
    return content


FAQ = [
    (('AcpGram платный?', 'AcpGram платний?', 'Is AcpGram paid?'),
     ('Нет, это бесплатный проект с открытым кодом (лицензия MIT). Вы платите только за самого агента — подписку или API вашего провайдера, как и при работе в терминале.',
      'Ні, це безкоштовний проєкт із відкритим кодом (ліцензія MIT). Ви платите лише за самого агента — підписку або API вашого провайдера, як і під час роботи в терміналі.',
      'No. It is free and open source (MIT license). You only pay for the agent itself — your provider’s subscription or API — just as in the terminal.')),
    (('Нужен ли сервер, публичный IP или открытые порты?', 'Чи потрібен сервер, публічна IP-адреса або відкриті порти?', 'Do I need a server, a public IP or open ports?'),
     ('Нет. Бот сам обращается к Telegram, поэтому подойдёт обычный домашний компьютер или ноутбук с интернетом. Сервер (VPS) удобен, если агент должен быть доступен круглосуточно.',
      'Ні. Бот сам звертається до Telegram, тож підійде звичайний домашній комп’ютер або ноутбук з інтернетом. Сервер (VPS) зручний, якщо агент має бути доступний цілодобово.',
      'No. The bot connects to Telegram itself, so a regular home computer or laptop with internet access is enough. A server (VPS) is handy if you want the agent available around the clock.')),
    (('Компьютер должен быть включён?', 'Комп’ютер має бути увімкнений?', 'Does my computer need to stay on?'),
     ('Да. Агент работает на той машине, где установлен AcpGram, — пока она выключена или спит, бот не ответит. После перезагрузки сервис запустит бота сам.',
      'Так. Агент працює на тій машині, де встановлено AcpGram, — поки вона вимкнена або спить, бот не відповість. Після перезавантаження сервіс запустить бота сам.',
      'Yes. The agent runs on the machine where AcpGram is installed; while it is off or asleep, the bot will not reply. After a reboot the service starts the bot again.')),
    (('Можно пользоваться своим аккаунтом, а не API-ключом?', 'Можна користуватися своїм акаунтом, а не API-ключем?', 'Can I use my account login instead of an API key?'),
     ('Да. Claude Code, Codex и Gemini CLI работают и со входом в аккаунт, и с API-ключом — как вы уже настроили агента. Antigravity CLI использует вход через Google.',
      'Так. Claude Code, Codex і Gemini CLI працюють і з входом в акаунт, і з API-ключем — як ви вже налаштували агента. Antigravity CLI використовує вхід через Google.',
      'Yes. Claude Code, Codex and Gemini CLI work with either an account login or an API key — whichever you already use. Antigravity CLI uses Google sign-in.')),
    (('Кто ещё может писать моему боту?', 'Хто ще може писати моєму боту?', 'Who else can talk to my bot?'),
     ('Только вы. Других людей вы добавляете сами — по ссылке-приглашению или одобрив запрос — и задаёте им уровень доступа: только чтение, работа с подтверждениями или полный доступ.',
      'Лише ви. Інших людей ви додаєте самі — за посиланням-запрошенням або схваливши запит — і задаєте їм рівень доступу: лише читання, робота з підтвердженнями або повний доступ.',
      'Only you. You add other people yourself — via an invite link or by approving a request — and set their access level: read-only, work with approvals, or full access.')),
    (('Где хранятся мои данные?', 'Де зберігаються мої дані?', 'Where is my data stored?'),
     ('Настройки и история сессий — в локальной базе SQLite на вашей машине. Сообщения проходят через Telegram, а сами запросы обрабатывает провайдер выбранного агента.',
      'Налаштування й історія сесій — у локальній базі SQLite на вашій машині. Повідомлення проходять через Telegram, а самі запити обробляє провайдер вибраного агента.',
      'Settings and session history live in a local SQLite database on your machine. Messages go through Telegram, and the requests themselves are processed by your agent’s provider.')),
    (('Можно подключить несколько компьютеров?', 'Можна підключити кілька комп’ютерів?', 'Can I connect several computers?'),
     ('Да: создайте отдельного бота для каждой машины и установите AcpGram на каждой со своим токеном. У каждого бота будет свой чат с агентами этой машины.',
      'Так: створіть окремого бота для кожної машини й встановіть AcpGram на кожній зі своїм токеном. У кожного бота буде свій чат з агентами цієї машини.',
      'Yes: create a separate bot for each machine and install AcpGram on each with its own token. Each bot gets its own chat with that machine’s agents.')),
    (('На каком языке говорит бот?', 'Якою мовою говорить бот?', 'Which language does the bot speak?'),
     ('На русском, украинском или английском — по языку вашего Telegram. Сменить можно командой /language.',
      'Українською, російською або англійською — за мовою вашого Telegram. Змінити можна командою /language.',
      'English, Ukrainian or Russian — matching your Telegram language. Change it with /language.')),
    (('Чем отличается от OpenACP и telegram-acp-bot?', 'Чим відрізняється від OpenACP і telegram-acp-bot?', 'How is it different from OpenACP and telegram-acp-bot?'),
     ('AcpGram объединяет четыре агента в одном боте, поддерживает темы Telegram как отдельные диалоги, командный доступ и журнал действий, и работает на чистом Node.js без зависимостей. У каждого проекта свои сильные стороны — сравните README и выберите подходящий.',
      'AcpGram об’єднує чотири агенти в одному боті, підтримує теми Telegram як окремі діалоги, командний доступ і журнал дій, і працює на чистому Node.js без залежностей. Кожен проєкт має свої сильні сторони — порівняйте README й виберіть відповідний.',
      'AcpGram combines four agents in one bot, supports Telegram topics as separate dialogs, team access and an audit log, and runs on plain Node.js with no dependencies. Each project has its strengths — compare the READMEs and pick what suits you.')),
    (('Как сообщить об ошибке?', 'Як повідомити про помилку?', 'How do I report a bug?'),
     ('Создайте issue на GitHub: укажите ОС, версию AcpGram, агента и шаги воспроизведения. Токены и API-ключи не прикладывайте.',
      'Створіть issue на GitHub: вкажіть ОС, версію AcpGram, агента й кроки відтворення. Токени та API-ключі не додавайте.',
      'Open an issue on GitHub with your OS, AcpGram version, agent and steps to reproduce. Never attach tokens or API keys.')),
]


def build_acpgram():
    snapshot = ROOT / 'assets/acpgram-stats.json'
    stats = json.loads(snapshot.read_text(encoding='utf-8')) if snapshot.exists() else {}
    def metric(path):
        result = stats
        for key in path.split('.'):
            result = result.get(key) if isinstance(result, dict) else None
        return f'<strong data-stat="{path}">{esc(result) if result is not None else "—"}</strong>'
    desc = 'AcpGram — бесплатный open source бот: управляйте Claude Code, Codex, Gemini CLI и Antigravity CLI на своём компьютере из Telegram. Установка за пару минут.'
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'SoftwareApplication', 'name': 'AcpGram', 'description': desc,
         'applicationCategory': 'DeveloperApplication', 'operatingSystem': 'Windows, Linux, macOS',
         'url': 'https://alexey-seleznev.pro/acpgram/', 'codeRepository': REPO,
         'license': REPO + '/blob/main/LICENSE', 'downloadUrl': NPM,
         'author': {'@type': 'Person', 'name': 'Alexey Seleznev', 'url': 'https://alexey-seleznev.pro/'}},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q[0], 'acceptedAnswer': {'@type': 'Answer', 'text': a[0]}} for q, a in FAQ]}]}
    page = head('acpgram', 'AcpGram — кодинг-агенты в Telegram', desc,
                image='https://alexey-seleznev.pro/img/acpgram/og-acpgram.jpg', jsonld=ld)
    page = page.replace('    <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">\n', '').replace('    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>\n', '')
    page = page.replace('content="summary"', 'content="summary_large_image"').replace('content="Алексей Селезнёв"', 'content="AcpGram — AI coding agents in Telegram"')
    page = page.replace('    <!-- Tailwind', '    <link rel="stylesheet" href="/acpgram/acpgram.css">\n    <!-- Tailwind')
    page = page.replace('</head>', '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">\n</head>')
    page = page.replace('class="relative lang-en"', 'class="relative lang-en acpgram-page"')
    # Load analytics after interaction or a short grace period to prioritize page rendering.
    page = page.replace('<script async src="https://www.googletagmanager.com/gtag/js?id=G-Z56YHE916N"></script>', '''<script>
    (() => {
      let loaded = false;
      const events = ['pointerdown', 'keydown', 'scroll'];
      function loadAnalytics() {
        if (loaded) return;
        loaded = true;
        const script = document.createElement('script');
        script.async = true;
        script.src = 'https://www.googletagmanager.com/gtag/js?id=G-Z56YHE916N';
        document.head.append(script);
        events.forEach(event => window.removeEventListener(event, loadAnalytics));
      }
      events.forEach(event => window.addEventListener(event, loadAnalytics, {once:true, passive:true}));
      setTimeout(loadAnalytics, 10000);
    })();
    </script>''')
    page += nav('acpgram')
    page += '<main id="main-content" class="ap-main">'
    logo = '<picture><source srcset="/img/acpgram/acpgram-logo.webp" type="image/webp"><img class="ap-logo" src="/img/acpgram/acpgram-logo-light.svg" alt="AcpGram" width="353" height="285" fetchpriority="high"></picture>'
    page += f'''<section id="hero" class="ap-hero ap-section"><div><div class="ap-brand">{logo}<span>AcpGram<span class="ap-eyebrow">OPEN SOURCE · MIT</span></span></div>
    <h1>{text('Ваш кодинг-агент — в Telegram', 'Ваш кодинг-агент — у Telegram', 'Your coding agent, in Telegram')}</h1>
    {p('Поставьте задачу Claude Code, Codex, Gemini CLI или Antigravity CLI с телефона и занимайтесь своими делами. Агент работает на вашем компьютере, а ход работы, запросы на подтверждение и готовый результат приходят в чат.', 'Поставте завдання Claude Code, Codex, Gemini CLI або Antigravity CLI з телефона й займайтеся своїми справами. Агент працює на вашому комп’ютері, а хід роботи, запити на підтвердження й готовий результат надходять у чат.', 'Give a task to Claude Code, Codex, Gemini CLI or Antigravity CLI from your phone and get on with your day. The agent runs on your computer; its progress, approval requests and the finished result arrive in the chat.', 'ap-lead')}
    <div class="ap-actions ap-hero-actions">{link('#install', text('Установить', 'Встановити', 'Install'), True, 'download')}{link('#video', text('Видео: 3 минуты', 'Відео: 3 хвилини', 'Video: 3 minutes'), icon='play')}</div>
    <ul class="ap-trust">{''.join(f'<li><i aria-hidden="true" class="fa-solid fa-check"></i>{text(*t)}</li>' for t in [
        ('Бесплатно и с открытым кодом', 'Безкоштовно й з відкритим кодом', 'Free and open source'),
        ('Windows, Linux, macOS', 'Windows, Linux, macOS', 'Windows, Linux, macOS'),
        ('Без публичного IP и открытых портов', 'Без публічної IP та відкритих портів', 'No public IP or open ports'),
        ('Код и данные остаются у вас', 'Код і дані залишаються у вас', 'Your code and data stay with you')])}</ul>
    <div class="ap-badges"><a href="{REPO}">★ GitHub {metric('github.stars')}</a><a href="{NPM}">npm v{metric('npm.version')}</a></div></div>
    <div class="ap-visual"><figure class="hero-photo"><div class="hero-photo-plate"></div><div class="hero-photo-frame"><picture><source srcset="/img/acpgram/acpgram-hero.webp" type="image/webp"><img src="/img/acpgram/acpgram-hero.jpg" alt="AcpGram: coding agents in Telegram" data-alt-ru="AcpGram: кодинг-агенты в Telegram" data-alt-ua="AcpGram: кодинг-агенти в Telegram" data-alt-en="AcpGram: coding agents in Telegram" width="1024" height="577" fetchpriority="high"></picture><div class="hero-photo-tint"></div></div></figure>
    </div></section>'''

    scenarios = [
        (('Запустили и ушли', 'Запустили й пішли', 'Start it and walk away'),
         ('Долгий рефакторинг, тесты или разбор данных идут без вас. Когда агент закончит, результат придёт в Telegram.', 'Довгий рефакторинг, тести чи аналіз даних ідуть без вас. Коли агент закінчить, результат прийде в Telegram.', 'A long refactor, test run or data analysis carries on without you. When the agent finishes, the result lands in Telegram.'), 'person-walking'),
        (('Подтверждение одной кнопкой', 'Підтвердження однією кнопкою', 'Approve with one tap'),
         ('Агенту нужно разрешение на команду? Он спросит в чате, вы нажмёте «Разрешить» — и работа не простаивает, пока вас нет за столом.', 'Агенту потрібен дозвіл на команду? Він запитає в чаті, ви натиснете «Дозволити» — і робота не простоює, поки вас немає за столом.', 'Agent needs permission to run a command? It asks in the chat, you tap “Allow”, and work doesn’t stall while you’re away from your desk.'), 'hand-pointer'),
        (('Задача пришла в голову в дороге', 'Завдання спало на думку в дорозі', 'An idea on the go'),
         ('Напишите боту из метро или кафе. Агент начнёт работать в нужном проекте на вашем компьютере или сервере.', 'Напишіть боту з метро чи кафе. Агент почне працювати в потрібному проєкті на вашому комп’ютері чи сервері.', 'Message the bot from the subway or a café. The agent starts working in the right project on your computer or server.'), 'mobile-screen'),
    ]
    page += section('why', ('Когда это нужно', 'Коли це потрібно', 'When you need it'),
                    '<div class="ap-grid ap-three">' + ''.join(card(*c) for c in scenarios) + '</div>',
                    ('Кодинг-агенты работают в терминале и ждут вас у монитора. AcpGram переносит общение с ними в Telegram.', 'Кодинг-агенти працюють у терміналі й чекають на вас біля монітора. AcpGram переносить спілкування з ними в Telegram.', 'Coding agents live in a terminal and wait for you at your desk. AcpGram moves the conversation to Telegram.'))

    steps = [
        (('Пишете задачу', 'Пишете завдання', 'Write a task'), ('Обычным сообщением, как коллеге.', 'Звичайним повідомленням, як колезі.', 'As a plain message, like to a colleague.')),
        (('Подтверждаете действие', 'Підтверджуєте дію', 'Approve an action'), ('Агент спрашивает разрешение — вы нажимаете кнопку.', 'Агент просить дозвіл — ви натискаєте кнопку.', 'The agent asks for permission — you tap a button.')),
        (('Следите за ходом работы', 'Стежите за ходом роботи', 'Watch the progress'), ('Каждый шаг агента появляется в чате.', 'Кожен крок агента з’являється в чаті.', 'Every agent step shows up in the chat.')),
        (('Получаете результат', 'Отримуєте результат', 'Get the result'), ('Ответ и готовые файлы — прямо в Telegram.', 'Відповідь і готові файли — просто в Telegram.', 'The answer and finished files, right in Telegram.')),
    ]
    demo = '<div class="ap-demo"><div class="ap-demo-phone ap-reveal"><video class="ap-demo-video" muted loop playsinline preload="none" poster="/img/acpgram/acpgram-demo-poster.webp" width="432" height="936" aria-label="AcpGram demo"><source src="/img/acpgram/acpgram-demo.webm" type="video/webm"><source src="/img/acpgram/acpgram-demo.mp4" type="video/mp4"></video></div>'
    demo += '<ol class="ap-demo-steps">' + ''.join(f'<li class="ap-reveal"><span class="ap-start-number">{i+1}</span><div><h3>{text(*t)}</h3>{p(*d)}</div></li>' for i, (t, d) in enumerate(steps)) + '</ol></div>'
    demo += f'<p class="ap-demo-cta ap-reveal">{text("Хотите увидеть всё целиком — от установки до первой задачи?", "Хочете побачити все повністю — від встановлення до першого завдання?", "Want to see the whole thing — from install to the first task?")} <a class="ap-text-link" href="#video">{text("Смотрите видео на 3 минуты ↓", "Дивіться відео на 3 хвилини ↓", "Watch the 3-minute video ↓")}</a></p>'
    page += section('demo', ('Как это выглядит в Telegram', 'Як це виглядає в Telegram', 'What it looks like in Telegram'), demo)

    video = f'''<div class="ap-video-layout"><div class="ap-video-copy"><span class="ap-pill">3 {text('минуты', 'хвилини', 'minutes')}</span><h3>{text('Что это, как поставить и как пользоваться', 'Що це, як встановити й як користуватися', 'What it is, how to install it and how to use it')}</h3>{p('Короткое видео, в котором весь путь показан целиком: от установки и настройки до первой задачи агенту из Telegram.', 'Коротке відео, у якому весь шлях показано повністю: від встановлення й налаштування до першого завдання агенту з Telegram.', 'A short video showing the whole journey: from installation and setup to the first task you send an agent from Telegram.')}<ol class="ap-video-points"><li>{text('Зачем нужен AcpGram', 'Навіщо потрібен AcpGram', 'Why AcpGram')}</li><li>{text('Установка и настройка', 'Встановлення й налаштування', 'Installation and setup')}</li><li>{text('Работа с агентом в Telegram', 'Робота з агентом у Telegram', 'Working with an agent in Telegram')}</li></ol></div><div class="ap-video-column"><div class="ap-video" id="ap-video"><button class="ap-video-facade" type="button" aria-label="Play AcpGram video"><img src="/img/acpgram/video-poster.webp" width="480" height="854" loading="lazy" alt="AcpGram video preview" data-alt-ru="Превью видео об AcpGram" data-alt-ua="Прев’ю відео про AcpGram" data-alt-en="AcpGram video preview"><span class="ap-play"><i class="fa-solid fa-play" aria-hidden="true"></i></span></button><noscript><iframe src="https://www.youtube-nocookie.com/embed/3CIc8QJZpkk" title="AcpGram: installation and demo" loading="lazy" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe></noscript></div><a class="ap-video-link" href="https://youtube.com/shorts/3CIc8QJZpkk">{text('Смотреть на YouTube', 'Дивитися на YouTube', 'Watch on YouTube')} ↗</a></div></div>'''
    page += section('video', ('Посмотрите, как это работает', 'Подивіться, як це працює', 'See it in action'), video)

    nodes = [
        ('Telegram', ('Вы пишете задачу боту с телефона или компьютера', 'Ви пишете завдання боту з телефона чи комп’ютера', 'You message the bot from your phone or computer')),
        ('AcpGram', ('Бот, запущенный на вашем компьютере или сервере', 'Бот, запущений на вашому комп’ютері чи сервері', 'A bot running on your computer or server')),
        (text('Ваш агент', 'Ваш агент', 'Your agent'), ('Claude Code, Codex, Gemini CLI или Antigravity CLI работает в папке проекта', 'Claude Code, Codex, Gemini CLI або Antigravity CLI працює в папці проєкту', 'Claude Code, Codex, Gemini CLI or Antigravity CLI works in the project folder')),
    ]
    flow = '<ol class="ap-flow ap-flow-3 ap-reveal">' + ''.join(f'<li><span class="ap-step-num">{i+1}</span><strong>{name}</strong><span class="ap-flow-desc">{text(*desc)}</span></li>' for i, (name, desc) in enumerate(nodes)) + '</ol>'
    flow += p('AcpGram сам подключается к Telegram, поэтому не нужны ни публичный IP, ни открытые порты, ни облачный посредник. С агентом он общается по открытому протоколу Agent Client Protocol (ACP).',
              'AcpGram сам підключається до Telegram, тому не потрібні ні публічна IP, ні відкриті порти, ні хмарний посередник. З агентом він спілкується за відкритим протоколом Agent Client Protocol (ACP).',
              'AcpGram connects to Telegram on its own, so you need no public IP, no open ports and no cloud middleman. It talks to the agent over the open Agent Client Protocol (ACP).', 'ap-lead')
    page += section('how-it-works', ('Как это устроено', 'Як це влаштовано', 'How it works'), flow)

    features = [
        (('Видно, что делает агент', 'Видно, що робить агент', 'See what the agent is doing'), ('Шаги агента — чтение файлов, команды, правки — появляются в чате в реальном времени. В конце — ответ и журнал всех действий.', 'Кроки агента — читання файлів, команди, правки — з’являються в чаті в реальному часі. Наприкінці — відповідь і журнал усіх дій.', 'Agent steps — reading files, running commands, editing — appear in the chat live. At the end: the answer plus a log of every action.'), 'wave-square'),
        (('Ничего важного без вашего «да»', 'Нічого важливого без вашого «так»', 'Nothing important without your “yes”'), ('Запросы приходят кнопками «Разрешить», «Разрешить на сессию», «Отклонить». Любую задачу можно остановить командой /stop.', 'Запити надходять кнопками «Дозволити», «Дозволити на сесію», «Відхилити». Будь-яке завдання можна зупинити командою /stop.', 'Requests arrive as “Allow”, “Allow for session” and “Reject” buttons. Stop any task with /stop.'), 'shield-halved'),
        (('Несколько задач параллельно', 'Кілька завдань паралельно', 'Several tasks in parallel'), ('Включите темы — и каждая тема чата станет отдельным диалогом со своим проектом, агентом и историей.', 'Увімкніть теми — і кожна тема чату стане окремим діалогом зі своїм проєктом, агентом та історією.', 'Turn on topics and every chat topic becomes its own dialog with its own project, agent and history.'), 'layer-group'),
        (('Любой агент и модель', 'Будь-який агент і модель', 'Any agent, any model'), ('Переключайте агента и модель прямо в чате. Прошлые сессии продолжаются с того же места, даже после перезапуска.', 'Перемикайте агента й модель просто в чаті. Попередні сесії продовжуються з того ж місця, навіть після перезапуску.', 'Switch agent and model right in the chat. Past sessions resume where they left off, even after a restart.'), 'shuffle'),
        (('Файлы туда и обратно', 'Файли туди й назад', 'Files both ways'), ('Отправьте агенту скриншот ошибки, PDF, таблицу или архив. Готовые файлы он пришлёт вам в чат.', 'Надішліть агенту скриншот помилки, PDF, таблицю чи архів. Готові файли він надішле вам у чат.', 'Send the agent a screenshot of an error, a PDF, a spreadsheet or an archive. It sends finished files back to the chat.'), 'paperclip'),
        (('Доступ для команды', 'Доступ для команди', 'Team access'), ('Пригласите коллег, задайте каждому права, доступных агентов и модели. Все действия записываются в локальный журнал.', 'Запросіть колег, задайте кожному права, доступних агентів і моделі. Усі дії записуються в локальний журнал.', 'Invite teammates and set each one’s rights, agents and models. Every action is recorded in a local audit log.'), 'users'),
    ]
    page += section('features', ('Что умеет', 'Що вміє', 'What it does'), '<div class="ap-grid ap-three">' + ''.join(card(*c) for c in features) + '</div>')

    engines = [
        ('Claude Code', ('Claude Code + мост claude-agent-acp', 'Claude Code + міст claude-agent-acp', 'Claude Code + claude-agent-acp bridge'), ('Вход в аккаунт или API-ключ', 'Вхід в акаунт або API-ключ', 'Account login or API key')),
        ('OpenAI Codex', ('Codex CLI + мост codex-acp', 'Codex CLI + міст codex-acp', 'Codex CLI + codex-acp bridge'), ('Вход в аккаунт или API-ключ', 'Вхід в акаунт або API-ключ', 'Account login or API key')),
        ('Gemini CLI', ('Только Gemini CLI', 'Лише Gemini CLI', 'Just Gemini CLI'), ('Вход в аккаунт или API-ключ', 'Вхід в акаунт або API-ключ', 'Account login or API key')),
        ('Antigravity CLI', ('Только Antigravity CLI 1.5+', 'Лише Antigravity CLI 1.5+', 'Just Antigravity CLI 1.5+'), ('Вход через Google', 'Вхід через Google', 'Google sign-in')),
    ]
    content = '<div class="ap-grid ap-four">' + ''.join(f'<article class="bento-glass ap-card ap-reveal"><div class="bento-content"><h3>{name}</h3><p><span class="ap-small">{text("Нужно:", "Потрібно:", "Needs:")}</span><br>{text(*need)}</p><p class="ap-small">{text(*auth)}</p></div></article>' for name, need, auth in engines) + '</div>'
    content += p('Достаточно одного агента. Остальные можно подключить позже — AcpGram сам найдёт установленные.', 'Достатньо одного агента. Інших можна підключити пізніше — AcpGram сам знайде встановлені.', 'One agent is enough. Add others later — AcpGram finds installed ones on its own.', 'ap-small')
    page += section('agents', ('Поддерживаемые агенты', 'Підтримувані агенти', 'Supported agents'), content)

    page += section('install', ('Установка за пять шагов', 'Встановлення за п’ять кроків', 'Install in five steps'), install_content(),
                    ('Обычно это занимает несколько минут. Если агент у вас уже работает, понадобятся две-три команды.', 'Зазвичай це займає кілька хвилин. Якщо агент у вас уже працює, знадобляться дві-три команди.', 'Usually takes a few minutes. If your agent already works, you need just two or three commands.'))

    security = '<div class="ap-grid ap-three">' + ''.join(card(*c) for c in [
        (('Бот отвечает только вам', 'Бот відповідає лише вам', 'The bot answers only you'), ('Других пользователей добавляете вы сами и задаёте им уровень доступа: только чтение, работа с подтверждениями или полный доступ.', 'Інших користувачів додаєте ви самі й задаєте їм рівень доступу: лише читання, робота з підтвердженнями або повний доступ.', 'You add other users yourself and set their access level: read-only, work with approvals, or full access.'), 'user-lock'),
        (('Данные на вашей машине', 'Дані на вашій машині', 'Data on your machine'), ('Код, настройки и история сессий остаются на компьютере с ботом. Сторонних серверов AcpGram нет.', 'Код, налаштування й історія сесій залишаються на комп’ютері з ботом. Сторонніх серверів AcpGram немає.', 'Code, settings and session history stay on the bot’s machine. AcpGram has no servers of its own.'), 'hard-drive'),
        (('Открытый код', 'Відкритий код', 'Open source'), ('Лицензия MIT: можно проверить, как устроены доступ и хранение данных, и доработать под себя.', 'Ліцензія MIT: можна перевірити, як влаштовані доступ і зберігання даних, і доопрацювати під себе.', 'MIT license: check how access and storage work and adapt it to your needs.'), 'code-branch'),
    ]) + '</div>'
    security += '<div class="bento-glass ap-note">' + p('Совет: агент работает с правами пользователя, под которым запущен бот, — папка проекта не изолирует остальные файлы. Запускайте бота под отдельной учётной записью и выдавайте полный доступ (без подтверждений) только тем, кому доверяете.', 'Порада: агент працює з правами користувача, під яким запущено бота, — папка проєкту не ізолює решту файлів. Запускайте бота під окремим обліковим записом і надавайте повний доступ (без підтверджень) лише тим, кому довіряєте.', 'Tip: the agent runs with the rights of the account the bot runs under — the project folder does not isolate other files. Run the bot under a dedicated account and grant full access (no approvals) only to people you trust.') + '</div>'
    page += section('security', ('Безопасность', 'Безпека', 'Security'), security)

    metrics = [('downloadsTotal', ('загрузок всего: npm + GitHub', 'завантажень загалом: npm + GitHub', 'downloads in total: npm + GitHub')),
               ('npm.last30d', ('скачиваний npm за месяц', 'завантажень npm за місяць', 'npm downloads this month')),
               ('github.releases.downloads', ('скачиваний установщика с GitHub', 'завантажень інсталятора з GitHub', 'installer downloads from GitHub')),
               ('github.stars', ('звёзд на GitHub', 'зірок на GitHub', 'GitHub stars'))]
    content = '<div class="ap-grid ap-four">' + ''.join(f'<div class="bento-glass ap-stat ap-reveal">{metric(path)}<span>{text(*label)}</span></div>' for path, label in metrics) + '</div>'
    content += '<p class="ap-stat-dates"><span id="ap-updated">' + text('Обновлено: ', 'Оновлено: ', 'Updated: ') + esc(stats.get('updated') or '—') + '</span> · ' + text('Загрузки включают обновления, CI и автоматические скачивания, поэтому это не число пользователей.', 'Завантаження включають оновлення, CI та автоматичні завантаження, тому це не кількість користувачів.', 'Downloads include updates, CI and automated fetches, so they are not a user count.') + '</p>'
    page += section('stats', ('Проект в цифрах', 'Проєкт у цифрах', 'By the numbers'), content)

    content = '<div class="ap-faq">' + ''.join(f'<details class="bento-glass"><summary>{text(*q)}<span aria-hidden="true">+</span></summary>{p(*a)}</details>' for q, a in FAQ) + f'</div><a class="ap-text-link" href="{REPO}/issues">GitHub Issues ↗</a>'
    page += section('faq', ('Частые вопросы', 'Часті запитання', 'FAQ'), content)

    press = [('AI Волна', 'https://aivolna.com/lenta/3682', ('AcpGram в AI Волне', 'AcpGram в AI Волні', 'AcpGram on AI Volna')), ('Lord GPT', 'https://lord-gpt.com/blog/claude/claude-i-drugie-koding-agenty-teper-mozno-vesti-cerez-telegram/', ('Claude и другие кодинг-агенты теперь можно вести через Telegram', 'Claude та інші кодинг-агенти тепер у Telegram', 'Claude and other coding agents, now in Telegram')), ('Хабр', 'https://habr.com/ru/articles/1107278/', ('Как работать с кодинг-агентами через Telegram', 'Як працювати з кодинг-агентами через Telegram', 'Working with coding agents via Telegram'))]
    content = '<div class="ap-grid ap-three">' + ''.join(f'<a href="{href}" class="bento-glass ap-card ap-press ap-reveal"><div class="bento-content"><span class="ap-eyebrow">{name}</span><h3>{text(*title)}</h3><span aria-hidden="true">↗</span></div></a>' for name, href, title in press) + '</div>'
    page += section('press', ('О проекте пишут', 'Про проєкт пишуть', 'In the press'), content)

    content = f'<div class="ap-author"><figure class="hero-photo"><div class="hero-photo-plate"></div><div class="hero-photo-frame"><img src="/photo.jpg" width="400" height="400" loading="lazy" alt="Alexey Seleznev" data-alt-ru="Алексей Селезнёв" data-alt-ua="Олексій Селезньов" data-alt-en="Alexey Seleznev"></div></figure><div><h3>{text("Алексей Селезнёв", "Олексій Селезньов", "Alexey Seleznev")}</h3>'
    content += p('Руководитель отдела аналитики Netpeak Group, автор open source R-пакетов и проекта R4marketing. Создаю инструменты для аналитики и автоматизации.', 'Керівник відділу аналітики Netpeak Group, автор open source R-пакетів і проєкту R4marketing. Створюю інструменти для аналітики й автоматизації.', 'Head of Analytics at Netpeak Group, author of open-source R packages and the R4marketing project. I build tools for analytics and automation.')
    content += '<div class="ap-actions">' + link(CHANNEL, 'Telegram R4marketing') + link('https://github.com/selesnow', 'GitHub') + link('/', text('Сайт автора', 'Сайт автора', 'Author’s site')) + '</div></div></div>'
    page += section('author', ('Об авторе', 'Про автора', 'About the author'), content)

    page += '<section class="ap-section bento-glass ap-final ap-reveal"><div class="bento-content"><h2>' + text('Пусть агент работает, пока вы заняты своим', 'Нехай агент працює, поки ви зайняті своїм', 'Let the agent work while you get on with your day') + '</h2>'
    page += p('Установка займёт несколько минут. Если AcpGram пригодился, поставьте проекту звезду на GitHub — это помогает его развивать.', 'Встановлення займе кілька хвилин. Якщо AcpGram став у пригоді, поставте проєкту зірку на GitHub — це допомагає його розвивати.', 'Installation takes a few minutes. If AcpGram helps you, star it on GitHub — it helps the project grow.')
    page += '<div class="ap-actions">' + link('#install', text('Установить', 'Встановити', 'Install'), True, 'download') + link(REPO, text('★ Звезда на GitHub', '★ Зірка на GitHub', '★ Star on GitHub'), icon='star') + '</div></div></section></main>'
    page += footer()
    page += '<div class="ap-toast" role="status" aria-live="polite" id="ap-status"></div>'
    page += '<script id="ap-stats-fallback" type="application/json">' + json.dumps(stats, ensure_ascii=False).replace('<', '\\u003c') + '</script>'
    # Same scripts as every other page (three.js + Vanta.js animated background + site.js), then the landing's own JS.
    page += tail().replace('    <script src="../assets/site.js"></script>', '    <script src="../assets/site.js"></script>\n    <script src="../acpgram/acpgram.js"></script>')
    # Relative assets work both on the site and when index.html is opened directly from disk.
    # The web server redirects /acpgram to /acpgram/ before resolving these paths.
    page = re.sub(r'((?:src|href|srcset)=")/(?!/)', r'\1../', page)
    out = ROOT / 'acpgram'
    out.mkdir(exist_ok=True)
    (out / 'index.html').write_text(page, encoding='utf-8')
    print('acpgram/index.html')


if __name__ == '__main__':
    build_acpgram()
