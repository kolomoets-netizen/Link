#!/usr/bin/env python3
"""Rich editable SVG banners (1200x628). Run: python3 generate_rich_banners.py"""
from pathlib import Path

OUT = Path(__file__).parent
LOGO = (
    '<g transform="translate(56,42) scale(1.4)">'
    '<path d="M10.9507 5.57031V13.6455H14.4852C13.6015 14.6783 12.3393 15.3982 10.9507 15.586V19.9678'
    'C12.7495 19.8113 14.4536 19.2166 15.9368 18.1838C17.3885 17.1822 18.5246 15.8051 19.282 14.2401'
    'C19.4082 13.9585 19.5344 13.6455 19.6607 13.3325C19.7238 13.176 19.7238 12.9882 19.7238 12.8317V5.57031H10.9507Z" fill="#fff"/>'
    '<path d="M9.278 0C6.75338 0.219092 4.4181 1.34585 2.68242 3.19249C0.946738 5.03914 0 7.44914 0 9.98433'
    'C0 12.5196 0.946738 14.9609 2.68242 16.8075C4.4181 18.6541 6.75338 19.7809 9.24648 20V0H9.278Z" fill="#fff"/>'
    '</g>'
    '<text x="108" y="62" fill="#fff" font-family="Arial,Helvetica,sans-serif" font-size="30" font-weight="700">iStockLink</text>'
)

DEFS = """
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1200" y2="628" gradientUnits="userSpaceOnUse">
    <stop offset="0%" stop-color="#153fb8"/>
    <stop offset="45%" stop-color="#1c50de"/>
    <stop offset="100%" stop-color="#4d7aef"/>
  </linearGradient>
  <linearGradient id="bgGlow" cx="75%" cy="20%" r="60%">
    <stop offset="0%" stop-color="#ffffff" stop-opacity="0.22"/>
    <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="panel" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#ffffff"/>
    <stop offset="100%" stop-color="#f4f7ff"/>
  </linearGradient>
  <linearGradient id="cardHi" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#2f63ea"/>
    <stop offset="100%" stop-color="#1c50de"/>
  </linearGradient>
  <filter id="shadow" x="-30%" y="-30%" width="160%" height="160%">
    <feDropShadow dx="0" dy="18" stdDeviation="22" flood-color="#0f172a" flood-opacity="0.22"/>
  </filter>
  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
    <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#1c50de" flood-opacity="0.18"/>
  </filter>
</defs>
"""

BG = """
<rect width="1200" height="628" fill="url(#bg)"/>
<circle cx="980" cy="80" r="280" fill="url(#bgGlow)"/>
<circle cx="1100" cy="520" r="200" fill="#ffffff" opacity="0.06"/>
<path d="M0,420 C200,520 380,360 620,430 C860,500 1000,300 1200,380 L1200,628 L0,628 Z" fill="#ffffff" opacity="0.05"/>
<path d="M0,120 C260,40 420,180 700,100 C920,40 1080,80 1200,40" fill="none" stroke="#ffffff" stroke-opacity="0.16" stroke-width="2.5"/>
<path d="M40,500 C220,420 360,560 560,500 C760,440 940,380 1160,460" fill="none" stroke="#ffffff" stroke-opacity="0.1" stroke-width="2"/>
"""

def panel(x, y, w, h, title):
    return f"""
<g filter="url(#shadow)">
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="26" fill="url(#panel)" stroke="#ffffff" stroke-opacity="0.65" stroke-width="1.5"/>
  <rect x="{x}" y="{y}" width="{w}" height="52" rx="26" fill="#1c50de"/>
  <rect x="{x}" y="{y+26}" width="{w}" height="26" fill="#1c50de"/>
  <circle cx="{x+28}" cy="{y+26}" r="6" fill="#ff6b6b"/>
  <circle cx="{x+48}" cy="{y+26}" r="6" fill="#ffd166"/>
  <circle cx="{x+68}" cy="{y+26}" r="6" fill="#06d6a0"/>
  <text x="{x+w/2}" y="{y+34}" text-anchor="middle" fill="#ffffff" font-family="Arial,Helvetica,sans-serif" font-size="16" font-weight="700">{title}</text>
</g>"""

def headline(lines, subtitle):
    y = 170
    parts = []
    for line in lines:
        parts.append(f'<text x="56" y="{y}" fill="#ffffff" font-family="Arial,Helvetica,sans-serif" font-size="58" font-weight="800">{line}</text>')
        y += 64
    parts.append(f'<text x="56" y="{y+12}" fill="#dbeafe" font-family="Arial,Helvetica,sans-serif" font-size="24">{subtitle}</text>')
    return "\n".join(parts)

def wrap(name, headline_html, visual_html):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 628" width="1200" height="628">
{DEFS}
<g id="background">{BG}</g>
<g id="brand">{LOGO}</g>
<g id="headline">{headline_html}</g>
<g id="visual">{visual_html}</g>
</svg>
'''

# --- Visuals ---

def visual_funnel():
    p = panel(580, 72, 560, 484, "Воронка торгов")
    cols = ["Новые", "Анализ", "Подача", "Контракт"]
    cards = [
        [("Медтехника", "4,2 млн"), ("Лицензии", "890 тыс.")],
        [("Ремонт", "1,1 млн", True)],
        [("3 КП", "сбор")],
        [("—", "")],
    ]
    body = [p]
    cw = 118
    for i, col in enumerate(cols):
        cx = 608 + i * (cw + 14)
        cy = 150
        body.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="360" rx="16" fill="#f8faff" stroke="#e2e8f0"/>')
        body.append(f'<text x="{cx+cw/2}" y="{cy+28}" text-anchor="middle" fill="#64748b" font-family="Arial" font-size="12" font-weight="700">{col}</text>')
        for j, card in enumerate(cards[i]):
            active = len(card) > 2 and card[2]
            yy = cy + 48 + j * 78
            fill = 'url(#cardHi)' if active else '#ffffff'
            tc = '#ffffff' if active else '#334155'
            mc = '#dbeafe' if active else '#94a3b8'
            body.append(f'<rect x="{cx+10}" y="{yy}" width="{cw-20}" height="64" rx="12" fill="{fill}" filter="url(#soft)"/>')
            body.append(f'<text x="{cx+cw/2}" y="{yy+28}" text-anchor="middle" fill="{tc}" font-family="Arial" font-size="12" font-weight="700">{card[0]}</text>')
            body.append(f'<text x="{cx+cw/2}" y="{yy+48}" text-anchor="middle" fill="{mc}" font-family="Arial" font-size="10">{card[1]}</text>')
    return "\n".join(body)

def visual_aggregator():
    p = panel(580, 72, 560, 484, "Источники → лента")
    body = [p]
    chips = [("Контур", 620, "#fff", "#1e293b"), ("Seldon", 770, "#fff", "#1e293b"), ("iStockLink", 920, "#1c50de", "#fff")]
    for label, x, bg, tc in chips:
        body.append(f'<rect x="{x}" y="150" width="130" height="58" rx="16" fill="{bg}" stroke="#dbeafe" filter="url(#soft)"/>')
        body.append(f'<text x="{x+65}" y="185" text-anchor="middle" fill="{tc}" font-family="Arial" font-size="15" font-weight="700">{label}</text>')
    for ax in [755, 905, 1055]:
        body.append(f'<text x="{ax}" y="186" fill="#ffffff" font-size="26" font-weight="700">→</text>')
    rows = [("Поставка медоборудования", "4,2 млн · Контур · анализ"), ("Ремонт офиса", "1,1 млн · Seldon · новый")]
    for i, (t, m) in enumerate(rows):
        yy = 260 + i * 92
        body.append(f'<rect x="608" y="{yy}" width="504" height="72" rx="14" fill="#ffffff" stroke="#e8edf5"/>')
        body.append(f'<circle cx="636" cy="{yy+36}" r="14" fill="#eef3ff"/>')
        body.append(f'<text x="{636}" y="{yy+41}" text-anchor="middle" fill="#1c50de" font-size="14">📋</text>')
        body.append(f'<text x="662" y="{yy+30}" fill="#1e293b" font-family="Arial" font-size="14" font-weight="700">{t}</text>')
        body.append(f'<text x="662" y="{yy+50}" fill="#64748b" font-family="Arial" font-size="11">{m}</text>')
    return "\n".join(body)

def visual_cycle():
    p = panel(580, 72, 560, 484, "Полный цикл")
    body = [p]
    steps = ["Закупки", "Воронка", "Поставщики", "КП"]
    for i, s in enumerate(steps):
        x = 620 + i * 128
        body.append(f'<rect x="{x}" y="210" width="108" height="50" rx="25" fill="#ffffff" filter="url(#soft)"/>')
        body.append(f'<text x="{x+54}" y="242" text-anchor="middle" fill="#1c50de" font-family="Arial" font-size="14" font-weight="700">{s}</text>')
        if i < 3:
            body.append(f'<text x="{x+118}" y="242" fill="#ffffff" font-size="18" font-weight="700">→</text>')
    body.append('<path d="M620 340 C700 280 820 400 900 320 S1020 260 1080 360" fill="none" stroke="#1c50de" stroke-width="3" opacity="0.25"/>')
    body.append('<rect x="640" y="360" width="440" height="140" rx="20" fill="#ffffff" opacity="0.92"/>')
    body.append('<text x="860" y="420" text-anchor="middle" fill="#1c50de" font-family="Arial" font-size="22" font-weight="800">Всё в одном окне</text>')
    body.append('<text x="860" y="452" text-anchor="middle" fill="#64748b" font-family="Arial" font-size="14">от поиска до контракта</text>')
    return "\n".join(body)

def visual_goszakupki():
    p = panel(580, 72, 560, 484, "Госзакупки · ЕИС")
    body = [p]
    body.append('<rect x="608" y="140" width="504" height="56" rx="14" fill="#eef3ff" stroke="#c7d7ff"/>')
    body.append('<text x="630" y="175" fill="#1c50de" font-family="Arial" font-size="16" font-weight="700">🏛  Реестр подключён</text>')
    items = [
        ("Медоборудование", "4,2 млн · 44-ФЗ · Москва", "новый"),
        ("Лицензии ПО", "890 тыс. · 223-ФЗ", "анализ"),
        ("Ремонт школы", "2,1 млн · 44-ФЗ · СПб", "подача"),
    ]
    for i, (t, m, st) in enumerate(items):
        yy = 220 + i * 98
        body.append(f'<rect x="608" y="{yy}" width="504" height="78" rx="16" fill="#ffffff" filter="url(#soft)"/>')
        body.append(f'<text x="630" y="{yy+32}" fill="#1e293b" font-family="Arial" font-size="14" font-weight="700">{t}</text>')
        body.append(f'<text x="630" y="{yy+54}" fill="#64748b" font-family="Arial" font-size="11">{m}</text>')
        body.append(f'<rect x="1000" y="{yy+24}" width="90" height="30" rx="8" fill="#eef3ff"/>')
        body.append(f'<text x="1045" y="{yy+44}" text-anchor="middle" fill="#1c50de" font-family="Arial" font-size="11" font-weight="700">{st}</text>')
    return "\n".join(body)

def visual_suppliers():
    p = panel(580, 72, 560, 484, "Поставщики и КП")
    body = [p]
    body.append('<rect x="608" y="140" width="504" height="88" rx="16" fill="#ffffff" filter="url(#soft)"/>')
    body.append('<circle cx="640" cy="184" r="22" fill="#eef3ff"/>')
    body.append('<text x="640" y="190" text-anchor="middle" font-size="16">🤝</text>')
    body.append('<text x="674" y="172" fill="#1e293b" font-family="Arial" font-size="15" font-weight="700">МедТех Снаб</text>')
    body.append('<text x="674" y="194" fill="#64748b" font-family="Arial" font-size="11">12 контрактов · в базе</text>')
    body.append('<rect x="608" y="248" width="504" height="96" rx="16" fill="#ffffff" stroke="#e8edf5"/>')
    body.append('<text x="630" y="282" fill="#1e293b" font-family="Arial" font-size="15" font-weight="700">КП_МедТех.pdf</text>')
    body.append('<text x="630" y="306" fill="#64748b" font-family="Arial" font-size="11">3 890 000 ₽ · 45 дней · 47 позиций</text>')
    body.append('<rect x="1000" y="268" width="90" height="30" rx="8" fill="#d1fae5"/>')
    body.append('<text x="1045" y="288" text-anchor="middle" fill="#059669" font-family="Arial" font-size="11" font-weight="700">готово</text>')
    body.append('<rect x="608" y="364" width="504" height="96" rx="16" fill="#f8faff" stroke="#e2e8f0" stroke-dasharray="6 4"/>')
    body.append('<text x="630" y="398" fill="#1e293b" font-family="Arial" font-size="15" font-weight="700">ПромКомплект.xlsx</text>')
    body.append('<text x="630" y="422" fill="#64748b" font-family="Arial" font-size="11">извлечение цен и сроков…</text>')
    return "\n".join(body)

def visual_free():
    p = panel(580, 72, 560, 484, "Демо-доступ")
    body = [p]
    body.append('<circle cx="860" cy="290" r="118" fill="none" stroke="#1c50de" stroke-width="4" opacity="0.35"/>')
    body.append('<circle cx="860" cy="290" r="96" fill="#ffffff" filter="url(#soft)"/>')
    body.append('<text x="860" y="282" text-anchor="middle" fill="#1c50de" font-family="Arial" font-size="72" font-weight="800">14</text>')
    body.append('<text x="860" y="322" text-anchor="middle" fill="#64748b" font-family="Arial" font-size="20" font-weight="600">дней</text>')
    body.append('<rect x="700" y="430" width="320" height="54" rx="27" fill="url(#cardHi)" filter="url(#soft)"/>')
    body.append('<text x="860" y="463" text-anchor="middle" fill="#ffffff" font-family="Arial" font-size="18" font-weight="700">Запросить демо</text>')
    body.append('<text x="860" y="510" text-anchor="middle" fill="#94a3b8" font-family="Arial" font-size="13">без привязки карты</text>')
    return "\n".join(body)

BANNERS = [
    ("banner-01-voronka.svg", ["Все тендеры", "в одной воронке"], "Этапы · задачи · команда", visual_funnel),
    ("banner-02-svoj-agregator.svg", ["Подключи", "свой Контур"], "Единая лента в iStockLink", visual_aggregator),
    ("banner-03-do-kontrakta.svg", ["От тендера", "до контракта"], "Закупки · воронка · поставщики · КП", visual_cycle),
    ("banner-04-goszakupki.svg", ["Госзакупки", "в iStockLink"], "44-ФЗ · 223-ФЗ · фильтры", visual_goszakupki),
    ("banner-05-postavshchiki-kp.svg", ["Поставщики", "и оцифровка КП"], "Сравнивайте предложения", visual_suppliers),
    ("banner-06-besplatno.svg", ["14 дней", "бесплатно"], "Попробуйте без карты", visual_free),
]

for fname, lines, sub, vis_fn in BANNERS:
    content = wrap(fname, headline(lines, sub), vis_fn())
    (OUT / fname).write_text(content, encoding="utf-8")
    print("wrote", fname)