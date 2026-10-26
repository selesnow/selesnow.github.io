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
    './assets/site.js',
    './_build/build.py',
  ],
  theme: { extend: {} },
  plugins: [],
};
