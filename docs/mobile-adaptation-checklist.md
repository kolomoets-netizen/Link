# Mobile adaptation and spacing checklist

## Status

V tekuschem repozitorii net frontend-ishodnikov: otsutstvuyut HTML, CSS, React/Vue/Svelte/Next files, package manifest i design assets. Poetomu fakticheskie pravki mobilnoj versii vypolnit nelzya, poka ne budut dobavleny:

- kod stranicy ili prilozheniya;
- ssylka na maket;
- screenshots problemnyh ekranov;
- design tokens / UI-kit, esli oni est.

Etot dokument fiksiruet standart proverki, kotoryj nuzhno primenit pri pervoj vozmozhnosti.

## Target breakpoints

| Viewport | Purpose |
| --- | --- |
| 320px | Minimal mobile width, iPhone SE class |
| 360px | Typical narrow Android |
| 375px | Common iPhone width |
| 390-414px | Modern iPhone width |
| 768px | Tablet portrait |
| 1024px | Tablet landscape / small desktop |

## Spacing system

Rekomenduemaya shkala:

- 4px - micro gaps;
- 8px - compact inner gaps;
- 12px - form/control vertical gaps;
- 16px - base mobile padding;
- 20px - section inner padding on larger phones;
- 24px - card/section gap;
- 32px - major section gap.

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

## Mobile layout rules

### Page

- Net horizontal scroll at 320px.
- Body background reaches edges correctly.
- Page content has consistent left/right padding.
- Header and first content block do not collapse into each other.
- Bottom content is not hidden behind sticky footer/nav.

### Header

- Logo and menu controls fit into one row.
- Tap targets at least 44x44px.
- Mobile menu has safe-area padding.
- Header horizontal padding matches page container.
- Sticky header, if present, does not cover anchors/content.

### Hero / first screen

- H1 wraps without orphan words where possible.
- H1 line-height remains readable.
- CTA buttons stack vertically on narrow screens.
- Primary CTA is visible without horizontal scroll.
- Secondary links/buttons have at least 8-12px gap.

### Cards and lists

- Cards use `padding: 16px` on mobile.
- Gap between cards: 12-16px.
- Multi-column grids collapse to one column below 768px.
- Card titles do not overflow.
- Long IDs, tender numbers, URLs use wrapping rules.

Recommended:

```css
.card-title,
.tender-number,
.source-url {
  overflow-wrap: anywhere;
}
```

### Tables

Tables are risky on mobile. Use one of two patterns:

1. Convert rows to cards on mobile.
2. Keep table but wrap it in horizontal scroll container.

```css
.table-scroll {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}
```

If this product has tender lists, preferred mobile pattern is **card list**, not wide table.

### Forms

- Inputs full width on mobile.
- Label -> input gap: 6-8px.
- Field group gap: 12-16px.
- Submit button full width below 390px.
- Error text does not change layout aggressively.
- Date pickers and selects fit screen width.

### Buttons

- Minimum height: 44px.
- Horizontal padding: 16px.
- Gap between stacked buttons: 8-12px.
- Avoid two primary-sized buttons in one row below 390px.

### Modals / drawers

- On mobile, modal should become bottom sheet or full-screen dialog.
- Padding: 16px.
- Close button tap target at least 44x44px.
- Dialog max-height respects viewport.
- Content scrolls inside dialog without locking the page incorrectly.

### Sticky elements

- Account for mobile safe areas:

```css
.bottom-bar {
  padding-bottom: max(12px, env(safe-area-inset-bottom));
}
```

- Sticky CTA/footer should not hide final form fields.

## Tender-product specific mobile checks

### Tender card

Each card should show, in this order:

1. Status / deadline badge.
2. Tender title.
3. Price.
4. Customer.
5. Submission deadline.
6. Source / platform.
7. Responsible user or next action.

Avoid showing too many secondary metadata fields in the first viewport.

### Deduplication UI

If duplicate sources are shown:

- Show one canonical tender card.
- Put source badges in a horizontally wrapping row.
- Do not duplicate the whole tender card for every source.
- On mobile, source details should expand/collapse.

### Pipeline / kanban

Kanban columns are hard on mobile. Recommended mobile behavior:

- Replace full kanban with status tabs or vertical grouped list.
- Allow swipe only if there are clear affordances.
- Preserve quick action: change status, assign user, add comment.

## QA checklist

Run manual checks at:

- 320x568
- 360x740
- 375x812
- 390x844
- 414x896
- 768x1024

For each viewport:

- [ ] No horizontal scroll.
- [ ] Main container padding is consistent.
- [ ] Header does not overlap content.
- [ ] Buttons have 44px+ tap targets.
- [ ] Forms are usable with keyboard opened.
- [ ] Cards/lists have consistent vertical rhythm.
- [ ] Tables either collapse or scroll intentionally.
- [ ] Long tender titles/numbers/URLs wrap correctly.
- [ ] Sticky footer/header respects safe areas.
- [ ] Empty/loading/error states have same padding as content.

## Definition of done for future implementation

Mobile adaptation can be considered done when:

1. All key pages pass the QA checklist at 320px+.
2. Spacing uses a single scale, not one-off values.
3. Tender lists are readable without horizontal scroll.
4. Critical actions fit above the fold or are reachable with clear hierarchy.
5. Screenshots before/after are attached for the main mobile states.
