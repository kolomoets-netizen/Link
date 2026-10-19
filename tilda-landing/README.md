# Лендинг для Tilda

HTML-блоки для встраивания в Tilda через блок **T123 «HTML-код»**.

## Важно: превью ≠ сайт на Tilda

| Где смотрите | Что нужно сделать |
|--------------|-------------------|
| **GitHub Pages** (превью) | Откройте **https://kolomoets-netizen.github.io/Link/** — обновляется автоматически после пуша в `main` |
| **Сайт на Tilda** | Изменения **не появятся сами** — скопируйте обновлённые файлы из `tilda-landing/` в блоки T123 на странице |

**Как понять, что превью свежее:** вверху страницы синяя полоска «Превью GitHub Pages · сборка … · тарифы от 6 000 ₽».

**Правильный URL превью:** `https://kolomoets-netizen.github.io/Link/` (с `/Link/` в конце). Без `/Link/` будет 404.

**Только последние правки `/trading`:** [preview-trading-changes.html](https://kolomoets-netizen.github.io/Link/preview-trading-changes.html) — блоки «Как работает», сравнение CRM и переход с Битрикса.

**Зонтик главной + страница `/crm`:** [preview-home-crm.html](https://kolomoets-netizen.github.io/Link/preview-home-crm.html) — блоки `15–17` (главная) и `20–25` (`/crm`). Инструкция: `docs/positioning/tilda-homepage-edit-guide.md`.

**Жёсткое обновление:** Ctrl+Shift+R (Win) / Cmd+Shift+R (Mac).

## Порядок блоков на `/trading`

| № | Файл | Секция |
|---|------|--------|
| 1 | `01-hero.html` | Hero |
| 2 | `09-audience-positioning.html` | Позиционирование и ЦА |
| 3 | `07-crm-srm-kp.html` | Вся тендерная работа в iStockLink |
| 3a | `08-kontur-search-widget.html` | Виджет Контур.Закупки (iframe) |
| 4 | `02-how-it-works.html` | Как это работает |
| 5 | `08-crm-compare.html` | Сравнение: Excel, Битрикс, поиск тендеров, iStockLink |
| 5b | `14-bitrix-switch-promo.html` | Переход с Битрикс24: −50% на год, старт за день |
| 6 | `11-pricing-value.html` | Стоимость: ценность, от 1 260 ₽, ссылка на тарифы |
| 7 | `04-audience-pricing.html` | *(опционально)* три карточки тарифов с переключателем |
| 8 | `06-director-case-proof.html` | Подтверждённый пример директора торговой компании |
| 8b | `06-industrial-case-proof.html` | Кейс: промышленная компания, снабжение |
| 8 | `10-seldon-email-preview.html` | Превью письма для поставщиков (Seldon) |
| 9 | `05-faq-cta.html` | CTA «Подключите iStockLink за 2 минуты» |
| 0 | `00-enhancements-tilda.html` | *(опционально)* плавный скролл и анимации — **в конце страницы** |

## Главная (зонтик) — вставка T123

| № | Файл | Куда |
|---|------|------|
| 1 | `15-home-umbrella-bridge.html` | После hero |
| 2 | `16-home-pillars.html` | Ниже |
| 3 | `17-home-process.html` | Ниже |

Плюс в меню Tilda: пункт **CRM** → `/crm`.

## Страница `/crm` — порядок T123

| № | Файл | Секция |
|---|------|--------|
| 1 | `20-crm-hero.html` | Hero модуля |
| 2 | `21-crm-for-whom.html` | Для кого |
| 3 | `22-crm-capabilities.html` | Возможности CRM |
| 4 | `23-crm-srm-bridge.html` | Мост в SRM |
| 5 | `24-crm-compare.html` | Сравнение (без −50%) |
| 6 | `25-crm-boundaries-cta.html` | Кому не подходит + CTA |

Архив (не в сборке): `archive/03-features.html`, `archive/06-integrations.html`

## Анимации и шрифты (превью)

На GitHub Pages подключены библиотеки из npm:

- **Plus Jakarta Sans** — шрифт превью (AOS + Lenis)
- **AOS** — появление блоков при скролле
- **Lenis** — плавная прокрутка

Сборка: `npm install && npm run build:preview`

Для Tilda вставьте `00-enhancements-tilda.html` **один раз** в Zero Block **в конце страницы** (после всех T123-блоков). CDN.

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

## Блок «Кто может стать партнером» (`13-partner-audience-cards.html`)

**Страница:** https://istock.link/partneristocklink — заменяет стандартные карточки Tilda (T123).

Три карточки с **фоновым фото** и синим оверлеем; заголовок внизу, при наведении — текст и кнопка **«Стать партнером»** → `#PartnerForm`. Фоны: `assets/partner-audience/*.jpg` (интеграторы, консультанты, блогеры).

**Превью:** https://kolomoets-netizen.github.io/Link/preview-partner-audience.html

## Блок «Партнёры» (`12-partners-grid.html`)

**Страница:** https://istock.link/partneristocklink — вставьте T123 (например, перед футером или после блока про вознаграждение).

**Сетка:** 8 плиток — Контур, Селдон, СБИС, Албато, ПроАйти, MatrixN, Os24, Тендертех (файлы в `assets/partners/`).

**Логотипы:** лежат в `tilda-landing/assets/partners/` (+ `kontur.png` на GitHub Pages в `assets/`). **В Tilda:** можно оставить ссылки на `kolomoets-netizen.github.io/Link/assets/...` — они работают в T123. Для автономности загрузите те же файлы в **Контент сайта → Файлы**, скопируйте URL с `static.tildacdn.com` и замените `src` у каждого `<img>` в блоке.

**Превью:** https://kolomoets-netizen.github.io/Link/preview-partners-grid.html

## SEO страницы `/trading` (Title, Description, OG)

Мета-теги **не в HTML-блоках** — только в Tilda: настройки страницы «Торговые компanies» → SEO. Подробно: [docs/tilda-trading-seo.md](../docs/tilda-trading-seo.md).

## Блок «Переход с Битрикс24» (`14-bitrix-switch-promo.html`)

**Куда ставить на `/trading`:** сразу после `08-crm-compare.html` (логично после сравнения с CRM).

**Смысл:** оффер «за день», бесплатный период, **−50% на год** при переходе с Битрикс24. CTA ведёт на `#demo` — привяжите к вашей форме/якорю на Tilda.

## Блок «Поиск Контур» (`08-kontur-search-widget.html`)

**Куда ставить на `/trading`:** после секции «Агрегаторы / Сбор» или сразу после блока «Как это работает» (шаг «Подключите агрегаторы») — так виджет логично продолжает тему источников закупок.

**Смысл:** для аудитории «только поиск» — виджет партнёра Контур.Закупки без CTA на CRM в этом блоке.

**Превью только этого блока (страница в браузере):** https://kolomoets-netizen.github.io/Link/preview-kontur-widget.html — после push в `main` подождите 1–2 мин и обновите **Ctrl+Shift+R**. В шапке превью указана дата сборки; код для Tilda — отдельная ссылка «код для Tilda», не открывайте `raw`/`cdn.jsdelivr` для просмотра (там HTML как текст).

## Как вставить в Tilda

**Копируйте код с GitHub Pages** (обновляется вместе с превью, без кэша `raw.githubusercontent.com`):

**https://kolomoets-netizen.github.io/Link/tilda-blocks/**

- `02-how-it-works.html` — «Как работает», кнопка агрегатора  
- `08-crm-compare.html` — сравнение с CRM  
- `14-bitrix-switch-promo.html` — переход с Битрикс24  

Альтернатива: файлы в репозитории `tilda-landing/*.html` (ветка `main`).

1. Откройте редактор страницы → **Добавить блок** → **Другое** → **T123 HTML-код**
2. Скопируйте **весь** код из ссылки выше (включая `<style>` и первую строку-комментарий с `build …`) и вставьте в блок
3. У блока в настройках отключите отступы сверху/снизу (0px), если нужен seamless-вид
4. Для якорей `#demo` и `#how` — в Tilda можно добавить Zero Block с id или привязать кнопки Tilda к якорям

## Кастомизация

- **Название продукта**: iStockLink — логотип в `assets/istocklink-icon.png`
- **Цены**: отредактируйте в `04-audience-pricing.html`
- **Форма CTA**: в `05-faq-cta.html` замените `action="#"` на URL формы Tilda или webhook (AmoCRM, Битрикс)
- **Кейс директора**: фото в `06-director-case-proof.html` — замените `case-director.svg` на реальное фото; полное интервью — `docs/blog/interview-director.html`
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
