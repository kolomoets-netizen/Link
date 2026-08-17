#!/usr/bin/env node
/**
 * Builds 16:9 slide prototypes (эскизы) for the promo — ready to animate later.
 */
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "../..");
const outDir = path.join(root, "docs/promo/slides");
const shotDir = path.join(root, "docs/promo/screenshots");

const LOGO = `<svg class="mark" viewBox="0 0 31 32" fill="none" aria-hidden="true">
  <path d="M17.2 8.9V21.8H22.8C21.4 23.5 19.4 24.6 17.2 24.9V31.9C20 31.7 22.7 30.7 25 29.1C27.3 27.5 29.1 25.3 30.3 22.8V8.9H17.2Z" fill="#5B8AF5"/>
  <path d="M14.6 0C10.6.4 6.9 2.2 4.2 5.1C1.5 8.1 0 11.9 0 16s1.5 7.9 4.2 10.9C6.9 29.8 10.6 31.6 14.5 32V0Z" fill="#7DA2FF"/>
</svg>`;

const css = `
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');
:root {
  --bg0: #070b16;
  --bg1: #0f1a36;
  --primary: #1c50de;
  --glow: #3b6df0;
  --text: #f8fafc;
  --muted: #94a3b8;
  --line: rgba(255,255,255,0.12);
}
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body {
  width: 1920px; height: 1080px; overflow: hidden;
  font-family: "Plus Jakarta Sans", system-ui, sans-serif;
  background: var(--bg0); color: var(--text);
}
.slide {
  position: relative;
  width: 1920px; height: 1080px;
  overflow: hidden;
  background:
    radial-gradient(ellipse 70% 55% at 18% 20%, rgba(28,80,222,0.28), transparent 60%),
    radial-gradient(ellipse 60% 50% at 85% 85%, rgba(59,109,240,0.16), transparent 55%),
    linear-gradient(145deg, #070b16 0%, #0f1a36 50%, #0a1228 100%);
}
.slide::before {
  content: "";
  position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 64px 64px;
  mask-image: radial-gradient(ellipse at center, #000 25%, transparent 78%);
  opacity: 0.7; pointer-events: none;
}
.safe {
  position: relative; z-index: 1;
  width: 100%; height: 100%;
  padding: 72px 96px;
  display: flex; flex-direction: column;
}
.brand-row {
  display: flex; align-items: center; gap: 14px;
  font-weight: 800; font-size: 28px; letter-spacing: -0.03em;
}
.brand-row .mark { width: 36px; height: 37px; }
.brand-row .dot { color: #7da2ff; }
.meta {
  margin-left: auto;
  font-size: 14px; font-weight: 650; color: var(--muted);
  letter-spacing: 0.06em; text-transform: uppercase;
}
.center {
  flex: 1; display: flex; flex-direction: column;
  justify-content: center; align-items: flex-start;
  max-width: 1400px;
}
.eyebrow {
  display: inline-flex; align-items: center; gap: 10px;
  font-size: 15px; font-weight: 700; letter-spacing: 0.1em;
  text-transform: uppercase; color: #93b4ff; margin-bottom: 22px;
}
.eyebrow i {
  width: 8px; height: 8px; border-radius: 50%; background: #5b8af5;
  box-shadow: 0 0 0 5px rgba(91,138,245,0.22);
}
.headline {
  font-size: 88px; line-height: 1.05; font-weight: 800;
  letter-spacing: -0.04em; max-width: 1500px;
}
.headline.sm { font-size: 64px; }
.sub {
  margin-top: 24px; font-size: 28px; line-height: 1.4;
  color: rgba(226,232,240,0.78); max-width: 900px; font-weight: 500;
}
.footer {
  display: flex; align-items: center; justify-content: space-between;
  color: var(--muted); font-size: 15px; font-weight: 600;
}
.progress {
  width: 280px; height: 3px; background: rgba(255,255,255,0.1);
  border-radius: 99px; overflow: hidden;
}
.progress > i { display: block; height: 100%; background: linear-gradient(90deg, #1c50de, #7da2ff); }

/* UI composition slides */
.ui-layout {
  flex: 1; display: grid; grid-template-columns: 520px 1fr;
  gap: 40px; align-items: center; min-height: 0; padding: 20px 0;
}
.ui-copy .headline { font-size: 48px; }
.ui-copy .sub { font-size: 22px; margin-top: 16px; }
.ui-frame {
  background: #fff; border-radius: 18px; overflow: hidden;
  box-shadow: 0 40px 100px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,255,255,0.08);
  height: 760px; display: flex; flex-direction: column;
}
.ui-frame img {
  width: 100%; height: 100%; object-fit: cover; object-position: top left;
  display: block;
}
.chrome {
  height: 36px; background: #f1f5f9; border-bottom: 1px solid #e2e8f0;
  display: flex; align-items: center; gap: 6px; padding: 0 14px; flex-shrink: 0;
}
.chrome span { width: 9px; height: 9px; border-radius: 50%; }
.chrome .r { background: #ff5f57; }
.chrome .y { background: #febc2e; }
.chrome .g { background: #28c840; }
.chrome .url {
  margin-left: 10px; flex: 1; height: 20px; border-radius: 6px;
  background: #fff; border: 1px solid #e2e8f0;
  font-size: 11px; color: #64748b; display: flex; align-items: center; padding: 0 8px;
  font-weight: 600;
}

/* Motion hints (эскиз notes — not visible in export if .hint hidden, keep subtle) */
.hint {
  position: absolute; right: 96px; bottom: 110px; z-index: 2;
  padding: 10px 14px; border-radius: 10px;
  background: rgba(15,23,42,0.55); border: 1px dashed rgba(147,180,255,0.35);
  color: #93b4ff; font-size: 13px; font-weight: 650; max-width: 360px;
  line-height: 1.35;
}

.outro-cta {
  margin-top: 36px; display: inline-flex; align-items: center;
  padding: 16px 26px; border-radius: 14px; font-size: 22px; font-weight: 750;
  background: linear-gradient(135deg, #1c50de, #3b6df0);
  box-shadow: 0 18px 40px rgba(28,80,222,0.35);
}
`;

function shell({ id, meta, body, progress = 0, hint = "" }) {
  return `<!DOCTYPE html>
<html lang="ru"><head>
<meta charset="UTF-8"/>
<title>${id}</title>
<style>${css}</style>
</head><body>
<section class="slide" data-slide="${id}">
  <div class="safe">
    <div class="brand-row">
      ${LOGO}
      <div>istock<span class="dot">.link</span></div>
      <div class="meta">${meta}</div>
    </div>
    ${body}
    <div class="footer">
      <div class="progress"><i style="width:${progress}%"></i></div>
      <div>${id}</div>
    </div>
  </div>
  ${hint ? `<div class="hint">motion: ${hint}</div>` : ""}
</section>
</body></html>`;
}

function phraseSlide({ id, eyebrow, headline, sub, progress, hint, sm = false }) {
  return shell({
    id,
    meta: "фраза",
    progress,
    hint,
    body: `<div class="center">
      ${eyebrow ? `<div class="eyebrow"><i></i>${eyebrow}</div>` : ""}
      <h1 class="headline${sm ? " sm" : ""}">${headline}</h1>
      ${sub ? `<p class="sub">${sub}</p>` : ""}
    </div>`,
  });
}

function uiSlide({ id, eyebrow, headline, sub, img, url, progress, hint }) {
  return shell({
    id,
    meta: "ui · возможность",
    progress,
    hint,
    body: `<div class="ui-layout">
      <div class="ui-copy">
        <div class="eyebrow"><i></i>${eyebrow}</div>
        <h1 class="headline">${headline}</h1>
        <p class="sub">${sub}</p>
      </div>
      <div class="ui-frame">
        <div class="chrome"><span class="r"></span><span class="y"></span><span class="g"></span>
          <div class="url">${url}</div>
        </div>
        <img src="../screenshots/${img}" alt=""/>
      </div>
    </div>`,
  });
}

const slides = {
  "00-teaser-chaos": phraseSlide({
    id: "00-teaser-chaos",
    eyebrow: "Затравка",
    headline: "Закупки без хаоса.",
    sub: "Цифровая платформа для закупочного контура",
    progress: 4,
    hint: "punch-in текста 95→100%, hold 2с, hard cut",
  }),
  "01-teaser-demand": phraseSlide({
    id: "01-teaser-demand",
    eyebrow: "Затравка",
    headline: "Спрос — под контролем.",
    progress: 8,
    hint: "появление на snare, без fade",
  }),
  "02-teaser-cycle": phraseSlide({
    id: "02-teaser-cycle",
    eyebrow: "Затравка",
    headline: "Один контур. Весь цикл.",
    progress: 12,
    hint: "две строки stagger 80мс",
  }),
  "03-phrase-needs": phraseSlide({
    id: "03-phrase-needs",
    eyebrow: "Потребности",
    headline: "Спрос из подразделений — в одном окне",
    sub: "Статусы, фильтры и приоритеты",
    progress: 18,
    sm: true,
    hint: "cut → UI needs",
  }),
  "04-ui-needs": uiSlide({
    id: "04-ui-needs",
    eyebrow: "Потребности",
    headline: "Спрос — в одном окне",
    sub: "Пайплайн: новая → в работе → закупка",
    img: "01-needs.png",
    url: "app.istock.link / Потребности",
    progress: 24,
    hint: "slow zoom в чип «Новая»",
  }),
  "05-phrase-approval": phraseSlide({
    id: "05-phrase-approval",
    eyebrow: "Согласование",
    headline: "Согласование по маршруту, не в переписке",
    sub: "Ответственные на каждом шаге",
    progress: 30,
    sm: true,
    hint: "cut на snare",
  }),
  "06-ui-approval": uiSlide({
    id: "06-ui-approval",
    eyebrow: "Согласование",
    headline: "Маршрут заявки",
    sub: "От старта до публикации — прозрачно",
    img: "03-approval-flow.png",
    url: "app.istock.link / Согласование",
    progress: 36,
    hint: "pan слева направо по стрелкам",
  }),
  "07-phrase-requests": phraseSlide({
    id: "07-phrase-requests",
    eyebrow: "Запросы",
    headline: "Запросы и отклики — сравнивайте сразу",
    sub: "Цены и условия в одной таблице",
    progress: 42,
    sm: true,
    hint: "clap accent",
  }),
  "08-ui-compare": uiSlide({
    id: "08-ui-compare",
    eyebrow: "Сравнение",
    headline: "Лучшее предложение — сразу видно",
    sub: "Отклики поставщиков рядом",
    img: "05-compare-offers.png",
    url: "app.istock.link / Сравнение откликов",
    progress: 48,
    hint: "highlight колонки best",
  }),
  "09-phrase-products": phraseSlide({
    id: "09-phrase-products",
    eyebrow: "Товары",
    headline: "Каждая позиция — под контролем",
    sub: "Актуальный статус по всем закупкам",
    progress: 54,
    sm: true,
    hint: "808 hint",
  }),
  "10-ui-products": uiSlide({
    id: "10-ui-products",
    eyebrow: "Товары",
    headline: "Статус каждой позиции",
    sub: "От закупки до доставки",
    img: "06-products.png",
    url: "app.istock.link / Товары",
    progress: 60,
    hint: "pan по статусам",
  }),
  "11-phrase-suppliers": phraseSlide({
    id: "11-phrase-suppliers",
    eyebrow: "Поставщики",
    headline: "Реестр, квалификация, оценка",
    sub: "Контрагенты в одном контуре",
    progress: 66,
    sm: true,
    hint: "brass stab",
  }),
  "12-ui-suppliers": uiSlide({
    id: "12-ui-suppliers",
    eyebrow: "Поставщики",
    headline: "Квалификация и оценка",
    sub: "Прозрачные процедуры",
    img: "08-qualification.png",
    url: "app.istock.link / Квалификация",
    progress: 72,
    hint: "hard cut qualification→evaluation later",
  }),
  "13-phrase-warehouse": phraseSlide({
    id: "13-phrase-warehouse",
    eyebrow: "Склад",
    headline: "Склад связан с закупкой",
    sub: "Приёмка, резервирование, запасы",
    progress: 78,
    sm: true,
    hint: "hat roll",
  }),
  "14-ui-receiving": uiSlide({
    id: "14-ui-receiving",
    eyebrow: "Склад",
    headline: "Приёмка на склад",
    sub: "План и факт в одной операции",
    img: "10-receiving.png",
    url: "app.istock.link / Приёмка",
    progress: 84,
    hint: "акцент на кнопку «Принять»",
  }),
  "15-phrase-tenders": phraseSlide({
    id: "15-phrase-tenders",
    eyebrow: "Тендеры",
    headline: "Тендеры с агрегаторов — в воронку",
    sub: "Лента и доска сделок",
    progress: 90,
    sm: true,
    hint: "pre-drop riser",
  }),
  "16-ui-tenders": uiSlide({
    id: "16-ui-tenders",
    eyebrow: "Тендеры",
    headline: "Воронка команды",
    sub: "От ленты до сделки",
    img: "11-tenders-board.png",
    url: "app.istock.link / Тендеры",
    progress: 94,
    hint: "DROP — punch zoom на kanban",
  }),
  "17-outro": phraseSlide({
    id: "17-outro",
    eyebrow: "istock.link",
    headline: "От потребности до склада — в одной системе",
    sub: `<span class="outro-cta">Узнать больше</span>`,
    progress: 100,
    sm: true,
    hint: "logo lockup + final hit, hold",
  }),
};

async function main() {
  await mkdir(outDir, { recursive: true });
  // ensure screenshots reachable via relative path
  for (const [name, html] of Object.entries(slides)) {
    await writeFile(path.join(outDir, `${name}.html`), html);
  }

  const indexItems = Object.keys(slides)
    .map((k) => `<a href="${k}.html"><img src="png/${k}.png" alt=""/><span>${k}</span></a>`)
    .join("\n");

  await writeFile(
    path.join(outDir, "index.html"),
    `<!DOCTYPE html><html lang="ru"><head><meta charset="UTF-8"/><title>Эскизы слайдов</title>
<style>
body{margin:0;font-family:system-ui;background:#0b1224;color:#e2e8f0;padding:32px}
h1{font-size:28px;margin:0 0 8px}
p{color:#94a3b8;margin:0 0 28px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px}
a{display:block;background:#111827;border:1px solid rgba(255,255,255,.08);border-radius:12px;overflow:hidden;color:#93b4ff;text-decoration:none}
a img{width:100%;aspect-ratio:16/9;object-fit:cover;background:#000;display:block}
a span{display:block;padding:10px 12px;font-size:13px;font-weight:650}
</style></head><body>
<h1>Эскизы слайдов промо istock.link</h1>
<p>18 кадров 16:9 — фразы и UI. PNG в папке png/. Подсказки motion на каждом слайде.</p>
<div class="grid">${indexItems}</div>
</body></html>`
  );

  await writeFile(
    path.join(outDir, "README.md"),
    `# Эскизы слайдов (для оживления)

18 прототипов кадров 16:9 под сценарий \`docs/promo/SCRIPT.md\`.

## Структура

| Тип | Слайды | Потом оживить |
|-----|--------|----------------|
| Затравка | 00–02 | punch text, hard cuts на snare |
| Фраза → UI | 03–16 | phrase hold → cut → UI zoom/pan |
| Аутро | 17 | logo + CTA |

## Файлы

- HTML-эскизы: \`*.html\` (с подсказкой \`motion:\` в углу)
- PNG: \`png/*.png\`
- Индекс: \`index.html\`

## Пересъёмка PNG

\`\`\`bash
node scripts/promo/capture-slides.mjs
\`\`\`
`
  );

  console.log("Built", Object.keys(slides).length, "slides →", outDir);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
