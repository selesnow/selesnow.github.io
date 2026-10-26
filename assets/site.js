// Общий скрипт внутренних страниц: язык, меню, свечение карточек, фильтры, видео-плеер, фон.

// --- ДИНАМИЧЕСКИЙ ЭФФЕКТ СВЕЧЕНИЯ ДЛЯ BENTO CARDS ---
document.querySelectorAll('.bento-glass').forEach(card => {
    card.addEventListener('mousemove', e => {
        const rect = card.getBoundingClientRect();
        card.style.setProperty('--mouse-x', `${e.clientX - rect.left}px`);
        card.style.setProperty('--mouse-y', `${e.clientY - rect.top}px`);
    });
});

// --- ЯЗЫК (общий с лендингом через localStorage) ---
// При первом визите язык берётся из настроек браузера (uk → UA, ru → RU), иначе английский.
// Явный выбор кнопкой EN/RU/UA запоминается и дальше имеет приоритет.
function detectLang() {
    const langs = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || 'en'];
    for (const l of langs) {
        const code = (l || '').toLowerCase().split('-')[0];
        if (code === 'uk') return 'ua';
        if (code === 'ru') return 'ru';
        if (code === 'en') return 'en';
    }
    return 'en';
}

function currentLang() {
    return ['ru', 'ua', 'en'].find(l => document.body.classList.contains('lang-' + l)) || 'en';
}

function changeLang(lang, remember = true) {
    document.body.classList.remove('lang-ru', 'lang-en', 'lang-ua');
    // Принудительный reflow для обнуления CSS анимаций
    void document.body.offsetWidth;
    document.body.classList.add('lang-' + lang);
    document.documentElement.lang = lang === 'ua' ? 'uk' : lang;

    ['en', 'ru', 'ua'].forEach(l => {
        const btn = document.getElementById('btn-' + l);
        if (!btn) return;
        btn.classList.toggle('active', l === lang);
        btn.classList.toggle('text-slate-500', l !== lang);
    });

    // Переводимые атрибуты (placeholder, aria-label)
    document.querySelectorAll('[data-ph-' + lang + ']').forEach(el => {
        el.setAttribute('placeholder', el.getAttribute('data-ph-' + lang));
    });

    if (remember) localStorage.setItem('preferredLang', lang);
    setTimeout(() => { if (typeof AOS !== 'undefined') AOS.refresh(); }, 50);
}

window.addEventListener('DOMContentLoaded', () => {
    const savedLang = localStorage.getItem('preferredLang');
    changeLang(savedLang || detectLang(), Boolean(savedLang));
});

// --- ANIMATION ON SCROLL ---
if (typeof AOS !== 'undefined') {
    AOS.init({ duration: 900, once: true, offset: 20, easing: 'ease-out-cubic' });
    window.addEventListener('load', () => setTimeout(() => AOS.refresh(), 100));
}

// --- МОБИЛЬНОЕ МЕНЮ ---
(function () {
    const btn = document.getElementById('mobile-menu-btn');
    const menu = document.getElementById('mobile-menu');
    const icon = document.getElementById('mobile-menu-icon');
    if (!btn || !menu) return;

    function toggle(open) {
        const isOpen = open !== undefined ? open : menu.classList.contains('hidden');
        menu.classList.toggle('hidden', !isOpen);
        icon.classList.toggle('fa-bars', !isOpen);
        icon.classList.toggle('fa-xmark', isOpen);
        btn.classList.toggle('bg-purple-500/20', isOpen);
        btn.classList.toggle('border-purple-500/40', isOpen);
        btn.classList.toggle('text-white', isOpen);
        document.body.classList.toggle('overflow-hidden', isOpen);
    }

    btn.addEventListener('click', e => { e.stopPropagation(); toggle(); });
    menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => toggle(false)));
    document.addEventListener('click', e => {
        if (!menu.contains(e.target) && !btn.contains(e.target)) toggle(false);
    });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') toggle(false); });
    window.addEventListener('resize', () => { if (window.innerWidth >= 1280) toggle(false); });
})();

// --- ФИЛЬТРЫ И ПОИСК ---
// Кнопки: [data-filter-group][data-filter-value]; элементы: [data-filter-item] с data-<group>="a b c";
// поиск: [data-filter-search] по data-search; группы по годам: [data-year-group].
(function () {
    const items = Array.from(document.querySelectorAll('[data-filter-item]'));
    if (!items.length) return;

    const state = {};
    const search = document.querySelector('[data-filter-search]');
    const counter = document.querySelector('[data-filter-count]');
    const empty = document.querySelector('[data-filter-empty]');

    function apply() {
        const q = search ? search.value.trim().toLowerCase() : '';
        let visible = 0;
        items.forEach(item => {
            let ok = Object.entries(state).every(([group, value]) =>
                value === 'all' || (item.dataset[group] || '').split(' ').includes(value));
            if (ok && q) ok = (item.dataset.search || '').includes(q);
            item.classList.toggle('is-hidden', !ok);
            if (ok) visible++;
        });
        document.querySelectorAll('[data-year-group]').forEach(g => {
            g.classList.toggle('is-hidden', !g.querySelector('[data-filter-item]:not(.is-hidden)'));
        });
        if (counter) counter.textContent = visible;
        if (empty) empty.classList.toggle('hidden', visible !== 0);
        if (typeof AOS !== 'undefined') AOS.refresh();
    }

    document.querySelectorAll('[data-filter-group]').forEach(btn => {
        const group = btn.dataset.filterGroup;
        if (btn.classList.contains('active')) state[group] = btn.dataset.filterValue;
        btn.addEventListener('click', () => {
            document.querySelectorAll(`[data-filter-group="${group}"]`).forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            state[group] = btn.dataset.filterValue;
            apply();
        });
    });

    if (search) search.addEventListener('input', apply);
    apply();
})();

// --- ВИДЕО-ПЛЕЕР (CINEMA LIGHTBOX) ---
function openVideoModal(videoId, title) {
    const modal = document.getElementById('videoModal');
    const content = document.getElementById('videoModalContent');
    const iframe = document.getElementById('videoModalIframe');
    const titleEl = document.getElementById('videoModalTitle');
    if (!modal || !iframe) return;

    if (window.location.protocol === 'file:') {
        window.open('https://www.youtube.com/watch?v=' + videoId.split('?')[0], '_blank');
        return;
    }

    if (titleEl) titleEl.textContent = title || '';
    const separator = videoId.includes('?') ? '&' : '?';
    iframe.src = `https://www.youtube.com/embed/${videoId}${separator}autoplay=1&rel=0`;

    modal.classList.remove('hidden');
    modal.classList.add('flex');
    document.body.style.overflow = 'hidden';
    setTimeout(() => {
        modal.classList.replace('opacity-0', 'opacity-100');
        if (content) content.classList.replace('scale-95', 'scale-100');
    }, 10);
}

function closeVideoModal() {
    const modal = document.getElementById('videoModal');
    const content = document.getElementById('videoModalContent');
    const iframe = document.getElementById('videoModalIframe');
    if (!modal || !iframe || modal.classList.contains('hidden')) return;

    modal.classList.replace('opacity-100', 'opacity-0');
    if (content) content.classList.replace('scale-100', 'scale-95');
    setTimeout(() => {
        iframe.src = '';
        modal.classList.remove('flex');
        modal.classList.add('hidden');
        document.body.style.overflow = '';
    }, 250);
}

document.querySelectorAll('[data-video]').forEach(el => {
    el.addEventListener('click', e => {
        e.preventDefault();
        const lang = currentLang();
        const t = el.querySelector(`[data-video-title] .${lang}-text`);
        openVideoModal(el.dataset.video, t ? t.textContent.trim() : '');
    });
});

document.addEventListener('keydown', e => { if (e.key === 'Escape') closeVideoModal(); });

// --- VANTA.JS ИНТЕРАКТИВНЫЙ ФОН (как на лендинге) ---
window.addEventListener('DOMContentLoaded', () => {
    if (typeof VANTA === 'undefined') return;
    VANTA.NET({
        el: '#vanta-bg',
        mouseControls: true,
        touchControls: true,
        gyroControls: false,
        minHeight: 200.00,
        minWidth: 200.00,
        scale: 1.00,
        scaleMobile: 1.00,
        color: 0x6366f1,
        backgroundColor: 0x020617,
        points: 9.00,
        maxDistance: 19.00,
        spacing: 18.00,
        showDots: true
    });
});
