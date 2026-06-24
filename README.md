# Expense Bot

Telegram-бот для учёта расходов с веб-интерфейсом.

## Состав

| Компонент | Назначение |
|-----------|-----------|
| `bot` | Telegram-бот, принимает траты |
| `web-app` | Веб-интерфейс для управления |
| `db` | MariaDB, хранение данных |

## Переменные окружения

Скопировать `.env.example` в `.env` и заполнить:

- `BOT_TOKEN` — токен Telegram-бота
- `ALL_PROXY` — прокси для Telegram API
- `DB_USER`, `DB_PASSWORD`, `DB_DATABASE` — БД
- `WEB_USER`, `WEB_PASSWORD` — доступ к веб-интерфейсу
- `LOG_ID` — Telegram ID для логов ошибок

## Запуск

```bash
docker compose up -d
```

Веб-интерфейс: `http://localhost:5000`.
