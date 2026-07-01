# HTML-письма iStockLink

## product-update.html

Дайджест для действующих пользователей. Шаблон для **Postmark** (Broadcast stream).

### Тема письма (в Postmark Template → Subject)

```
Дайджест «Новые возможности системы iStockLink»
```

В теле письма заголовок не дублируется — сразу логотип и «Добрый день!».

---

## Отправка через Postmark

### 1. Message Stream

Создайте отдельный **Broadcast** stream, например `product-digest` или `newsletter`.

- Дайджесты — только через **Broadcast** (там обязательна отписка).
- Транзакционные письма (регистрация, приглашения к закупке) — отдельный **Transactional** stream.

### 2. Шаблон

1. Postmark → **Templates** → **Add template**.
2. Вставьте HTML из `product-update.html` в поле **HTML body**.
3. **Subject:** `Дайджест «Новые возможности системы iStockLink»`
4. Добавьте **Plain text** версию (упрощённый текст + `{{{ pm:unsubscribe }}}` внизу).
5. Отправьте **test email** себе.

### 3. Отписка — как Postmark знает email

В футере шаблона уже есть:

```html
<a href="{{{ pm:unsubscribe }}}">Отписаться от рассылки</a>
```

Postmark подставляет **уникальную ссылку на каждого получателя**. Кто нажал — видно в:

**Postmark → ваш Broadcast stream → Suppressions → Unsubscribes**

Там список email-адресов. Tilda для отписки **не нужна**.

- `Настроить параметры рассылки` — ссылка в кабинет iStock.Link (тонкая настройка уведомлений).
- `Отписаться от рассылки` — полная отписка от этого Broadcast stream в Postmark.

При следующей рассылке Postmark **не отправит** письма адресам из Suppressions.

### 4. API / массовая отправка

```json
{
  "From": "noreply@istock.link",
  "To": "user@company.ru",
  "TemplateAlias": "product-digest",
  "TemplateModel": {},
  "MessageStream": "product-digest"
}
```

`TemplateModel` может быть пустым — весь контент уже в шаблоне. Если позже понадобится персонализация (`{{ name }}`), добавьте переменные в Mustachio-синтаксисе Postmark.

### 5. Синхронизация с iStock.Link (опционально)

Postmark отдаёт список отписавшихся через **Suppressions API** или вебхуки. Можно периодически подтягивать в свою БД и не слать дайджест из приложения тем, кто отписался в Postmark.

---

## Шрифт

Системный стек (San Francisco на Apple, Segoe UI на Windows):

`-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif`

Кастомные web-fonts в письме не используем — Gmail и Outlook их часто ломают.

---

## Превью Rutube

- обложка: `https://i.rtimg.ru/vi/006e7fc4772734af1a1ba0191b9e6785/xl/`
- ссылка: `https://rutube.ru/video/006e7fc4772734af1a1ba0191b9e6785/`

---

## Локальный просмотр (без Postmark)

`{{{ pm:unsubscribe }}}` в браузере не сработает — это плейсхолдер Postmark. Для проверки вёрстки откройте файл в Chrome; перед продакшеном — test email из Postmark.
