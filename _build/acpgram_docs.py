"""AcpGram documentation: /acpgram/docs/.

Content lives in three Markdown files, one per language: _build/acpgram_docs/{ru,ua,en}.md.
Every heading carries an explicit id — `## Title {#id}` (section) or `### Title {#id}` (subsection) —
and the three files must have the same headings in the same order: the id is the anchor shared by all
languages, so a link like /acpgram/docs/#git-signin works whatever language the reader picked.

Screenshots: a line `{{shot: name | alt text}}` becomes a figure when img/acpgram/docs/<name>.webp
(or .png / .jpg; `<name>.<lang>.webp` overrides it for one language) exists, and is skipped otherwise.
The build prints the names that are still missing, so adding a screenshot is: drop the file, rebuild.

Facts come from the AcpGram README (see _build/ACPGRAM.md). Run: python _build/acpgram_docs.py
"""
import json
import re
from pathlib import Path

import markdown

from build import T, esc, head, nav, footer, tail, ROOT

SRC = Path(__file__).parent / 'acpgram_docs'
IMG = ROOT / 'img' / 'acpgram' / 'docs'
LANGS = ('ru', 'ua', 'en')
REPO = 'https://github.com/selesnow/acpgram'
HEAD_RE = re.compile(r'^(#{2,3}) (.+?) \{#([a-z0-9-]+)\}\s*$')
SHOT_RE = re.compile(r'^\{\{shot:\s*([a-z0-9-]+)\s*\|\s*(.+?)\s*\}\}\s*$', re.M)
CHAT_API = 'https://acpgram-docs-chat.selesnow.workers.dev/api/ask'   # the worker: _worker/acpgram-docs-chat
COPY = {'ru': 'Копировать', 'ua': 'Копіювати', 'en': 'Copy'}


def deep(s):
    """Shared header / menu / scripts are written for first-level pages; this page is two levels deep."""
    return s.replace('="../', '="../../')


def parse(lang):
    """Markdown file → list of blocks {level, id, title, body}."""
    blocks = []
    for line in (SRC / f'{lang}.md').read_text(encoding='utf-8').splitlines():
        m = HEAD_RE.match(line)
        if m:
            blocks.append({'level': len(m.group(1)), 'id': m.group(3), 'title': m.group(2).strip(), 'body': []})
        elif blocks:
            blocks[-1]['body'].append(line)
        elif line.strip():
            raise SystemExit(f'acpgram_docs: {lang}.md has text before the first heading')
    for b in blocks:
        b['body'] = '\n'.join(b['body']).strip()
    return blocks


def shot_file(name, lang):
    for stem in (f'{name}.{lang}', name):
        for ext in ('webp', 'png', 'jpg'):
            if (IMG / f'{stem}.{ext}').exists():
                return f'{stem}.{ext}'
    return None


def shot_html(name, alt, lang, missing):
    file = shot_file(name, lang)
    if not file:
        missing.setdefault(name, alt)
        return ''
    size = ''
    try:
        from PIL import Image
        with Image.open(IMG / file) as im:
            size = f' width="{im.width}" height="{im.height}"'
    except Exception:
        pass
    src = f'../../img/acpgram/docs/{file}'
    return (f'<figure class="ad-shot"><a class="ad-zoom" href="{src}"><img src="{src}" alt="{esc(alt)}"{size} loading="lazy" decoding="async"></a>'
            f'<figcaption>{esc(alt)}</figcaption></figure>')


def render(body, lang, missing):
    """Markdown of one block → HTML: screenshots, copy buttons on code, scrollable tables, external links."""
    shots = []

    def stash(m):
        shots.append(shot_html(m.group(1), m.group(2), lang, missing))
        return f'\n\nADSHOT{len(shots) - 1:04d}\n\n'

    out = markdown.markdown(SHOT_RE.sub(stash, body), extensions=['fenced_code', 'tables', 'sane_lists'])
    out = re.sub(r'<pre><code(?: class="[^"]*")?>(.*?)</code></pre>',
                 lambda m: f'<div class="ap-code"><pre><code>{m.group(1).rstrip()}</code></pre>'
                           f'<button type="button" class="ap-copy">{COPY[lang]}</button></div>',
                 out, flags=re.S)
    out = out.replace('<table>', '<div class="ad-table"><table>').replace('</table>', '</table></div>')
    out = re.sub(r'<a href="(https?://(?!(?:www\.)?alexey-seleznev\.pro))', r'<a target="_blank" rel="noopener" href="\1', out)
    return segments(out, shots)


def segments(out, shots):
    """Puts the screenshots back into the block. They stay outside the text, between its paragraphs, centred;
    screenshots that follow one another stand in a row."""
    parts = re.split(r'<p>ADSHOT(\d{4})</p>', out)
    result, figs = [parts[0]], []

    def flush():
        if figs:
            result.append(f'<div class="ad-figs">{"".join(figs)}</div>')
            figs.clear()

    for i in range(1, len(parts), 2):
        fig = shots[int(parts[i])]
        if fig:
            figs.append(fig)
        if parts[i + 1].strip():
            flush()
            result.append(parts[i + 1])
    flush()
    return ''.join(result)


def load():
    """Three languages → one list of blocks with titles and HTML per language; fails if the structures differ."""
    docs = {lang: parse(lang) for lang in LANGS}
    shape = [(b['level'], b['id']) for b in docs['ru']]
    for lang in LANGS[1:]:
        other = [(b['level'], b['id']) for b in docs[lang]]
        if other != shape:
            diff = next((i for i, (a, b) in enumerate(zip(shape, other)) if a != b), min(len(shape), len(other)))
            raise SystemExit(f'acpgram_docs: {lang}.md differs from ru.md at heading {diff + 1}: '
                             f'{shape[diff] if diff < len(shape) else "—"} vs {other[diff] if diff < len(other) else "—"}')
    ids = [i for _, i in shape]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        raise SystemExit(f'acpgram_docs: duplicate ids: {sorted(dup)}')
    if shape and shape[0][0] != 2:
        raise SystemExit('acpgram_docs: the first heading must be a section (##)')
    missing = {}
    blocks = []
    for i, (level, id) in enumerate(shape):
        blocks.append({'level': level, 'id': id,
                       'title': tuple(docs[lang][i]['title'] for lang in LANGS),
                       'html': tuple(render(docs[lang][i]['body'], lang, missing) for lang in LANGS)})
    for b in blocks:   # internal links must point at existing anchors
        for h in b['html']:
            for target in re.findall(r'href="#([^"]+)"', h):
                if target not in ids:
                    raise SystemExit(f'acpgram_docs: link to a missing anchor #{target} in section {b["id"]}')
    return blocks, missing


def write_plain(out):
    """The documentation as plain text, one file per language: docs.<lang>.txt. The chat worker puts it into
    the model's prompt, so the headings keep their {#id} anchors and the screenshot lines are dropped.
    A .txt and not a .md: GitHub Pages would turn a Markdown file into an HTML page."""
    for lang in LANGS:
        src = SHOT_RE.sub('', (SRC / f'{lang}.md').read_text(encoding='utf-8'))
        src = re.sub(r'\n{3,}', '\n\n', src).strip()
        (out / f'docs.{lang}.txt').write_text(f'# AcpGram documentation ({lang})\n\n{src}\n', encoding='utf-8', newline='\n')


def chat_html():
    """The AI chat about the documentation: a floating button and a panel, both hidden until chat.js starts."""
    chips = (('Как установить AcpGram?', 'Як встановити AcpGram?', 'How do I install AcpGram?'),
             ('Как подключить GitHub?', 'Як підключити GitHub?', 'How do I connect GitHub?'),
             ('Как дать доступ коллеге?', 'Як дати доступ колезі?', 'How do I give a teammate access?'))
    return f'''<button type="button" class="dc-fab" id="dc-fab" aria-expanded="false" aria-controls="dc-panel" hidden><i aria-hidden="true" class="fa-solid fa-wand-magic-sparkles"></i>{text('Спросить ИИ', 'Запитати ШІ', 'Ask AI')}</button>
    <section class="dc-panel" id="dc-panel" role="dialog" aria-labelledby="dc-title" data-api="{CHAT_API}" hidden>
    <header class="dc-head"><i aria-hidden="true" class="fa-solid fa-wand-magic-sparkles"></i><div><p class="dc-title" id="dc-title">{text('Помощник по документации', 'Помічник із документації', 'Documentation assistant')}</p><p class="dc-sub">{text('ИИ отвечает по тексту этой страницы', 'ШІ відповідає за текстом цієї сторінки', 'AI answers from the text of this page')}</p></div>
    <button type="button" class="dc-icon" id="dc-reset" aria-label="New chat" hidden><i aria-hidden="true" class="fa-solid fa-rotate-left"></i></button><button type="button" class="dc-icon" id="dc-close" aria-label="Close">×</button></header>
    <div class="dc-log" id="dc-log" role="log" aria-live="polite"><div class="dc-msg dc-bot dc-hello">{text('Спросите об установке, настройках, Git, работе в команде или командах бота. Отвечу по документации и дам ссылки на разделы.',
                                                                                                           'Запитайте про встановлення, налаштування, Git, роботу в команді чи команди бота. Відповім за документацією й дам посилання на розділи.',
                                                                                                           'Ask about installation, settings, Git, team work or the bot commands. I answer from the documentation and link the sections.')}</div></div>
    <div class="dc-chips" id="dc-chips">{''.join(f'<button type="button">{text(*c)}</button>' for c in chips)}</div>
    <form class="dc-form" id="dc-form"><textarea id="dc-input" rows="1" maxlength="600" placeholder="Your question" data-ph-ru="Ваш вопрос" data-ph-ua="Ваше запитання" data-ph-en="Your question" aria-label="Your question"></textarea><button type="submit" class="dc-send" aria-label="Send"><i aria-hidden="true" class="fa-solid fa-paper-plane"></i></button></form>
    <p class="dc-note">{text('ИИ может ошибаться: сверяйтесь с разделами по ссылкам. Не отправляйте пароли и токены.', 'ШІ може помилятися: звіряйтеся з розділами за посиланнями. Не надсилайте паролі й токени.', 'AI can be wrong: check the linked sections. Do not send passwords or tokens.')}</p></section>'''


def lang_blocks(htmls):
    return ''.join(f'<div class="{lang}-text ad-lang">{h}</div>' for lang, h in zip(LANGS, htmls) if h)


def title_html(tag, b):
    return (f'<{tag}>{T(*(esc(t) for t in b["title"]))}'
            f'<a class="ad-anchor" href="#{b["id"]}" aria-label="Link to this section">#</a></{tag}>')


def pager_html(tops, i):
    """Previous / next section links at the end of a section."""
    def one(b, cls, label):
        return f'<a class="{cls}" href="#{b["id"]}"><small>{label}</small><span>{T(*(esc(t) for t in b["title"]))}</span></a>'
    prev = one(tops[i - 1], 'ad-prev', '← ' + text('Назад', 'Назад', 'Previous')) if i > 0 else ''
    nxt = one(tops[i + 1], 'ad-next', text('Далее', 'Далі', 'Next') + ' →') if i + 1 < len(tops) else ''
    return f'<nav class="ad-pager" aria-label="Sections">{prev}{nxt}</nav>'


def content_html(blocks):
    tops = [b for b in blocks if b['level'] == 2]
    out, open_section = '', -1
    for b in blocks:
        if b['level'] == 2:
            out += (pager_html(tops, open_section) + '</section>' if open_section >= 0 else '') + f'<section id="{b["id"]}" class="ad-section">{title_html("h2", b)}{lang_blocks(b["html"])}'
            open_section += 1
        else:
            out += f'<section id="{b["id"]}" class="ad-sub">{title_html("h3", b)}{lang_blocks(b["html"])}</section>'
    return out + (pager_html(tops, open_section) + '</section>' if open_section >= 0 else '')


def toc_html(blocks):
    out, open_sub = '<ul>', False
    for i, b in enumerate(blocks):
        link = f'<a href="#{b["id"]}">{T(*(esc(t) for t in b["title"]))}</a>'
        if b['level'] == 2:
            out += ('</ul></li>' if open_sub else ('</li>' if i else '')) + f'<li>{link}'
            open_sub = False
        else:
            out += ('' if open_sub else '<ul>') + f'<li>{link}</li>'
            open_sub = True
    return out + ('</ul></li>' if open_sub else '</li>') + '</ul>'


def text(ru, ua, en):
    return T(esc(ru), esc(ua), esc(en))


def build_acpgram_docs():
    blocks, missing = load()
    snapshot = ROOT / 'assets/acpgram-stats.json'
    stats = json.loads(snapshot.read_text(encoding='utf-8')) if snapshot.exists() else {}
    version = (stats.get('npm') or {}).get('version')

    desc = ('Подробная документация AcpGram: установка и настройка, проекты и сессии, агенты и модели, файлы и секреты, '
            'Git с GitHub и GitLab, работа в команде, песочница, все настройки и команды.')
    ld = {'@context': 'https://schema.org', '@type': 'TechArticle',
          'headline': 'AcpGram documentation', 'description': desc, 'inLanguage': ['ru', 'uk', 'en'],
          'url': 'https://alexey-seleznev.pro/acpgram/docs/',
          'about': {'@type': 'SoftwareApplication', 'name': 'AcpGram', 'url': 'https://alexey-seleznev.pro/acpgram/',
                    'applicationCategory': 'DeveloperApplication', 'operatingSystem': 'Windows, Linux, macOS'},
          'author': {'@type': 'Person', 'name': 'Alexey Seleznev', 'url': 'https://alexey-seleznev.pro/'}}
    page = deep(head('acpgram/docs', 'Документация AcpGram — кодинг-агенты в Telegram', desc,
                     image='https://alexey-seleznev.pro/img/acpgram/og-acpgram.jpg', jsonld=ld))
    page = page.replace('    <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">\n', '').replace('    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>\n', '')
    page = page.replace('content="summary"', 'content="summary_large_image"').replace('content="Алексей Селезнёв"', 'content="AcpGram — AI coding agents in Telegram"')
    page = page.replace('    <!-- Tailwind', '    <link rel="stylesheet" href="../acpgram.css">\n    <link rel="stylesheet" href="docs.css">\n    <link rel="stylesheet" href="chat.css">\n    <!-- Tailwind')
    page = page.replace('class="relative lang-en"', 'class="relative lang-en acpgram-page acpgram-docs"')
    page = page.replace('<html lang="en" class="scroll-smooth">', '<html lang="en" class="scroll-smooth ad-root">')   # scroll-padding under the sticky header, see docs.css
    page += deep(nav('acpgram'))

    sections = sum(1 for b in blocks if b['level'] == 2)
    page += '<main id="main-content" class="ap-main ad-main">'
    # Quick links fill the right half of the hero: the sections people open most often.
    QUICK = (('install', 'download'), ('first-steps', 'play'), ('git', 'code-branch'), ('team', 'users'), ('env', 'sliders'), ('troubleshooting', 'life-ring'))
    by_id = {b['id']: b for b in blocks}
    quick = ''.join(f'<a href="#{id}"><i aria-hidden="true" class="fa-solid fa-{icon}"></i><span>{T(*(esc(t) for t in by_id[id]["title"]))}</span></a>'
                    for id, icon in QUICK if id in by_id)
    page += f'''<header class="ad-hero"><div class="ad-hero-text"><nav class="ad-crumbs" aria-label="Breadcrumb"><a href="../../">{text('Главная', 'Головна', 'Home')}</a><span>/</span><a href="../">AcpGram</a><span>/</span><span>{text('Документация', 'Документація', 'Documentation')}</span></nav>
    <h1>{text('Документация AcpGram', 'Документація AcpGram', 'AcpGram documentation')}</h1>
    <p class="ap-lead">{text('Всё об установке и работе: от первого запуска до Git, работы в команде и песочницы. Содержание с поиском по разделам всегда под рукой, язык переключается в шапке сайта.',
                             'Усе про встановлення й роботу: від першого запуску до Git, роботи в команді й пісочниці. Зміст із пошуком за розділами завжди під рукою, мова перемикається в шапці сайту.',
                             'Everything about installing and using AcpGram: from the first run to Git, team work and the sandbox. The contents with a section search stay within reach; switch the language in the site header.')}</p>
    <div class="ad-meta">{f'<span class="ad-pill">AcpGram v{esc(version)}</span>' if version else ''}<span class="ad-pill">{sections} {text('разделов', 'розділів', 'sections')}</span><a class="ad-pill" href="../#install">{text('Установка за пять шагов', 'Встановлення за п’ять кроків', 'Install in five steps')} →</a><a class="ad-pill" href="{REPO}" rel="noopener">GitHub ↗</a></div></div>
    <nav class="ad-quick" aria-label="Quick links"><p class="ad-quick-title">{text('Быстрый переход', 'Швидкий перехід', 'Jump to')}</p>{quick}</nav></header>'''

    page += f'''<div class="ad-layout"><aside class="ad-toc" aria-label="Contents"><button type="button" class="ad-toc-toggle" aria-expanded="true" aria-controls="ad-toc-body"><i aria-hidden="true" class="fa-solid fa-list"></i>{text('Содержание', 'Зміст', 'Contents')}</button>
    <div class="ad-toc-body" id="ad-toc-body"><div class="ad-search-box"><i aria-hidden="true" class="fa-solid fa-magnifying-glass"></i><input type="search" class="ad-search" id="ad-search" placeholder="Search sections" data-ph-ru="Поиск по разделам" data-ph-ua="Пошук за розділами" data-ph-en="Search sections" aria-label="Search sections" aria-keyshortcuts="/" autocomplete="off"><kbd class="ad-kbd" aria-hidden="true">/</kbd></div>
    <nav class="ad-toc-nav">{toc_html(blocks)}</nav><p class="ad-toc-count" hidden></p><p class="ad-toc-empty" hidden>{text('Ничего не найдено', 'Нічого не знайдено', 'Nothing found')}</p></div></aside>
    <article class="ad-content">{content_html(blocks)}
    <footer class="ad-foot bento-glass"><p>{text('Не нашли ответ? Напишите в GitHub Issues — и документация станет лучше.', 'Не знайшли відповіді? Напишіть у GitHub Issues — і документація стане кращою.', 'Didn’t find the answer? Open a GitHub issue — and the documentation gets better.')}</p>
    <div class="ap-actions"><a class="ap-button ap-primary" href="../#install"><i aria-hidden="true" class="fa-solid fa-download"></i>{text('Установить', 'Встановити', 'Install')}</a><a class="ap-button" href="{REPO}/issues" rel="noopener"><i aria-hidden="true" class="fa-brands fa-github"></i>GitHub Issues</a><a class="ap-button" href="../../blog/?tag=acpgram#posts"><i aria-hidden="true" class="fa-solid fa-newspaper"></i>{text('Новости', 'Новини', 'News')}</a></div></footer></article></div>'''
    page += '</main>'
    page += footer('../../')
    page += '<div class="ap-toast" role="status" aria-live="polite" id="ap-status"></div>'
    page += ('<dialog class="ad-lightbox" id="ad-lightbox" aria-label="Screenshot"><button type="button" class="ad-lightbox-close" aria-label="Close">×</button>'
             '<img alt=""><p class="ad-lightbox-cap"></p></dialog>')
    page += chat_html()
    page += deep(tail()).replace('    <script src="../../assets/site.js"></script>', '    <script src="../../assets/site.js"></script>\n    <script src="docs.js"></script>\n    <script src="chat.js"></script>')

    out = ROOT / 'acpgram' / 'docs'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'index.html').write_text(page, encoding='utf-8')
    write_plain(out)
    print(f'acpgram/docs/index.html: {sections} sections, {len(blocks) - sections} subsections')
    if missing:
        print(f'  screenshots still missing ({len(missing)}): ' + ', '.join(missing))
    return missing


if __name__ == '__main__':
    build_acpgram_docs()
