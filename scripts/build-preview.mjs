import { readFileSync, writeFileSync, cpSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const base = join(root, 'tilda-landing');

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
writeFileSync(join(root, 'docs/index.html'), html, 'utf-8');

const docsAssets = join(root, 'docs/assets');
mkdirSync(docsAssets, { recursive: true });
cpSync(join(base, 'assets/enhancements.css'), join(docsAssets, 'enhancements.css'));
cpSync(join(base, 'assets/enhancements.js'), join(docsAssets, 'enhancements.js'));
cpSync(join(base, 'assets/vendor'), join(docsAssets, 'vendor'), { recursive: true });
console.log('built preview-standalone.html and docs/index.html');
