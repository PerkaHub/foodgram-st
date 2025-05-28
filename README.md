# Foodgram - Продуктовый помощник 🍳

## Описание проекта

Foodgram - это веб-приложение, в котором пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Технологический стек 🛠️

### Фронтенд:
- React 17.0.1
- React Router DOM
- JavaScript
- Nginx

### Бэкенд:
- Django
- Django REST Framework
- PostgreSQL
- Docker
- Docker Compose

## Установка и запуск проекта 🚀

### Предварительные требования
- Docker
- Docker Compose

### Шаги по установке

1. Клонируйте репозиторий:
```bash
git clone git@github.com:PerkaHub/foodgram-st.git
cd foodgram
```

2. Создайте файл `.env` в корневой директории проекта:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DEBUG=False
ALLOWED_HOSTS=127.0.0.1,localhost
```

3. Запустите проект через Docker Compose:
```bash
docker-compose up -d --build
```

4. Загрузите ингридиенты в базу данных:
```bash
docker-compose exec backend python manage.py load_ingredients
```
## Основной функционал 📋

- 👤 Регистрация и авторизация пользователей
- 📝 Создание, просмотр, редактирование и удаление рецептов
- ⭐ Добавление рецептов в избранное
- 🛒 Добавление рецептов в список покупок
- 📥 Скачивание списка покупок
- 👥 Подписка на авторов
- 🔍 Фильтрация рецептов по тегам

## Работа с API 🔌

Документация API доступна по адресу: `http://localhost/api/docs/`

### Основные эндпоинты:
- `/api/users/` - пользователи
- `/api/recipes/` - рецепты
- `/api/ingredients/` - ингредиенты
- `/api/tags/` - теги

## Автор проекта ✨

Егор Опекин
