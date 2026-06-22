import { readFileSync, writeFileSync, cpSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const base = join(root, 'tilda-landing');
const docs = join(root, 'docs');

const labels = [
  ['01 — Hero', '01-hero.html'],
  ['06 — Интеграции', '06-integrations.html'],
  ['02 — Как работает', '02-how-it-works.html'],
  ['07 — CRM · SRM · КП', '07-crm-srm-kp.html'],
  ['03 — Возможности', '03-features.html'],
  ['08 — Сравнение с CRM', '08-crm-compare.html'],
  ['04 — Тарифы', '04-audience-pricing.html'],
  ['05 — CTA', '05-faq-cta.html'],
];

const body = labels
  .map(([label, file]) => {
    const html = readFileSync(join(base, file), 'utf-8').trim();
    return `<div class="preview-label">${label}</div>\n${html}`;
  })
  .join('\n\n');

const shell = (inner) => `<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>iStockLink — превью лендинга</title>
  <style>
    body { margin: 0; background: #e8edf5; }
    .preview-bar {
      position: sticky; top: 0; z-index: 99999;
      background: #0f172a; color: #fff;
      padding: 12px 16px;
      font-family: system-ui, sans-serif;
      font-size: 13px;
      text-align: center;
    }
    .preview-bar strong { color: #7aa2ff; }
    .preview-label {
      background: #1c50de; color: #fff;
      padding: 8px 16px; font-size: 11px; font-weight: 700;
      letter-spacing: 0.06em; text-transform: uppercase;
      font-family: system-ui, sans-serif;
    }
  </style>
</head>
<body>
  <div class="preview-bar"><strong>iStockLink</strong> · превью лендинга</div>
${inner}
</body>
</html>
`;

const html = shell(body);
writeFileSync(join(base, 'preview-standalone.html'), html, 'utf-8');
mkdirSync(docs, { recursive: true });
writeFileSync(join(docs, 'index.html'), html, 'utf-8');
