(() => {
    'use strict';
    const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
    const languages = {ru:'ru-RU',ua:'uk-UA',en:'en-US'};
    const label = (ru, ua, en) => ({ru,ua,en})[currentLang()] || en;
    let data = JSON.parse(document.getElementById('ap-stats-fallback').textContent);
    const pathValue = path => path.split('.').reduce((value,key) => value?.[key], data);
    const format = n => new Intl.NumberFormat(languages[currentLang()]).format(n);
    const statSeen = new WeakSet();
    let toastTimer;

    function localize() {
        const lang = currentLang();
        document.querySelectorAll('[data-alt-' + lang + ']').forEach(el => { el.alt = el.getAttribute('data-alt-' + lang); });
        document.querySelectorAll('.ap-copy').forEach(el => { el.setAttribute('aria-label', label('Копировать команду','Копіювати команду','Copy command')); });
        document.querySelector('.ap-video-facade')?.setAttribute('aria-label', label('Воспроизвести видео об AcpGram','Відтворити відео про AcpGram','Play AcpGram video'));
        document.querySelectorAll('#tab-agent-claude').forEach(el => el.parentElement.setAttribute('aria-label', label('Агент','Агент','Agent')));
        document.querySelectorAll('#tab-os-win').forEach(el => el.parentElement.setAttribute('aria-label', label('Операционная система','Операційна система','Operating system')));
        const iframe = document.querySelector('#ap-video iframe');
        if (iframe) iframe.title = label('AcpGram: установка, настройка и демонстрация','AcpGram: встановлення, налаштування та демонстрація','AcpGram: installation, setup and demo');
        document.querySelectorAll('[data-stat]').forEach(el => {
            const value = pathValue(el.dataset.stat);
            if (value !== null && value !== undefined) el.textContent = typeof value === 'number' ? format(value) : value;
        });
        const date = value => value ? new Date(value).toLocaleDateString(languages[lang], {year:'numeric',month:'short',day:'numeric',timeZone:'UTC'}) : '—';
        document.getElementById('ap-updated').textContent = label('Обновлено: ','Оновлено: ','Updated: ') + date(data.updated);
        const cloneDate = document.getElementById('ap-clones-updated');
        if (cloneDate) cloneDate.textContent = label('Клоны обновлены: ','Клони оновлено: ','Clone data updated: ') + date(data.sourcesUpdated?.clones);
    }
    new MutationObserver(localize).observe(document.body, {attributes:true, attributeFilter:['class']});
    localize();

    document.querySelectorAll('.ap-copy').forEach(button => button.addEventListener('click', async () => {
        const value = button.parentElement.querySelector('code').textContent;
        const status = document.getElementById('ap-status');
        try {
            await navigator.clipboard.writeText(value);
            status.textContent = label('Скопировано','Скопійовано','Copied');
            sendGAEvent('acpgram_copy', {section:button.closest('section')?.id});
        } catch {
            const selection = getSelection();
            const range = document.createRange();
            range.selectNodeContents(button.parentElement.querySelector('code'));
            selection.removeAllRanges(); selection.addRange(range);
            status.textContent = label('Команда выделена. Нажмите Ctrl+C или ⌘C.','Команду виділено. Натисніть Ctrl+C або ⌘C.','Command selected. Press Ctrl+C or ⌘C.');
        }
        clearTimeout(toastTimer);
        toastTimer = setTimeout(() => { status.textContent = ''; }, 4000);
    }));

    // A real inline player: the poster becomes an iframe in the same 9:16 frame.
    // No YouTube connection or iframe is created until the visitor presses play.
    document.querySelector('.ap-video-facade').addEventListener('click', () => {
        const iframe = document.createElement('iframe');
        iframe.src = 'https://www.youtube-nocookie.com/embed/3CIc8QJZpkk?autoplay=1&rel=0';
        iframe.title = label('AcpGram: установка, настройка и демонстрация','AcpGram: встановлення, налаштування та демонстрація','AcpGram: installation, setup and demo');
        iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
        iframe.allowFullscreen = true;
        iframe.referrerPolicy = 'strict-origin-when-cross-origin';
        document.getElementById('ap-video').replaceChildren(iframe);
        iframe.focus();
        sendGAEvent('acpgram_video_play', {video_id:'3CIc8QJZpkk'});
    });

    // Silent looping demo: loads and plays only while visible; stays a poster with reduced motion.
    const demo = document.querySelector('.ap-demo-video');
    if (demo && !reducedMotion.matches && 'IntersectionObserver' in window) {
        new IntersectionObserver(entries => entries.forEach(entry => {
            if (entry.isIntersecting) { demo.preload = 'auto'; demo.play().catch(() => {}); }
            else demo.pause();
        }), {threshold:.35}).observe(demo);
    }

    // Each .ap-tabset is an independent tab group (agent, OS).
    document.querySelectorAll('.ap-tabset').forEach(set => {
        const tabs = [...set.querySelectorAll('[role=tab]')];
        function selectTab(button) {
            tabs.forEach(tab => {
                const selected = tab === button;
                tab.setAttribute('aria-selected', String(selected));
                tab.tabIndex = selected ? 0 : -1;
                document.getElementById(tab.getAttribute('aria-controls')).hidden = !selected;
            });
        }
        tabs.forEach((button, index) => {
            button.addEventListener('click', () => selectTab(button));
            button.addEventListener('keydown', event => {
                const next = event.key === 'ArrowRight' ? (index+1)%tabs.length : event.key === 'ArrowLeft' ? (index+tabs.length-1)%tabs.length : event.key === 'Home' ? 0 : event.key === 'End' ? tabs.length-1 : null;
                if (next === null) return;
                event.preventDefault(); selectTab(tabs[next]); tabs[next].focus();
            });
        });
        // Preselect the visitor's OS in the OS group.
        const isWin = /Win/i.test(navigator.userAgentData?.platform || navigator.platform || '');
        const preferred = set.querySelector(isWin ? '#tab-os-win' : '#tab-os-unix');
        selectTab(preferred || tabs[0]);
        set.classList.add('ap-tabs-ready');
    });

    if ('IntersectionObserver' in window) {
        const reveal = new IntersectionObserver(entries => entries.forEach(entry => {
            if (!entry.isIntersecting) return;
            entry.target.classList.add('ap-visible');
            reveal.unobserve(entry.target);
        }), {threshold:.08});
        if (!reducedMotion.matches) document.querySelectorAll('.ap-reveal').forEach(el => {
            const siblings = [...el.parentElement.children];
            el.style.setProperty('--ap-delay', `${Math.min(siblings.indexOf(el)%4,3)*90}ms`);
            el.classList.add('ap-reveal-ready'); reveal.observe(el);
        });
        const counters = new IntersectionObserver(entries => entries.forEach(entry => {
            if (!entry.isIntersecting) return;
            const el = entry.target, value = pathValue(el.dataset.stat);
            if (typeof value !== 'number') return;
            counters.unobserve(el);
            if (statSeen.has(el) || reducedMotion.matches) return;
            statSeen.add(el);
            const start = performance.now();
            function frame(now) {
                const progress = Math.min(1,(now-start)/700);
                el.textContent = format(Math.round(value*(1-(1-progress)**3)));
                if (progress<1 && !reducedMotion.matches) requestAnimationFrame(frame);
                else el.textContent = format(value);
            }
            requestAnimationFrame(frame);
        }), {threshold:.4});
        document.querySelectorAll('.ap-stat [data-stat]').forEach(el => counters.observe(el));
    }
    if (location.protocol !== 'file:') fetch('../assets/acpgram-stats.json', {cache:'no-store'})
        .then(r => { if (!r.ok) throw new Error('snapshot unavailable'); return r.json(); })
        .then(snapshot => { data = snapshot; localize(); })
        .catch(() => { /* Keep the build-time snapshot visible. */ });
})();
