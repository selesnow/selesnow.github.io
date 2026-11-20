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

    const toc = document.querySelector('.ad-toc');
    if (!toc) return;
    toc.classList.add('ad-js');

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
    links.forEach(a => a.addEventListener('click', () => { if (!wide.matches) setOpen(false); }));

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
            if (block.getBoundingClientRect().top <= 130) id = block.id; else if (block.classList.contains('ad-section')) break;
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
    }
    input.addEventListener('input', search);
    new MutationObserver(() => { if (input.value) search(); }).observe(document.body, {attributes: true, attributeFilter: ['class']});
})();
