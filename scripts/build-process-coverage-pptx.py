#!/usr/bin/env python3
"""One-slide PPTX: trading process coverage — iStockLink vs Bitrix / amoCRM (v3)."""
from __future__ import annotations

from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

INK = RGBColor(0x0F, 0x17, 0x2A)
MUTED = RGBColor(0x47, 0x55, 0x69)
LINE = RGBColor(0xE2, 0xE8, 0xF0)
BLUE = RGBColor(0x1C, 0x50, 0xDE)
BLUE_SOFT = RGBColor(0xEE, 0xF2, 0xFF)
PAPER = RGBColor(0xF8, 0xFA, 0xFC)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BX_BOX = RGBColor(0x94, 0xA3, 0xB8)
BX_CUSTOM = RGBColor(0x38, 0xBD, 0xF8)
AMO = RGBColor(0xF5, 0x9E, 0x0B)
PHASE_SALES_BG = RGBColor(0xF1, 0xF5, 0xF9)
PHASE_SALES_FG = RGBColor(0x64, 0x74, 0x8B)
DASH = RGBColor(0xCB, 0xD5, 0xE1)

W = Inches(13.333)
H = Inches(7.5)
MX = Inches(0.55)
MY = Inches(0.32)

LABEL_W = Inches(2.15)
STAGES = [
    ("Лид", "Клиент или тендер"),
    ("КП клиенту", "Коммерция"),
    ("Сделка", "Договор"),
    ("Заявка\nна закупку", "Потребность"),
    ("Запрос\nпоставщикам", "RFQ"),
    ("Сравнение\nКП", "Выбор"),
    ("Поставка", "От поставщика"),
    ("Отгрузка\nклиенту", "Закрытие"),
]
N = len(STAGES)


def font(run, size=14, bold=False, color=INK):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = "Calibri"
    rPr = run._r.get_or_add_rPr()
    ea = rPr.find(qn("a:ea"))
    if ea is None:
        ea = etree.SubElement(rPr, qn("a:ea"))
    ea.set("typeface", "Calibri")


def fill(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()


def stroke(shape, color, pt=1.0):
    shape.line.color.rgb = color
    shape.line.width = Pt(pt)


def rect(slide, left, top, width, height, color):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    fill(sh, color)
    return sh


def round_rect(slide, left, top, width, height, color, adj=0.08):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    fill(sh, color)
    try:
        sh.adjustments[0] = adj
    except Exception:
        pass
    return sh


def oval(slide, left, top, width, height, color):
    sh = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, width, height)
    fill(sh, color)
    return sh


def txt(
    slide,
    left,
    top,
    width,
    height,
    text,
    size=14,
    bold=False,
    color=INK,
    align=PP_ALIGN.LEFT,
    anchor=MSO_ANCHOR.TOP,
):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    try:
        tf.auto_size = None
    except Exception:
        pass
    try:
        tf.paragraphs[0].alignment = align
        box.text_frame._txBody.bodyPr.set("anchor", {MSO_ANCHOR.TOP: "t", MSO_ANCHOR.MIDDLE: "ctr", MSO_ANCHOR.BOTTOM: "b"}[anchor])
    except Exception:
        pass
    # multi-line support
    lines = text.split("\n")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        run = p.add_run()
        run.text = line
        font(run, size=size, bold=bold, color=color)
        p.space_after = Pt(0)
        p.space_before = Pt(0)
    return box


def dashed_cell(slide, left, top, width, height):
    """Hatched-like empty cell: light fill + dashed border."""
    sh = round_rect(slide, left, top, width, height, PAPER, adj=0.12)
    stroke(sh, DASH, 1.0)
    # approximate dash via diagonal thin rects
    try:
        ln = sh.line
        ln.dash_style = 4  # dash
    except Exception:
        pass
    return sh


def build(out: Path):
    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    rect(slide, 0, 0, W, H, WHITE)

    # brand
    ring = oval(slide, MX - Inches(0.04), MY - Inches(0.02), Inches(0.26), Inches(0.26), BLUE_SOFT)
    mark = oval(slide, MX + Inches(0.01), MY + Inches(0.03), Inches(0.16), Inches(0.16), BLUE)
    # ensure ring under mark
    spTree = slide.shapes._spTree
    spTree.remove(ring._element)
    spTree.insert(2, ring._element)
    txt(slide, MX + Inches(0.32), MY, Inches(3), Inches(0.28), "iStockLink", 15, True, INK)

    badge_w = Inches(2.4)
    badge = round_rect(slide, W - MX - badge_w, MY - Inches(0.02), badge_w, Inches(0.32), BLUE_SOFT, adj=0.5)
    txt(slide, W - MX - badge_w, MY, badge_w, Inches(0.28), "ОДИН СЛАЙД · V3", 10, True, BLUE, PP_ALIGN.CENTER)

    # title
    title_top = Inches(0.72)
    txt(slide, MX, title_top, Inches(12.2), Inches(0.4), "Процесс торговой компании: кто что закрывает", 22, True, BLUE)
    rect(slide, MX, title_top + Inches(0.42), Inches(12.2), Emu(19050), BLUE)
    txt(
        slide,
        MX,
        title_top + Inches(0.5),
        Inches(12.2),
        Inches(0.4),
        "Восемь этапов от лида до отгрузки. Покрытие: iStockLink, Битрикс24 и amoCRM. "
        "Процесс один; различаются вход (источник лида) и глубина контура.",
        11,
        False,
        MUTED,
    )

    # layout geometry
    track_left = MX + LABEL_W
    track_w = W - MX - track_left - Inches(0.05)
    cell_gap = Inches(0.04)
    cell_w = (track_w - cell_gap * (N - 1)) / N

    def col_x(i: int):
        return track_left + i * (cell_w + cell_gap)

    # phases
    phase_top = Inches(1.72)
    phase_h = Inches(0.28)
    sales_w = 3 * cell_w + 2 * cell_gap - Inches(0.03)
    buy_left = col_x(3) + Inches(0.03)
    buy_w = track_w - (buy_left - track_left)
    round_rect(slide, col_x(0), phase_top, sales_w, phase_h, PHASE_SALES_BG, adj=0.15)
    txt(slide, col_x(0), phase_top + Inches(0.02), sales_w, phase_h, "ПРОДАЖИ", 9, True, PHASE_SALES_FG, PP_ALIGN.CENTER)
    round_rect(slide, buy_left, phase_top, buy_w, phase_h, BLUE_SOFT, adj=0.15)
    txt(slide, buy_left, phase_top + Inches(0.02), buy_w, phase_h, "ЗАКУПКА И ИСПОЛНЕНИЕ", 9, True, BLUE, PP_ALIGN.CENTER)

    # timeline label + rail + stages
    stages_top = Inches(2.12)
    txt(slide, MX, stages_top + Inches(0.15), LABEL_W - Inches(0.1), Inches(0.3), "Этапы", 12, True, MUTED)

    rail_y = stages_top + Inches(0.12)
    rail_left = col_x(0) + cell_w / 2
    rail_right = col_x(N - 1) + cell_w / 2
    rect(slide, rail_left, rail_y + Inches(0.05), rail_right - rail_left, Emu(28575), LINE)

    for i, (name, hint) in enumerate(STAGES):
        cx = col_x(i) + cell_w / 2
        # white ring + blue ring
        oval(slide, cx - Inches(0.11), rail_y, Inches(0.22), Inches(0.22), WHITE)
        ring_d = oval(slide, cx - Inches(0.09), rail_y + Inches(0.02), Inches(0.18), Inches(0.18), BLUE)
        fill(ring_d, WHITE)
        stroke(ring_d, BLUE, 2.25)
        # inner blue fill small
        oval(slide, cx - Inches(0.035), rail_y + Inches(0.055), Inches(0.07), Inches(0.07), BLUE)
        txt(
            slide,
            col_x(i),
            rail_y + Inches(0.28),
            cell_w,
            Inches(0.48),
            name,
            10,
            True,
            INK,
            PP_ALIGN.CENTER,
        )
        txt(
            slide,
            col_x(i),
            rail_y + Inches(0.72),
            cell_w,
            Inches(0.22),
            hint,
            8,
            False,
            MUTED,
            PP_ALIGN.CENTER,
        )

    # capability callout under lead (cols 0-2)
    cap_top = Inches(3.18)
    cap_h = Inches(0.58)
    cap_w = 3 * cell_w + 2 * cell_gap
    cap = round_rect(slide, track_left, cap_top, cap_w, cap_h, BLUE_SOFT, adj=0.1)
    stroke(cap, RGBColor(0xBF, 0xDB, 0xFE), 1.0)
    # left accent
    rect(slide, track_left, cap_top, Inches(0.06), cap_h, BLUE)
    txt(slide, track_left + Inches(0.14), cap_top + Inches(0.04), Inches(1.7), Inches(0.18), "ВОЗМОЖНОСТЬ ISTOCKLINK", 8, True, BLUE)
    txt(
        slide,
        track_left + Inches(0.14),
        cap_top + Inches(0.22),
        cap_w - Inches(0.24),
        Inches(0.34),
        "Источник лида — компания-заказчик или тендер. Интеграции с агрегаторами и ЭТП; "
        "тендер входит в тот же этап «Лид», процесс дальше не меняется.",
        9,
        False,
        INK,
    )

    # lanes
    lanes = [
        {
            "title": "iStockLink",
            "sub": "CRM + SRM + тендеры",
            "cover": 8,
            "color": BLUE,
            "label": "Весь контур: лид (клиент / тендер) → закупка → отгрузка",
            "label_color": WHITE,
            "note": "",
            "continuous": True,
        },
        {
            "title": "Битрикс24 из коробки",
            "sub": "Без проекта внедрения",
            "cover": 3,
            "color": BX_BOX,
            "label": "CRM продаж",
            "label_color": WHITE,
            "note": "закупка и тендеры — вне контура",
            "continuous": True,
        },
        {
            "title": "Битрикс24 + доработки",
            "sub": "Проект интегратора",
            "cover": 5,
            "color": BX_CUSTOM,
            "label": "Продажи + часть закупок",
            "label_color": INK,
            "note": "сравнение / поставка — ещё кастом",
            "continuous": True,
        },
        {
            "title": "amoCRM",
            "sub": "CRM продаж",
            "cover": 3,
            "color": AMO,
            "label": "Воронка продаж",
            "label_color": INK,
            "note": "SRM / тендеры / ЭТП — нет",
            "continuous": True,
        },
    ]

    lane_top0 = Inches(3.88)
    lane_h = Inches(0.38)
    lane_gap = Inches(0.1)
    bar_h = Inches(0.32)

    for li, lane in enumerate(lanes):
        top = lane_top0 + li * (lane_h + lane_gap)
        txt(slide, MX, top, LABEL_W - Inches(0.08), Inches(0.2), lane["title"], 11, True, INK)
        txt(slide, MX, top + Inches(0.18), LABEL_W - Inches(0.08), Inches(0.18), lane["sub"], 9, False, MUTED)

        # background cells
        for i in range(N):
            dashed_cell(slide, col_x(i), top + Inches(0.03), cell_w, bar_h)

        cover = lane["cover"]
        if cover > 0:
            bar_w = cover * cell_w + (cover - 1) * cell_gap
            bar = round_rect(slide, track_left, top + Inches(0.03), bar_w, bar_h, lane["color"], adj=0.12)
            txt(
                slide,
                track_left + Inches(0.1),
                top + Inches(0.06),
                min(bar_w - Inches(0.15), Inches(5.8)),
                Inches(0.26),
                lane["label"],
                9,
                True,
                lane["label_color"],
                PP_ALIGN.LEFT,
                MSO_ANCHOR.MIDDLE,
            )
        if lane["note"] and cover < N:
            note_x = col_x(cover) + Inches(0.06)
            note_w = track_w - (note_x - track_left) - Inches(0.05)
            txt(slide, note_x, top + Inches(0.08), note_w, Inches(0.22), lane["note"], 9, True, MUTED)

    # takeaway
    take_top = Inches(5.85)
    take_h = Inches(0.55)
    round_rect(slide, MX, take_top, W - 2 * MX, take_h, BLUE_SOFT, adj=0.08)
    rect(slide, MX, take_top, Inches(0.07), take_h, BLUE)
    txt(
        slide,
        MX + Inches(0.2),
        take_top + Inches(0.08),
        W - 2 * MX - Inches(0.35),
        Inches(0.42),
        "Вывод: iStockLink закрывает линию целиком и принимает лид как компанию или тендер "
        "(агрегаторы, ЭТП). Битрикс и amoCRM сильны в продажах; закупка и тендерный вход — "
        "зона пробелов или кастома.",
        11,
        True,
        INK,
    )

    # legend
    leg_top = Inches(6.52)
    items = [
        (BLUE, "iStockLink"),
        (BX_BOX, "Битрикс из коробки"),
        (BX_CUSTOM, "Битрикс + доработки"),
        (AMO, "amoCRM"),
    ]
    x = MX
    for color, label in items:
        sw = round_rect(slide, x, leg_top + Inches(0.04), Inches(0.22), Inches(0.12), color, adj=0.2)
        txt(slide, x + Inches(0.28), leg_top, Inches(1.9), Inches(0.22), label, 10, True, MUTED)
        x += Inches(2.15)
    # gap swatch
    gap_sw = round_rect(slide, x, leg_top + Inches(0.04), Inches(0.22), Inches(0.12), PAPER, adj=0.2)
    stroke(gap_sw, DASH, 1.0)
    txt(slide, x + Inches(0.28), leg_top, Inches(2.0), Inches(0.22), "Не закрыто / вручную", 10, True, MUTED)

    # footer
    rect(slide, MX, H - Inches(0.42), W - 2 * MX, Emu(12700), LINE)
    txt(slide, MX, H - Inches(0.34), Inches(9), Inches(0.25), "Процесс торговой компании · покрытие · v3", 10, False, MUTED)
    txt(slide, W - MX - Inches(1.4), H - Inches(0.34), Inches(1.4), Inches(0.25), "01 / 01", 10, False, MUTED, PP_ALIGN.RIGHT)

    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(out)
    print(f"Wrote {out}")


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    out = root / "content" / "business" / "slide-process-coverage.pptx"
    build(out)
    docs = root / "docs" / "business" / "slide-process-coverage.pptx"
    build(docs)
