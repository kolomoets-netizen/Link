import { readFileSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execSync } from 'node:child_process';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const base = join(root, 'tilda-landing');
const REF = '6290d63';

const mergeFiles = [
  '01-hero.html',
  '02-how-it-works.html',
  '03-features.html',
  '06-integrations.html',
  '07-crm-srm-kp.html',
];

function gitShow(path) {
  return execSync(`git show ${REF}:${path}`, { cwd: root, encoding: 'utf-8' });
}

function extractStyle(html) {
  const m = html.match(/<style>([\s\S]*?)<\/style>/);
  return m ? m[1] : '';
}

function extractBody(html) {
  const m = html.match(/<\/style>\s*([\s\S]*)$/);
  return m ? m[1].trim() : html;
}

for (const name of mergeFiles) {
  const oldHtml = gitShow(`tilda-landing/${name}`);
  const curHtml = readFileSync(join(base, name), 'utf-8');
  let style = extractStyle(oldHtml);
  let body = extractBody(curHtml);

  if (name === '07-crm-srm-kp.html') {
    const curStyle = extractStyle(curHtml);
    const kanbanRules = curStyle.match(/\.tg-kanban-col[\s\S]*?min-height: 188px[\s\S]*?\.tg-kanban-card[\s\S]*?min-height: 72px[\s\S]*?\.tg-pillar-list li \{[\s\S]*?font-size: 14px;/);
    if (kanbanRules) {
      style = style
        .replace(/min-height: 156px/, 'min-height: 188px')
        .replace(/padding: 10px 10px 12px/, 'padding: 12px 12px 14px')
        .replace(/padding: 8px 8px;\s*font-size: 9px/, 'padding: 12px 11px;\n    font-size: 11px')
        .replace(/min-height: 48px/, 'min-height: 72px')
        .replace(/font-size: 9px; font-weight: 700; line-height: 1\.25/, 'font-size: 12px; font-weight: 700; line-height: 1.3')
        .replace(/font-size: 8px; font-weight: 500; line-height: 1\.3/, 'font-size: 10px; font-weight: 500; line-height: 1.35')
        .replace(/min-height: 160px/, 'min-height: 188px')
        .replace(/min-height: 52px/, 'min-height: 68px');
      style = style.replace(
        /\.tg-pillar-list li \{[^}]+\}/,
        '.tg-pillar-list li {\n    font-size: 14px; color: #475569;\n    padding: 5px 0 5px 18px; position: relative;\n  }'
      );
    }
  }

  if (name === '02-how-it-works.html') {
    style = style.replace(
      /\.tg-step-title \{[^}]+\}/,
      '.tg-step-title { font-size: 17px; font-weight: 600; color: var(--tg-text); margin: 0 0 8px; }'
    ).replace(
      /\.tg-step-text \{[^}]+\}/,
      '.tg-step-text { font-size: 14px; line-height: 1.6; color: #64748b; margin: 0; }'
    );
  }

  const out = `<!-- Tilda block -->\n<style>${style}</style>\n\n${body}\n`;
  writeFileSync(join(base, name), out.replace('<!-- Tilda block -->\n', `<!-- ${name.replace('.html', '')} -->\n`.replace('01-hero', 'Tilda block: Hero').replace('02-how-it-works', 'Tilda block: How it works').replace('03-features', 'Tilda block: Features').replace('06-integrations', 'Tilda block: Aggregators strip').replace('07-crm-srm-kp', 'Tilda block: Воронка + поставщики + КП')), 'utf-8');
  console.log('merged', name);
}

// Fix first line comments properly
const comments = {
  '01-hero.html': '<!-- Tilda block: Hero -->',
  '02-how-it-works.html': '<!-- Tilda block: How it works -->',
  '03-features.html': '<!-- Tilda block: Features -->',
  '06-integrations.html': '<!-- Tilda block: Aggregators strip -->',
  '07-crm-srm-kp.html': '<!-- Tilda block: Воронка + поставщики + КП -->',
};
for (const [name, comment] of Object.entries(comments)) {
  let html = readFileSync(join(base, name), 'utf-8');
  html = html.replace(/^<!--[\s\S]*?-->/, comment);
  writeFileSync(join(base, name), html, 'utf-8');
}

console.log('done');
