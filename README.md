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
git clone <ваш-репозиторий>
cd foodgram
```

2. Создайте файл `.env` в корневой директории проекта:
```
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=your-secret-key
```

3. Запустите проект через Docker Compose:
```bash
docker-compose up -d --build
```

4. Выполните миграции:
```bash
docker-compose exec backend python manage.py migrate
```

5. Создайте суперпользователя:
```bash
docker-compose exec backend python manage.py createsuperuser
```

6. Соберите статические файлы:
```bash
docker-compose exec backend python manage.py collectstatic --no-input
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

[Егор Опекин]
