#!/usr/bin/env python3
"""GTM PPTX in the same visual system as the B2B PDF (white, blue accent, tables)."""
from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

# PDF tokens
INK = RGBColor(0x0F, 0x17, 0x2A)
MUTED = RGBColor(0x47, 0x55, 0x69)
LINE = RGBColor(0xE2, 0xE8, 0xF0)
BLUE = RGBColor(0x1C, 0x50, 0xDE)
BLUE_SOFT = RGBColor(0xEE, 0xF2, 0xFF)
PAPER = RGBColor(0xF8, 0xFA, 0xFC)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
US = RGBColor(0x15, 0x3F, 0xB8)

W = Inches(13.333)
H = Inches(7.5)
MX = Inches(0.75)
MY = Inches(0.5)


def font(run, size=14, bold=False, color=INK):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = "Calibri"
    rPr = run._r.get_or_add_rPr()
    ea = rPr.find(qn("a:ea"))
    if ea is None:
        from lxml import etree

        ea = etree.SubElement(rPr, qn("a:ea"))
    ea.set("typeface", "Calibri")


def fill(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()


def rect(slide, left, top, width, height, color):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    fill(sh, color)
    return sh


def round_rect(slide, left, top, width, height, color):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    fill(sh, color)
    try:
        sh.adjustments[0] = 0.08
    except Exception:
        pass
    return sh


def txt(slide, left, top, width, height, text, size=14, bold=False, color=INK, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    try:
        tf.auto_size = None
    except Exception:
        pass
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    font(run, size=size, bold=bold, color=color)
    return box


def lines(slide, left, top, width, height, items, size=13, color=MUTED, bold=False, gap=6):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        run = p.add_run()
        run.text = item
        font(run, size=size, bold=bold, color=color)
        p.space_after = Pt(gap)
    return box


def brand_row(slide):
    mark = slide.shapes.add_shape(MSO_SHAPE.OVAL, MX, MY + Inches(0.02), Inches(0.18), Inches(0.18))
    fill(mark, BLUE)
    # soft ring via larger pale circle behind
    ring = slide.shapes.add_shape(MSO_SHAPE.OVAL, MX - Inches(0.05), MY - Inches(0.03), Inches(0.28), Inches(0.28))
    fill(ring, BLUE_SOFT)
    spTree = slide.shapes._spTree
    spTree.remove(ring._element)
    spTree.insert(2, ring._element)
    txt(slide, MX + Inches(0.32), MY - Inches(0.02), Inches(3), Inches(0.3), "iStockLink", 16, True, INK)
    # badge
    badge = round_rect(slide, W - MX - Inches(2.35), MY - Inches(0.05), Inches(2.35), Inches(0.34), BLUE_SOFT)
    try:
        badge.adjustments[0] = 0.5
    except Exception:
        pass
    txt(slide, W - MX - Inches(2.35), MY - Inches(0.02), Inches(2.35), Inches(0.3), "B2B · CONFIDENTIAL", 10, True, BLUE, PP_ALIGN.CENTER)


def section_title(slide, text):
    """Blue underlined H2 like PDF."""
    txt(slide, MX, Inches(1.05), Inches(12), Inches(0.45), text, 22, True, BLUE)
    rect(slide, MX, Inches(1.5), Inches(12), Emu(19050), BLUE)  # ~1.5pt line


def footer(slide, left_text, num, total):
    rect(slide, MX, H - Inches(0.55), W - 2 * MX, Emu(12700), LINE)
    txt(slide, MX, H - Inches(0.45), Inches(7), Inches(0.3), left_text, 11, False, MUTED)
    txt(slide, W - MX - Inches(1.6), H - Inches(0.45), Inches(1.6), Inches(0.3), f"{num:02d} / {total:02d}", 11, False, MUTED, PP_ALIGN.RIGHT)


def table(slide, left, top, width, rows, col_w, font_size=11, highlight_last=False):
    rows_n, cols_n = len(rows), len(rows[0])
    # estimate height
    row_h = Inches(0.38)
    height = int(row_h * rows_n)
    shape = slide.shapes.add_table(rows_n, cols_n, left, top, width, height)
    tbl = shape.table
    for i, w in enumerate(col_w):
        tbl.columns[i].width = w
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            cell = tbl.cell(r, c)
            cell.text = str(val)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            for p in cell.text_frame.paragraphs:
                for run in p.runs:
                    is_h = r == 0
                    color = WHITE if is_h else (US if highlight_last and c == cols_n - 1 and r > 0 else INK)
                    font(run, size=font_size, bold=is_h or (highlight_last and c == cols_n - 1), color=color)
            if r == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = INK
            elif highlight_last and c == cols_n - 1:
                cell.fill.solid()
                cell.fill.fore_color.rgb = BLUE_SOFT
            elif r % 2 == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = PAPER
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = WHITE
    return shape


def note_box(slide, left, top, width, height, text):
    round_rect(slide, left, top, width, height, PAPER)
    txt(slide, left + Inches(0.2), top + Inches(0.12), width - Inches(0.4), height - Inches(0.2), text, 12, False, MUTED)


def meta_box(slide, left, top, width, height, items):
    """Paper box with blue left bar — PDF cover style."""
    round_rect(slide, left, top, width, height, PAPER)
    rect(slide, left, top, Inches(0.08), height, BLUE)
    lines(slide, left + Inches(0.28), top + Inches(0.2), width - Inches(0.45), height - Inches(0.3), items, 13, INK, False, 8)


def kpi_card(slide, left, top, width, height, number, label):
    round_rect(slide, left, top, width, height, PAPER)
    txt(slide, left + Inches(0.22), top + Inches(0.25), width - Inches(0.4), Inches(0.55), number, 24, True, BLUE)
    txt(slide, left + Inches(0.22), top + Inches(0.9), width - Inches(0.4), height - Inches(1.1), label, 12, False, MUTED)


def build(out: Path):
    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H
    blank = prs.slide_layouts[6]
    slides = []

    def add():
        s = prs.slides.add_slide(blank)
        rect(s, 0, 0, W, H, WHITE)
        slides.append(s)
        return s

    # —— 01 Cover (PDF cover) ——
    s = add()
    brand_row(s)
    txt(s, MX, Inches(1.8), Inches(8), Inches(0.35), "GO-TO-MARKET ДОКУМЕНТ", 12, True, BLUE)
    txt(s, MX, Inches(2.25), Inches(11.5), Inches(1.6), "Анализ рынка и план\nпродвижения продукта\nCRM + SRM", 34, True, INK)
    txt(
        s,
        MX,
        Inches(4.1),
        Inches(10),
        Inches(0.7),
        "Позиционирование iStockLink как связки продаж и закупок в одном окне.\nОтдельный блок — сравнительная матрица с Битрикс24.",
        15,
        False,
        MUTED,
    )
    meta_box(
        s,
        MX,
        Inches(5.0),
        Inches(8.2),
        Inches(1.55),
        [
            "Продукт: iStockLink CRM + SRM",
            "Рынок: Россия, B2B / B2G · горизонт 12 месяцев",
            "Версия 1.2 · калибровка на Директе сентябрь 2026",
        ],
    )
    footer(s, "istock.link", 1, 0)

    # —— 02 TOC ——
    s = add()
    brand_row(s)
    section_title(s, "Содержание")
    toc = [
        ("01", "Резюме для руководства"),
        ("02", "Анализ рынка — CRM, SRM, ICP, конкуренты"),
        ("03", "Факт Директа и деньги → результат"),
        ("04", "Сценарии бюджета A / B / C"),
        ("05", "Таблица сравнения с Битрикс24"),
        ("06", "Риски и что нужно для точного win rate"),
    ]
    y = Inches(1.9)
    for n, t in toc:
        txt(s, MX, y, Inches(0.7), Inches(0.4), n, 16, True, BLUE)
        txt(s, MX + Inches(0.9), y, Inches(10), Inches(0.4), t, 16, False, INK)
        rect(s, MX, y + Inches(0.45), W - 2 * MX, Emu(6350), LINE)
        y += Inches(0.65)
    note_box(
        s,
        MX,
        Inches(6.0),
        W - 2 * MX,
        Inches(0.7),
        "Источники рынка: TAdviser, Kept, Data Insight. Реклама: отчёт Яндекс Директ iStockLink, сентябрь 2026.",
    )
    footer(s, "Содержание", 2, 0)

    # —— 03 Exec ——
    s = add()
    brand_row(s)
    section_title(s, "1. Резюме для руководства")
    txt(
        s,
        MX,
        Inches(1.75),
        Inches(12),
        Inches(0.7),
        "Ниша между универсальной CRM и тяжёлым SRM. Ценность — один контур «сделка → запрос КП → поставка».",
        15,
        False,
        INK,
    )
    kpi_card(s, MX, Inches(2.6), Inches(3.85), Inches(1.9), "~44 млрд ₽", "Рынок CRM РФ, 2025\nTAdviser, +25% г/г")
    kpi_card(s, MX + Inches(4.1), Inches(2.6), Inches(3.85), Inches(1.9), "~3,5 млрд ₽", "Рынок SRM РФ, 2025\nKept / TAdviser")
    kpi_card(s, MX + Inches(8.2), Inches(2.6), Inches(3.85), Inches(1.9), "5 515 ₽", "Cost / SQL факт\nДирект, сентябрь 2026")
    txt(s, MX, Inches(4.8), Inches(12), Inches(0.35), "Ключевые выводы", 16, True, INK)
    lines(
        s,
        MX,
        Inches(5.2),
        Inches(12),
        Inches(1.4),
        [
            "• Директ уже даёт SQL за ~5,5 тыс. ₽ — канал не «холодный тест».",
            "• Средний бизнес платит за Битрикс дважды: лицензия + внедрение 150–600 тыс. ₽.",
            "• Рекомендация: сценарий A (150 тыс ₽/мес), затем B после фиксации win rate.",
        ],
        14,
        MUTED,
        False,
        4,
    )
    footer(s, "Резюме", 3, 0)

    # —— 04 Market ——
    s = add()
    brand_row(s)
    section_title(s, "2. Анализ рынка")
    txt(s, MX, Inches(1.7), Inches(12), Inches(0.35), "Рынок CRM и SRM в России", 16, True, INK)
    table(
        s,
        MX,
        Inches(2.15),
        W - 2 * MX,
        [
            ["Показатель", "Оценка", "Источник"],
            ["CRM РФ, 2024", "~35,3 млрд ₽", "TAdviser"],
            ["CRM РФ, 2025", "~44,1 млрд ₽ (+25%)", "TAdviser"],
            ["Комплексные CRM, 2025", "~20,5 млрд ₽", "Kept"],
            ["SRM РФ, 2025", "~3,5 млрд ₽", "Kept / TAdviser"],
            ["CAGR SRM 2020–2025", "~30,6%", "Kept"],
            ["Автоматизация закупок, 2024", "~11,5 млрд ₽", "Data Insight"],
        ],
        [Inches(4.4), Inches(4.0), Inches(3.5)],
        12,
    )
    footer(s, "Анализ рынка", 4, 0)

    # —— 05 ICP ——
    s = add()
    brand_row(s)
    section_title(s, "2.4. Целевой сегмент (ICP)")
    round_rect(s, MX, Inches(1.85), Inches(5.85), Inches(4.5), PAPER)
    txt(s, MX + Inches(0.3), Inches(2.1), Inches(5.2), Inches(0.4), "Primary ICP", 16, True, BLUE)
    lines(
        s,
        MX + Inches(0.3),
        Inches(2.7),
        Inches(5.2),
        Inches(3.3),
        [
            "• B2B / B2G, 15–150 сотрудников",
            "• Отдел продаж + регулярные закупки / тендеры",
            "• Сейчас: Excel или «сырой» Битрикс24",
            "• Боли: потеря сделок, ручной сбор КП,",
            "  нет единой картины для РОП",
        ],
        14,
        INK,
        False,
        8,
    )
    round_rect(s, MX + Inches(6.15), Inches(1.85), Inches(5.85), Inches(4.5), PAPER)
    txt(s, MX + Inches(6.45), Inches(2.1), Inches(5.2), Inches(0.4), "Secondary ICP", 16, True, BLUE)
    lines(
        s,
        MX + Inches(6.45),
        Inches(2.7),
        Inches(5.2),
        Inches(3.3),
        [
            "• Торговля / производство под клиента",
            "• Тендерные команды in-house / outsource",
            "• Переход с Битрикс без бюджета на интегратора",
            "• Нужны Контур / Seldon в том же контуре",
        ],
        14,
        INK,
        False,
        8,
    )
    footer(s, "ICP", 5, 0)

    # —— 06 Competition ——
    s = add()
    brand_row(s)
    section_title(s, "2.5. Конкурентная карта")
    table(
        s,
        MX,
        Inches(1.9),
        W - 2 * MX,
        [
            ["Кластер", "Примеры", "Слабость vs iStockLink"],
            ["Универсальные CRM", "Битрикс24, amoCRM", "SRM/КП — доработка; долгое внедрение"],
            ["Тяжёлые SRM / S2P", "Norbit, ELMA365…", "Дорого, слабо связано с продажами SMB"],
            ["Агрегаторы тендеров", "Контур, Seldon", "Нет CRM/SRM-операционки"],
            ["Excel + почта", "Статус-кво", "Нет контроля и масштаба"],
        ],
        [Inches(3.6), Inches(3.8), Inches(4.5)],
        12,
    )
    note_box(
        s,
        MX,
        Inches(5.3),
        W - 2 * MX,
        Inches(1.1),
        "Окно iStockLink: готовая CRM + SRM и оцифровка КП в одном окне, старт за день, без интегратора. Продаём снижение TCO и цикл «клиент → поставка», не «ещё одну CRM».",
    )
    footer(s, "Конкуренты", 6, 0)

    # —— 07 Direct fact ——
    s = add()
    brand_row(s)
    section_title(s, "3. Факт Яндекс Директа · сентябрь 2026")
    table(
        s,
        MX,
        Inches(1.85),
        W - 2 * MX,
        [
            ["Показатель", "Значение", "Комментарий"],
            ["Расход", "27 576 ₽", "Поиск 93% + ретаргет 7%"],
            ["Показы / клики", "15 337 / 457", "CTR ~3,0%"],
            ["Конверсии Метрики", "56 · CPA 492 ₽", "Не все = лид в CRM"],
            ["Реальные лиды", "8 · CPL 3 447 ₽", "База для планирования"],
            ["SQL", "5 · 5 515 ₽ / SQL", "Lead→SQL = 62,5%"],
        ],
        [Inches(3.8), Inches(3.8), Inches(4.3)],
        12,
    )
    note_box(
        s,
        MX,
        Inches(5.5),
        W - 2 * MX,
        Inches(0.9),
        "CPA 492 ₽ по Метрике завышает картину. Для денег ориентируемся на CPL 3,4 тыс. ₽ и ~5,5 тыс. ₽ за SQL. Win rate (SQL→оплата) в выгрузках пока нет.",
    )
    footer(s, "Факт Директа", 7, 0)

    # —— 08 Assumptions ——
    s = add()
    brand_row(s)
    section_title(s, "3.7. Допущения модели после калибровки")
    table(
        s,
        MX,
        Inches(1.9),
        W - 2 * MX,
        [
            ["Параметр", "Значение", "Комментарий"],
            ["ACV команды", "120 000 ₽ / год", "Уточнить по факту сделок"],
            ["Cost / SQL сейчас", "~5 500 ₽", "Факт сентября"],
            ["Cost / SQL при масштабе", "6–10 тыс. ₽", "Рост аукциона"],
            ["Lead → SQL", "62%", "5 из 8"],
            ["SQL → оплата", "15% / 22% / 28%", "Факта закрытий нет — три ветки"],
        ],
        [Inches(4.0), Inches(3.6), Inches(4.3)],
        12,
    )
    footer(s, "Допущения", 8, 0)

    # —— 09 Scenarios ——
    s = add()
    brand_row(s)
    section_title(s, "Сценарии: если столько денег — такой результат")
    # four cards: 0 A B C
    cards = [
        ("0 · Как сейчас", "~28 тыс ₽/мес", "SQL ~60/год", "~13 оплат*", "~1,6 млн ₽", "Факт run-rate"),
        ("A · Разогрев", "150 тыс ₽/мес", "SQL ~300/год", "~66 оплат*", "~7,9 млн ₽", "Рекомендуемый шаг"),
        ("B · База", "300 тыс ₽/мес", "SQL ~480/год", "~106 оплат*", "~12,7 млн ₽", "После win rate"),
        ("C · Рост", "600 тыс ₽/мес", "SQL ~720/год", "~158 оплат*", "~19 млн ₽", "Сайт + 2+ продавца"),
    ]
    for i, (name, bud, sql, deals, rev, note) in enumerate(cards):
        left = MX + i * Inches(3.1)
        round_rect(s, left, Inches(1.85), Inches(2.95), Inches(4.0), PAPER)
        if i == 1:
            rect(s, left, Inches(1.85), Inches(0.08), Inches(4.0), BLUE)
        txt(s, left + Inches(0.18), Inches(2.05), Inches(2.6), Inches(0.4), name, 13, True, BLUE)
        txt(s, left + Inches(0.18), Inches(2.55), Inches(2.6), Inches(0.4), bud, 14, True, INK)
        lines(
            s,
            left + Inches(0.18),
            Inches(3.15),
            Inches(2.6),
            Inches(2.4),
            [sql, deals, "Выручка: " + rev, note],
            12,
            MUTED,
            False,
            8,
        )
    note_box(
        s,
        MX,
        Inches(6.05),
        W - 2 * MX,
        Inches(0.55),
        "* Оплаты при win rate 22%. Диапазон 15–28% см. в PDF. Сначала A на 6–8 недель, затем B.",
    )
    footer(s, "Сценарии бюджета", 9, 0)

    # —— 10 Channel mix ——
    s = add()
    brand_row(s)
    section_title(s, "Куда класть деньги внутри бюджета")
    table(
        s,
        MX,
        Inches(1.85),
        W - 2 * MX,
        [
            ["Канал", "A", "B", "C", "Зачем"],
            ["Яндекс Директ — поиск", "55%", "45%", "40%", "Заявки на демо"],
            ["Ретаргет", "15%", "15%", "15%", "Догон сайта"],
            ["Контент / кейсы / PDF", "15%", "15%", "12%", "Доверие + sales kit"],
            ["Вебинары / посевы", "5%", "10%", "12%", "Квалифицированный inbound"],
            ["Партнёры", "5%", "10%", "15%", "Агентства, 1С"],
            ["Тесты каналов", "5%", "5%", "6%", "Telegram / ABM"],
        ],
        [Inches(3.6), Inches(1.3), Inches(1.3), Inches(1.3), Inches(4.3)],
        11,
    )
    footer(s, "Микс каналов", 10, 0)

    # —— 11 Bitrix ——
    s = add()
    brand_row(s)
    section_title(s, "4. Таблица сравнения с Битрикс24")
    table(
        s,
        MX,
        Inches(1.8),
        W - 2 * MX,
        [
            ["Критерий", "Битрикс24 + внедрение", "iStockLink CRM+SRM"],
            ["Время до процесса", "Недели–месяцы", "Около 1 дня"],
            ["SRM / поставщики", "Доработка", "В том же окне"],
            ["КП и сравнение", "Почта / кастом", "Сводная таблица"],
            ["Сделка → закупка", "Проектируется", "Единый маршрут"],
            ["Агрегаторы", "Через интегратора", "Контур / Seldon из коробки"],
            ["Модель затрат", "Подписка + 150–600+ тыс.", "Подписка, без проекта"],
        ],
        [Inches(3.5), Inches(4.5), Inches(4.0)],
        12,
        highlight_last=True,
    )
    footer(s, "Сравнение с Битрикс24", 11, 0)

    # —— 12 Next ——
    s = add()
    brand_row(s)
    section_title(s, "Рекомендация и следующий шаг")
    kpi_card(s, MX, Inches(1.85), Inches(4.0), Inches(2.2), "Сценарий A", "150 тыс ₽ / мес\n~300 SQL / год\n~7,9 млн ₽ при win 22%")
    kpi_card(s, MX + Inches(4.2), Inches(1.85), Inches(4.0), Inches(2.2), "×5 к факту", "Сейчас ~28 тыс ₽/мес\nКанал уже даёт SQL\nза 5 515 ₽")
    kpi_card(s, MX + Inches(8.4), Inches(1.85), Inches(4.0), Inches(2.2), "Потом B", "После 6–8 недель\nи фиксации win rate\nпо CRM")
    txt(s, MX, Inches(4.4), Inches(12), Inches(0.35), "Чтобы убрать вилку 15–28% по оплатам, пришлите:", 14, True, INK)
    lines(
        s,
        MX,
        Inches(4.85),
        Inches(12),
        Inches(1.3),
        [
            "1. По 5 SQL сентября — статус, тариф, won/lost",
            "2. Касания 3–6 мес. с UTM / источником",
            "3. Факт ACV по оплаченным аккаунтам",
        ],
        14,
        MUTED,
        False,
        4,
    )
    footer(s, "istock.link · GTM CRM+SRM", 12, 0)

    total = len(slides)
    # rewrite footers with total
    for i, slide in enumerate(slides):
        # remove previous footer texts is hard; add overlay numbers only if needed
        # We already wrote wrong totals (0). Rebuild footers by adding correct ones on top area — cleaner to set total in second pass via regenerating numbers.
        pass

    # Fix page numbers: delete last two textboxes approach is fragile.
    # Instead re-save with correct numbers by rebuilding footer line numbers only — simplest: recreate presentation with total known.
    # We'll just patch by adding correct number boxes at the end (covering old).
    for i, slide in enumerate(slides):
        rect(slide, W - MX - Inches(1.65), H - Inches(0.48), Inches(1.65), Inches(0.32), WHITE)
        txt(slide, W - MX - Inches(1.6), H - Inches(0.45), Inches(1.6), Inches(0.3), f"{i+1:02d} / {total:02d}", 11, False, MUTED, PP_ALIGN.RIGHT)

    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(out))
    print(f"saved {out} ({total} slides)")


if __name__ == "__main__":
    out = Path("/workspace/content/business/istocklink-crm-srm-gtm.pptx")
    build(out)
    Path("/workspace/docs/business/istocklink-crm-srm-gtm.pptx").write_bytes(out.read_bytes())
    Path("/opt/cursor/artifacts/istocklink_crm_srm_gtm.pptx").write_bytes(out.read_bytes())
