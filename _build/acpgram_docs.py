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
    return f'<figure class="ad-shot"><img src="../../img/acpgram/docs/{file}" alt="{esc(alt)}"{size} loading="lazy" decoding="async"></figure>'


def render(body, lang, missing):
    """Markdown of one block → HTML: screenshots, copy buttons on code, scrollable tables, external links."""
    shots = []

    def stash(m):
        shots.append(shot_html(m.group(1), m.group(2), lang, missing))
        return f'\n\nADSHOT{len(shots) - 1:04d}\n\n'

    out = markdown.markdown(SHOT_RE.sub(stash, body), extensions=['fenced_code', 'tables', 'sane_lists'])
    out = re.sub(r'<p>ADSHOT(\d{4})</p>', lambda m: shots[int(m.group(1))], out)
    out = re.sub(r'<pre><code(?: class="[^"]*")?>(.*?)</code></pre>',
                 lambda m: f'<div class="ap-code"><pre><code>{m.group(1).rstrip()}</code></pre>'
                           f'<button type="button" class="ap-copy">{COPY[lang]}</button></div>',
                 out, flags=re.S)
    out = out.replace('<table>', '<div class="ad-table"><table>').replace('</table>', '</table></div>')
    out = re.sub(r'<a href="(https?://(?!(?:www\.)?alexey-seleznev\.pro))', r'<a target="_blank" rel="noopener" href="\1', out)
    return out


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


def lang_blocks(htmls):
    return ''.join(f'<div class="{lang}-text ad-lang">{h}</div>' for lang, h in zip(LANGS, htmls) if h)


def title_html(tag, b):
    return (f'<{tag}>{T(*(esc(t) for t in b["title"]))}'
            f'<a class="ad-anchor" href="#{b["id"]}" aria-label="Link to this section">#</a></{tag}>')


def content_html(blocks):
    out, open_section = '', False
    for b in blocks:
        if b['level'] == 2:
            out += ('</section>' if open_section else '') + f'<section id="{b["id"]}" class="ad-section">{title_html("h2", b)}{lang_blocks(b["html"])}'
            open_section = True
        else:
            out += f'<section id="{b["id"]}" class="ad-sub">{title_html("h3", b)}{lang_blocks(b["html"])}</section>'
    return out + ('</section>' if open_section else '')


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
    page = page.replace('    <!-- Tailwind', '    <link rel="stylesheet" href="../acpgram.css">\n    <link rel="stylesheet" href="docs.css">\n    <!-- Tailwind')
    page = page.replace('class="relative lang-en"', 'class="relative lang-en acpgram-page acpgram-docs"')
    page += deep(nav('acpgram'))

    sections = sum(1 for b in blocks if b['level'] == 2)
    page += '<main id="main-content" class="ap-main ad-main">'
    page += f'''<header class="ad-hero"><nav class="ad-crumbs" aria-label="Breadcrumb"><a href="../../">{text('Главная', 'Головна', 'Home')}</a><span>/</span><a href="../">AcpGram</a><span>/</span><span>{text('Документация', 'Документація', 'Documentation')}</span></nav>
    <h1>{text('Документация AcpGram', 'Документація AcpGram', 'AcpGram documentation')}</h1>
    <p class="ap-lead">{text('Всё об установке и работе: от первого запуска до Git, работы в команде и песочницы. В содержании есть поиск по разделам, язык переключается в шапке сайта.',
                             'Усе про встановлення й роботу: від першого запуску до Git, роботи в команді й пісочниці. У змісті є пошук за розділами, мова перемикається в шапці сайту.',
                             'Everything about installing and using AcpGram: from the first run to Git, team work and the sandbox. The contents include a section search; switch the language in the site header.')}</p>
    <div class="ad-meta">{f'<span class="ad-pill">AcpGram v{esc(version)}</span>' if version else ''}<span class="ad-pill">{sections} {text('разделов', 'розділів', 'sections')}</span><a class="ad-pill" href="../#install">{text('Установка за пять шагов', 'Встановлення за п’ять кроків', 'Install in five steps')} →</a><a class="ad-pill" href="{REPO}" rel="noopener">GitHub ↗</a></div></header>'''

    page += f'''<div class="ad-layout"><aside class="ad-toc" aria-label="Contents"><button type="button" class="ad-toc-toggle" aria-expanded="true" aria-controls="ad-toc-body"><i aria-hidden="true" class="fa-solid fa-list"></i>{text('Содержание', 'Зміст', 'Contents')}</button>
    <div class="ad-toc-body" id="ad-toc-body"><input type="search" class="ad-search" id="ad-search" placeholder="Search sections" data-ph-ru="Поиск по разделам" data-ph-ua="Пошук за розділами" data-ph-en="Search sections" aria-label="Search sections" autocomplete="off">
    <nav class="ad-toc-nav">{toc_html(blocks)}</nav><p class="ad-toc-empty" hidden>{text('Ничего не найдено', 'Нічого не знайдено', 'Nothing found')}</p></div></aside>
    <article class="ad-content">{content_html(blocks)}
    <footer class="ad-foot bento-glass"><p>{text('Не нашли ответ? Напишите в GitHub Issues — и документация станет лучше.', 'Не знайшли відповіді? Напишіть у GitHub Issues — і документація стане кращою.', 'Didn’t find the answer? Open a GitHub issue — and the documentation gets better.')}</p>
    <div class="ap-actions"><a class="ap-button ap-primary" href="../#install"><i aria-hidden="true" class="fa-solid fa-download"></i>{text('Установить', 'Встановити', 'Install')}</a><a class="ap-button" href="{REPO}/issues" rel="noopener"><i aria-hidden="true" class="fa-brands fa-github"></i>GitHub Issues</a><a class="ap-button" href="../../blog/?tag=acpgram#posts"><i aria-hidden="true" class="fa-solid fa-newspaper"></i>{text('Новости', 'Новини', 'News')}</a></div></footer></article></div>'''
    page += '</main>'
    page += footer('../../')
    page += '<div class="ap-toast" role="status" aria-live="polite" id="ap-status"></div>'
    page += deep(tail()).replace('    <script src="../../assets/site.js"></script>', '    <script src="../../assets/site.js"></script>\n    <script src="docs.js"></script>')

    out = ROOT / 'acpgram' / 'docs'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'index.html').write_text(page, encoding='utf-8')
    print(f'acpgram/docs/index.html: {sections} sections, {len(blocks) - sections} subsections')
    if missing:
        print(f'  screenshots still missing ({len(missing)}): ' + ', '.join(missing))
    return missing


if __name__ == '__main__':
    build_acpgram_docs()
