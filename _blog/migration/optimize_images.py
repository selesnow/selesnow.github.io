"""Оптимизация картинок блога: images_orig/ (оригиналы) → images/ (сжатые копии для сайта).

* растровые форматы → WebP; ширина ограничивается MAX_W (хватает колонке статьи и экранам с высокой плотностью);
* JPG — с потерями, quality=82;
* PNG: маленькие (схемы, иконки) — без потерь; крупные скриншоты без прозрачности — с потерями quality=90
  (в 3–4 раза легче, текст остаётся читаемым); если с потерями не выгоднее — остаётся lossless;
* GIF и SVG копируются как есть (анимация, вектор);
* пишет images.json с размерами {имя: [ширина, высота]} — по ним в вёрстке задаются width/height (без скачков страницы).

Запуск (после export.py):  python _blog_export/optimize_images.py [--force]
"""
import io
import json
import shutil
import struct
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image, ImageOps, ImageSequence

HERE = Path(__file__).resolve().parent
SRC, DST = HERE / 'images_orig', HERE / 'images'
MAX_W = 1600
JPG_Q, PNG_LOSSY_Q = 82, 90
PNG_LOSSY_FROM = 150_000          # байт: PNG тяжелее этого пробуем сжать с потерями
FORCE = '--force' in sys.argv


def open_image(path):
    """Открывает файл; у PNG с «нестандартными» текстовыми чанками (draw.io) вырезает метаданные и повторяет."""
    data = path.read_bytes()
    if data[:1] == b'<':
        raise ValueError('это HTML-заглушка, а не картинка')
    try:
        im = Image.open(io.BytesIO(data))
        im.load()
        return im
    except Exception:
        if data[:8] != b'\x89PNG\r\n\x1a\n':
            raise
        out, i = data[:8], 8
        while i < len(data):
            n, = struct.unpack('>I', data[i:i + 4])
            if data[i + 4:i + 8] not in (b'zTXt', b'tEXt', b'iTXt'):
                out += data[i:i + 12 + n]
            i += 12 + n
        im = Image.open(io.BytesIO(out))
        im.load()
        return im


def fit(im):
    if im.width > MAX_W:
        return im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    return im


def optimize(src):
    ext = src.suffix.lower()
    if ext in ('.svg', '.gif'):          # вектор и анимация копируем как есть (анимированный WebP из GIF оказался тяжелее)
        out = DST / src.name
        if FORCE or not out.exists() or out.stat().st_mtime < src.stat().st_mtime:
            shutil.copy2(src, out)
        dims = None
        if ext == '.gif':
            with Image.open(out) as g:
                dims = g.size
        return src.name, out.name, dims, src.stat().st_size, out.stat().st_size, False

    out = DST / (src.stem + '.webp')
    if out.exists() and not FORCE and out.stat().st_mtime >= src.stat().st_mtime:
        with Image.open(out) as done:
            return src.name, out.name, done.size, src.stat().st_size, out.stat().st_size, False

    im = open_image(src)
    resized = im.width > MAX_W
    im = fit(ImageOps.exif_transpose(im))
    has_alpha = im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info)
    im = im.convert('RGBA' if has_alpha else 'RGB')
    if ext in ('.jpg', '.jpeg'):
        im.save(out, 'WEBP', quality=JPG_Q, method=5)
    else:
        im.save(out, 'WEBP', lossless=True, method=4)
        if not has_alpha and out.stat().st_size > PNG_LOSSY_FROM:
            tmp = out.with_suffix('.tmp.webp')
            im.save(tmp, 'WEBP', quality=PNG_LOSSY_Q, method=5)
            if tmp.stat().st_size < out.stat().st_size * 0.7:
                tmp.replace(out)
            else:
                tmp.unlink()
    return src.name, out.name, im.size, src.stat().st_size, out.stat().st_size, resized


def safe(src):
    try:
        return optimize(src)
    except Exception as e:  # битый файл не должен останавливать всю пачку
        return src.name, None, None, src.stat().st_size, 0, str(e)


def main():
    DST.mkdir(exist_ok=True)
    files = sorted(p for p in SRC.iterdir() if p.is_file())
    with ThreadPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(safe, files))
    manifest, before, after, resized, errors = {}, 0, 0, 0, []
    by_ext = {}
    for name, out, dims, b, a, flag in results:
        if out is None:
            errors.append((name, flag))
            continue
        before += b
        after += a
        resized += bool(flag)
        e = Path(name).suffix.lower() or '(нет)'
        by_ext.setdefault(e, [0, 0, 0])
        by_ext[e][0] += 1
        by_ext[e][1] += b
        by_ext[e][2] += a
        if dims:
            manifest[out] = list(dims)
    for p in (DST / 'covers').glob('*.webp'):       # обложки уже готовые WebP 1200×630
        manifest[f'covers/{p.name}'] = [1200, 630]
    (HERE / 'images.json').write_text(json.dumps(manifest, ensure_ascii=False), encoding='utf-8')
    mb = lambda x: f'{x / 1e6:.1f} МБ'
    print(f'файлов: {len(files)}, уменьшено по ширине: {resized}')
    for e, (n, b, a) in sorted(by_ext.items(), key=lambda kv: -kv[1][1]):
        print(f'  {e:6} {n:4} шт  {mb(b):>9} → {mb(a):>9}')
    print(f'ИТОГО: {mb(before)} → {mb(after)}  (−{100 - after * 100 / max(before, 1):.0f}%)')
    for name, err in errors:
        print('  ! не обработан:', name[:70], '—', err[:80])


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
