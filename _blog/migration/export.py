"""Выгрузка постов alexeyseleznev.wordpress.com в Markdown (папка не в git)."""
import html, json, re, sys, time, urllib.parse, urllib.request, pathlib
import yaml
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import tagmap
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

SITE = "alexeyseleznev.wordpress.com"
API = f"https://public-api.wordpress.com/rest/v1.1/sites/{SITE}/posts"
OUT = pathlib.Path(__file__).parent
POSTS, IMGS, RAW = OUT / "posts", OUT / "images_orig", OUT / "raw"   # оригиналы; сжатые копии делает optimize_images.py → images/
for d in (POSTS, IMGS, RAW):
    d.mkdir(exist_ok=True)

MISSING = []
KNOWN_DEAD = set()
_f = pathlib.Path(__file__).parent / 'raw' / 'missing_images.txt'
if _f.exists() and '--retry-images' not in sys.argv:
    KNOWN_DEAD = set(_f.read_text(encoding='utf-8').split())
UA = {"User-Agent": "Mozilla/5.0 blog-export"}


def get(url, binary=False):
    for i in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                data = r.read()
                return data if binary else json.loads(data)
        except Exception as e:
            err = e
            time.sleep(2)
    raise err


def fetch_all():
    posts, page = [], 1
    while True:
        q = urllib.parse.urlencode({"number": 100, "page": page, "type": "post", "status": "publish,draft,private"})
        d = get(f"{API}?{q}")
        posts += d["posts"]
        if len(d["posts"]) < 100:
            return posts
        page += 1


class MD(MarkdownConverter):
    def convert_pre(self, el, text, parent_tags=None, **kw):
        code = el.get_text()
        lang = ""
        for c in [el] + list(el.find_all(True)):
            for cls in c.get("class", []):
                m = re.match(r"(?:language-|lang-|brush:\s*)(\w+)", cls)
                if m:
                    lang = m.group(1)
        return f"\n\n```{lang}\n{code.rstrip()}\n```\n\n"


def slugify(s):
    s = urllib.parse.unquote(s)
    return re.sub(r"[^\w\-]+", "-", s, flags=re.U).strip("-").lower()[:80] or "post"


def final_name(name):
    """Имя файла после оптимизации: растровые форматы → .webp, SVG и GIF (анимация) остаются как есть."""
    p = pathlib.PurePosixPath(name)
    return name if p.suffix.lower() in (".svg", ".gif") else p.stem + ".webp"


def local_image(url, slug):
    clean = url.split("?")[0]
    name = f"{slug}-{pathlib.PurePosixPath(urllib.parse.urlparse(clean).path).name}"
    name = re.sub(r"[^\w.\-]+", "_", urllib.parse.unquote(name))
    path = IMGS / name
    if path.exists() and path.read_bytes()[:1] == b"<":     # сервер отдал HTML-заглушку вместо картинки
        MISSING.append(url)
        return url
    if not path.exists() and url in KNOWN_DEAD:
        MISSING.append(url)
        return url
    if not path.exists():
        try:
            path.write_bytes(get(clean, binary=True))
        except Exception as e:
            print("  ! image failed", url, e)
            MISSING.append(url)
            return url
    return f"../images/{final_name(name)}"


def fix_glue(md):
    """Чинит слипшиеся фрагменты: «R.Я» → «R. Я», картинка вплотную к тексту → отдельный абзац (код не трогаем)."""
    parts = re.split(r"(```.*?```)", md, flags=re.S)
    for i in range(0, len(parts), 2):
        t = parts[i]
        keep = []

        def stash(m):
            keep.append(m.group(0))
            return f"\x00{len(keep) - 1}\x00"
        t = re.sub(r"`[^`\n]*`|\S*://\S*|\]\([^)]*\)", stash, t)
        t = re.sub(r"(?<=[\w)»”])([.!?])(?=[А-ЯЁ])", r"\1 ", t)
        t = re.sub(r"\x00(\d+)\x00", lambda m: keep[int(m.group(1))], t)
        t = re.sub(r"(!\[[^\]]*\]\([^)\s]+(?:\s+\"[^\"]*\")?\))(?=[^\s)\]])", r"\1\n\n", t)
        t = re.sub(r"(?<=[^\s\[!])(!\[[^\]]*\]\()", r"\n\n\1", t)
        parts[i] = t
    return "".join(parts)


SLIDESHARE_PAGE = re.compile(r"slideshare\.net/(?!slideshow/embed_code)[\w.-]+/[\w%.-]+")
_SS_CACHE = pathlib.Path(__file__).parent / "raw" / "slideshare.json"


def slideshare_embed(page_url):
    """Страница презентации → адрес для встраивания через oEmbed SlideShare (результат кэшируется в raw/slideshare.json)."""
    cache = json.loads(_SS_CACHE.read_text(encoding="utf-8")) if _SS_CACHE.exists() else {}
    if page_url not in cache:
        api = "https://www.slideshare.net/api/oembed/2?format=json&url=" + urllib.parse.quote(page_url, safe="")
        try:
            html_ = get(api)["html"]
            m = re.search(r'src="([^"]+)"', html_)
            cache[page_url] = m.group(1) if m else None
        except Exception as e:
            print("  ! slideshare oembed failed", page_url, e)
            cache[page_url] = None
        _SS_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")
    return cache[page_url]


def convert(p):
    slug = slugify(p["slug"])
    soup = BeautifulSoup(p["content"], "html.parser")
    for t in soup.select("script, style, .sharedaddy, .jp-relatedposts"):
        t.decompose()
    # ссылки на страницы SlideShare (oEmbed в WordPress отдаёт просто ссылку) → токен встраивания
    for a in soup.find_all("a", href=SLIDESHARE_PAGE):
        box = a.find_parent("figure") or a.parent
        if box is None or box.get_text(strip=True) != a.get_text(strip=True):
            continue                      # ссылка внутри текста — оставляем ссылкой
        src = slideshare_embed(a["href"])
        if src:
            tok = soup.new_tag("p")
            tok.string = f"{{{{video: {src}}}}}"
            box.replace_with(tok)
    for fr in soup.find_all("iframe"):
        src = fr.get("src") or fr.get("data-src") or ""
        tok = soup.new_tag("p")
        tok.string = f"{{{{video: {src}}}}}" if src else ""
        (fr.find_parent("figure") or fr).replace_with(tok)
    for img in soup.find_all("img"):
        src = img.get("data-orig-file") or img.get("src")
        if src:
            img["src"] = local_image(src, slug)
        for a in ("srcset", "data-orig-file", "data-large-file", "data-medium-file"):
            img.attrs.pop(a, None)
    for a in soup.find_all("a"):  # ссылки-обёртки на оригинал картинки
        href = a.get("href", "")
        if a.find("img") and re.search(r"\.(png|jpe?g|gif|webp)(\?|$)", href, re.I):
            a.unwrap()
    body = MD(heading_style="ATX", bullets="-").convert_soup(soup)
    body = fix_glue(body)
    body = re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"
    desc = BeautifulSoup(p.get("excerpt", ""), "html.parser").get_text().strip()
    title = html.unescape(p["title"]).strip()   # WordPress отдаёт заголовки с HTML-кодами (&#8211; → –)
    tags, cats, is_ai = tagmap.unify(title, desc, list((p.get("tags") or {}).keys()),
                                     list((p.get("categories") or {}).keys()), body)
    head = {
        "title": title,
        "date": p["date"][:10],
        "slug": slug,
        "tags": tags,
        "categories": cats,
        "description": desc,
        "original_url": p["URL"],
        "wp_id": p["ID"],
        "draft": p["status"] != "publish",
    }
    fi = p.get("featured_image")
    if fi:
        head["cover"] = local_image(fi, slug)
    fm = yaml.safe_dump(head, allow_unicode=True, sort_keys=False, width=1000)
    return slug, f"---\n{fm}---\n\n{body}"


def main():
    if "--offline" in sys.argv:
        posts = json.loads((RAW / "all.json").read_text(encoding="utf-8"))
    else:
        posts = fetch_all()
        (RAW / "all.json").write_text(json.dumps(posts, ensure_ascii=False), encoding="utf-8")
    print("posts:", len(posts))
    for old in POSTS.glob("*.md"):
        old.unlink()
    for i, p in enumerate(posts, 1):
        slug, text = convert(p)
        (POSTS / f"{p['date'][:10]}-{slug}.md").write_text(text, encoding="utf-8")
        print(f"{i}/{len(posts)}", p["date"][:10], p["title"][:60])
    (RAW / "missing_images.txt").write_text("\n".join(sorted(set(MISSING))), encoding="utf-8")
    print("missing images:", len(set(MISSING)))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
