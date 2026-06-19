# Лендинг для Tilda

HTML-блоки для встраивания в Tilda через блок **T123 «HTML-код»**.

## Порядок блоков на странице

| № | Файл | Секция |
|---|------|--------|
| 1 | `01-hero.html` | Hero + мини-превью ленты |
| 2 | `06-integrations.html` | Поддерживаемые агрегаторы |
| 3 | `02-how-it-works.html` | Как работает (главная схема) |
| 4 | `07-crm-srm-kp.html` | Воронка торгов + поставщики + оцифровка КП |
| 5 | `03-features.html` | Возможности платформы |
| 6 | `08-crm-compare.html` | Сравнение с обычной CRM |
| 7 | `04-audience-pricing.html` | Стоимость платформы |
| 8 | `05-faq-cta.html` | FAQ + CTA |
| 0 | `00-enhancements-tilda.html` | *(опционально)* шрифт, анимации, плавный скролл |

## Анимации и шрифты (превью)

На GitHub Pages подключены библиотеки из npm:

- **Tilda Sans** — шрифт сайта (на Tilda подключается автоматически)
- **AOS** — появление блоков при скролле
- **Lenis** — плавная прокрутка

Сборка: `npm install && npm run build:preview`

Для Tilda вставьте `00-enhancements-tilda.html` **один раз** в Zero Block в начале страницы (CDN).

## Превью на планшете / телефоне

### Прототип интерфейса (не для Tilda)

**https://kolomoets-netizen.github.io/Link/prototype.html**

Единая лента + поиск + фильтры + источники. Файл: `tilda-landing/prototype-feed.html`

### Рабочая ссылка (GitHub Pages)

**https://kolomoets-netizen.github.io/Link/**

> Важно: в конце URL обязательно **`/Link/`** (с заглавной L).  
> Адрес `https://kolomoets-netizen.github.io/` без `/Link/` — это 404.

Откройте в Safari или Chrome на планшете — сервер не нужен.

**Если видите старую версию:**
1. Убедитесь, что изменения в ветке `main` на GitHub (деплой идёт только с `main`)
2. Подождите 2–5 минут после пуша — GitHub Actions собирает сайт
3. Обновите страницу с очисткой кэша: **Ctrl+Shift+R** (Windows) или **Cmd+Shift+R** (Mac)
4. На телефоне: закройте вкладку и откройте ссылку заново

### Баннеры

- Редактируемые SVG: `tilda-landing/banners/svg/` (6 вариантов)
- Готовые PNG-превью: `tilda-landing/banners/`
- На GitHub: `Link/tilda-landing/banners/svg/`

### Скачать файл

https://github.com/kolomoets-netizen/Link/raw/main/tilda-landing/preview-standalone.html

Скачайте → откройте в браузере планшета через «Файлы».

### Локально на компьютере

Файл `preview-standalone.html` — откройте двойным кликом.

## Как вставить в Tilda

1. Откройте редактор страницы → **Добавить блок** → **Другое** → **T123 HTML-код**
2. Скопируйте **весь** содержимое файла (включая `<style>`) и вставьте в блок
3. У блока в настройках отключите отступы сверху/снизу (0px), если нужен seamless-вид
4. Для якорей `#demo` и `#how` — в Tilda можно добавить Zero Block с id или привязать кнопки Tilda к якорям

## Кастомизация

- **Название продукта**: iStockLink — логотип в `assets/istocklink-icon.png`
- **Цены**: отредактируйте в `04-audience-pricing.html`
- **Форма CTA**: в `05-faq-cta.html` замените `action="#"` на URL формы Tilda или webhook (AmoCRM, Битрикс)
- **Цвет**: основной `#1c50de` — везде через CSS-переменную `--tg-primary`

## Цветовая палитра

| Роль | HEX |
|------|-----|
| Primary | `#1c50de` |
| Primary dark | `#153fb8` |
| Primary light | `#4d7aef` |
| Background | `#f4f7ff` |
| Text | `#0f172a` |
| Muted | `#64748b` |

## Адаптивность

Все блоки адаптивны (breakpoints 960px, 700px, 560px). На мобильных схема «Как работает» перестраивается в вертикальный поток.
