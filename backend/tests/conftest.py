from django.core.management import call_command
from rest_framework.test import APIClient
import pytest

from recipes.models import Recipe, RecipeIngredient, Ingredient


@pytest.fixture(autouse=True)
def _patch_cache(settings):
    """
    Отключаем redis на время выполнения тестов.
    """
    settings.CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }


@pytest.fixture(scope='session')
def django_db_setup(django_db_blocker):
    """
    Настройка тестовой БД с миграциями и загрузкой данных.
    """
    with django_db_blocker.unblock():
        call_command('migrate', interactive=False, verbosity=0)

        try:
            call_command('load_ingredients')
        except Exception as e:
            pytest.skip(f"Не удалось загрузить данные: {str(e)}")


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = APIClient()
    client.force_authenticate(user=author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = APIClient()
    client.force_authenticate(user=not_author)
    return client


@pytest.fixture
def recipe(author):
    recipe = Recipe.objects.create(
        name='Тестовый рецепт',
        author=author,
        text='Описание',
        cooking_time=33,
    )
    RecipeIngredient.objects.create(
        recipe=recipe,
        ingredient=Ingredient.objects.create(
            name='Тестовый ингредиент',
            measurement_unit='Грамм'
        ),
        amount=200
    )
    return recipe


@pytest.fixture
def mock_image_base64():
    """Фикстура возвращает валидное base64-изображение."""
    return (
        'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMA'
        'AABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4b'
        'AAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=='
    )
