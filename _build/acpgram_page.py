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
DOCS = '/acpgram/docs/'   # the documentation page, built by _build/acpgram_docs.py


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

    opencode = p('Самый простой старт: OpenCode работает сразу на бесплатных моделях, без ключей и аккаунтов. Поставьте его одной командой — или просто запустите мастер AcpGram: если агентов нет, он предложит установить OpenCode сам.',
                 'Найпростіший старт: OpenCode працює одразу на безкоштовних моделях, без ключів і акаунтів. Встановіть його однією командою — або просто запустіть майстер AcpGram: якщо агентів немає, він запропонує встановити OpenCode сам.',
                 'The easiest start: OpenCode works right away on free models, with no keys or accounts. Install it with one command, or just run the AcpGram wizard: if no agent is installed, it offers to install OpenCode for you.')
    opencode += code('npm install -g opencode-ai')
    opencode += more(text('Модели других провайдеров', 'Моделі інших провайдерів', 'Models from other providers'),
                     p('Каждый ключ провайдера добавляет его модели: Anthropic, OpenAI, Gemini, OpenRouter (сотни моделей по одному ключу), Groq, DeepSeek, Mistral. Мастер AcpGram спросит ключи сам, их можно добавить и позже в .env. Бесплатные модели могут использовать запросы для обучения — не отправляйте в них секреты.',
                       'Кожен ключ провайдера додає його моделі: Anthropic, OpenAI, Gemini, OpenRouter (сотні моделей за одним ключем), Groq, DeepSeek, Mistral. Майстер AcpGram запитає ключі сам, їх можна додати й пізніше в .env. Безкоштовні моделі можуть використовувати запити для навчання — не надсилайте в них секрети.',
                       'Each provider key adds that provider’s models: Anthropic, OpenAI, Gemini, OpenRouter (hundreds of models with one key), Groq, DeepSeek, Mistral. The AcpGram wizard asks for the keys, or add them to .env later. Free models may use requests for training — keep secrets out of them.')
                     + node + '<a class="ap-text-link" href="https://opencode.ai/docs">' + text('Документация OpenCode', 'Документація OpenCode', 'OpenCode docs') + ' ↗</a>')

    return tabs('agent', 'Agent', [('claude', 'Claude Code', claude), ('codex', 'Codex', codex),
                                   ('gemini', 'Gemini CLI', gemini), ('agy', 'Antigravity CLI', agy),
                                   ('opencode', 'OpenCode', opencode)])


def os_panels():
    note = p('Установщик скачает AcpGram, при необходимости сам поставит Node.js 24 (без прав администратора) и сразу запустит мастер настройки.',
             'Інсталятор завантажить AcpGram, за потреби сам встановить Node.js 24 (без прав адміністратора) і одразу запустить майстер налаштування.',
             'The installer downloads AcpGram, installs Node.js 24 if needed (no admin rights) and launches the setup wizard right away.', 'ap-small')
    return tabs('os', 'OS', [
        ('win', 'Windows', p('Выполните в PowerShell:', 'Виконайте в PowerShell:', 'Run in PowerShell:') + code('irm https://raw.githubusercontent.com/selesnow/acpgram/main/install.ps1 | iex') + note + p('На Windows установщик также сам ставит NSSM, нужный только для службы.', 'На Windows інсталятор також сам встановлює NSSM, потрібний лише для служби.', 'On Windows, the installer also sets up NSSM, which is only needed for the service.', 'ap-small')),
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
             ('выберите агента по умолчанию и, если нужно, укажите API-ключ (агентов нет — мастер предложит поставить OpenCode);', 'виберіть агента за замовчуванням і, якщо потрібно, вкажіть API-ключ (агентів немає — майстер запропонує встановити OpenCode);', 'choose the default agent and enter an API key if you need one (no agent yet? the wizard offers to install OpenCode);'),
             ('согласитесь установить сервис — бот будет запускаться вместе с системой.', 'погодьтеся встановити сервіс — бот запускатиметься разом із системою.', 'accept the service install — the bot will start with your system.'),
         ]) + '</ul>'),
        (('Напишите боту задачу', 'Напишіть боту завдання', 'Send your bot a task'),
         p('В Telegram: /start → выберите папку проекта через /project → напишите, что сделать. Готово.',
           'У Telegram: /start → виберіть папку проєкту через /project → напишіть, що зробити. Готово.',
           'In Telegram: /start → pick the project folder with /project → write what to do. Done.')
         + '<div class="ap-command-tags"><code>/start</code><code>/project</code><code>/files</code><code>/git</code><code>/engine</code><code>/model</code><code>/new</code><code>/stop</code></div>'),
    ]
    content = '<ol class="ap-start-steps">' + ''.join(
        f'<li class="bento-glass ap-reveal"><span class="ap-start-number">{i+1}</span><div class="bento-content"><h3>{text(*title)}</h3>{body}</div></li>'
        for i, (title, body) in enumerate(steps)) + '</ol>'

    # Everything below is optional and folded.
    npm = (p('Нужен Node.js 22.13+ с npm. После установки запустите мастер.', 'Потрібен Node.js 22.13+ з npm. Після встановлення запустіть майстер.', 'Requires Node.js 22.13+ with npm. Run the wizard after installing.')
           + code('npm install -g acpgram') + code('acpgram setup')
           + p('На Windows NSSM нужен только для службы. Установщик одной командой ставит его сам, а при установке через npm его нужно поставить вручную:', 'На Windows NSSM потрібен лише для служби. Інсталятор однією командою встановлює його сам, а при встановленні через npm його потрібно встановити вручну:', 'On Windows, NSSM is only needed for the service. The one-line installer sets it up automatically, but with npm you need to install it manually:', 'ap-small')
           + code('winget install --id NSSM.NSSM -e')
           + p('Для запуска бота в консоли NSSM не нужен.', 'Для запуску бота в консолі NSSM не потрібен.', 'NSSM is not needed to run the bot in a console.', 'ap-small')
           + p('Настройки и база хранятся в ~/.acpgram (или ACPGRAM_HOME) и не теряются при обновлении.', 'Налаштування й база зберігаються в ~/.acpgram (або ACPGRAM_HOME) і не губляться під час оновлення.', 'Settings and the database live in ~/.acpgram (or ACPGRAM_HOME) and survive updates.', 'ap-small'))
    source = (p('Нужны Git и Node.js 24+. Зависимости npm самому AcpGram не нужны.', 'Потрібні Git і Node.js 24+. Залежності npm самому AcpGram не потрібні.', 'Requires Git and Node.js 24+. AcpGram itself has no npm dependencies.')
              + code('git clone https://github.com/selesnow/acpgram.git\ncd acpgram\nnpm run setup')
              + p('Если отказались от сервиса, бот запускается командой:', 'Якщо відмовилися від сервісу, бот запускається командою:', 'If you skipped the service, start the bot with:') + code('npm start'))
    docker = (p('Нужны Git и Docker с Docker Compose. Все пять агентов и мосты уже внутри образа — на хост ничего ставить не нужно, мастер тоже не нужен.',
                'Потрібні Git і Docker із Docker Compose. Усі п’ять агентів і мости вже всередині образу — на хост нічого встановлювати не потрібно, майстер теж не потрібен.',
                'Requires Git and Docker with Docker Compose. All five agents and bridges ship in the image — nothing to install on the host, no wizard needed.')
              + code('git clone https://github.com/selesnow/acpgram.git\ncd acpgram\ncp .env.example .env')
              + p('Заполните в .env токен бота, свой Telegram ID, ключ агента и папку с проектами. Например, для Gemini CLI:',
                  'Заповніть у .env токен бота, свій Telegram ID, ключ агента й папку з проєктами. Наприклад, для Gemini CLI:',
                  'Fill in .env with the bot token, your Telegram ID, the agent key and the projects folder. For example, for Gemini CLI:')
              + code('TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN\nALLOWED_USER_ID=YOUR_TELEGRAM_ID\nDEFAULT_ENGINE=gemini\nGEMINI_API_KEY=YOUR_API_KEY\nPROJECTS_DIR=./projects')
              + code('docker compose up -d --build')
              + p('Для Claude Code — ANTHROPIC_API_KEY, для Codex — OPENAI_API_KEY. OpenCode (DEFAULT_ENGINE=opencode) работает и без ключа — на бесплатных моделях, а любые ключи провайдеров добавляют их модели. Antigravity CLI: после запуска один раз выполните docker compose exec -it bot agy acp --login. В контейнере агент видит только папку проектов. На Windows вместо cp используйте Copy-Item.',
                  'Для Claude Code — ANTHROPIC_API_KEY, для Codex — OPENAI_API_KEY. OpenCode (DEFAULT_ENGINE=opencode) працює й без ключа — на безкоштовних моделях, а будь-які ключі провайдерів додають їхні моделі. Antigravity CLI: після запуску один раз виконайте docker compose exec -it bot agy acp --login. У контейнері агент бачить лише папку проєктів. На Windows замість cp використовуйте Copy-Item.',
                  'Claude Code uses ANTHROPIC_API_KEY, Codex uses OPENAI_API_KEY. OpenCode (DEFAULT_ENGINE=opencode) works without a key on free models, and any provider key adds that provider’s models. Antigravity CLI: after start, run docker compose exec -it bot agy acp --login once. Inside the container the agent sees only the projects folder. On Windows use Copy-Item instead of cp.', 'ap-small'))
    service = (p('Обычно сервис ставит мастер. Управлять им можно так:', 'Зазвичай сервіс встановлює майстер. Керувати ним можна так:', 'The wizard normally installs the service. To manage it:')
               + code('acpgram service install\nacpgram service status\nacpgram service restart\nacpgram service uninstall')
                + p('Windows: сервис ставится через NSSM из терминала администратора и просит пароль вашей учётной записи (для аккаунта Microsoft — его пароль, не PIN). Установщик одной командой ставит NSSM сам, при npm-установке выполните winget install --id NSSM.NSSM -e. Для запуска в консоли NSSM не нужен. Linux: systemd --user; чтобы бот работал без входа в систему, выполните sudo loginctl enable-linger $USER. macOS: LaunchAgent.',
                    'Windows: сервіс встановлюється через NSSM із термінала адміністратора й просить пароль вашого облікового запису (для акаунта Microsoft — його пароль, не PIN). Інсталятор однією командою встановлює NSSM сам, при встановленні через npm виконайте winget install --id NSSM.NSSM -e. Для запуску в консолі NSSM не потрібен. Linux: systemd --user; щоб бот працював без входу в систему, виконайте sudo loginctl enable-linger $USER. macOS: LaunchAgent.',
                    'Windows: the service is installed via NSSM from an administrator terminal and asks for your account password (for a Microsoft account, its password, not the PIN). The one-line installer sets up NSSM itself; with npm, run winget install --id NSSM.NSSM -e. NSSM is not needed for console runs. Linux: systemd --user; to keep it running without a login session, run sudo loginctl enable-linger $USER. macOS: LaunchAgent.', 'ap-small')
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
    content += f'<a class="ap-text-link" href="{DOCS}">{text("Подробная документация", "Докладна документація", "Full documentation")} →</a>'
    content += f'<a class="ap-text-link" href="{REPO}#readme">{text("README на GitHub", "README на GitHub", "README on GitHub")} ↗</a></div>'
    return content


# News: blog posts about AcpGram, newest first. The landing shows the first two plus a card linking to every
# post tagged AcpGram, so a new post only needs a new entry on top: (date, link, title, description), each ru / ua / en.
# The posts themselves are in Russian — the ua / en dates say so.
NEWS = [
    (('20 ноября 2026', '20 листопада 2026 · російською', 'Nov 20, 2026 · in Russian'),
     '/blog/acpgram-1-30-proekty-fayly-i-git-iz-telegram/',
     ('AcpGram 1.30: проекты, файлы и Git прямо из Telegram', 'AcpGram 1.30: проєкти, файли та Git просто з Telegram', 'AcpGram 1.30: projects, files and Git right from Telegram'),
     ('Вход в GitHub и GitLab без токена, изменения и ветки кнопками, секреты в обход модели, личные пространства и песочница агента.',
      'Вхід у GitHub і GitLab без токена, зміни й гілки кнопками, секрети в обхід моделі, особисті простори й пісочниця агента.',
      'Token-free sign-in to GitHub and GitLab, changes and branches as buttons, secrets that bypass the model, personal workspaces and an agent sandbox.')),
    (('17 ноября 2026', '17 листопада 2026 · російською', 'Nov 17, 2026 · in Russian'),
     '/blog/acpgram-teper-rabotaet-s-opencode/',
     ('AcpGram теперь работает с OpenCode', 'AcpGram тепер працює з OpenCode', 'AcpGram now works with OpenCode'),
     ('Можно пользоваться бесплатно, без ключа и аккаунта, и подключать практически любую модель.',
      'Можна користуватися безкоштовно, без ключа й акаунта, і підключати практично будь-яку модель.',
      'Use it for free, with no key or account, and connect almost any model.')),
]


FAQ = [
    (('AcpGram платный?', 'AcpGram платний?', 'Is AcpGram paid?'),
     ('Нет, это бесплатный проект с открытым кодом (лицензия MIT). Вы платите только за самого агента — подписку или API вашего провайдера, как и при работе в терминале. А с OpenCode можно начать совсем без оплаты: у него есть бесплатные модели, которым не нужен ключ (они могут использовать запросы для обучения — не отправляйте в них секреты).',
      'Ні, це безкоштовний проєкт із відкритим кодом (ліцензія MIT). Ви платите лише за самого агента — підписку або API вашого провайдера, як і під час роботи в терміналі. А з OpenCode можна почати зовсім без оплати: у нього є безкоштовні моделі, яким не потрібен ключ (вони можуть використовувати запити для навчання — не надсилайте в них секрети).',
      'No. It is free and open source (MIT license). You only pay for the agent itself — your provider’s subscription or API — just as in the terminal. With OpenCode you can start without paying at all: it has free models that need no key (they may use requests for training — keep secrets out of them).')),
    (('У Claude Code и Codex уже есть удалённое управление. Зачем AcpGram?', 'У Claude Code і Codex уже є віддалене керування. Навіщо AcpGram?', 'Claude Code and Codex already have remote control. Why AcpGram?'),
     ('Встроенные решения есть, и если вам хватает одного агента, пользуйтесь ими. AcpGram — вопрос удобства, а не единственный способ: у каждого агента свой клиент, а удалённый доступ может не работать при входе по API-ключу. Здесь все агенты (Claude Code, Codex, Gemini CLI, Antigravity CLI, OpenCode) живут в одном Telegram-боте с общим интерфейсом и командами, а внутри бота можно переключать агента, модель, проект и сессию.',
      'Вбудовані рішення є, і якщо вам вистачає одного агента, користуйтеся ними. AcpGram — питання зручності, а не єдиний спосіб: у кожного агента свій клієнт, а віддалений доступ може не працювати за входу через API-ключ. Тут усі агенти (Claude Code, Codex, Gemini CLI, Antigravity CLI, OpenCode) живуть в одному Telegram-боті зі спільним інтерфейсом і командами, а всередині бота можна перемикати агента, модель, проєкт і сесію.',
      'Built-in options exist, and if one agent is enough for you, use them. AcpGram is about convenience, not the only way: each agent has its own client, and remote access may not work when you sign in with an API key. Here all agents (Claude Code, Codex, Gemini CLI, Antigravity CLI, OpenCode) live in one Telegram bot with a shared interface and commands, and inside the bot you switch the agent, model, project and session.')),
    (('Это бот для клиентов сайта или готовый ИИ-агент?', 'Це бот для клієнтів сайту чи готовий ШІ-агент?', 'Is it a customer-facing bot or a ready-made AI agent?'),
     ('Нет. AcpGram — пульт для кодинг-агентов, которые работают на вашем компьютере или сервере: читают файлы, запускают команды и правят код в выбранном проекте. Он не отвечает клиентам и не принимает заказы, а подключает вас, как разработчика, к вашим агентам.',
      'Ні. AcpGram — пульт для кодинг-агентів, які працюють на вашому комп’ютері або сервері: читають файли, запускають команди й правлять код у вибраному проєкті. Він не відповідає клієнтам і не приймає замовлення, а підключає вас, як розробника, до ваших агентів.',
      'No. AcpGram is a remote for coding agents that run on your computer or server: they read files, run commands and edit code in the chosen project. It does not answer customers or take orders; it connects you, as a developer, to your agents.')),
    (('Нужен ли сервер, публичный IP или открытые порты?', 'Чи потрібен сервер, публічна IP-адреса або відкриті порти?', 'Do I need a server, a public IP or open ports?'),
     ('Нет. Бот сам обращается к Telegram, поэтому подойдёт обычный домашний компьютер или ноутбук с интернетом. Сервер (VPS) удобен, если агент должен быть доступен круглосуточно.',
      'Ні. Бот сам звертається до Telegram, тож підійде звичайний домашній комп’ютер або ноутбук з інтернетом. Сервер (VPS) зручний, якщо агент має бути доступний цілодобово.',
      'No. The bot connects to Telegram itself, so a regular home computer or laptop with internet access is enough. A server (VPS) is handy if you want the agent available around the clock.')),
    (('Компьютер должен быть включён?', 'Комп’ютер має бути увімкнений?', 'Does my computer need to stay on?'),
     ('Да. Агент работает на той машине, где установлен AcpGram, — пока она выключена или спит, бот не ответит. После перезагрузки сервис запустит бота сам.',
      'Так. Агент працює на тій машині, де встановлено AcpGram, — поки вона вимкнена або спить, бот не відповість. Після перезавантаження сервіс запустить бота сам.',
      'Yes. The agent runs on the machine where AcpGram is installed; while it is off or asleep, the bot will not reply. After a reboot the service starts the bot again.')),
    (('Можно пользоваться своим аккаунтом, а не API-ключом?', 'Можна користуватися своїм акаунтом, а не API-ключем?', 'Can I use my account login instead of an API key?'),
     ('Да. Claude Code, Codex и Gemini CLI работают и со входом в аккаунт, и с API-ключом — как вы уже настроили агента. Antigravity CLI работает со входом через Google или с ключом Gemini API: задайте GEMINI_API_KEY и укажите в settings.json Antigravity "modelProvider": "gemini". OpenCode берёт модели тех провайдеров, чьи ключи вы указали (или подключили командой opencode auth login), а бесплатные модели работают вообще без ключа.',
      'Так. Claude Code, Codex і Gemini CLI працюють і з входом в акаунт, і з API-ключем — як ви вже налаштували агента. Antigravity CLI працює з входом через Google або з ключем Gemini API: задайте GEMINI_API_KEY і вкажіть у settings.json Antigravity "modelProvider": "gemini". OpenCode бере моделі тих провайдерів, чиї ключі ви вказали (або підключили командою opencode auth login), а безкоштовні моделі працюють узагалі без ключа.',
      'Yes. Claude Code, Codex and Gemini CLI work with either an account login or an API key — whichever you already use. Antigravity CLI works with either Google sign-in or a Gemini API key: set GEMINI_API_KEY and put "modelProvider": "gemini" in Antigravity’s settings.json. OpenCode uses models from the providers whose keys you add (or connect with opencode auth login), and its free models need no key at all.')),
    (('Кто ещё может писать моему боту?', 'Хто ще може писати моєму боту?', 'Who else can talk to my bot?'),
     ('Только вы. Других людей вы добавляете сами — по ссылке-приглашению или одобрив запрос — и задаёте им уровень доступа: только чтение, работа с подтверждениями или полный доступ.',
      'Лише ви. Інших людей ви додаєте самі — за посиланням-запрошенням або схваливши запит — і задаєте їм рівень доступу: лише читання, робота з підтвердженнями або повний доступ.',
      'Only you. You add other people yourself — via an invite link or by approving a request — and set their access level: read-only, work with approvals, or full access.')),
    (('Увидят ли сотрудники проекты друг друга?', 'Чи побачать співробітники проєкти одне одного?', 'Will teammates see each other’s projects?'),
     ('По умолчанию у всех общий корень проектов. С настройкой USER_WORKSPACES=1 у каждого своя папка: чужие проекты не показываются и не выбираются. На Linux добавьте песочницу AGENT_SANDBOX=bwrap — тогда и сам агент сотрудника не видит ничего, кроме его папки. Без песочницы агент работает с правами учётной записи бота и по просьбе пользователя может прочитать файлы вне проекта.',
      'За замовчуванням у всіх спільний корінь проєктів. З налаштуванням USER_WORKSPACES=1 у кожного своя папка: чужі проєкти не показуються й не вибираються. На Linux додайте пісочницю AGENT_SANDBOX=bwrap — тоді й сам агент співробітника не бачить нічого, крім його папки. Без пісочниці агент працює з правами облікового запису бота й на прохання користувача може прочитати файли поза проєктом.',
      'By default everyone shares one projects root. With USER_WORKSPACES=1 each person gets a private folder: other people’s projects are neither shown nor selectable. On Linux add the AGENT_SANDBOX=bwrap sandbox, and the teammate’s agent itself sees nothing but their folder. Without the sandbox the agent runs with the bot account’s rights and can read files outside the project if a user asks it to.')),
    (('Как передать проекту пароли и ключи, не отправляя их модели?', 'Як передати проєкту паролі й ключі, не надсилаючи їх моделі?', 'How do I give a project passwords and keys without sending them to the model?'),
     ('Командой /files: бот создаст файл (например, .env) или примет загруженный и положит его прямо в папку проекта. Сообщение с содержимым сразу удаляется из чата, в запрос к модели оно не попадает. Сам файл агенту доступен — иначе приложение не смогло бы им пользоваться, — но бот напоминает агенту не открывать и не выводить такие файлы. Это указание, а не запрет: для особо чувствительных данных выбирайте модель провайдера, который не обучается на запросах.',
      'Командою /files: бот створить файл (наприклад, .env) або прийме завантажений і покладе його просто в папку проєкту. Повідомлення з вмістом одразу видаляється з чату, у запит до моделі воно не потрапляє. Сам файл агенту доступний — інакше застосунок не зміг би ним користуватися, — але бот нагадує агенту не відкривати й не виводити такі файли. Це вказівка, а не заборона: для особливо чутливих даних вибирайте модель провайдера, який не навчається на запитах.',
      'With /files: the bot creates a file (for example, .env) or takes an uploaded one and puts it straight into the project folder. The message with the contents is deleted from the chat at once and never enters a model request. The file itself stays readable by the agent — otherwise your app could not use it — but the bot reminds the agent not to open or print such files. That is an instruction, not a hard block: for highly sensitive data pick a model from a provider that does not train on requests.')),
    (('Можно ли работать с GitHub и GitLab из Telegram?', 'Чи можна працювати з GitHub і GitLab із Telegram?', 'Can I work with GitHub and GitLab from Telegram?'),
     ('Да, командой /git (на машине с ботом нужен установленный git). GitHub и GitLab.com подключаются по ссылке и короткому коду, без токена; свои серверы GitLab и GitHub Enterprise добавляет администратор, аккаунт на них подключается токеном доступа. Дальше всё кнопками: клонировать репозиторий, посмотреть изменения, переключить ветку, сохранить и отправить, опубликовать новый проект, открыть запрос на слияние. Вход на сервер хранится только у бота: агенту он по умолчанию не передаётся.',
      'Так, командою /git (на машині з ботом потрібен встановлений git). GitHub і GitLab.com підключаються за посиланням і коротким кодом, без токена; свої сервери GitLab і GitHub Enterprise додає адміністратор, акаунт на них підключається токеном доступу. Далі все кнопками: клонувати репозиторій, переглянути зміни, перемкнути гілку, зберегти й надіслати, опублікувати новий проєкт, відкрити запит на злиття. Вхід на сервер зберігається лише в бота: агенту він за замовчуванням не передається.',
      'Yes, with /git (git must be installed on the bot’s machine). GitHub and GitLab.com connect with a link and a short code, no token; your own GitLab and GitHub Enterprise servers are added by the admin, and accounts on them connect with an access token. After that it is all buttons: clone a repository, review changes, switch a branch, save and push, publish a new project, open a merge request. The sign-in is stored only by the bot: by default it is not passed to the agent.')),
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
     ('AcpGram объединяет пять агентов в одном боте, поддерживает темы Telegram как отдельные диалоги, командный доступ и журнал действий, и работает на чистом Node.js без зависимостей. У каждого проекта свои сильные стороны — сравните README и выберите подходящий.',
      'AcpGram об’єднує п’ять агентів в одному боті, підтримує теми Telegram як окремі діалоги, командний доступ і журнал дій, і працює на чистому Node.js без залежностей. Кожен проєкт має свої сильні сторони — порівняйте README й виберіть відповідний.',
      'AcpGram combines five agents in one bot, supports Telegram topics as separate dialogs, team access and an audit log, and runs on plain Node.js with no dependencies. Each project has its strengths — compare the READMEs and pick what suits you.')),
    (('Чем отличается от T3 Code, OpenClaw и Hermes?', 'Чим відрізняється від T3 Code, OpenClaw і Hermes?', 'How is it different from T3 Code, OpenClaw and Hermes?'),
     ('T3 Code решает близкую задачу — единый интерфейс к кодинг-агентам, но как отдельное приложение, а не через Telegram, и с более широким выбором агентов. OpenClaw, Hermes и NanoClaw — самостоятельные ИИ-агенты, а AcpGram не заменяет агента, а управляет вашими кодинг-агентами (Claude Code, Codex и другими) из Telegram.',
      'T3 Code розв’язує близьке завдання — єдиний інтерфейс до кодинг-агентів, але як окремий застосунок, а не через Telegram, і з ширшим вибором агентів. OpenClaw, Hermes і NanoClaw — самостійні ШІ-агенти, а AcpGram не замінює агента, а керує вашими кодинг-агентами (Claude Code, Codex та іншими) з Telegram.',
      'T3 Code solves a close problem — one interface to coding agents — but as a standalone app rather than through Telegram, and with a wider choice of agents. OpenClaw, Hermes and NanoClaw are standalone AI agents; AcpGram does not replace an agent, it controls your coding agents (Claude Code, Codex and others) from Telegram.')),
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
    desc = 'AcpGram — бесплатный open source бот: управляйте Claude Code, Codex, Gemini CLI, Antigravity CLI и OpenCode на своём компьютере из Telegram. Установка за пару минут.'
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
    {p('Поставьте задачу Claude Code, Codex, Gemini CLI, Antigravity CLI или OpenCode с телефона и занимайтесь своими делами. Агент работает на вашем компьютере, а ход работы, запросы на подтверждение и готовый результат приходят в чат.', 'Поставте завдання Claude Code, Codex, Gemini CLI, Antigravity CLI або OpenCode з телефона й займайтеся своїми справами. Агент працює на вашому комп’ютері, а хід роботи, запити на підтвердження й готовий результат надходять у чат.', 'Give a task to Claude Code, Codex, Gemini CLI, Antigravity CLI or OpenCode from your phone and get on with your day. The agent runs on your computer; its progress, approval requests and the finished result arrive in the chat.', 'ap-lead')}
    <div class="ap-actions ap-hero-actions">{link('#install', text('Установить', 'Встановити', 'Install'), True, 'download')}{link('#video', text('Видео: 3 минуты', 'Відео: 3 хвилини', 'Video: 3 minutes'), icon='play')}{link(DOCS, text('Документация', 'Документація', 'Docs'), icon='book-open')}</div>
    <ul class="ap-trust">{''.join(f'<li><i aria-hidden="true" class="fa-solid fa-check"></i>{text(*t)}</li>' for t in [
        ('Бесплатно и с открытым кодом', 'Безкоштовно й з відкритим кодом', 'Free and open source'),
        ('Windows, Linux, macOS', 'Windows, Linux, macOS', 'Windows, Linux, macOS'),
        ('Без публичного IP и открытых портов', 'Без публічної IP та відкритих портів', 'No public IP or open ports'),
        ('Код и данные остаются у вас', 'Код і дані залишаються у вас', 'Your code and data stay with you'),
        ('Можно начать бесплатно с OpenCode', 'Можна почати безкоштовно з OpenCode', 'Start free with OpenCode')])}</ul>
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
        (text('Ваш агент', 'Ваш агент', 'Your agent'), ('Claude Code, Codex, Gemini CLI, Antigravity CLI или OpenCode работает в папке проекта', 'Claude Code, Codex, Gemini CLI, Antigravity CLI або OpenCode працює в папці проєкту', 'Claude Code, Codex, Gemini CLI, Antigravity CLI or OpenCode works in the project folder')),
    ]
    flow = '<ol class="ap-flow ap-flow-3 ap-reveal">' + ''.join(f'<li><span class="ap-step-num">{i+1}</span><strong>{name}</strong><span class="ap-flow-desc">{text(*desc)}</span></li>' for i, (name, desc) in enumerate(nodes)) + '</ol>'
    flow += p('AcpGram сам подключается к Telegram, поэтому не нужны ни публичный IP, ни открытые порты, ни облачный посредник. С агентом он общается по открытому протоколу Agent Client Protocol (ACP).',
              'AcpGram сам підключається до Telegram, тому не потрібні ні публічна IP, ні відкриті порти, ні хмарний посередник. З агентом він спілкується за відкритим протоколом Agent Client Protocol (ACP).',
              'AcpGram connects to Telegram on its own, so you need no public IP, no open ports and no cloud middleman. It talks to the agent over the open Agent Client Protocol (ACP).', 'ap-lead')
    page += section('how-it-works', ('Как это устроено', 'Як це влаштовано', 'How it works'), flow)

    features = [
        (('Видно, что делает агент', 'Видно, що робить агент', 'See what the agent is doing'), ('Шаги агента — чтение файлов, команды, правки — появляются в чате в реальном времени, в конце — ответ и журнал действий. Некоторые агенты показывают и план работы. На вопрос агента можно ответить кнопкой, а сообщение, отправленное во время работы, встанет в очередь.', 'Кроки агента — читання файлів, команди, правки — з’являються в чаті в реальному часі, наприкінці — відповідь і журнал дій. Деякі агенти показують і план роботи. На запитання агента можна відповісти кнопкою, а повідомлення, надіслане під час роботи, стане в чергу.', 'Agent steps — reading files, running commands, editing — appear in the chat live, with the answer and an action log at the end. Some agents also show their plan. Answer the agent’s questions with a button; a message sent while it works is queued.'), 'wave-square'),
        (('Ничего важного без вашего «да»', 'Нічого важливого без вашого «так»', 'Nothing important without your “yes”'), ('Запросы приходят кнопками «Разрешить», «Разрешить на сессию», «Отклонить», а в запросе на правку файла виден дифф — понятно, что именно вы разрешаете. Любую задачу можно остановить командой /stop.', 'Запити надходять кнопками «Дозволити», «Дозволити на сесію», «Відхилити», а в запиті на правку файлу видно диф — зрозуміло, що саме ви дозволяєте. Будь-яке завдання можна зупинити командою /stop.', 'Requests arrive as “Allow”, “Allow for session” and “Reject” buttons, and a file-edit request shows the diff, so you know exactly what you approve. Stop any task with /stop.'), 'shield-halved'),
        (('Несколько задач параллельно', 'Кілька завдань паралельно', 'Several tasks in parallel'), ('Включите темы — и каждая тема чата станет отдельным диалогом со своим проектом, агентом и историей.', 'Увімкніть теми — і кожна тема чату стане окремим діалогом зі своїм проєктом, агентом та історією.', 'Turn on topics and every chat topic becomes its own dialog with its own project, agent and history.'), 'layer-group'),
        (('Любой агент и модель', 'Будь-який агент і модель', 'Any agent, any model'), ('Переключайте агента и модель прямо в чате: сотни моделей разложены по провайдерам, нужную найдёт /model sonnet, а последние выбранные — под рукой. Прошлые сессии продолжаются с того же места, даже после перезапуска.', 'Перемикайте агента й модель просто в чаті: сотні моделей розкладено за провайдерами, потрібну знайде /model sonnet, а останні вибрані — під рукою. Попередні сесії продовжуються з того ж місця, навіть після перезапуску.', 'Switch agent and model right in the chat: hundreds of models are grouped by provider, /model sonnet finds the one you need, and your recent picks are one tap away. Past sessions resume where they left off, even after a restart.'), 'shuffle'),
        (('Файлы туда и обратно', 'Файли туди й назад', 'Files both ways'), ('Отправьте агенту скриншот ошибки, PDF, таблицу или архив. Готовые файлы он пришлёт вам в чат.', 'Надішліть агенту скриншот помилки, PDF, таблицю чи архів. Готові файли він надішле вам у чат.', 'Send the agent a screenshot of an error, a PDF, a spreadsheet or an archive. It sends finished files back to the chat.'), 'paperclip'),
        (('Доступ для команды', 'Доступ для команди', 'Team access'), ('Пригласите коллег, задайте каждому права, доступных агентов и модели. У каждого может быть своя папка проектов, а расход по сотрудникам покажет /usage. Все действия записываются в локальный журнал.', 'Запросіть колег, задайте кожному права, доступних агентів і моделі. У кожного може бути своя папка проєктів, а витрати за співробітниками покаже /usage. Усі дії записуються в локальний журнал.', 'Invite teammates and set each one’s rights, agents and models. Each can have a private projects folder, and /usage shows spending per person. Every action is recorded in a local audit log.'), 'users'),
    ]
    page += section('features', ('Что умеет', 'Що вміє', 'What it does'), '<div class="ap-grid ap-three">' + ''.join(card(*c) for c in features) + '</div>')

    # Facts: README sections «Файлы проекта и секреты», «Git: GitHub и GitLab», «Личные пространства» (AcpGram 1.24–1.30).
    project_cards = [
        (('Новый проект — кнопкой', 'Новий проєкт — кнопкою', 'A new project in one tap'), ('В /project есть «Новый проект»: бот спросит название, создаст папку и сразу сделает её рабочей. Чтобы начать с чистого листа, заходить на компьютер не нужно.', 'У /project є «Новий проєкт»: бот запитає назву, створить папку й одразу зробить її робочою. Щоб почати з чистого аркуша, заходити на комп’ютер не потрібно.', '/project has “New project”: the bot asks for a name, creates the folder and makes it the working one. No need to touch the computer to start from scratch.'), 'folder-plus'),
        (('Секреты — мимо модели', 'Секрети — повз модель', 'Secrets that skip the model'), ('Команда /files создаёт файл или принимает загруженный и кладёт его прямо в папку проекта. Пароли и ключи для .env не попадают в запрос к модели, а сообщение с ними сразу удаляется из чата.', 'Команда /files створює файл або приймає завантажений і кладе його просто в папку проєкту. Паролі й ключі для .env не потрапляють у запит до моделі, а повідомлення з ними одразу видаляється з чату.', 'The /files command creates a file, or takes an uploaded one, and puts it straight into the project folder. Passwords and keys for .env never enter a model request, and the message carrying them is deleted from the chat at once.'), 'key'),
        (('Проект из репозитория', 'Проєкт із репозиторію', 'A project from a repository'), ('«Из Git» в /project показывает ваши репозитории на GitHub и GitLab списком с поиском. Выбранный клонируется и сразу становится рабочим проектом.', '«З Git» у /project показує ваші репозиторії на GitHub і GitLab списком із пошуком. Вибраний клонується й одразу стає робочим проєктом.', '“From Git” in /project lists your GitHub and GitLab repositories, with search. The one you pick is cloned and becomes the working project right away.'), 'cloud-arrow-down'),
    ]
    page += section('projects', ('Проект целиком — из чата', 'Проєкт повністю — із чату', 'The whole project, from the chat'),
                    '<div class="ap-grid ap-three">' + ''.join(card(*c) for c in project_cards) + '</div>',
                    ('Создать проект, положить в него ключи и отправить код на GitHub или GitLab можно, не подходя к компьютеру, на котором работает агент.', 'Створити проєкт, покласти в нього ключі й надіслати код на GitHub або GitLab можна, не підходячи до комп’ютера, на якому працює агент.', 'Create a project, drop keys into it and push the code to GitHub or GitLab without going near the computer the agent runs on.'))

    # Git: GitHub, GitLab.com and self-hosted servers. Facts: README section «Git: GitHub и GitLab» (AcpGram 1.27–1.30).
    git_cards = [
        (('Вход без токена', 'Вхід без токена', 'Sign in without a token'), ('GitHub и GitLab.com подключаются по ссылке и короткому коду: открыли страницу сервиса, ввели код, подтвердили доступ. Ничего секретного в чат не попадает. Вход по токену доступа тоже есть.', 'GitHub і GitLab.com підключаються за посиланням і коротким кодом: відкрили сторінку сервісу, ввели код, підтвердили доступ. Нічого секретного в чат не потрапляє. Вхід за токеном доступу теж є.', 'GitHub and GitLab.com connect with a link and a short code: open the service page, enter the code, confirm access. Nothing secret enters the chat. Access-token sign-in is there too.'), 'right-to-bracket'),
        (('Свои серверы', 'Свої сервери', 'Your own servers'), ('GitLab и GitHub Enterprise вашей компании администратор добавляет прямо в боте — по адресу сервера. После этого каждый пользователь подключает на нём свой аккаунт токеном доступа.', 'GitLab і GitHub Enterprise вашої компанії адміністратор додає просто в боті — за адресою сервера. Після цього кожен користувач підключає на ньому свій акаунт токеном доступу.', 'The admin adds your company’s GitLab or GitHub Enterprise right in the bot, by server address. After that each user connects their own account on it with an access token.'), 'server'),
        (('Изменения до отправки', 'Зміни до надсилання', 'Changes before you push'), ('Список изменённых файлов с числом добавленных и убранных строк, дифф каждого файла и коммиты, которые ещё не отправлены. Бот показывает это сам — без агента и запросов к модели.', 'Список змінених файлів із кількістю доданих і прибраних рядків, диф кожного файлу й коміти, які ще не надіслано. Бот показує це сам — без агента й запитів до моделі.', 'A list of changed files with added and removed line counts, a diff for each file and the commits not pushed yet. The bot shows it on its own — no agent, no model requests.'), 'code-compare'),
        (('Сохранить и отправить', 'Зберегти й надіслати', 'Save and push'), ('Одна кнопка коммитит изменения с вашим описанием и отправляет их на сервер, другая получает свежие. Агент может предложить отправку, но код уходит только после вашего нажатия.', 'Одна кнопка комітить зміни з вашим описом і надсилає їх на сервер, інша отримує свіжі. Агент може запропонувати надсилання, але код іде лише після вашого натискання.', 'One button commits the changes with your description and pushes them; another pulls fresh ones. The agent may suggest a push, but code leaves only after your tap.'), 'cloud-arrow-up'),
        (('Ветки и отмена', 'Гілки й скасування', 'Branches and undo'), ('Переключайте и создавайте ветки кнопками: при несохранённых изменениях бот сначала предложит их сохранить. Неудачные правки агента отменяются по файлу или все сразу, с подтверждением.', 'Перемикайте й створюйте гілки кнопками: за незбережених змін бот спершу запропонує їх зберегти. Невдалі правки агента скасовуються по файлу або всі одразу, з підтвердженням.', 'Switch and create branches with buttons: with unsaved changes the bot offers to save them first. Unwanted agent edits can be discarded per file or all at once, with a confirmation.'), 'code-branch'),
        (('Публикация и запрос на слияние', 'Публікація й запит на злиття', 'Publish and merge request'), ('Новый проект публикуется в личное пространство, группу GitLab или организацию GitHub: бот создаёт репозиторий и отправляет первый коммит. Запрос на слияние открывается из текущей ветки, в ответ — ссылка.', 'Новий проєкт публікується в особистий простір, групу GitLab або організацію GitHub: бот створює репозиторій і надсилає перший коміт. Запит на злиття відкривається з поточної гілки, у відповідь — посилання.', 'A new project is published to your personal space, a GitLab group or a GitHub organization: the bot creates the repository and pushes the first commit. A merge request opens from the current branch, and you get the link.'), 'code-pull-request'),
    ]
    content = '<div class="ap-grid ap-three">' + ''.join(card(*c) for c in git_cards) + '</div>'
    content += '<div class="bento-glass ap-note">' + p('Вход на сервер хранится только у бота и агенту по умолчанию не передаётся. Файлы с секретами (.env, ключи) в коммит не попадают: бот исключает их и дописывает в .gitignore. Работает с репозиториями по HTTPS; на машине с ботом нужен установленный git.', 'Вхід на сервер зберігається лише в бота й агенту за замовчуванням не передається. Файли із секретами (.env, ключі) у коміт не потрапляють: бот виключає їх і дописує в .gitignore. Працює з репозиторіями за HTTPS; на машині з ботом потрібен встановлений git.', 'The sign-in is stored only by the bot and is not passed to the agent by default. Files with secrets (.env, keys) stay out of commits: the bot excludes them and adds them to .gitignore. Works with HTTPS repositories; git must be installed on the bot’s machine.') + '</div>'
    page += section('git', ('Git, GitHub и GitLab — без терминала', 'Git, GitHub і GitLab — без термінала', 'Git, GitHub and GitLab without a terminal'), content,
                    ('Команда /git связывает проект с репозиторием. Подключить аккаунт, посмотреть, что изменил агент, отправить код и открыть запрос на слияние можно кнопками в чате.', 'Команда /git пов’язує проєкт із репозиторієм. Підключити акаунт, подивитися, що змінив агент, надіслати код і відкрити запит на злиття можна кнопками в чаті.', 'The /git command links a project to a repository. Connect an account, review what the agent changed, push the code and open a merge request — all with buttons in the chat.'))

    engines = [
        ('Claude Code', ('Claude Code + мост claude-agent-acp', 'Claude Code + міст claude-agent-acp', 'Claude Code + claude-agent-acp bridge'), ('Вход в аккаунт или API-ключ', 'Вхід в акаунт або API-ключ', 'Account login or API key')),
        ('OpenAI Codex', ('Codex CLI + мост codex-acp', 'Codex CLI + міст codex-acp', 'Codex CLI + codex-acp bridge'), ('Вход в аккаунт или API-ключ', 'Вхід в акаунт або API-ключ', 'Account login or API key')),
        ('Gemini CLI', ('Только Gemini CLI', 'Лише Gemini CLI', 'Just Gemini CLI'), ('Вход в аккаунт или API-ключ', 'Вхід в акаунт або API-ключ', 'Account login or API key')),
        ('Antigravity CLI', ('Только Antigravity CLI 1.5+', 'Лише Antigravity CLI 1.5+', 'Just Antigravity CLI 1.5+'), ('Вход через Google или ключ Gemini API', 'Вхід через Google або ключ Gemini API', 'Google sign-in or Gemini API key')),
        ('OpenCode', ('Только OpenCode', 'Лише OpenCode', 'Just OpenCode'), ('Бесплатные модели без ключа или ключи провайдеров', 'Безкоштовні моделі без ключа або ключі провайдерів', 'Free models with no key, or provider keys')),
    ]
    content = '<div class="ap-grid ap-five">' + ''.join(f'<article class="bento-glass ap-card ap-reveal"><div class="bento-content"><h3>{name}</h3><p><span class="ap-small">{text("Нужно:", "Потрібно:", "Needs:")}</span><br>{text(*need)}</p><p class="ap-small">{text(*auth)}</p></div></article>' for name, need, auth in engines) + '</div>'
    content += p('Достаточно одного агента. Остальные можно подключить позже — AcpGram сам найдёт установленные.', 'Достатньо одного агента. Інших можна підключити пізніше — AcpGram сам знайде встановлені.', 'One agent is enough. Add others later — AcpGram finds installed ones on its own.', 'ap-small')
    page += section('agents', ('Поддерживаемые агенты', 'Підтримувані агенти', 'Supported agents'), content)

    page += section('install', ('Установка за пять шагов', 'Встановлення за п’ять кроків', 'Install in five steps'), install_content(),
                    ('Обычно это занимает несколько минут. Если агент у вас уже работает, понадобятся две-три команды.', 'Зазвичай це займає кілька хвилин. Якщо агент у вас уже працює, знадобляться дві-три команди.', 'Usually takes a few minutes. If your agent already works, you need just two or three commands.'))

    security = '<div class="ap-grid ap-three">' + ''.join(card(*c) for c in [
        (('Бот отвечает только вам', 'Бот відповідає лише вам', 'The bot answers only you'), ('Других пользователей добавляете вы сами и задаёте им уровень доступа: только чтение, работа с подтверждениями или полный доступ.', 'Інших користувачів додаєте ви самі й задаєте їм рівень доступу: лише читання, робота з підтвердженнями або повний доступ.', 'You add other users yourself and set their access level: read-only, work with approvals, or full access.'), 'user-lock'),
        (('Данные на вашей машине', 'Дані на вашій машині', 'Data on your machine'), ('Код, настройки и история сессий остаются на компьютере с ботом. Сторонних серверов AcpGram нет.', 'Код, налаштування й історія сесій залишаються на комп’ютері з ботом. Сторонніх серверів AcpGram немає.', 'Code, settings and session history stay on the bot’s machine. AcpGram has no servers of its own.'), 'hard-drive'),
        (('Открытый код', 'Відкритий код', 'Open source'), ('Лицензия MIT: можно проверить, как устроены доступ и хранение данных, и доработать под себя.', 'Ліцензія MIT: можна перевірити, як влаштовані доступ і зберігання даних, і доопрацювати під себе.', 'MIT license: check how access and storage work and adapt it to your needs.'), 'code-branch'),
    ]) + '</div>'
    # trust: how the package is built, signed and checked (facts: npm provenance, Sigstore, CodeQL, OpenSSF)
    def a(href, label):
        return f'<a href="{href}" rel="noopener">{esc(label)}</a>'

    verify = '<div class="bento-glass ap-note ap-verify">' + '<p>' + T(
        '<strong>' + esc('Релизы можно проверить.') + '</strong> ' + esc('Публикуется с npm provenance: точный коммит за каждым релизом можно проверить. Каждая версия собирается из публичного кода в GitHub Actions и подписывается там же, а не загружается вручную. Проверить: блок Provenance на ') + a(NPM, 'странице пакета в npm') + esc(' или команда ') + '<code>npm audit signatures</code>' + esc('. Файлы релизов на GitHub подписаны Sigstore, код проверяют CodeQL и OpenSSF Scorecard, а у проекта есть бейдж ') + a('https://www.bestpractices.dev/projects/16722', 'OpenSSF Best Practices (passing)') + esc('. Как сообщить об уязвимости — в ') + a(REPO + '/blob/main/SECURITY.md', 'политике безопасности') + '.',
        '<strong>' + esc('Релізи можна перевірити.') + '</strong> ' + esc('Публікується з npm provenance: точний коміт за кожним релізом можна перевірити. Кожна версія збирається з публічного коду в GitHub Actions і підписується там же, а не завантажується вручну. Перевірити: блок Provenance на ') + a(NPM, 'сторінці пакета в npm') + esc(' або команда ') + '<code>npm audit signatures</code>' + esc('. Файли релізів на GitHub підписані Sigstore, код перевіряють CodeQL і OpenSSF Scorecard, а в проєкту є бейдж ') + a('https://www.bestpractices.dev/projects/16722', 'OpenSSF Best Practices (passing)') + esc('. Як повідомити про вразливість — у ') + a(REPO + '/blob/main/SECURITY.md', 'політиці безпеки') + '.',
        '<strong>' + esc('Releases you can verify.') + '</strong> ' + esc('Published with npm provenance: verify the exact commit behind every release. Every version is built from the public code in GitHub Actions and signed there, not uploaded by hand. Check it in the Provenance block on the ') + a(NPM, 'npm page') + esc(' or with ') + '<code>npm audit signatures</code>' + esc('. Release files on GitHub are signed with Sigstore, the code is scanned by CodeQL and OpenSSF Scorecard, and the project has the ') + a('https://www.bestpractices.dev/projects/16722', 'OpenSSF Best Practices (passing)') + esc(' badge. To report a vulnerability, see the ') + a(REPO + '/blob/main/SECURITY.md', 'security policy') + '.') + '</p></div>'
    security += verify
    security += '<div class="bento-glass ap-note">' + p('Для команды на Linux: личные пространства (USER_WORKSPACES=1) дают каждому сотруднику свою папку проектов, а песочница (AGENT_SANDBOX=bwrap) запускает его агента изолированно — внутри нет ни чужих папок, ни настроек и базы бота. Сеть песочница не ограничивает, а агентам в ней нужен ключ API или бесплатные модели OpenCode.', 'Для команди на Linux: особисті простори (USER_WORKSPACES=1) дають кожному співробітнику свою папку проєктів, а пісочниця (AGENT_SANDBOX=bwrap) запускає його агента ізольовано — усередині немає ні чужих папок, ні налаштувань і бази бота. Мережу пісочниця не обмежує, а агентам у ній потрібен ключ API або безкоштовні моделі OpenCode.', 'For a team on Linux: personal workspaces (USER_WORKSPACES=1) give each teammate a private projects folder, and the sandbox (AGENT_SANDBOX=bwrap) runs their agent in isolation — no other people’s folders, no bot settings or database inside. The sandbox does not restrict the network, and agents in it need an API key or OpenCode’s free models.') + '</div>'
    security += '<div class="bento-glass ap-note">' + p('Совет: без песочницы агент работает с правами пользователя, под которым запущен бот, — папка проекта не изолирует остальные файлы. Запускайте бота под отдельной учётной записью и выдавайте полный доступ (без подтверждений) только тем, кому доверяете.', 'Порада: без пісочниці агент працює з правами користувача, під яким запущено бота, — папка проєкту не ізолює решту файлів. Запускайте бота під окремим обліковим записом і надавайте повний доступ (без підтверджень) лише тим, кому довіряєте.', 'Tip: without the sandbox the agent runs with the rights of the account the bot runs under — the project folder does not isolate other files. Run the bot under a dedicated account and grant full access (no approvals) only to people you trust.') + '</div>'
    page += section('security', ('Безопасность', 'Безпека', 'Security'), security)

    metrics = [('downloadsTotal', ('загрузок всего: npm + GitHub', 'завантажень загалом: npm + GitHub', 'downloads in total: npm + GitHub')),
               ('npm.last30d', ('скачиваний npm за месяц', 'завантажень npm за місяць', 'npm downloads this month')),
               ('github.releases.downloads', ('скачиваний установщика с GitHub', 'завантажень інсталятора з GitHub', 'installer downloads from GitHub')),
               ('github.stars', ('звёзд на GitHub', 'зірок на GitHub', 'GitHub stars'))]
    content = '<div class="ap-grid ap-four">' + ''.join(f'<div class="bento-glass ap-stat ap-reveal">{metric(path)}<span>{text(*label)}</span></div>' for path, label in metrics) + '</div>'
    content += '<p class="ap-stat-dates"><span id="ap-updated">' + text('Обновлено: ', 'Оновлено: ', 'Updated: ') + esc(stats.get('updated') or '—') + '</span> · ' + text('Загрузки включают обновления, CI и автоматические скачивания, поэтому это не число пользователей.', 'Завантаження включають оновлення, CI та автоматичні завантаження, тому це не кількість користувачів.', 'Downloads include updates, CI and automated fetches, so they are not a user count.') + '</p>'
    page += section('stats', ('Проект в цифрах', 'Проєкт у цифрах', 'By the numbers'), content)

    news = ''.join(
        f'<a href="{href}" class="bento-glass ap-card ap-press ap-reveal"><div class="bento-content"><span class="ap-eyebrow">{text(*date)}</span><h3>{text(*title)}</h3>{p(*desc)}<span aria-hidden="true">→</span></div></a>'
        for date, href, title, desc in NEWS[:2])
    news += f'<a href="/blog/?tag=acpgram#posts" class="bento-glass ap-card ap-press ap-reveal"><div class="bento-content"><span class="ap-eyebrow">{text("Блог", "Блог", "Blog")}</span><h3>{text("Все статьи об AcpGram", "Усі статті про AcpGram", "All posts about AcpGram")}</h3>{p("Обзоры версий, инструкции и ответы на вопросы.", "Огляди версій, інструкції й відповіді на запитання.", "Release write-ups, how-tos and answers to questions.")}<span aria-hidden="true">→</span></div></a>'
    page += section('news', ('Новости', 'Новини', 'News'), '<div class="ap-grid ap-three">' + news + '</div>',
                    ('Что появилось в последних версиях — в блоге автора.', 'Що з’явилося в останніх версіях — у блозі автора.', 'What the latest versions brought, from the author’s blog.'))

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
    page += '<div class="ap-actions">' + link('#install', text('Установить', 'Встановити', 'Install'), True, 'download') + link(DOCS, text('Документация', 'Документація', 'Docs'), icon='book-open') + link(REPO, text('★ Звезда на GitHub', '★ Зірка на GitHub', '★ Star on GitHub'), icon='star') + '</div>'
    # Peerlist: голосование за проект (виджет-картинка подгружается с peerlist.io, показывает число голосов)
    page += '<div class="ap-peerlist">' + p('Понравился проект? Поддержите его голосом на Peerlist.', 'Сподобався проєкт? Підтримайте його голосом на Peerlist.', 'Like the project? Give it an upvote on Peerlist.', 'ap-small') + '<a href="https://peerlist.io/selesnow/project/acpgram--telegram-gateway-to-coding-agent" target="_blank" rel="noopener noreferrer"><img src="https://peerlist.io/api/v1/projects/embed/PRJHNN7K9L8R89AAO3NRDR9GA7L8PL?showUpvote=true&amp;theme=dark" alt="AcpGram — Telegram gateway to coding agent" width="296" height="72" loading="lazy" decoding="async"></a></div>'
    page += '</div></section></main>'
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
