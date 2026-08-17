#!/usr/bin/env node
/**
 * Builds anonymized high-fidelity HTML screens matching istock.link UI.
 */
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const outDir = path.resolve(__dirname, "../../docs/promo/screens");

const LOGO = `<svg viewBox="0 0 31 32" fill="none" aria-hidden="true"><path d="M17.2 8.9V21.8H22.8C21.4 23.5 19.4 24.6 17.2 24.9V31.9C20 31.7 22.7 30.7 25 29.1C27.3 27.5 29.1 25.3 30.3 22.8V8.9H17.2Z" fill="#1C50DE"/><path d="M14.6 0C10.6.4 6.9 2.2 4.2 5.1C1.5 8.1 0 11.9 0 16s1.5 7.9 4.2 10.9C6.9 29.8 10.6 31.6 14.5 32V0Z" fill="#1C50DE"/></svg>`;

function topbar() {
  return `<header class="topbar">
  <div class="logo">${LOGO} istock<span class="dot">.link</span></div>
  <div class="tabs"><span class="tab active">ЭТП</span><span class="tab">Маркетплейс</span></div>
  <div class="top-right">
    <div class="company-sel">ОРБИТА</div>
    <div class="role-switch"><span class="on">Покупатель</span><span>Поставщик</span></div>
    <div class="icon-btn">✉</div>
    <div class="icon-btn">⚙</div>
    <div class="icon-btn">💬<span class="ping">3</span></div>
    <div class="avatar">АП</div>
  </div>
</header>`;
}

function sidebar(active) {
  const item = (id, label, badge) =>
    `<div class="nav-item${active === id ? " active" : ""}"><span class="left"><span class="ico">▪</span>${label}</span>${badge ? `<span class="badge">${badge}</span>` : ""}</div>`;
  return `<aside class="sidebar">
  <div class="nav-group">
    <div class="nav-title">Закупки</div>
    ${item("orders", "Заказы")}
    ${item("requests", "Запросы")}
    ${item("purchase", "Заявки на закупку", "5")}
    ${item("products", "Товары")}
    ${item("needs", "Потребности")}
    ${item("needs-crm", "Потребности из CRM")}
    ${item("tenders-mod", "Тендеры")}
  </div>
  <div class="nav-group">
    <div class="nav-title">Управление поставщиками</div>
    ${item("qualification", "Квалификация")}
    ${item("evaluation", "Оценка")}
    ${item("accreditation", "Аккредитация")}
    ${item("counterparties", "Контрагенты")}
  </div>
  <div class="nav-group">
    <div class="nav-title">Склад</div>
    ${item("ops", "Операции")}
    ${item("stock", "Товары на складе")}
    ${item("warehouses", "Склады")}
  </div>
  <div class="nav-group">
    <div class="nav-title">Компании</div>
    ${item("messenger", "Мессенджер", "8")}
    ${item("company", "Моя компания")}
    ${item("staff", "Сотрудники")}
    ${item("finance", "Финансы")}
    ${item("analytics", "Аналитика")}
  </div>
  <div class="sidebar-foot">‹ Свернуть меню</div>
</aside>`;
}

function page(title, { active, actions = "", filter = "", body, subtabs = "", noFilter = false, extraHead = "" }) {
  return `<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8"/>
<title>${title} — istock.link</title>
<link rel="stylesheet" href="_shared.css"/>
</head>
<body>
<div class="app">
  ${topbar()}
  <div class="body">
    ${sidebar(active)}
    <div class="main">
      <div class="page-head">
        <div class="page-title"><span class="back">←</span> ${title}</div>
        <div class="page-actions">${actions}</div>
      </div>
      ${subtabs}
      ${extraHead}
      <div class="content-wrap${noFilter || !filter ? " no-filter" : ""}">
        <div class="content">${body}</div>
        ${filter && !noFilter ? `<aside class="filter">${filter}</aside>` : ""}
      </div>
    </div>
  </div>
</div>
</body>
</html>`;
}

const filterNeeds = `<h4>Фильтр потребностей</h4>
<div class="field"><label>Источник потребности</label><div class="control">Не выбрано</div></div>
<div class="field"><label>Автор</label><div class="control">Не выбрано</div></div>
<div class="field"><label>Инициатор</label><div class="control">Не выбрано</div></div>
<div class="field"><label>Статус потребности</label><div class="control">Новая</div></div>
<div class="field"><label>Склад</label><div class="control input">Введите значение</div></div>
<div class="field"><label>Номер заявки</label><div class="control input">Введите значение</div></div>
<div class="field"><label>Номер запроса</label><div class="control input">Введите значение</div></div>
<div class="field"><label>Дата потребности (с — по)</label><div class="control input">дд.мм.гггг — дд.мм.гггг</div></div>
<div class="field"><label>Категория</label><div class="control">Выберите категории</div></div>
<button class="apply">Очистить поля</button>`;

const filterPurchase = `<h4>Фильтр заявок</h4>
<div class="field"><label>Ответственный</label><div class="control">Не выбрано</div></div>
<div class="field"><label>Автор</label><div class="control">Не выбрано</div></div>
<div class="field"><label>Статусы заявки</label><div class="control">Не выбрано</div></div>
<button class="apply" style="background:#1c50de;color:#fff">Применить</button>
<span class="linkish">Очистить фильтр</span>
<span class="linkish">Обновить параметры</span>`;

const screens = {
  "01-needs": page("Потребности", {
    active: "needs",
    actions: `<button class="btn ghost">Опубликовать потребности</button>
      <button class="btn">Сформировать заявку</button>
      <button class="btn">Сформировать запрос</button>
      <button class="btn">Создать потребность</button>
      <button class="btn primary plus">Создать потребность</button>`,
    filter: filterNeeds,
    body: `
      <div class="status-row">
        <div class="chip"><strong>11</strong><span>Закупка состоялась</span></div>
        <div class="chip"><strong>8</strong><span>На согласовании</span></div>
        <div class="chip"><strong>64</strong><span>В работе</span></div>
        <div class="chip active"><strong>142</strong><span>Новая</span></div>
        <div class="chip"><strong>0</strong><span>Дубль потребности</span></div>
        <div class="chip"><strong>1</strong><span>Закупка отменена</span></div>
        <div class="chip"><strong>1</strong><span>Закупка не состоялась</span></div>
        <div class="chip"><strong>24</strong><span>Черновик</span></div>
        <div class="chip add">+</div>
      </div>
      <div class="toolbar">
        <div class="search">Наименование потребности / Артикул</div>
        <div class="sort">Сортировать: <b>по умолчанию</b></div>
        <div class="view-tog"><i></i><i></i></div>
      </div>
      <div class="panel">
        <table class="data">
          <thead>
            <tr>
              <th><span class="check"></span></th>
              <th>Наименование потребности</th>
              <th>Артикул</th>
              <th>Кол-во</th>
              <th>Ед. изм.</th>
              <th>Дата потребности</th>
              <th>Статус</th>
              <th>№ запроса / заявки</th>
              <th>Категория</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            ${[
              ["Пример позиции", "—", "1"],
              ["Автошина 300-15 PLT 328 20PR", "—", "2"],
              ["Автошина 215/60R16 шип.", "—", "8"],
              ["Автошина 225/75R16", "—", "4"],
              ["Автошина 235/45R18 шип.", "—", "16"],
              ["Автошина 185/75R16 шип.", "—", "42"],
              ["Автошина 255/70R20 шин. Nord", "—", "5"],
              ["Автошина 16.5/70-18", "—", "6"],
              ["Автошина 175R16", "—", "2"],
              ["Автошина 205/50R17 шип.", "—", "19"],
            ]
              .map(
                ([name, art, qty]) => `<tr>
              <td><span class="check"></span></td>
              <td class="link">${name}</td>
              <td class="muted">${art}</td>
              <td>${qty}</td>
              <td>шт</td>
              <td class="muted">—</td>
              <td><span class="status st-new">Новая</span></td>
              <td class="muted">—</td>
              <td class="muted">—</td>
              <td class="more">⋮</td>
            </tr>`
              )
              .join("")}
          </tbody>
        </table>
      </div>
      <div class="pager">Показать по: 20 &nbsp; 1–20 из 142</div>`,
  }),

  "02-purchase-requests": page("Заявки на закупку", {
    active: "purchase",
    actions: `<button class="btn">Сформировать запрос</button><button class="btn primary plus">Создать заявку</button>`,
    filter: filterPurchase,
    subtabs: `<div class="subtabs"><span class="on">Все заявки</span><span>Заявки на согласовании</span></div>`,
    body: `
      <div class="toolbar">
        <div class="search">Наименование заявки / номер заявки / наименование изделия</div>
        <div class="sort">Сортировать: <b>по умолчанию</b></div>
        <div class="view-tog"><i></i><i></i></div>
      </div>
      ${[
        ["№ 00000797-797", "Лампы", "07.07.2026, 14:11", "Новая"],
        ["№ 00000789-789", "Заявка 1", "22.06.2026, 12:21", "Новая"],
        ["№ 00000784-784", "товары", "16.06.2026, 10:38", "Новая"],
        ["№ 00000767-767", "Заявка на закупку", "07.05.2026, 15:39", "Новая"],
        ["№ 00000761-761", "пример", "23.04.2026, 16:35", "Новая"],
        ["№ 00000751-751", "Основание", "21.04.2026, 15:06", "Новая"],
        ["№ 00000726-726", "Компоненты для платы", "23.03.2026, 10:55", "Создан запрос"],
        ["№ 00000710-710", "Крепёж М8", "26.02.2026, 13:22", "Новая"],
      ]
        .map(
          ([num, name, date, st], i) => `<div class="list-card">
          <span class="check"></span>
          <div>
            <div class="title">${num}</div>
            <div class="sub">${name}</div>
          </div>
          <div class="meta">
            <div>Дата обновления: ${date}</div>
            <div>Ответственный: Петров Алексей</div>
            <span class="tag${st.includes("запрос") ? " ok" : ""}">${st}${st.includes("запрос") ? " №00004463-4463" : ""}</span>
          </div>
        </div>`
        )
        .join("")}`,
  }),

  "04-requests": page("Запросы", {
    active: "requests",
    actions: `<button class="btn primary plus">Создать запрос</button>`,
    noFilter: true,
    body: `
      <div class="toolbar">
        <div class="search">Наименование запроса / Номер запроса / Наименование изделия</div>
        <div class="sort">Сортировать: <b>по умолчанию</b></div>
        <div class="view-tog"><i></i><i></i></div>
      </div>
      <div class="list-card">
        <span></span>
        <div>
          <div class="title">№ 00004951 — 4951</div>
          <div class="sub">Запрос по тендеру: Поставка ремонтного комплекта для насоса Flygt CT 3400/865 или эквивалент — АО «ВОДОКАНАЛ»</div>
        </div>
        <div class="meta">
          <div>Дата обновления: 14.07.2026, 13:45</div>
          <div>Ответственный: Петров Алексей</div>
          <span class="tag muted">Черновик</span>
          <div>Отклики: 0</div>
        </div>
      </div>
      <div class="list-card" style="grid-template-columns:20px 1fr; align-items:stretch">
        <span></span>
        <div>
          <div style="display:flex;justify-content:space-between;gap:16px">
            <div>
              <div class="title">№ 00004947 — 4947</div>
              <div class="sub">Работа с заказов №2</div>
            </div>
            <div class="meta">
              <div>Дата обновления: 14.07.2026, 10:15</div>
              <div>Ответственный: Петров Алексей</div>
              <span class="tag ok">Закупка завершена</span>
              <div>Отклики: 1</div>
            </div>
          </div>
          <div style="margin-top:12px;padding:12px;border:1px solid var(--line);border-radius:10px;background:#fafbff;display:flex;justify-content:space-between;align-items:center">
            <div>
              <div style="font-weight:800;font-size:16px">180 696,00 ₽ <span class="muted" style="font-size:12px;font-weight:500">с учётом доставки</span></div>
              <div class="sub">★ — · ООО «СеверПоставка» · ИНН 7701987654</div>
            </div>
            <span class="tag ok">Предложение принято</span>
          </div>
        </div>
      </div>
      <div class="list-card">
        <span></span>
        <div>
          <div class="title">№ 00004923 — 4923</div>
          <div class="sub">Компоненты для платы 3</div>
        </div>
        <div class="meta">
          <div>Приём откликов: 08.07 – 10.07.2026, 17:36</div>
          <div>Ответственный: Петров Алексей</div>
          <span class="tag ok">Приём откликов завершён</span>
          <div>Отклики: 1</div>
        </div>
      </div>
      <div class="list-card">
        <span></span>
        <div>
          <div class="title">№ 00004921 — 4921</div>
          <div class="sub">Компоненты для платы</div>
        </div>
        <div class="meta">
          <div>Приём откликов: 08.07 – 08.07.2026, 17:35</div>
          <div>Ответственный: Петров Алексей</div>
          <span class="tag ok">Приём откликов завершён</span>
          <div>Отклики: 1</div>
        </div>
      </div>
      <div class="pager">1–20 из 51 &nbsp; Показать по: 20</div>`,
  }),

  "05-compare-offers": `<!DOCTYPE html>
<html lang="ru"><head><meta charset="UTF-8"/><title>Сравнение откликов — istock.link</title><link rel="stylesheet" href="_shared.css"/></head>
<body>
<div class="app" style="grid-template-rows:52px 1fr">
  ${topbar()}
  <div style="background:#f5f7fb;display:flex;flex-direction:column">
    <div class="page-head">
      <div class="page-title"><span class="back">←</span> Сравнение откликов по запросу №2870 Демонстрация работы по эл. почте</div>
      <div class="page-actions"><span class="tag warn">Закупка отменена</span><span class="more">⋮</span></div>
    </div>
    <div class="subtabs"><span class="on">Сравнение цен</span><span>Сравнение неценовых критериев</span></div>
    <div class="compare-wrap">
      <div style="display:flex;justify-content:flex-end;margin-bottom:10px"><button class="btn">Сравнить: Цена ▾</button></div>
      <table class="compare-table">
        <tr>
          <th style="width:160px">Компания</th>
          <th><span class="dot-s blue"></span>Просмотрен<br>ТехУниверситет<br><span class="muted">Петров Алексей</span></th>
          <th class="best"><span class="dot-s green"></span>Согласовано<br>ОАО «Городской Автопарк»<br><span class="stars">★ 65</span></th>
          <th><span class="dot-s blue"></span>Просмотрен<br>ООО «ПромТест»<br><span class="muted">Петров Алексей</span></th>
          <th><span class="dot-s blue"></span>Просмотрен<br>ООО «ОРБИТА»<br><span class="muted">Петров Алексей</span></th>
        </tr>
        <tr>
          <td class="muted">Предоплата / Стоимость доставки / НДС</td>
          <td>— / — / Без НДС</td>
          <td class="best">— / — / Без НДС</td>
          <td>— / — / Без НДС</td>
          <td>— / — / Без НДС</td>
        </tr>
        <tr>
          <td><strong>Итоговая сумма</strong></td>
          <td>1 518,00 ₽</td>
          <td class="best"><strong>230,00 ₽</strong></td>
          <td>4 500,00 ₽</td>
          <td>4 500,00 ₽</td>
        </tr>
        <tr>
          <td>+ Компрессор ЭКПВ 15/32</td>
          <td>66.00 · 23 шт<br>1 518.00</td>
          <td class="best">10.00 · 23 шт<br>230.00</td>
          <td>45.00 · 100 шт<br>4 500.00</td>
          <td>45.00 · 100 шт<br>4 500.00</td>
        </tr>
      </table>
    </div>
  </div>
</div>
</body></html>`,

  "06-products": page("Товары", {
    active: "products",
    noFilter: true,
    body: `
      <div class="status-row">
        <div class="chip"><strong>1</strong><span>Идёт закупка</span></div>
        <div class="chip"><strong>3</strong><span>Предложение отклонено</span></div>
        <div class="chip active"><strong>98</strong><span>Закупка состоялась</span></div>
        <div class="chip"><strong>10</strong><span>Требуется самовывоз</span></div>
        <div class="chip"><strong>3</strong><span>Производится доставка</span></div>
        <div class="chip add">+</div>
      </div>
      <div class="toolbar">
        <div class="search">Наименование товара / Артикул</div>
        <div class="view-tog"><i></i><i></i></div>
      </div>
      <div class="panel">
        <table class="data">
          <thead>
            <tr>
              <th><span class="check"></span></th>
              <th>Артикул</th>
              <th>Наименование товарной позиции</th>
              <th>Статус</th>
              <th>Количество</th>
              <th>Ед. измерения</th>
              <th>Инициатор</th>
              <th>Ответственный</th>
              <th>Запрос</th>
              <th>Поставщик</th>
            </tr>
          </thead>
          <tbody>
            ${[
              ["КСР-10", "Жидкая гидроизоляция", "Производится доставка", "ok", "3", "ООО «СеверПоставка»", "Запрос №00004947 Работа с заказов №2"],
              ["ПТ-120", "Противовес", "Закупка состоялась", "ok", "3", "ООО «СеверПоставка»", "Запрос №00004947 Работа с заказов №2"],
              ["В00А.КБ", "Каркас блока", "Получено предложение", "new", "4", "—", "Запрос №00004923 Компоненты для платы 3"],
              ["УТИП-00", "УТИП–00.000–19 в контейнере 7.35 МПа", "Получено предложение", "new", "6", "—", "Запрос №00004921 Закупка ткани"],
              ["SB 40 C", "Модель SB 40 C/СС", "Получено предложение", "new", "35", "—", "Запрос №00004921 Компоненты для платы"],
              ["СС004.1С", "Скамья садовая «Будапешт»", "Получено предложение", "new", "35", "—", "Запрос №00004921 Компоненты для платы"],
              ["—", "Саморез 5,5/6,3×75", "Получено предложение", "new", "53", "—", "Запрос №00004921 Компоненты для платы"],
              ["В00А.КБ", "Каркас блока", "Закупка состоялась", "ok", "4", "ООО «ТехСнаб»", "Запрос №00004920 new request"],
              ["27751", "Игровая площадка для детей от 3 до 14 лет", "Закупка состоялась", "ok", "4", "ООО «ТехСнаб»", "Запрос №00004920 new request"],
              ["КСР-10", "Жидкая гидроизоляция", "Получено предложение", "new", "4", "—", "Запрос №00004919 port"],
            ]
              .map(
                ([art, name, st, kind, qty, supplier, req]) => `<tr>
              <td><span class="check"></span></td>
              <td>${art}</td>
              <td class="link">${name}</td>
              <td><span class="status st-${kind}">${st}</span></td>
              <td>${qty}</td>
              <td>шт</td>
              <td>Петров Алексей</td>
              <td>Петров Алексей</td>
              <td class="link">${req}</td>
              <td>${supplier}</td>
            </tr>`
              )
              .join("")}
          </tbody>
        </table>
      </div>
      <div class="pager">Показать по: 20 &nbsp; 1–20 из 286</div>`,
  }),

  "07-counterparties": page("Контрагенты", {
    active: "counterparties",
    actions: `<button class="btn">Пригласить контрагента</button><button class="btn primary plus">Добавить контрагента</button>`,
    noFilter: true,
    body: `
      <div class="toolbar">
        <div class="search">Компания / Уникальный номер</div>
        <div class="sort">Сортировать: <b>Сначала новые</b></div>
        <button class="btn">Список групп</button>
        <div class="view-tog"><i></i><i></i></div>
      </div>
      <div style="margin-bottom:10px"><label style="display:flex;gap:8px;align-items:center;color:var(--muted)"><span class="check"></span> Выбрать все</label></div>
      ${[
        {
          name: "АО «СеверСтандарт»",
          meta: "рейтинг отсутствует · нет данных о надёжности",
          inn: "ИНН 7700123456 · ОГРН 1027700123456",
          contacts: "Россия, г. Санкт-Петербург, ул. Примерная, д. 10",
          group: "Металл",
          tag: "Компания не зарегистрирована в системе",
        },
        {
          name: "ООО «ИстЛайн»",
          meta: "рейтинг отсутствует",
          inn: "USCC: 44444",
          contacts: "Китай",
          group: "—",
          tag: "Компания не зарегистрирована в системе",
        },
        {
          name: "ООО «КолорЛайн»",
          meta: "рейтинг 61 · надёжность —",
          inn: "ИНН 7800987654 · ОГРН 1157800987654",
          contacts: "Основные контакты скрыты",
          group: "—",
          tag: "",
        },
      ]
        .map(
          (c) => `<div class="list-card" style="grid-template-columns:20px 1fr">
          <span class="check"></span>
          <div>
            ${c.tag ? `<div class="tag muted" style="margin-bottom:8px">${c.tag}</div>` : ""}
            <div class="title">${c.name}</div>
            <div class="sub">${c.meta}</div>
            <div class="mini-meta"><span>${c.inn}</span></div>
            <div class="mini-meta"><span>📍 ${c.contacts}</span><span>Группа: ${c.group}</span></div>
            <div class="sub" style="margin-top:8px">▸ Дополнительная информация</div>
          </div>
        </div>`
        )
        .join("")}`,
  }),

  "08-qualification": page("Квалификация", {
    active: "qualification",
    subtabs: `<div class="subtabs"><span class="on">Заявки на квалификацию</span><span>Квалифицированные поставщики</span></div>`,
    noFilter: true,
    body: `
      <div class="list-card" style="grid-template-columns:1fr auto;align-items:center">
        <div>
          <div class="title">Входная анкета для поставщиков</div>
          <div class="sub">Входная анкета будет добавляться автоматически к каждой заявке на квалификацию</div>
        </div>
        <div style="display:flex;gap:8px;color:var(--muted)">🔗 &nbsp; 📄 &nbsp; 🗑</div>
      </div>
      <div class="toolbar" style="margin-top:12px">
        <div class="search">Компания / Уникальный номер</div>
      </div>
      ${[
        ["№000013 от 04.07.2024", "ОАО «Городской Автопарк»", "рейтинг отсутствует · надёжность 20", "Стеклопластик", "На рассмотрении", "07.07.2026", "new"],
        ["№000014 от 04.07.2024", "РЕСУРС+", "★ 5.0 · надёжность 24 · квалифицированный · важный", "Вторсырьё, отходы, лом", "Квалификация пройдена", "26.01.2026", "ok"],
        ["№000009 от 05.02.2024", "АО «ВолгаДеталь»", "★ 3.5 · надёжность 7 · квалифицированный · важный", "Трубопроводная арматура, детали трубопроводов", "Квалификация пройдена", "23.01.2026", "ok"],
        ["№000018 от 13.01.2025", "ООО «ТехСнаб»", "★ 4.7 · надёжность 51 · квалифицированный · стратегический", "Безопасность, охрана / Инструменты", "На рассмотрении", "26.12.2025", "new"],
        ["№000001 от 05.02.2024", "РЕСУРС+", "★ 5.0 · надёжность 24 · квалифицированный · важный", "—", "На рассмотрении", "05.02.2024", "new"],
      ]
        .map(
          ([num, name, meta, cats, st, date, kind]) => `<div class="list-card" style="grid-template-columns:1fr auto">
          <div>
            <div class="sub">${num}</div>
            <div class="title" style="margin-top:4px">${name}</div>
            <div class="sub">${meta}</div>
            <div class="mini-meta">Заявленные категории: ${cats}</div>
          </div>
          <div class="meta">
            <span class="status st-${kind}">${st}</span>
            <div>Дата обновления: ${date}</div>
          </div>
        </div>`
        )
        .join("")}`,
  }),

  "09-evaluation": page("Оценка", {
    active: "evaluation",
    actions: `<button class="btn primary plus">Создать процедуру</button>`,
    subtabs: `<div class="subtabs"><span class="on">Процедуры</span><span>Анкеты</span><span>Опросы</span></div>`,
    noFilter: true,
    body: `
      <div class="toolbar">
        <div class="search">Наименование процедуры</div>
        <div class="sort">Сортировать: <b>сначала новые</b></div>
      </div>
      ${[
        ["Проверка поставщика 1", "Открытые вопросы", "06.01.2025–08.02.2025", "100%", "Оценка завершена", "ok"],
        ["Процедура 45", "Ежемесячная оценка поставщиков", "29.11.2024–30.11.2024", "100%", "Оценка завершена", "ok"],
        ["Проверка №4", "тест", "25.11.2024–28.11.2024", "0%", "Оценка не состоялась", "bad"],
        ["Проверка №3", "тест", "25.11.2024–27.11.2024", "0%", "Оценка не состоялась", "bad"],
        ["Проверка №2", "тест", "25.11.2024–27.11.2024", "0%", "Оценка не состоялась", "bad"],
        ["Открытые вопросы", "Открытые вопросы", "20.11.2024–21.11.2024", "100%", "Оценка завершена", "ok"],
        ["Тестовая процедура", "тест", "20.11.2024–22.11.2024", "100%", "Оценка завершена", "ok"],
      ]
        .map(
          ([name, sub, dates, pct, st, kind]) => `<div class="list-card" style="grid-template-columns:1fr auto">
          <div>
            <div class="title">${name}</div>
            <div class="sub">${sub}</div>
          </div>
          <div class="meta" style="min-width:260px">
            <div>Сроки проведения процедуры: ${dates}</div>
            <div><span class="bar"><i style="width:${pct}"></i></span>${pct}</div>
            <span class="status st-${kind}">${st}</span>
            <div class="link">Активность оценщиков</div>
          </div>
        </div>`
        )
        .join("")}`,
  }),

  "10-receiving": page("Приёмка товара", {
    active: "ops",
    actions: `<button class="btn primary">Принять на склад</button>`,
    filter: `<h4>Фильтр</h4>
      <div class="field"><label>Поставщик</label><div class="control">Не выбрано</div></div>
      <div class="field"><label>Запрос</label><div class="control">Не выбрано</div></div>
      <div class="field"><label>Склад</label><div class="control">Не выбрано</div></div>
      <button class="apply" style="background:#1c50de;color:#fff">Применить</button>
      <span class="linkish">Очистить фильтр</span>
      <span class="linkish">Сохранить параметры</span>`,
    body: `
      <div class="field" style="max-width:420px"><label>Склад *</label><div class="control">Не выбрано</div></div>
      <div class="field"><label>Комментарий</label><div class="control input" style="height:64px;align-items:flex-start;padding-top:10px">Введите комментарий</div>
        <div class="muted" style="text-align:right;margin-top:4px">0 / 5000</div>
      </div>
      <div style="margin:12px 0 10px;font-weight:700">Приложения (0)</div>
      <button class="btn" style="margin-bottom:14px">📎 Прикрепить файл</button>
      <div class="panel">
        <table class="data">
          <thead>
            <tr>
              <th>Наименование товарной позиции</th>
              <th>Плановое кол-во</th>
              <th>Фактическое кол-во</th>
              <th>Ед. изм.</th>
              <th>Наименование</th>
              <th>Цена за ед.</th>
              <th>Сумма</th>
              <th>Валюта</th>
              <th>Поставщик</th>
              <th>Комментарий</th>
            </tr>
          </thead>
          <tbody>
            ${[
              ["Жидкая гидроизоляция", "3", "3", "54 666,00", "ООО «СеверПоставка»"],
              ["Противовес", "3", "3", "5 566,00", "ООО «СеверПоставка»"],
              ["Каркас блока", "4", "4", "535,00", "ООО «ТехСнаб»"],
              ["Игровая площадка для детей от 3 до 14 лет", "4", "4", "5 535,00", "ООО «ТехСнаб»"],
              ["Саморез 5,5/6,3×75", "3", "3", "33,00", "ООО «ПолиТехСнаб»"],
              ["Фланец маховика", "10", "10", "149,00", "ОАО «Городской Автопарк»"],
              ["Манометр КМ-22Р", "4", "4", "445,00", "ООО «ЭнергоЛаб»"],
            ]
              .map(
                ([name, plan, fact, price, supplier]) => `<tr>
              <td class="link">${name}</td>
              <td>${plan} шт</td>
              <td>${fact} шт</td>
              <td>шт</td>
              <td>${name}</td>
              <td>${price}</td>
              <td>0,00</td>
              <td>RUB</td>
              <td>${supplier}</td>
              <td class="muted">Введите комментарий</td>
            </tr>`
              )
              .join("")}
          </tbody>
        </table>
      </div>
      <div class="pager">Итого: 0,00 RUB &nbsp;|&nbsp; Показать по: 10 &nbsp; 1–10 из 123</div>`,
  }),
};

const approval = `<!DOCTYPE html>
<html lang="ru"><head><meta charset="UTF-8"/><title>Согласование — istock.link</title><link rel="stylesheet" href="_shared.css"/></head>
<body>
<div class="flow-page">
  <div class="flow-top">
    <h1>Согласование кабеля</h1>
    <div class="page-actions">
      <button class="btn ghost">Закрыть конструктор</button>
      <button class="btn">Сохранить маршрут</button>
    </div>
  </div>
  <div class="flow-canvas">
    <div>
      <div class="step-label">Начало ( заявка )</div>
      <div class="fnode"><div class="h gray">Начало (заявка)</div><div class="b"><strong>Начало маршрута</strong></div></div>
    </div>
    <div class="farrow"></div>
    <div>
      <div class="step-label">Согласование &nbsp;&nbsp; Шаг 1</div>
      <div class="fnode"><div class="h blue">Согласование</div><div class="b"><div class="person"><div class="av">СА</div><div><strong>Соколова Анна</strong><small>МТО</small></div></div></div></div>
    </div>
    <div class="farrow"></div>
    <div>
      <div class="step-label">Публикация &nbsp;&nbsp; Шаг 2</div>
      <div class="fnode"><div class="h green">Публикация</div><div class="b"><div class="person"><div class="av">МД</div><div><strong>Морозов Дмитрий</strong><small>МТО</small></div></div></div></div>
    </div>
    <div class="farrow"></div>
    <div>
      <div class="step-label">Конец ( заявка )</div>
      <div class="fnode"><div class="h gray">Конец (заявка)</div><div class="b"><strong>Конец маршрута</strong></div></div>
    </div>
  </div>
</div>
</body></html>`;

const tendersBoard = `<!DOCTYPE html>
<html lang="ru"><head><meta charset="UTF-8"/><title>Тендеры — доска — istock.link</title><link rel="stylesheet" href="_shared.css"/></head>
<body>
<div class="tenders-app">
  <div class="t-top">
    <div class="t-tabs">
      <span>Тендеры</span>
      <span class="on">Лента <span class="badge">190</span></span>
      <span>Сделки</span>
      <span>Задачи</span>
    </div>
    <div class="t-actions">
      <button class="btn">Разведка ЭТП</button>
      <button class="btn">Почта</button>
      <button class="btn">Добавить из Seldon</button>
      <button class="btn primary plus">Добавить тендер</button>
    </div>
  </div>
  <div class="t-body">
    <div class="t-tools">
      <div class="role-switch"><span class="on">Доска</span><span>Таблица</span></div>
      <label style="display:flex;align-items:center;gap:8px;color:var(--muted)"><span class="check"></span> Показать завершённые</label>
      <div class="search" style="max-width:280px;margin-left:auto">Поиск по сделкам</div>
    </div>
    <div style="color:var(--muted);font-size:12px">102 503 546 ₽</div>
    <div class="kanban">
      <div class="kcol">
        <h4>Новые <em>30</em></h4>
        <div class="kcard">
          <div class="id">5015 · ПУБЛИЧ</div>
          <div class="name">Актуализация схемы теплоснабжения</div>
          <div class="price">7 239 949 ₽</div>
          <div class="who">Ответственный: Иванов Сергей<br>27.07.2026, 13:46 – 01.01.2027</div>
        </div>
        <div class="kcard">
          <div class="id">5008</div>
          <div class="name">Приобретение ЗИП для буровой установки SUNWARD 250 SWDRT</div>
          <div class="price muted">НМЦК —</div>
          <div class="who">ООО «Сервис Плюс» · Иванов Сергей</div>
        </div>
      </div>
      <div class="kcol">
        <h4>Подать предложение <em>1</em></h4>
        <div class="kcard urgent">
          <div class="id">4953</div>
          <div class="name">Оказание услуг по техническому обслуживанию масс-спектрометра</div>
          <div class="price">2 756 783 ₽</div>
          <div class="who" style="color:#ef4444">Срок истёк</div>
        </div>
      </div>
      <div class="kcol"><h4>Заключение контракта <em>0</em></h4></div>
      <div class="kcol"><h4>Закупка <em>0</em></h4></div>
      <div class="kcol"><h4>Исполнение контракта <em>0</em></h4></div>
    </div>
  </div>
</div>
</body></html>`;

const tendersFeed = `<!DOCTYPE html>
<html lang="ru"><head><meta charset="UTF-8"/><title>Тендеры — лента — istock.link</title><link rel="stylesheet" href="_shared.css"/></head>
<body>
<div class="tenders-app">
  <div class="t-top">
    <div class="t-tabs">
      <span>Тендеры</span>
      <span class="on">Лента <span class="badge">190</span></span>
      <span>Сделки</span>
      <span>Задачи</span>
    </div>
    <div class="t-actions">
      <button class="btn">Разведка ЭТП</button>
      <button class="btn">Почта</button>
      <button class="btn primary plus">Добавить тендер</button>
    </div>
  </div>
  <div class="t-body">
    <div class="t-tools">
      <div class="role-switch"><span class="on">Лента</span><span>Агрегатор</span></div>
      <div class="search" style="flex:1">Поиск в ленте</div>
      <div class="muted">Найдено 190 · новых 12</div>
      <button class="btn">Отметить все просмотренными</button>
    </div>
    <div class="feed-layout">
      <div>
        ${[
          ["Поставка хозяйственных товаров, средства передвижения, инструмента в ассортименте", "АО «Птицефабрика Рефинская»", "Свердловская область", "Хозтовары", "B2B-Center"],
          ["БГЕР-038882 Насос многоступенчатый центробежный V/V5 16-5", "ООО «Казанская медь»", "Забайкальский край", "Насосы", "B2B-Center"],
          ["Закупка насосного оборудования. Рассматриваем оригинал и аналоги РФ, Европа, Китай", "ООО «ТД ПолиметаллТорг»", "Республика Саха (Якутия)", "Насосы", "B2B-Center"],
          ["ТМЦ ЭЧ ДЛЯ ЦЕНТРИФУГИ DECANTER. Принимаются предложения на запасные части", "ООО «АИМ Менеджмент»", "Кемеровская область", "Лабораторные приборы", "B2B-Center"],
        ]
          .map(
            ([title, org, region, cat, src]) => `<div class="feed-card">
            <div class="row1">
              <div class="price-miss">Цена не указана · 28.07.2026 · 3 ч.</div>
              <div class="chips-inline"><span>${cat}</span><span class="src">${src}</span></div>
            </div>
            <div class="title">${title}</div>
            <div class="org">${org} · ${region}</div>
          </div>`
          )
          .join("")}
      </div>
      <aside class="filter" style="border:1px solid var(--line);border-radius:12px">
        <h4>Фильтр ленты</h4>
        <div class="field"><label>Статус</label><div class="control">Все</div></div>
        <div class="field"><label>Источник</label><div class="control">Все источники</div></div>
        <div class="field"><label>Период публикации с</label><div class="control input">Не выбрано</div></div>
        <div class="field"><label>Период публикации до</label><div class="control input">Не выбрано</div></div>
        <div class="field"><label>Диапазон начальной цены</label><div class="control input">от — до</div></div>
        <button class="apply" style="background:#1c50de;color:#fff">Применить</button>
        <span class="linkish">Очистить фильтр</span>
      </aside>
    </div>
  </div>
</div>
</body></html>`;

async function main() {
  await mkdir(outDir, { recursive: true });

  for (const [name, html] of Object.entries(screens)) {
    await writeFile(path.join(outDir, `${name}.html`), html);
  }
  await writeFile(path.join(outDir, "03-approval-flow.html"), approval);
  await writeFile(path.join(outDir, "11-tenders-board.html"), tendersBoard);
  await writeFile(path.join(outDir, "12-tenders-feed.html"), tendersFeed);

  const index = `<!DOCTYPE html><html lang="ru"><head><meta charset="UTF-8"/><title>Обезличенные экраны istock.link</title>
  <style>body{font-family:system-ui;max-width:800px;margin:40px auto;padding:0 20px;line-height:1.5}a{display:block;padding:8px 0;color:#1c50de}</style></head>
  <body><h1>Обезличенные заготовки экранов</h1><p>Данные вымышлены. UI приближен к продукту.</p>
  ${[
    ["01-needs.html", "Потребности"],
    ["02-purchase-requests.html", "Заявки на закупку"],
    ["03-approval-flow.html", "Согласование (маршрут)"],
    ["04-requests.html", "Запросы"],
    ["05-compare-offers.html", "Сравнение откликов"],
    ["06-products.html", "Товары"],
    ["07-counterparties.html", "Контрагенты"],
    ["08-qualification.html", "Квалификация"],
    ["09-evaluation.html", "Оценка"],
    ["10-receiving.html", "Приёмка товара"],
    ["11-tenders-board.html", "Тендеры — доска"],
    ["12-tenders-feed.html", "Тендеры — лента"],
  ]
    .map(([f, t]) => `<a href="${f}">${t}</a>`)
    .join("")}
  </body></html>`;
  await writeFile(path.join(outDir, "index.html"), index);
  console.log("Built screens in", outDir);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
