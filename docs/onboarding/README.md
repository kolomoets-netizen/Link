# Инструкции для новых пользователей iStockLink

Два формата: письмо заявителю и поток на Tilda.

## 1. Гайд для email (после заявки)

**Файл:** `guide-for-email.md`

Скопируйте текст в письмо или экспортируйте в PDF.

Ключевые пункты:
- Регистрация: https://zakupki.istock.link/registration
- Роль: **Покупатель**
- Подключение агрегатора, фильтры, воронка, поставщики

Замените перед отправкой:
- `[укажите ваш email поддержки]`
- `[ссылка на страницу Tilda с потоком]`

---

## 2. Поток на Tilda (6 шагов)

**Папка:** `tilda-flow/`

| Шаг | Файл | Содержание |
|-----|------|------------|
| 1 | `01-registration.html` | Регистрация, роль Покупатель |
| 2 | `02-overview.html` | Разделы кабинета |
| 3 | `03-aggregator.html` | API-ключ агрегатора |
| 4 | `04-feed.html` | Фильтры и лента |
| 5 | `05-funnel.html` | Воронка |
| 6 | `06-support.html` | КП, FAQ, поддержка |

### Как собрать поток в Tilda

1. Создайте страницу «Инструкция» или используйте **Потоки** (Tilda → Потоки).
2. На каждый шаг — блок **T123 HTML-код**.
3. Скопируйте **весь** файл шага (включая `<style>`) в блок.
4. Между шагами — кнопка «Далее» потока или навигация Tilda.
5. Отступы блоков: 0px сверху/снизу для seamless-вида.

### Скриншоты интерфейса

Схемы экранов (SVG): `screens/`

На GitHub Pages:
- https://kolomoets-netizen.github.io/Link/onboarding/screens/01-registration.svg
- https://kolomoets-netizen.github.io/Link/onboarding/screens/02-feed.svg
- https://kolomoets-netizen.github.io/Link/onboarding/screens/03-aggregator.svg
- https://kolomoets-netizen.github.io/Link/onboarding/screens/04-funnel.svg

Когда появятся реальные скриншоты приложения — замените URL в HTML-блоках на загруженные в Tilda изображения.

### Локальные пути (если без GitHub Pages)

Загрузите SVG в **Файлы сайта** Tilda и замените в `img src` на `/uploads/...`.

---

## Обновление инструкции

Если изменится интерфейс или названия разделов — правьте оба формата:
- `guide-for-email.md`
- соответствующий файл в `tilda-flow/`
