# Telegram Bot - registration and support

# Навигация

- [Навигация](#навигация)
- [Зачем нужен этот бот?](#зачем-нужен-этот-бот)
- [Установка](#установка)
     - [Установка необходимых Python-пакетов](#установка-необходимых-python-пакетов)
     - [Настройка перед запуском](#настройка-перед-запуском)
     - [Запуск бота](#запуск-бота)

# Зачем нужен этот бот?

Пример реализации регистрации пользователей, чата с админом/технической поддержкой и админкой.

### Пользовательский интерфейс

<img src="DOCS/start.gif" width="20%" height="420" alt="/start"/> <img src="DOCS/admin_chat.gif" width="20%" height="420" alt="admin_chat"/>

### Админка

<img src="DOCS/reg.gif" width="20%" height="420" alt="/admin_panel"/> <img src="DOCS/tickets.gif" width="20%" height="420" alt="tickets"/>


# Установка

Для работы бота необходимо установить [Python версии 3.10 и выше](https://www.python.org/downloads/).

### Установка необходимых Python-пакетов

    python3 -m pip install -r requirements.txt

### Настройка перед запуском

Перед запуском бота требуется:

1) создать телеграм токен у [@BotFather](https://t.me/BotFather) командой <b>/newbot</b>;
2) вставить полученный токен в файл [.env](.env);
3) получить свой телеграм ID у бота [@getmyid_bot](https://t.me/getmyid_bot);
4) вставить полученный user ID в поле admins в файле [config.py](lib/config.py)

## Запуск бота

    python3 main.py
