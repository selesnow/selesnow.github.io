"""Optimize the supplied pictures. Needs Pillow; logo PNG is rasterized from the supplied SVG."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / 'img/acpgram'


def font(size, bold=False):
    candidates = [Path('C:/Windows/Fonts') / ('arialbd.ttf' if bold else 'arial.ttf'),
                  Path('/usr/share/fonts/truetype/dejavu') / ('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')]
    return ImageFont.truetype(str(next(p for p in candidates if p.exists())), size)


logo = Image.open(DEST / 'acpgram-logo.png').convert('RGBA')
logo.save(DEST / 'acpgram-logo.webp', 'WEBP', lossless=True, method=6)
hero = Image.open(DEST / 'my_wallpaper.webp').convert('RGB')
hero.save(DEST / 'acpgram-hero.webp', 'WEBP', quality=83, method=6)
hero.save(DEST / 'acpgram-hero.jpg', 'JPEG', quality=85, optimize=True, progressive=True)

# Share image uses the real supplied photo and logo, without generated imagery.
og = Image.new('RGB', (1200, 630), '#030712')
photo = ImageOps.fit(hero, (660, 630), centering=(.55,.5))
og.paste(photo, (540,0))
overlay = Image.new('RGBA', og.size)
pixels = overlay.load()
for x in range(1200):
    alpha = 255 if x < 510 else int(235 * max(0, 1-(x-510)/550))
    for y in range(630):
        pixels[x,y] = (3,7,18,alpha)
og = Image.alpha_composite(og.convert('RGBA'), overlay)
mark = logo.copy(); mark.thumbnail((92,74), Image.Resampling.LANCZOS)
og.alpha_composite(mark, (64,64))
d = ImageDraw.Draw(og)
d.text((64,177), 'AcpGram', font=font(78, True), fill='#f8fafc')
d.text((68,282), 'Your coding agents.', font=font(38, True), fill='#c4b5fd')
d.text((68,334), 'In your Telegram.', font=font(38, True), fill='#e2e8f0')
d.text((68,442), 'Claude Code · Codex', font=font(23), fill='#cbd5e1')
d.text((68,480), 'Gemini CLI · Antigravity CLI', font=font(23), fill='#cbd5e1')
d.text((68,568), 'alexey-seleznev.pro/acpgram', font=font(19), fill='#a78bfa')
og.convert('RGB').save(DEST / 'og-acpgram.jpg', 'JPEG', quality=88, optimize=True)
og.convert('RGB').save(DEST / 'og-acpgram.webp', 'WEBP', quality=85, method=6)

# Offline poster fallback. A YouTube thumbnail may replace this when available.
poster = Image.new('RGB', (480,854), '#0b1120')
poster.paste(ImageOps.fit(hero, (480,400)), (0,290))
draw = ImageDraw.Draw(poster)
mark = logo.copy(); mark.thumbnail((110,90))
poster.paste(mark, (185,55), mark)
draw.text((87,180), 'AcpGram', font=font(64,True), fill='#f8fafc')
draw.text((54,746), 'INSTALL · SETUP · DEMO', font=font(24,True), fill='#c4b5fd')
poster.save(DEST / 'video-poster.webp', 'WEBP', quality=85, method=6)
print('Prepared WebP, JPEG fallbacks, 1200x630 OG and video poster.')
