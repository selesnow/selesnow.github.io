// Страницы курса «Язык R для интернет-маркетинга»: плеер, части урока, тайм-коды, отметки «пройдено», поиск.
// Без JS всё работает как набор ссылок на YouTube и обычные страницы.
(function () {
    'use strict';

    var DONE_KEY = 'rc_done';
    var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function track(name, params) {
        if (typeof sendGAEvent === 'function') sendGAEvent(name, params || {});
    }

    // ---------------------------------------------------------------- пройденные уроки
    function getDone() {
        try { return new Set(JSON.parse(localStorage.getItem(DONE_KEY) || '[]')); } catch (e) { return new Set(); }
    }
    function saveDone(set) {
        try { localStorage.setItem(DONE_KEY, JSON.stringify(Array.from(set))); } catch (e) { /* приватный режим */ }
    }
    function paintDone() {
        var done = getDone();
        document.querySelectorAll('[data-lesson]').forEach(function (el) {
            el.classList.toggle('is-done', done.has(el.dataset.lesson));
        });
        var progress = document.querySelector('[data-rc-progress]');
        if (progress) {
            var ids = Array.from(document.querySelectorAll('[data-rc-row]')).map(function (r) { return r.dataset.lesson; });
            var n = ids.filter(function (id) { return done.has(id); }).length;
            progress.hidden = n === 0;
            progress.textContent = 'Пройдено ' + n + ' из ' + ids.length + ' (отметки хранятся только в этом браузере)';
        }
        document.querySelectorAll('[data-rc-done]').forEach(function (btn) {
            var on = done.has(btn.dataset.rcDone);
            btn.hidden = false;
            btn.setAttribute('aria-pressed', on ? 'true' : 'false');
            btn.querySelector('span').textContent = on ? 'Урок пройден' : 'Отметить пройденным';
            btn.querySelector('i').className = on ? 'fa-solid fa-circle-check' : 'fa-regular fa-circle-check';
        });
    }
    document.querySelectorAll('[data-rc-done]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var done = getDone();
            var id = btn.dataset.rcDone;
            if (done.has(id)) done.delete(id); else done.add(id);
            saveDone(done);
            paintDone();
        });
    });
    paintDone();

    // ---------------------------------------------------------------- плеер
    function embedUrl(id, start) {
        var u = 'https://www.youtube.com/embed/' + encodeURIComponent(id) + '?autoplay=1&rel=0&modestbranding=1';
        if (start) u += '&start=' + Math.floor(start);
        return u;
    }

    function posterHtml(id, title) {
        return '<a href="https://www.youtube.com/watch?v=' + id + '" target="_blank" rel="noopener" class="rc-poster" data-rc-poster="' + id + '" aria-label="Смотреть видео: ' + title.replace(/"/g, '&quot;') + '">' +
            '<img src="https://i.ytimg.com/vi/' + id + '/hqdefault.jpg" alt="" width="480" height="360" decoding="async">' +
            '<span class="rc-play" aria-hidden="true"><i class="fa-solid fa-play"></i></span></a>';
    }

    function play(frame, id, start, title) {
        if (location.protocol === 'file:') { window.open('https://www.youtube.com/watch?v=' + id, '_blank'); return; }
        var iframe = document.createElement('iframe');
        iframe.src = embedUrl(id, start);
        iframe.title = title || 'Видео курса';
        iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
        iframe.allowFullscreen = true;
        iframe.referrerPolicy = 'strict-origin-when-cross-origin';
        frame.replaceChildren(iframe);
        frame.dataset.video = id;
        track('video_open', { video_id: id, video_title: title || '', section: 'r_for_marketing_course' });
    }

    function bindPoster(a) {
        a.addEventListener('click', function (e) {
            e.preventDefault();
            var frame = a.closest('.rc-frame');
            play(frame, a.dataset.rcPoster, 0, a.getAttribute('aria-label').replace('Смотреть видео: ', ''));
        });
    }
    document.querySelectorAll('[data-rc-poster]').forEach(bindPoster);

    var player = document.querySelector('[data-rc-player]');
    var parts = Array.from(document.querySelectorAll('[data-rc-part]'));
    var tcBlocks = Array.from(document.querySelectorAll('[data-rc-tc]'));

    function activate(id) {
        parts.forEach(function (p) {
            var on = p.dataset.rcPart === id;
            p.classList.toggle('is-active', on);
            if (on) p.setAttribute('aria-current', 'true'); else p.removeAttribute('aria-current');
        });
        tcBlocks.forEach(function (b) { b.hidden = b.dataset.rcTc !== id; });
    }

    function select(id, autoplay, start) {
        var part = parts.filter(function (p) { return p.dataset.rcPart === id; })[0];
        var title = part ? part.dataset.title : (player.querySelector('[aria-label]') || {}).title || '';
        activate(id);
        if (autoplay) {
            play(player, id, start, title);
        } else {
            player.innerHTML = posterHtml(id, title);
            player.dataset.video = id;
            bindPoster(player.querySelector('[data-rc-poster]'));
        }
        try { history.replaceState(null, '', '#v=' + id); } catch (e) { /* file:// */ }
    }

    if (player) {
        parts.forEach(function (p) {
            p.addEventListener('click', function (e) {
                e.preventDefault();
                select(p.dataset.rcPart, true, 0);
                if (!inView(player)) player.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'center' });
            });
        });
        document.querySelectorAll('[data-rc-seek]').forEach(function (b) {
            b.addEventListener('click', function () {
                select(b.dataset.video, true, Number(b.dataset.rcSeek));
                if (!inView(player)) player.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'center' });
            });
        });
        var m = /^#v=([\w-]{6,})$/.exec(location.hash);
        if (m && parts.some(function (p) { return p.dataset.rcPart === m[1]; })) select(m[1], false, 0);
    }

    function inView(el) {
        var r = el.getBoundingClientRect();
        return r.top >= 70 && r.bottom <= window.innerHeight;
    }

    // ---------------------------------------------------------------- поиск по урокам (главная курса)
    var search = document.querySelector('[data-rc-search]');
    if (search) {
        var rows = Array.from(document.querySelectorAll('[data-rc-row]'));
        var modules = Array.from(document.querySelectorAll('[data-rc-module]'));
        var empty = document.querySelector('[data-rc-empty]');
        var norm = function (s) { return s.toLowerCase().replace(/ё/g, 'е'); };
        search.addEventListener('input', function () {
            var tokens = norm(search.value).split(/\s+/).filter(Boolean);
            rows.forEach(function (r) {
                var text = norm(r.dataset.text);
                r.parentElement.hidden = !tokens.every(function (t) { return text.indexOf(t) !== -1; });
            });
            var any = false;
            modules.forEach(function (mod) {
                var visible = Array.from(mod.querySelectorAll('[data-rc-list] > li')).some(function (li) { return !li.hidden; });
                mod.style.display = visible ? '' : 'none';
                any = any || !!visible;
            });
            if (empty) empty.hidden = any;
        });
    }
})();
