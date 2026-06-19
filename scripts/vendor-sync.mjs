import { cpSync, mkdirSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const vendor = join(root, 'tilda-landing/assets/vendor');

const copies = [
  ['node_modules/aos/dist/aos.css', 'aos/aos.css'],
  ['node_modules/aos/dist/aos.js', 'aos/aos.js'],
  ['node_modules/lenis/dist/lenis.min.js', 'lenis/lenis.min.js'],
  [
    'node_modules/@fontsource-variable/plus-jakarta-sans/files/plus-jakarta-sans-latin-wght-normal.woff2',
    'fonts/plus-jakarta-sans-latin-wght-normal.woff2',
  ],
  [
    'node_modules/@fontsource-variable/commissioner/files/commissioner-latin-wght-normal.woff2',
    'fonts/commissioner-latin-wght-normal.woff2',
  ],
  [
    'node_modules/@fontsource-variable/commissioner/files/commissioner-cyrillic-wght-normal.woff2',
    'fonts/commissioner-cyrillic-wght-normal.woff2',
  ],
];

mkdirSync(vendor, { recursive: true });

for (const [from, to] of copies) {
  const src = join(root, from);
  const dest = join(vendor, to);
  if (!existsSync(src)) {
    console.warn(`skip missing: ${from}`);
    continue;
  }
  mkdirSync(dirname(dest), { recursive: true });
  cpSync(src, dest);
  console.log(`copied ${to}`);
}
