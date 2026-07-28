# Промо-ролик istock.link

Анимированный продуктовый тур для сайта (16:9, ~45 сек).

## Содержимое

| Файл | Назначение |
|------|------------|
| `docs/promo/product-tour.html` | Анимированные экраны (можно открыть с `?play=1`) |
| `docs/assets/videos/istocklink-product-tour.mp4` | Готовый ролик |
| `docs/assets/videos/poster-product-tour.png` | Постер |
| `tilda-landing/12-product-tour.html` | Блок для вставки на Тильду |
| `scripts/promo/record.mjs` | Пересъёмка ролика через Chrome + ffmpeg |

## Сцены

1. Интро — позиционирование платформы  
2. Потребности  
3. Согласование заявок  
4. Запросы и сравнение откликов  
5. Товарные позиции  
6. Контрагенты / квалификация / оценка  
7. Склад и приёмка  
8. Тендеры с агрегаторов  
9. Аутро

## Пересъёмка

Нужны `google-chrome`, `ffmpeg` и `puppeteer-core`:

```bash
npm install puppeteer-core --no-save
node scripts/promo/record.mjs
```
