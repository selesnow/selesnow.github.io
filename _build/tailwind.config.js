// Конфигурация сборки Tailwind CSS (запускается из корня репозитория, см. _build/build.py).
// Сканирует все страницы и скрипты, в том числе классы, которые JS добавляет динамически.
module.exports = {
  content: [
    './index.html',
    './404.html',
    './opensource/index.html',
    './courses/index.html',
    './videos/index.html',
    './talks/index.html',
    './articles/index.html',
    './interviews/index.html',
    './ads/index.html',
    './acpgram/index.html',
    './acpgram/acpgram.js',
    './r_for_marketing_course/**/*.html',
    './assets/rcourse.js',
    './assets/site.js',
    './_build/build.py',
    './_build/rcourse_page.py',
    './_build/blog.py',
    './blog/index.html',
  ],
  theme: { extend: {} },
  plugins: [],
};
