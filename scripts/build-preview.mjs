import { readFileSync, writeFileSync, cpSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const base = join(root, 'tilda-landing');
const docs = join(root, 'docs');

const blocks = [
  '01-hero.html',
  '06-integrations.html',
  '02-how-it-works.html',
  '07-crm-srm-kp.html',
  '03-features.html',
  '08-crm-compare.html',
  '04-audience-pricing.html',
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
<title>iStockLink</title>
<link rel="stylesheet" href="assets/vendor/aos/aos.css">
<link rel="stylesheet" href="assets/enhancements.css">
<style>body{margin:0}</style>
</head>
<body>
${body}
<script src="assets/vendor/lenis/lenis.min.js"></script>
<script src="assets/vendor/aos/aos.js"></script>
<script src="assets/enhancements.js"></script>
</body>
</html>
`;

writeFileSync(join(base, 'preview-standalone.html'), html, 'utf-8');
writeFileSync(join(docs, 'index.html'), html, 'utf-8');
writeFileSync(join(docs, 'preview-standalone.html'), html, 'utf-8');

const docsAssets = join(docs, 'assets');
mkdirSync(docsAssets, { recursive: true });
cpSync(join(base, 'assets'), docsAssets, { recursive: true });

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
