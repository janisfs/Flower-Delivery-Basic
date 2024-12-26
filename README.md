# Flower Delivery Basic

Веб-приложение для онлайн-магазина по доставке цветов с интегрированным Telegram-ботом.

## Основной функционал

- Каталог цветов с подробным описанием
- Корзина покупок
- Система авторизации пользователей
- Оформление заказов с выбором даты и времени доставки
- История заказов с фильтрацией
- Уведомления о заказах через Telegram-бота
- Система комментариев к товарам

## Технологии

- Python 3.x
- Django
- SQLite
- Bootstrap
- python-telegram-bot


## Структура проекта
my_flower_del/ - основное приложение

media/ - медиафайлы

templates/ - HTML шаблоны

static/ - статические файлы (CSS, JS)

Автор
Anis Samedinov [https://github.com/janisfs]

Лицензия
MIT License



## Установка и запуск

1. Клонировать репозиторий
2. Создать виртуальное окружение:
```bash
python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver


