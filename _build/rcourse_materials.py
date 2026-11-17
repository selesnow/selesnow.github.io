"""Материалы курса «Язык R для интернет-маркетинга»: ZIP-архивы по урокам.

Скачивает репозиторий https://github.com/selesnow/r_for_marketing, для каждой папки урока собирает
r_for_marketing_course/materials/<номер>.zip и описывает состав в _build/data/rcourse_materials.json
(его читает rcourse_page.py). Запуск из корня репозитория:  python _build/rcourse_materials.py

В архивы не попадает служебный мусор (.DS_Store, desktop.ini, ~$*, бинарники SQLite, _httr-oauth),
а токены, секреты и пароли в R-скриптах заменяются заглушками.
"""
import io
import json
import re
import tempfile
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'r_for_marketing_course' / 'materials'
MANIFEST = Path(__file__).resolve().parent / 'data' / 'rcourse_materials.json'
ZIP_URL = 'https://codeload.github.com/selesnow/r_for_marketing/zip/refs/heads/master'

SKIP_NAMES = {'.ds_store', 'desktop.ini', 'rplots.pdf', '_gitignore', '.gitignore', 'thumbs.db'}
SKIP_SUFFIXES = {'.exe', '.dll', '.def', '.gz'}

# значение в кавычках после token / secret / password / pwd / access_token ... заменяем заглушкой
SECRET = re.compile(
    r'''(?P<k>\b[\w.]*(?:token|secret|password|passwd|pwd)\b\s*(?:=|<-)\s*)(?P<q>["'])(?P<v>[^"'\r\n]{6,})(?P=q)''',
    re.I)


# PWD=значение; внутри строки подключения ODBC
CONN_PWD = re.compile(r'''(\b(?:pwd|password)=)[^;"'\s]+''', re.I)


def redact(text):
    text = CONN_PWD.sub(lambda m: f'{m.group(1)}<ВАШ_ЗНАЧЕНИЕ>', text)
    return SECRET.sub(lambda m: f'{m["k"]}{m["q"]}<ВАШ_ЗНАЧЕНИЕ>{m["q"]}', text)


def keep(rel):
    name = rel.name.lower()
    return not (name in SKIP_NAMES or name.startswith('~$') or rel.suffix.lower() in SKIP_SUFFIXES
                or name.startswith('_httr-oauth') or any(p.startswith('_httr') for p in rel.parts))


def slug(folder):
    return re.sub(r'[^0-9]+', '-', re.match(r'^[\d.\s-]+', folder).group(0)).strip('-')


def main():
    with tempfile.TemporaryDirectory() as tmp:
        data = urllib.request.urlopen(ZIP_URL, timeout=120).read()
        zf = zipfile.ZipFile(io.BytesIO(data))
        zf.extractall(tmp)
        repo = next(Path(tmp).iterdir())
        OUT.mkdir(parents=True, exist_ok=True)
        for old in OUT.glob('*.zip'):
            old.unlink()
        manifest = {}
        for module in sorted(repo.glob('[123]. *')):
            for folder in sorted(p for p in module.iterdir() if p.is_dir()):
                files = [f for f in sorted(folder.rglob('*')) if f.is_file()
                         and keep(f.relative_to(folder)) and f.stat().st_size > 0]
                if not files:
                    continue
                key = f'{module.name}/{folder.name}'
                zip_name = f'r-for-marketing-{slug(folder.name)}.zip'
                with zipfile.ZipFile(OUT / zip_name, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
                    for f in files:
                        rel = f.relative_to(folder)
                        raw = f.read_bytes()
                        if f.suffix.lower() in ('.r', '.rmd'):
                            raw = redact(raw.decode('utf-8', errors='replace')).encode('utf-8')
                        info = zipfile.ZipInfo(f'{folder.name}/{rel.as_posix()}', (2024, 1, 1, 0, 0, 0))
                        info.compress_type = zipfile.ZIP_DEFLATED
                        z.writestr(info, raw)
                manifest[key] = {
                    'zip': zip_name,
                    'size': (OUT / zip_name).stat().st_size,
                    'files': [{'name': f.relative_to(folder).as_posix(), 'size': f.stat().st_size,
                               'repo_path': f'{key}/{f.relative_to(folder).as_posix()}'} for f in files],
                }
                print(f'{zip_name}: {len(files)} файлов, {manifest[key]["size"]:,} байт')
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding='utf-8', newline='\n')
    print(f'{len(manifest)} архивов, манифест: {MANIFEST.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
