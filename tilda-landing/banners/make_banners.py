#!/usr/bin/env python3
"""Rich Telegram banners 1200x628. Run: python3 make_banners.py"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 628
OUT = Path(__file__).parent

def font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            pass
    return ImageFont.load_default()

def lerp(a, b, t):
    return int(a + (b - a) * t)

def gradient_bg(draw):
    for y in range(H):
        t = y / H
        draw.line([(0, y), (W, y)], fill=(lerp(20, 42, t), lerp(60, 110, t), lerp(210, 240, t)))
    # glow blobs
    for cx, cy, r, alpha in [(980, 120, 220, 40), (1050, 480, 180, 30), (700, 560, 140, 25)]:
        for i in range(r, 0, -2):
            a = int(alpha * (1 - i / r))
            draw.ellipse([cx - i, cy - i, cx + i, cy + i], fill=(255, 255, 255, a))

def draw_brand(draw, y=46):
    draw.rounded_rectangle([56, y, 96, y + 40], radius=10, fill=(255, 255, 255, 50))
    draw.rectangle([66, y + 10, 74, y + 30], fill=(255, 255, 255))
    draw.pieslice([74, y + 8, 90, y + 32], 270, 90, fill=(255, 255, 255))
    draw.text((108, y + 4), "iStockLink", fill=(255, 255, 255), font=font(30, True))

def text_block(draw, title_lines, subtitle):
    y = 130
    for line in title_lines:
        draw.text((56, y), line, fill=(255, 255, 255), font=font(54, True))
        y += 62
    draw.text((56, y + 10), subtitle, fill=(220, 230, 255), font=font(24))

def panel_base():
  img = Image.new("RGBA", (W, H))
  draw = ImageDraw.Draw(img, "RGBA")
  gradient_bg(draw)
  draw_brand(draw)
  return img, draw

def right_panel(draw, x, y, w, h):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=22, fill=(255, 255, 255, 245))
    draw.rounded_rectangle([x, y, x + w, y + 44], radius=22, fill=(28, 80, 222))
    draw.rectangle([x, y + 22, x + w, y + 44], fill=(28, 80, 222))
    for i, dx in enumerate([14, 26, 38]):
        draw.ellipse([x + dx, y + 16, x + dx + 10, y + 26], fill=(255, 255, 255, 120 if i else 255))

def banner01():
    img, draw = panel_base()
    text_block(draw, ["Все тендеры", "в одной воронке"], "Этапы · задачи · команда")
    px, py, pw, ph = 620, 90, 520, 460
    right_panel(draw, px, py, pw, ph)
    draw.text((px + 20, py + 12), "Воронка торгов", fill=(255, 255, 255), font=font(16, True))
    cols = ["Новые", "Анализ", "Подача", "Контракт"]
    cw = (pw - 60) // 4
    for i, col in enumerate(cols):
        cx = px + 20 + i * (cw + 8)
        cy = py + 60
        draw.rounded_rectangle([cx, cy, cx + cw, cy + 360], radius=12, fill=(244, 247, 255))
        draw.text((cx + cw // 2, cy + 14), col, fill=(100, 116, 139), font=font(12, True), anchor="mm")
        if i == 1:
            draw.rounded_rectangle([cx + 8, cy + 40, cx + cw - 8, cy + 100], radius=8, fill=(28, 80, 222))
            draw.text((cx + cw // 2, cy + 62), "Ремонт", fill=(255, 255, 255), font=font(11, True), anchor="mm")
            draw.text((cx + cw // 2, cy + 80), "1,1 млн", fill=(220, 230, 255), font=font(10), anchor="mm")
        elif i == 0:
            draw.rounded_rectangle([cx + 8, cy + 40, cx + cw - 8, cy + 88], radius=8, fill=(255, 255, 255))
            draw.text((cx + cw // 2, cy + 64), "Медтех", fill=(30, 41, 59), font=font(10, True), anchor="mm")
    img.convert("RGB").save(OUT / "telegram-banner-1-funnel.png", quality=92)
    print("1 ok")

def banner02():
    img, draw = panel_base()
    text_block(draw, ["Подключи", "свой Контур"], "Единая лента в iStockLink")
    px, py, pw, ph = 620, 90, 520, 460
    right_panel(draw, px, py, pw, ph)
    draw.text((px + 20, py + 12), "Источники → лента", fill=(255, 255, 255), font=font(16, True))
    chips = [("Контур", 80), ("Seldon", 210), ("iStockLink", 350)]
    for label, xoff in chips:
        x = px + xoff
        y = py + 120
        fill = (28, 80, 222) if label == "iStockLink" else (255, 255, 255)
        tc = (255, 255, 255) if label == "iStockLink" else (30, 41, 59)
        draw.rounded_rectangle([x, y, x + 130, y + 56], radius=14, fill=fill)
        draw.text((x + 65, y + 28), label, fill=tc, font=font(16, True), anchor="mm")
    for ax in [px + 200, px + 340, px + 480]:
        draw.text((ax, py + 138), "→", fill=(255, 255, 255), font=font(28, True), anchor="mm")
    draw.rounded_rectangle([px + 40, py + 240, px + pw - 40, py + 400], radius=14, fill=(248, 250, 255))
    for i, (t, m) in enumerate([("Медоборудование", "4,2 млн · Контур"), ("Ремонт офиса", "1,1 млн · Seldon")]):
        yy = py + 260 + i * 70
        draw.rounded_rectangle([px + 56, yy, px + pw - 56, yy + 52], radius=10, fill=(255, 255, 255))
        draw.text((px + 72, yy + 14), t, fill=(30, 41, 59), font=font(14, True))
        draw.text((px + 72, yy + 32), m, fill=(100, 116, 139), font=font(11))
    img.convert("RGB").save(OUT / "telegram-banner-2-aggregator.png", quality=92)
    print("2 ok")

def banner03():
    img, draw = panel_base()
    text_block(draw, ["От тендера", "до контракта"], "Закупки · воронка · поставщики · КП")
    px, py, pw, ph = 620, 90, 520, 460
    right_panel(draw, px, py, pw, ph)
    draw.text((px + 20, py + 12), "Полный цикл", fill=(255, 255, 255), font=font(16, True))
    steps = ["Закупки", "Воронка", "Поставщики", "КП"]
    for i, step in enumerate(steps):
        x = px + 40 + i * 118
        y = py + 200
        draw.rounded_rectangle([x, y, x + 100, y + 44], radius=22, fill=(255, 255, 255))
        draw.text((x + 50, y + 22), step, fill=(28, 80, 222), font=font(13, True), anchor="mm")
        if i < 3:
            draw.text((x + 108, y + 22), "→", fill=(255, 255, 255), font=font(20, True), anchor="mm")
    draw.rounded_rectangle([px + 40, py + 300, px + pw - 40, py + 400], radius=16, fill=(241, 245, 255))
    draw.text((px + pw // 2, py + 350), "Всё в одном окне iStockLink", fill=(28, 80, 222), font=font(20, True), anchor="mm")
    img.convert("RGB").save(OUT / "telegram-banner-3-full-cycle.png", quality=92)
    print("3 ok")

def banner04():
    img, draw = panel_base()
    text_block(draw, ["Госзакупки", "в iStockLink"], "44-ФЗ · 223-ФЗ · фильтры по регионам")
    px, py, pw, ph = 620, 90, 520, 460
    right_panel(draw, px, py, pw, ph)
    draw.text((px + 20, py + 12), "Реестр ЕИС", fill=(255, 255, 255), font=font(16, True))
    draw.rounded_rectangle([px + 40, py + 70, px + pw - 40, py + 130], radius=12, fill=(241, 245, 255))
    draw.text((px + 60, py + 100), "🏛  Госзакупки подключены", fill=(28, 80, 222), font=font(16, True), anchor="lm")
    for i, (t, m) in enumerate([
        ("Поставка медоборудования", "4,2 млн ₽ · 44-ФЗ · Москва"),
        ("Лицензии ПО", "890 тыс. ₽ · 223-ФЗ"),
        ("Ремонт школы", "2,1 млн ₽ · 44-ФЗ · СПб"),
    ]):
        yy = py + 160 + i * 88
        draw.rounded_rectangle([px + 40, yy, px + pw - 40, yy + 72], radius=12, fill=(255, 255, 255))
        draw.text((px + 60, yy + 18), t, fill=(30, 41, 59), font=font(14, True))
        draw.text((px + 60, yy + 42), m, fill=(100, 116, 139), font=font(12))
    img.convert("RGB").save(OUT / "telegram-banner-4-goszakupki.png", quality=92)
    print("4 ok")

def banner05():
    img, draw = panel_base()
    text_block(draw, ["Поставщики", "и оцифровка КП"], "Сравнивайте предложения за минуты")
    px, py, pw, ph = 620, 90, 520, 460
    right_panel(draw, px, py, pw, ph)
    draw.text((px + 20, py + 12), "КП по тендеру", fill=(255, 255, 255), font=font(16, True))
    draw.rounded_rectangle([px + 40, py + 70, px + pw - 40, py + 180], radius=14, fill=(255, 255, 255))
    draw.text((px + 60, py + 100), "КП_МедТех.pdf", fill=(30, 41, 59), font=font(15, True))
    draw.text((px + 60, py + 128), "3 890 000 ₽ · 45 дней · 47 позиций", fill=(100, 116, 139), font=font(12))
    draw.rounded_rectangle([px + pw - 150, py + 92, px + pw - 60, py + 124], radius=8, fill=(6, 214, 160, 60))
    draw.text((px + pw - 105, py + 108), "готово", fill=(5, 150, 105), font=font(12, True), anchor="mm")
    draw.rounded_rectangle([px + 40, py + 200, px + pw - 40, py + 310], radius=14, fill=(248, 250, 255))
    draw.text((px + 60, py + 230), "ПромКомплект.xlsx", fill=(30, 41, 59), font=font(15, True))
    draw.text((px + 60, py + 258), "обработка цен и сроков…", fill=(100, 116, 139), font=font(12))
    img.convert("RGB").save(OUT / "telegram-banner-5-postavshchiki.png", quality=92)
    print("5 ok")

def banner06():
    img, draw = panel_base()
    text_block(draw, ["14 дней", "бесплатно"], "Попробуйте iStockLink без карты")
    px, py, pw, ph = 620, 90, 520, 460
    right_panel(draw, px, py, pw, ph)
    draw.text((px + 20, py + 12), "Демо-доступ", fill=(255, 255, 255), font=font(16, True))
    cx, cy = px + pw // 2, py + 230
    draw.ellipse([cx - 110, cy - 110, cx + 110, cy + 110], outline=(28, 80, 222), width=4)
    draw.ellipse([cx - 90, cy - 90, cx + 90, cy + 90], fill=(241, 245, 255))
    draw.text((cx, cy - 12), "14", fill=(28, 80, 222), font=font(64, True), anchor="mm")
    draw.text((cx, cy + 36), "дней", fill=(100, 116, 139), font=font(20, True), anchor="mm")
    draw.rounded_rectangle([px + 120, py + 370, px + pw - 120, py + 420], radius=24, fill=(28, 80, 222))
    draw.text((px + pw // 2, py + 395), "Запросить демо", fill=(255, 255, 255), font=font(18, True), anchor="mm")
    img.convert("RGB").save(OUT / "telegram-banner-6-besplatno.png", quality=92)
    print("6 ok")

if __name__ == "__main__":
    banner01(); banner02(); banner03(); banner04(); banner05(); banner06()
