// AcpGram documentation: AI chat. The question goes to a Cloudflare Worker (_worker/acpgram-docs-chat),
// which adds the documentation text and asks a model; the answer arrives as a stream.
(() => {
    const panel = document.getElementById('dc-panel');
    const fab = document.getElementById('dc-fab');
    if (!panel || !fab || !window.fetch || !window.ReadableStream) return;

    // ?chat-api=http://127.0.0.1:8787/api/ask on a local server points the page at `wrangler dev`
    const local = /^(localhost|127\.0\.0\.1)$/.test(location.hostname);
    const API = (local && new URLSearchParams(location.search).get('chat-api')) || panel.dataset.api;
    const STORE = 'acpgramDocsChat';
    const HISTORY = 6;   // messages sent with a question, the question included

    const lang = () => ['ru', 'ua', 'en'].find(l => document.body.classList.contains('lang-' + l)) || 'en';
    const label = (ru, ua, en) => ({ru, ua, en})[lang()];
    const log = document.getElementById('dc-log');
    const form = document.getElementById('dc-form');
    const input = document.getElementById('dc-input');
    const chips = document.getElementById('dc-chips');
    const reset = document.getElementById('dc-reset');
    const send = form.querySelector('.dc-send');
    const phone = matchMedia('(max-width:639px)');
    const track = (name, params) => { if (typeof sendGAEvent === 'function') sendGAEvent(name, params); };

    let messages = [];   // {role: 'user' | 'assistant', content}
    let busy = false;

    // ---------- answer text: a small safe subset of Markdown ----------
    const escapeHtml = s => s.replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'})[c]);
    const DOCS_URL = /^https?:\/\/alexey-seleznev\.pro\/acpgram\/docs\/?(#[a-z0-9-]+)$/;
    function link(text, href) {   // both are already escaped
        const anchor = href.match(DOCS_URL)?.[1] || href;
        if (/^#[a-z0-9-]+$/.test(anchor)) return document.getElementById(anchor.slice(1)) ? `<a class="dc-ref" href="${anchor}">${text}</a>` : text;
        if (/^https?:\/\//.test(href)) return `<a href="${href}" target="_blank" rel="noopener">${text}</a>`;
        return text;
    }
    function inline(src) {
        return src.split(/(`[^`\n]+`)/).map((part, i) => {
            if (i % 2) return '<code>' + escapeHtml(part.slice(1, -1)) + '</code>';
            return escapeHtml(part)
                .replace(/\[([^\]\n]+)\]\(([^)\s]+)\)/g, (match, text, href) => link(text, href))
                .replace(/\*\*([^*\n]+)\*\*/g, '<strong>$1</strong>');
        }).join('');
    }
    function markdown(src) {
        const html = [];
        src.replace(/\s*\{#[a-z0-9-]+\}/g, '').split('```').forEach((part, i) => {
            if (i % 2) {   // a code block; while the answer is still arriving it may be unclosed
                html.push('<pre><code>' + escapeHtml(part.replace(/^[\w+-]*\n/, '').replace(/\s+$/, '')) + '</code></pre>');
                return;
            }
            let para = [], items = [], start = null;   // start: the first number of an ordered list, null for a bulleted one
            const flushPara = () => { if (para.length) html.push('<p>' + para.join('<br>') + '</p>'); para = []; };
            const flushList = () => {
                if (items.length) html.push((start === null ? '<ul>' : `<ol start="${start}">`) + items.map(item => '<li>' + item + '</li>').join('') + (start === null ? '</ul>' : '</ol>'));
                items = [];
            };
            for (const line of part.split('\n')) {
                const item = line.match(/^\s*(?:[-*•]|(\d{1,2})[.)])\s+(.*)$/);
                if (item) {
                    flushPara();
                    const ordered = item[1] !== undefined;
                    if (items.length && ordered !== (start !== null)) flushList();
                    if (!items.length) start = ordered ? Number(item[1]) : null;
                    items.push(inline(item[2]));
                } else if (!line.trim()) {
                    flushPara();
                } else if (items.length && /^\s{2,}/.test(line)) {
                    items[items.length - 1] += '<br>' + inline(line.trim());
                } else {
                    flushList();
                    para.push(inline(line.replace(/^#{1,6}\s+/, '')));
                }
            }
            flushPara();
            flushList();
        });
        return html.join('');
    }

    // ---------- messages ----------
    function bubble(role, content) {
        const el = document.createElement('div');
        el.className = 'dc-msg ' + (role === 'user' ? 'dc-user' : 'dc-bot');
        if (role === 'user') el.textContent = content; else el.innerHTML = markdown(content);
        log.append(el);
        log.scrollTop = log.scrollHeight;
        return el;
    }
    function refresh() {
        chips.hidden = messages.length > 0 || busy;
        reset.hidden = messages.length === 0 || busy;
        send.disabled = busy;
        try { sessionStorage.setItem(STORE, JSON.stringify(messages.slice(-20))); } catch {}
    }
    function failure(code) {
        if (code === 'rate_minute') return label('Слишком много вопросов подряд. Подождите минуту и спросите снова.', 'Забагато запитань поспіль. Зачекайте хвилину й запитайте знову.', 'Too many questions in a row. Wait a minute and ask again.');
        if (code === 'rate_day' || code === 'quota') return label('Лимит вопросов на сегодня исчерпан. Воспользуйтесь содержанием и поиском по разделам.', 'Ліміт запитань на сьогодні вичерпано. Скористайтеся змістом і пошуком за розділами.', 'The question limit for today is used up. Please use the contents and the section search.');
        if (code === 'too_long') return label('Вопрос слишком длинный. Сократите его, пожалуйста.', 'Запитання задовге. Скоротіть його, будь ласка.', 'The question is too long. Please shorten it.');
        if (code === 'busy') return label('Модели сейчас перегружены. Попробуйте ещё раз через минуту.', 'Моделі зараз перевантажені. Спробуйте ще раз за хвилину.', 'The models are busy right now. Try again in a minute.');
        return label('Помощник сейчас недоступен. Попробуйте позже или воспользуйтесь поиском по разделам.', 'Помічник зараз недоступний. Спробуйте пізніше або скористайтеся пошуком за розділами.', 'The assistant is unavailable right now. Try later or use the section search.');
    }

    async function readStream(res, onText) {
        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '', text = '';
        for (;;) {
            const {done, value} = await reader.read();
            if (done) break;
            buffer += decoder.decode(value, {stream: true});
            const lines = buffer.split('\n');
            buffer = lines.pop();
            for (const line of lines) {
                if (!line.startsWith('data:')) continue;   // comments keep the connection alive
                const data = line.slice(5).trim();
                if (!data || data === '[DONE]') continue;
                let chunk;
                try { chunk = JSON.parse(data); } catch { continue; }
                if (chunk.error) throw new Error('unavailable');
                const piece = chunk.choices?.[0]?.delta?.content;
                if (piece) { text += piece; onText(text); }
            }
        }
        return text;
    }

    async function ask(question) {
        question = question.trim();
        if (!question || busy) return;
        busy = true;
        messages.push({role: 'user', content: question});
        bubble('user', question);
        input.value = '';
        grow();
        refresh();
        const answer = bubble('assistant', '');
        answer.classList.add('dc-wait');
        answer.innerHTML = '<span class="dc-dots" aria-hidden="true"><i></i><i></i><i></i></span>';
        log.scrollTop = log.scrollHeight;
        track('docs_chat_question', {chat_language: lang(), chat_turn: messages.filter(m => m.role === 'user').length});
        try {
            const res = await fetch(API, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({lang: lang(), messages: messages.slice(-HISTORY)}),
            });
            if (!res.ok) throw new Error((await res.json().catch(() => ({}))).error || 'unavailable');
            let frame = 0, latest = '';
            const text = await readStream(res, value => {
                latest = value;
                if (frame) return;
                frame = requestAnimationFrame(() => {
                    frame = 0;
                    const pinned = log.scrollHeight - log.scrollTop - log.clientHeight < 60;   // do not pull a reader who scrolled up
                    answer.classList.remove('dc-wait');
                    answer.innerHTML = markdown(latest);
                    if (pinned) log.scrollTop = log.scrollHeight;
                });
            });
            cancelAnimationFrame(frame);
            if (!text.trim()) throw new Error('unavailable');
            answer.classList.remove('dc-wait');
            answer.innerHTML = markdown(text);
            messages.push({role: 'assistant', content: text});
        } catch (err) {
            messages.pop();   // the question got no answer: it must not stay in the history
            answer.classList.remove('dc-wait');
            answer.classList.add('dc-error');
            answer.textContent = failure(err.message);
            if (!input.value) { input.value = question; grow(); }
            track('docs_chat_error', {error_code: String(err.message).slice(0, 40)});
        }
        busy = false;
        refresh();
    }

    // ---------- window ----------
    function open() {
        panel.hidden = false;
        fab.hidden = true;
        fab.setAttribute('aria-expanded', 'true');
        log.scrollTop = log.scrollHeight;
        input.focus();
        track('docs_chat_open', {chat_language: lang()});
    }
    function close(focus = true) {
        panel.hidden = true;
        fab.hidden = false;
        fab.setAttribute('aria-expanded', 'false');
        if (focus) fab.focus();
    }
    function grow() {
        input.style.height = 'auto';
        input.style.height = Math.min(input.scrollHeight, 120) + 'px';
    }

    fab.addEventListener('click', open);
    document.getElementById('dc-close').addEventListener('click', () => close());
    panel.addEventListener('keydown', event => { if (event.key === 'Escape') { event.stopPropagation(); close(); } });
    form.addEventListener('submit', event => { event.preventDefault(); ask(input.value); });
    input.addEventListener('input', grow);
    input.addEventListener('keydown', event => {
        if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) { event.preventDefault(); ask(input.value); }
    });
    chips.addEventListener('click', event => {
        const chip = event.target.closest('button');
        if (chip) ask(chip.querySelector('.' + lang() + '-text').textContent);
    });
    reset.addEventListener('click', () => {
        messages = [];
        log.querySelectorAll('.dc-msg:not(.dc-hello)').forEach(el => el.remove());
        refresh();
        input.focus();
    });
    // A link to a section: on a phone the chat covers the page, so it steps aside; the section lights up for a moment.
    log.addEventListener('click', event => {
        const ref = event.target.closest('a.dc-ref');
        if (!ref) return;
        const target = document.getElementById(ref.hash.slice(1));
        if (phone.matches) close(false);
        if (!target) return;
        target.classList.remove('dc-flash');
        void target.offsetWidth;   // restarts the animation on a repeated click
        target.classList.add('dc-flash');
        track('docs_chat_section_click', {section_id: target.id});
    });

    try {
        const saved = JSON.parse(sessionStorage.getItem(STORE) || '[]');
        if (Array.isArray(saved)) messages = saved.filter(m => m && (m.role === 'user' || m.role === 'assistant') && typeof m.content === 'string');
    } catch {}
    while (messages.length && messages[messages.length - 1].role === 'user') messages.pop();   // the page was closed before the answer came
    messages.forEach(m => bubble(m.role, m.content));
    refresh();
    fab.hidden = false;
})();
