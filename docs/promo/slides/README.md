# Эскизы слайдов (для оживления)

18 прототипов кадров 16:9 под сценарий `docs/promo/SCRIPT.md`.

## Структура

| Тип | Слайды | Потом оживить |
|-----|--------|----------------|
| Затравка | 00–02 | punch text, hard cuts на snare |
| Фраза → UI | 03–16 | phrase hold → cut → UI zoom/pan |
| Аутро | 17 | logo + CTA |

## Файлы

- HTML-эскизы: `*.html` (с подсказкой `motion:` в углу)
- PNG: `png/*.png`
- Индекс: `index.html`

## Пересъёмка PNG

```bash
node scripts/promo/capture-slides.mjs
```
