#!/usr/bin/env python3
"""Regenerate SVG banners. Run: python3 _generate.py"""
from pathlib import Path

LOGO_PATH = (
    "M17.2112 8.91393V21.8341H22.7664C21.3776 23.4867 19.3936 24.6385 17.2112 24.939V31.9499"
    "C20.0384 31.6995 22.7168 30.748 25.048 29.0955C27.3296 27.493 29.1152 25.2895 30.3056 22.7856"
    "C30.504 22.3349 30.7024 21.8341 30.9008 21.3333C31 21.0829 31 20.7825 31 20.5321V8.91393H17.2112Z"
    " M14.5824 0C10.6144 0.350548 6.944 2.15336 4.216 5.10798C1.488 8.0626 0 11.9186 0 15.975"
    "C0 20.0313 1.488 23.9374 4.216 26.892C6.944 29.8466 10.6144 31.6495 14.5328 32V0H14.5824Z"
)

COMMON_DEFS = f"""
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1200" y2="628" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#1c50de"/>
      <stop offset="55%" stop-color="#2a5fe8"/>
      <stop offset="100%" stop-color="#3b6df0"/>
    </linearGradient>
    <linearGradient id="card" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.08"/>
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="8" stdDeviation="16" flood-color="#0f172a" flood-opacity="0.18"/>
    </filter>
  </defs>
"""

COMMON_BG = """
  <rect width="1200" height="628" fill="url(#bg)"/>
  <path d="M900,-80 C1050,120 1150,280 1280,420 L1280,-80 Z" fill="#ffffff" fill-opacity="0.06"/>
  <path d="M-60,500 C180,380 320,560 520,628 L-60,628 Z" fill="#ffffff" fill-opacity="0.05"/>
  <path d="M0,180 C220,80 380,220 600,160 C820,100 980,40 1200,120" fill="none" stroke="#ffffff" stroke-opacity="0.14" stroke-width="2"/>
  <path d="M0,420 C260,500 420,340 680,400 C900,450 1040,360 1200,440" fill="none" stroke="#ffffff" stroke-opacity="0.1" stroke-width="2"/>
"""

BRAND = """
  <g id="brand" transform="translate(64,48)">
    <g transform="scale(1.55)">
      <path d="{logo}" fill="#ffffff"/>
    </g>
    <text x="58" y="36" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="34" font-weight="700">iStockLink</text>
  </g>
""".format(logo=LOGO_PATH)


def wrap(title1, title2, subtitle, body, filename):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 628" width="1200" height="628">
{COMMON_DEFS}
  <g id="background">
{COMMON_BG}
  </g>
  <g id="brand-block">
{BRAND}
  </g>
  <g id="headline">
    <text x="64" y="210" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="62" font-weight="800">{title1}</text>
    <text x="64" y="285" fill="#ffffff" font-family="Arial, Helvetica, sans-serif" font-size="62" font-weight="800">{title2}</text>
    <text x="64" y="350" fill="#e8efff" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="400">{subtitle}</text>
  </g>
  <g id="visual" filter="url(#shadow)">
{body}
  </g>
</svg>
"""


BANNERS = [
    (
        "banner-01-voronka.svg",
        "Все тендеры",
        "в одной воронке",
        "Этапы торгов · задачи · команда",
        """
    <g transform="translate(680,150)">
      <rect x="0" y="0" width="110" height="300" rx="14" fill="url(#card)" stroke="#ffffff" stroke-opacity="0.25"/>
      <text x="55" y="34" text-anchor="middle" fill="#dbeafe" font-family="Arial" font-size="14" font-weight="700">Новые</text>
      <rect x="12" y="52" width="86" height="54" rx="8" fill="#ffffff" fill-opacity="0.15"/>
      <text x="55" y="84" text-anchor="middle" fill="#fff" font-family="Arial" font-size="12" font-weight="600">Медтехника</text>
      <rect x="130" y="0" width="110" height="300" rx="14" fill="url(#card)" stroke="#ffffff" stroke-opacity="0.35"/>
      <text x="185" y="34" text-anchor="middle" fill="#dbeafe" font-family="Arial" font-size="14" font-weight="700">Анализ</text>
      <rect x="142" y="52" width="86" height="54" rx="8" fill="#ffffff"/>
      <text x="185" y="84" text-anchor="middle" fill="#1c50de" font-family="Arial" font-size="12" font-weight="700">Ремонт</text>
      <rect x="260" y="0" width="110" height="300" rx="14" fill="url(#card)" stroke="#ffffff" stroke-opacity="0.25"/>
      <text x="315" y="34" text-anchor="middle" fill="#dbeafe" font-family="Arial" font-size="14" font-weight="700">Подача</text>
      <rect x="390" y="0" width="110" height="300" rx="14" fill="url(#card)" stroke="#ffffff" stroke-opacity="0.25"/>
      <text x="445" y="34" text-anchor="middle" fill="#dbeafe" font-family="Arial" font-size="14" font-weight="700">Контракт</text>
    </g>
""",
    ),
    (
        "banner-02-svoj-agregator.svg",
        "Подключи",
        "свой Контур",
        "Единая лента закупок в iStockLink",
        """
    <g transform="translate(620,210)">
      <rect x="0" y="0" width="120" height="72" rx="14" fill="#ffffff"/>
      <text x="60" y="44" text-anchor="middle" fill="#1e293b" font-family="Arial" font-size="18" font-weight="700">Контур</text>
      <text x="140" y="46" fill="#ffffff" font-family="Arial" font-size="28" font-weight="700">→</text>
      <rect x="170" y="0" width="120" height="72" rx="14" fill="#ffffff"/>
      <text x="230" y="44" text-anchor="middle" fill="#1e293b" font-family="Arial" font-size="18" font-weight="700">Seldon</text>
      <text x="310" y="46" fill="#ffffff" font-family="Arial" font-size="28" font-weight="700">→</text>
      <rect x="340" y="0" width="150" height="72" rx="14" fill="#153fb8" stroke="#ffffff" stroke-opacity="0.4"/>
      <text x="415" y="44" text-anchor="middle" fill="#ffffff" font-family="Arial" font-size="18" font-weight="700">iStockLink</text>
      <text x="510" y="46" fill="#ffffff" font-family="Arial" font-size="28" font-weight="700">→</text>
      <rect x="540" y="0" width="120" height="72" rx="14" fill="#ffffff" fill-opacity="0.2" stroke="#ffffff" stroke-opacity="0.35"/>
      <text x="600" y="44" text-anchor="middle" fill="#ffffff" font-family="Arial" font-size="18" font-weight="700">Лента</text>
    </g>
""",
    ),
    (
        "banner-03-do-kontrakta.svg",
        "От тендера",
        "до контракта",
        "Закупки · воронка · поставщики · КП",
        """
    <g transform="translate(64,390)">
      <rect x="0" y="0" width="200" height="56" rx="28" fill="#ffffff"/>
      <text x="100" y="36" text-anchor="middle" fill="#1c50de" font-family="Arial" font-size="22" font-weight="700">Закупки</text>
      <text x="215" y="38" fill="#ffffff" font-family="Arial" font-size="28" font-weight="700">→</text>
      <rect x="250" y="0" width="200" height="56" rx="28" fill="#ffffff"/>
      <text x="350" y="36" text-anchor="middle" fill="#1c50de" font-family="Arial" font-size="22" font-weight="700">Воронка</text>
      <text x="465" y="38" fill="#ffffff" font-family="Arial" font-size="28" font-weight="700">→</text>
      <rect x="500" y="0" width="220" height="56" rx="28" fill="#ffffff"/>
      <text x="610" y="36" text-anchor="middle" fill="#1c50de" font-family="Arial" font-size="22" font-weight="700">Поставщики</text>
      <text x="735" y="38" fill="#ffffff" font-family="Arial" font-size="28" font-weight="700">→</text>
      <rect x="770" y="0" width="120" height="56" rx="28" fill="#ffffff"/>
      <text x="830" y="36" text-anchor="middle" fill="#1c50de" font-family="Arial" font-size="22" font-weight="700">КП</text>
    </g>
""",
    ),
    (
        "banner-04-vstroennyj-poisk.svg",
        "Встроенный",
        "поиск закупок",
        "Без подписки на агрегатор — старт за 2 минуты",
        """
    <g transform="translate(700,170)">
      <rect x="0" y="0" width="420" height="260" rx="22" fill="url(#card)" stroke="#ffffff" stroke-opacity="0.3"/>
      <text x="30" y="48" fill="#ffffff" font-family="Arial" font-size="20" font-weight="700">Поиск iStockLink</text>
      <rect x="30" y="70" width="360" height="48" rx="10" fill="#ffffff" fill-opacity="0.14"/>
      <text x="46" y="100" fill="#e8efff" font-family="Arial" font-size="14">медоборудование · Москва · 44-ФЗ</text>
      <rect x="30" y="132" width="360" height="48" rx="10" fill="#ffffff"/>
      <text x="46" y="162" fill="#1c50de" font-family="Arial" font-size="14" font-weight="600">Поставка медоборудования · 4,2 млн ₽</text>
      <rect x="30" y="194" width="360" height="48" rx="10" fill="#ffffff" fill-opacity="0.14"/>
      <text x="46" y="224" fill="#e8efff" font-family="Arial" font-size="14">Ремонт офиса · коммерция · СПб</text>
    </g>
""",
    ),
    (
        "banner-05-postavshchiki-kp.svg",
        "Поставщики",
        "и оцифровка КП",
        "Сравнивайте предложения в одной таблице",
        """
    <g transform="translate(700,165)">
      <rect x="0" y="0" width="420" height="120" rx="18" fill="url(#card)" stroke="#ffffff" stroke-opacity="0.28"/>
      <text x="28" y="42" fill="#ffffff" font-family="Arial" font-size="18" font-weight="700">МедТех Снаб</text>
      <text x="28" y="68" fill="#dbeafe" font-family="Arial" font-size="13">12 контрактов · в базе</text>
      <rect x="300" y="28" width="90" height="32" rx="8" fill="#06d6a0" fill-opacity="0.25"/>
      <text x="345" y="49" text-anchor="middle" fill="#d1fae5" font-family="Arial" font-size="12" font-weight="700">в базе</text>
      <rect x="0" y="140" width="420" height="120" rx="18" fill="#ffffff"/>
      <text x="28" y="182" fill="#1e293b" font-family="Arial" font-size="16" font-weight="700">КП_МедТех.pdf</text>
      <text x="28" y="210" fill="#64748b" font-family="Arial" font-size="13">3 890 000 ₽ · 45 дней · 47 позиций</text>
      <rect x="300" y="168" width="90" height="32" rx="8" fill="#1c50de" fill-opacity="0.12"/>
      <text x="345" y="189" text-anchor="middle" fill="#1c50de" font-family="Arial" font-size="12" font-weight="700">готово</text>
    </g>
""",
    ),
    (
        "banner-06-besplatno.svg",
        "14 дней",
        "бесплатно",
        "Попробуйте iStockLink без привязки карты",
        """
    <g transform="translate(700,185)">
      <circle cx="210" cy="120" r="118" fill="none" stroke="#ffffff" stroke-opacity="0.22" stroke-width="3"/>
      <circle cx="210" cy="120" r="96" fill="#ffffff" fill-opacity="0.12"/>
      <text x="210" y="108" text-anchor="middle" fill="#ffffff" font-family="Arial" font-size="54" font-weight="800">14</text>
      <text x="210" y="148" text-anchor="middle" fill="#dbeafe" font-family="Arial" font-size="20" font-weight="600">дней</text>
      <rect x="40" y="250" width="340" height="48" rx="24" fill="#ffffff"/>
      <text x="210" y="281" text-anchor="middle" fill="#1c50de" font-family="Arial" font-size="18" font-weight="700">Запросить демо</text>
    </g>
""",
    ),
]

out_dir = Path(__file__).parent
for fname, t1, t2, sub, body in BANNERS:
    (out_dir / fname).write_text(wrap(t1, t2, sub, body, fname), encoding="utf-8")
    print("wrote", fname)