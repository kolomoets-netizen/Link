import { readFileSync, writeFileSync, cpSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execSync } from 'node:child_process';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const base = join(root, 'tilda-landing');
const docs = join(root, 'docs');

function getBuildId() {
  if (process.env.GITHUB_SHA) return process.env.GITHUB_SHA.slice(0, 7);
  try {
    return execSync('git rev-parse --short HEAD', { cwd: root, encoding: 'utf-8' }).trim();
  } catch {
    return String(Date.now());
  }
}

const buildId = getBuildId();
const buildDate = new Date().toISOString().slice(0, 10);

const blocks = [
  '01-hero.html',
  '09-audience-positioning.html',
  '07-crm-srm-kp.html',
  '02-how-it-works.html',
  '08-crm-compare.html',
  '11-pricing-value.html',
  '06-director-case-proof.html',
  '05-faq-cta.html',
];

const body = blocks
  .map((name) => readFileSync(join(base, name), 'utf-8').trim())
  .join('\n\n');

const html = `<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta name="build" content="${buildId}">
<title>iStockLink</title>
<link rel="stylesheet" href="https://static.tildacdn.com/css/fonts-tildasans.css">
<link rel="stylesheet" href="assets/vendor/aos/aos.css?v=${buildId}">
<link rel="stylesheet" href="assets/enhancements.css?v=${buildId}">
<style>
  body{margin:0}
  .tg-preview-bar{
    position:sticky;top:0;z-index:9999;
    padding:8px 16px;text-align:center;font-size:13px;font-weight:600;
    background:#1c50de;color:#fff;font-family:'TildaSans',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
    border-bottom:1px solid rgba(255,255,255,.2);
  }
  .tg-preview-bar a{color:#dbeafe}
</style>
</head>
<body>
<div class="tg-preview-bar">Превью GitHub Pages · Tilda Sans · сборка ${buildDate} (${buildId}) · <a href="https://github.com/kolomoets-netizen/Link/tree/main/tilda-landing">блоки для Tilda</a></div>
${body}
<script src="assets/vendor/lenis/lenis.min.js?v=${buildId}"></script>
<script src="assets/vendor/aos/aos.js?v=${buildId}"></script>
<script src="assets/enhancements.js?v=${buildId}"></script>
</body>
</html>
`;

writeFileSync(join(base, 'preview-standalone.html'), html, 'utf-8');
writeFileSync(join(docs, 'index.html'), html, 'utf-8');
writeFileSync(join(docs, 'preview-standalone.html'), html, 'utf-8');

const docsAssets = join(docs, 'assets');
mkdirSync(docsAssets, { recursive: true });
cpSync(join(base, 'assets'), docsAssets, { recursive: true });

const extraPages = [
  'pricing-value-variants.html',
  '11-pricing-value-v1.html',
  '11-pricing-value-v2.html',
  '11-pricing-value-v3.html',
];
for (const name of extraPages) {
  cpSync(join(base, name), join(docs, name));
}

const redirect404 = `<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>iStockLink</title>
  <meta http-equiv="refresh" content="0;url=./">
  <style>
    body { font-family: Arial, sans-serif; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; background: #f4f7ff; color: #1c50de; text-align: center; padding: 24px; }
    a { color: #1c50de; }
  </style>
</head>
<body>
  <p>Страница не найдена. <a href="./">Перейти на лендинг iStockLink</a></p>
</body>
</html>
`;
writeFileSync(join(docs, '404.html'), redirect404, 'utf-8');

console.log('built preview-standalone.html, docs/index.html and docs/preview-standalone.html');
