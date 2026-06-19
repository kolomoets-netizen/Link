# Чеклист мобильной адаптации и отступов

## Статус

В текущем репозитории нет frontend-исходников: отсутствуют HTML, CSS, React/Vue/Svelte/Next-файлы, package manifest и дизайн-ассеты. Поэтому фактические правки мобильной версии выполнить нельзя, пока не будут добавлены:

- код страницы или приложения;
- ссылка на макет;
- screenshots проблемных экранов;
- design tokens / UI-kit, если они есть.

Этот документ фиксирует стандарт проверки, который нужно применить при первой возможности.

## Целевые breakpoint'ы

| Viewport | Назначение |
| --- | --- |
| 320px | Минимальная мобильная ширина, iPhone SE class |
| 360px | Узкий Android |
| 375px | Частая ширина iPhone |
| 390-414px | Современные iPhone |
| 768px | Tablet portrait |
| 1024px | Tablet landscape / small desktop |

## Система отступов

Рекомендуемая шкала:

- 4px - микрозазоры;
- 8px - компактные внутренние зазоры;
- 12px - вертикальные зазоры в формах/контролах;
- 16px - базовый мобильный padding;
- 20px - внутренний padding секций на крупных телефонах;
- 24px - gap между карточками/секциями;
- 32px - крупный gap между смысловыми блоками.

Mobile container:

```css
.container {
  width: 100%;
  padding-inline: 16px;
}

@media (min-width: 390px) {
  .container {
    padding-inline: 20px;
  }
}
```

## Правила мобильного layout

### Страница

- Нет горизонтального скролла на 320px.
- Фон body корректно доходит до краев.
- Основной контент имеет единый левый/правый padding.
- Header и первый контентный блок не слипаются.
- Нижний контент не скрыт под sticky footer/nav.

### Header

- Логотип и menu controls помещаются в одну строку.
- Tap target не меньше 44x44px.
- Mobile menu учитывает safe-area padding.
- Горизонтальный padding header совпадает с page container.
- Sticky header, если есть, не перекрывает anchors/content.

### Hero / первый экран

- H1 переносится без критичных обрывов.
- H1 line-height остается читаемым.
- CTA-кнопки складываются вертикально на узких экранах.
- Primary CTA видна без горизонтального скролла.
- Между secondary links/buttons есть gap 8-12px.

### Карточки и списки

- Карточки используют `padding: 16px` на mobile.
- Gap между карточками: 12-16px.
- Multi-column grids схлопываются в одну колонку ниже 768px.
- Заголовки карточек не вылезают за контейнер.
- Длинные ID, номера тендеров и URL корректно переносятся.

Рекомендуемое правило:

```css
.card-title,
.tender-number,
.source-url {
  overflow-wrap: anywhere;
}
```

### Таблицы

Таблицы рискованны на mobile. Использовать один из двух паттернов:

1. Превращать строки в карточки на mobile.
2. Оставлять таблицу, но оборачивать ее в горизонтальный scroll container.

```css
.table-scroll {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}
```

Для списка тендеров предпочтительный mobile pattern - **card list**, а не широкая таблица.

### Формы

- Inputs full width на mobile.
- Label -> input gap: 6-8px.
- Field group gap: 12-16px.
- Submit button full width ниже 390px.
- Error text не должен резко ломать layout.
- Date pickers и selects помещаются в экран.

### Кнопки

- Минимальная высота: 44px.
- Горизонтальный padding: 16px.
- Gap между stacked buttons: 8-12px.
- Не ставить две крупные кнопки в один ряд ниже 390px.

### Modals / drawers

- На mobile modal должен становиться bottom sheet или full-screen dialog.
- Padding: 16px.
- Close button tap target не меньше 44x44px.
- Dialog max-height учитывает viewport.
- Контент скроллится внутри dialog без некорректной блокировки страницы.

### Sticky elements

- Учитывать mobile safe areas:

```css
.bottom-bar {
  padding-bottom: max(12px, env(safe-area-inset-bottom));
}
```

- Sticky CTA/footer не должен скрывать последние поля формы.

## Проверки, специфичные для tender-product

### Tender card

Каждая карточка должна показывать в таком порядке:

1. Status / deadline badge.
2. Название тендера.
3. Цена.
4. Заказчик.
5. Дедлайн подачи.
6. Источник / площадка.
7. Ответственный или следующее действие.

Не нужно показывать слишком много вторичных metadata fields в первом viewport.

### Deduplication UI

Если показываются duplicate sources:

- показывать одну canonical tender card;
- source badges выводить в строку с переносом;
- не дублировать всю карточку тендера для каждого источника;
- на mobile source details должны раскрываться/сворачиваться.

### Pipeline / kanban

Kanban columns сложны на mobile. Рекомендуемое поведение:

- заменить full kanban на status tabs или вертикальный grouped list;
- разрешать swipe только при понятных affordances;
- сохранить быстрые действия: change status, assign user, add comment.

## QA checklist

Проверять вручную на:

- 320x568;
- 360x740;
- 375x812;
- 390x844;
- 414x896;
- 768x1024.

Для каждого viewport:

- [ ] Нет горизонтального скролла.
- [ ] Main container padding консистентный.
- [ ] Header не перекрывает content.
- [ ] Buttons имеют tap target 44px+.
- [ ] Forms usable при открытой клавиатуре.
- [ ] Cards/lists имеют ровный vertical rhythm.
- [ ] Tables либо схлопываются, либо скроллятся намеренно.
- [ ] Длинные tender titles/numbers/URLs корректно переносятся.
- [ ] Sticky footer/header учитывает safe areas.
- [ ] Empty/loading/error states имеют такие же отступы, как основной content.

## Definition of done для будущей реализации

Мобильную адаптацию можно считать завершенной, когда:

1. Все ключевые страницы проходят QA checklist на 320px+.
2. Отступы используют единую шкалу, а не разовые значения.
3. Списки тендеров читаются без горизонтального скролла.
4. Критичные действия помещаются выше fold или имеют понятную иерархию.
5. Для основных mobile states приложены screenshots before/after.
