// AcpGram documentation: contents (collapse on phones, current section, search) and copy buttons.
(() => {
    const lang = () => ['ru', 'ua', 'en'].find(l => document.body.classList.contains('lang-' + l)) || 'en';
    const label = (ru, ua, en) => ({ru, ua, en})[lang()];

    // ---------- copy buttons ----------
    const status = document.getElementById('ap-status');
    let toastTimer;
    document.querySelectorAll('.ap-copy').forEach(button => button.addEventListener('click', async () => {
        const code = button.parentElement.querySelector('code');
        try {
            await navigator.clipboard.writeText(code.textContent);
            status.textContent = label('Скопировано', 'Скопійовано', 'Copied');
        } catch {
            const range = document.createRange();
            range.selectNodeContents(code);
            getSelection().removeAllRanges();
            getSelection().addRange(range);
            status.textContent = label('Команда выделена. Нажмите Ctrl+C или ⌘C.', 'Команду виділено. Натисніть Ctrl+C або ⌘C.', 'Command selected. Press Ctrl+C or ⌘C.');
        }
        clearTimeout(toastTimer);
        toastTimer = setTimeout(() => { status.textContent = ''; }, 4000);
    }));

    // ---------- full-size screenshot (a link to the file without JS) ----------
    const viewer = document.getElementById('ad-lightbox');
    if (viewer?.showModal) {
        const picture = viewer.querySelector('img');
        const caption = viewer.querySelector('.ad-lightbox-cap');
        document.querySelectorAll('.ad-zoom').forEach(link => link.addEventListener('click', event => {
            event.preventDefault();
            const small = link.querySelector('img');
            picture.src = link.href;
            picture.alt = small.alt;
            picture.width = small.naturalWidth || small.width;
            picture.height = small.naturalHeight || small.height;
            caption.textContent = small.alt;
            viewer.querySelector('.ad-lightbox-close').setAttribute('aria-label', label('Закрыть', 'Закрити', 'Close'));
            viewer.showModal();
        }));
        viewer.addEventListener('click', event => { if (event.target === viewer || event.target.closest('.ad-lightbox-close')) viewer.close(); });
    }

    const toc = document.querySelector('.ad-toc');
    if (!toc) return;
    toc.classList.add('ad-js');

    // ---------- the found word is highlighted in the text (CSS Custom Highlight API: no changes to the page itself) ----------
    const firstMatch = new Map();   // section id → the first match in it
    const count = toc.querySelector('.ad-toc-count');
    function highlight(query) {
        firstMatch.clear();
        if (!window.CSS?.highlights || typeof Highlight === 'undefined') return -1;
        CSS.highlights.delete('ad-find');
        if (query.length < 2) return 0;
        const ranges = [];
        const current = lang() + '-text';
        const roots = document.querySelectorAll('.ad-content .' + current + '.ad-lang, .ad-content h2 > .' + current + ', .ad-content h3 > .' + current);
        for (const root of roots) {
            const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
            for (let node; (node = walker.nextNode()) && ranges.length < 3000;) {
                const text = node.nodeValue.toLowerCase();
                for (let at = text.indexOf(query); at !== -1; at = text.indexOf(query, at + query.length)) {
                    const range = new Range();
                    range.setStart(node, at);
                    range.setEnd(node, at + query.length);
                    ranges.push(range);
                    const section = node.parentElement.closest('.ad-sub, .ad-section');
                    if (section && !firstMatch.has(section.id)) firstMatch.set(section.id, range);
                }
            }
        }
        if (ranges.length) CSS.highlights.set('ad-find', new Highlight(...ranges));
        return ranges.length;
    }

    // ---------- contents: collapsed on phones, always open on wide screens ----------
    const toggle = toc.querySelector('.ad-toc-toggle');
    const wide = matchMedia('(min-width:1024px)');
    const setOpen = open => {
        toc.classList.toggle('ad-collapsed', !open);
        toggle.setAttribute('aria-expanded', String(open));
    };
    setOpen(wide.matches);
    wide.addEventListener('change', event => setOpen(event.matches));
    toggle.addEventListener('click', () => setOpen(toc.classList.contains('ad-collapsed')));

    const links = [...toc.querySelectorAll('.ad-toc-nav a')];
    const linkById = new Map(links.map(a => [a.hash.slice(1), a]));
    links.forEach(a => a.addEventListener('click', event => {
        if (!wide.matches) setOpen(false);
        const match = firstMatch.get(a.hash.slice(1));
        if (!match) return;
        event.preventDefault();
        history.replaceState(null, '', a.hash);
        match.startContainer.parentElement.scrollIntoView({block: 'center', behavior: 'instant'});   // a long smooth scroll would overshoot the reader's patience
    }));

    // ---------- current section ----------
    const blocks = [...document.querySelectorAll('.ad-section, .ad-sub')];
    let current;
    function activate(id) {
        if (id === current) return;
        current = id;
        links.forEach(a => a.classList.remove('ad-active'));
        toc.querySelectorAll('.ad-open').forEach(li => li.classList.remove('ad-open'));
        const link = linkById.get(id);
        if (!link) return;
        link.classList.add('ad-active');
        const top = link.closest('.ad-toc-nav > ul > li');
        top.classList.add('ad-open');
        if (wide.matches && !toc.classList.contains('ad-searching')) reveal(link);
    }
    // Keeps the current link visible inside the sticky contents. Scrolls only the contents box:
    // scrollIntoView() would also move the page and shift the very section being read.
    function reveal(link) {
        const box = toc.getBoundingClientRect();
        const rect = link.getBoundingClientRect();
        if (rect.top < box.top + 8) toc.scrollTop -= box.top + 8 - rect.top;
        else if (rect.bottom > box.bottom - 8) toc.scrollTop += rect.bottom - box.bottom + 8;
    }
    let ticking = false;
    function spy() {
        ticking = false;
        let id = blocks[0]?.id;
        for (const block of blocks) {
            // on phones the contents bar sticks under the site header, so headings stop lower
            if (block.getBoundingClientRect().top <= (wide.matches ? 130 : 190)) id = block.id; else if (block.classList.contains('ad-section')) break;
        }
        activate(id);
    }
    addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(spy); } }, {passive: true});
    spy();

    // ---------- search: section titles and the text of the current language ----------
    const input = document.getElementById('ad-search');
    const empty = toc.querySelector('.ad-toc-empty');
    const cache = new Map();
    function textOf(id) {
        const key = lang() + ':' + id;
        if (!cache.has(key)) {
            const block = document.getElementById(id);
            const title = block.querySelector(':scope > h2, :scope > h3');
            const body = block.querySelector(':scope > .' + lang() + '-text');
            cache.set(key, ((title?.textContent || '') + ' ' + (body?.textContent || '')).toLowerCase());
        }
        return cache.get(key);
    }
    function search() {
        const query = input.value.trim().toLowerCase();
        toc.classList.toggle('ad-searching', Boolean(query));
        let found = 0;
        toc.querySelectorAll('.ad-toc-nav > ul > li').forEach(top => {
            const own = !query || textOf(top.querySelector(':scope > a').hash.slice(1)).includes(query);
            let any = own;
            top.querySelectorAll(':scope > ul > li').forEach(sub => {
                const match = !query || textOf(sub.querySelector('a').hash.slice(1)).includes(query);
                sub.hidden = !match;
                any = any || match;
            });
            top.hidden = !any;
            if (any) found++;
        });
        empty.hidden = found > 0;
        const matches = highlight(query);
        count.hidden = matches <= 0;
        if (matches > 0) count.textContent = label('Совпадений в тексте: ', 'Збігів у тексті: ', 'Matches in the text: ') + matches;
    }
    input.addEventListener('input', search);
    // «/» moves to the search from anywhere on the page, Esc clears it
    addEventListener('keydown', event => {
        const el = document.activeElement;
        const typing = el && (/^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName) || el.isContentEditable);
        if (event.key === '/' && !typing && !event.ctrlKey && !event.metaKey && !event.altKey) {
            event.preventDefault();
            if (!wide.matches) setOpen(true);
            input.focus();
        } else if (event.key === 'Escape' && el === input) {
            input.value = '';
            search();
            input.blur();
        }
    });
    new MutationObserver(() => { if (input.value) search(); }).observe(document.body, {attributes: true, attributeFilter: ['class']});
})();
