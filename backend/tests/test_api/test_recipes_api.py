from http import HTTPStatus
from unittest.mock import patch

from django.urls import reverse
import pytest

from foodgram import settings


@pytest.mark.django_db
def test_get_recipes(client):
    """Тест для проверки получения рецептов."""
    url = reverse('recipe-list')
    response = client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert 'count' in response.data
    assert 'results' in response.data
    assert 'next' in response.data
    assert 'previous' in response.data


@pytest.mark.parametrize(
    'id, name, expected_status',
    (
        (1, 'Тестовый рецепт', HTTPStatus.OK),
        (22, None, HTTPStatus.NOT_FOUND),
    )
)
@pytest.mark.django_db
def test_get_recipe(author_client, id, name, expected_status, recipe):
    """Тест для проверки получения одного рецепта."""
    url = reverse('recipe-detail', kwargs={'pk': id})
    response = author_client.get(url)

    assert response.status_code == expected_status

    if expected_status == HTTPStatus.OK:
        assert response.data['name'] == name


@pytest.mark.parametrize(
    'id, expected_status',
    (
        (1, HTTPStatus.OK),
        (22, HTTPStatus.NOT_FOUND),
    )
)
@pytest.mark.django_db
def test_get_short_link(client, id, expected_status, recipe):
    """Тест для проверки получени короткой ссылки."""
    url = reverse('recipe-get-link', kwargs={'pk': id})
    response = client.get(url)

    assert response.status_code == expected_status
    if expected_status == HTTPStatus.OK:
        assert 'short-link' in response.data
        assert settings.BASE_URL in response.data['short-link']


@pytest.mark.parametrize(
    'parametrized_client, expected_status, cooking_time, id_ingredient',
    (
        (
            pytest.lazy_fixture('author_client'),
            HTTPStatus.CREATED,
            2,
            2
        ),
        (
            pytest.lazy_fixture('client'),
            HTTPStatus.UNAUTHORIZED,
            33,
            654
        ),
        (
            pytest.lazy_fixture('author_client'),
            HTTPStatus.BAD_REQUEST,
            -3,
            333
        ),
        (
            pytest.lazy_fixture('author_client'),
            HTTPStatus.BAD_REQUEST,
            3,
            22222
        )
    )
)
@pytest.mark.django_db
def test_create_recipe_auth_or_anon(
    parametrized_client,
    expected_status,
    mock_image_base64,
    cooking_time,
    id_ingredient
):
    """
    Тест для проверки POST запроса для добавления новых рецептов:
    1. Проверяет валидность данных.
    2. Проверяет аутентифицирован ли пользователь.
    """
    url = reverse('recipe-list')
    recipe_data = {
        'name': 'Тестовый ингредиент',
        'text': 'Описание',
        'ingredients': [{'id': id_ingredient, 'amount': 22}],
        'cooking_time': cooking_time,
        'image': mock_image_base64
    }

    with patch('django.core.files.storage.FileSystemStorage.save') as mock:
        mock.return_value = 'mocked_filename.png'
        response = parametrized_client.post(
            url,
            data=recipe_data,
            format='json'
        )

    assert response.status_code == expected_status

    if expected_status == HTTPStatus.CREATED:
        assert response.data['name'] == 'Тестовый ингредиент'


@pytest.mark.parametrize(
    (
        "recipe_id",
        "new_name",
        "new_text",
        "new_ingredients",
        "new_cooking_time",
        "expected_status",
    ),
    (
        (
            1,
            'Корректное изменение',
            'Новое описание',
            [{'id': 222, 'amount': 22}],
            45,
            HTTPStatus.OK
        ),
        (
            2,
            'Изменение несуществующего рецепта',
            'Новое описание',
            [{'id': 2, 'amount': 221}],
            22,
            HTTPStatus.NOT_FOUND
        ),
        (
            1,
            'Добавление несуществующего ингредиента',
            'Новое описание',
            [{'id': 111111, 'amount': 22}],
            35,
            HTTPStatus.BAD_REQUEST
        ),
        (
            1,
            'Добавление ингредиента с отрицательным amount',
            'Новое описание',
            [{'id': 111, 'amount': -44}],
            25,
            HTTPStatus.BAD_REQUEST
        ),
        (
            1,
            'Отрицательное время приготовления',
            'Новое описание',
            [{'id': 111111, 'amount': 22}],
            -35,
            HTTPStatus.BAD_REQUEST
        ),
    )
)
@pytest.mark.django_db
def test_patch_recipe_auth_and_validation(
    recipe_id,
    new_name,
    new_text,
    new_ingredients,
    new_cooking_time,
    expected_status,
    author_client,
    recipe,
):
    """
    Тест частичного обновления рецепта с проверкой авторизации и валидации.
    """
    url = reverse('recipe-detail', kwargs={'pk': recipe_id})
    recipe_patch_data = {
        'name': new_name,
        'text': new_text,
        'ingredients': new_ingredients,
        'cooking_time': new_cooking_time,
    }

    response = author_client.patch(
        url,
        data=recipe_patch_data,
        format='json'
    )

    assert response.status_code == expected_status

    if expected_status == HTTPStatus.OK:
        assert response.data['name'] == new_name
        assert response.data['text'] == new_text

        ingredient_response = response.data['ingredients'][0]
        ingredient_expected = new_ingredients[0]

        assert ingredient_response['id'] == ingredient_expected['id']
        assert ingredient_response['amount'] == ingredient_expected['amount']
        assert response.data['cooking_time'] == new_cooking_time


@pytest.mark.django_db
def test_anonymous_cannot_update_recipe(client, recipe):
    """Тест, что анонимный пользователь не может изменять рецепты."""
    url = reverse('recipe-detail', kwargs={'pk': 1})
    response = client.patch(url)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.django_db
def test_non_author_cannot_update_others_recipes(not_author_client, recipe):
    """Тест, что пользователь-неавтор не может изменять чужие рецепты."""
    url = reverse('recipe-detail', kwargs={'pk': 1})
    response = not_author_client.patch(url)
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.parametrize(
    'parametrize_client, expected_status',
    (
        (pytest.lazy_fixture('author_clieвnt'), HTTPStatus.NO_CONTENT),
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.FORBIDDEN),
        (pytest.lazy_fixture('client'), HTTPStatus.UNAUTHORIZED)
    )
)
@pytest.mark.django_db
def test_delete_recipe_permissions(
    parametrize_client,
    expected_status,
    recipe
):
    """
    Тестирует права доступа для удаления рецепта.
    """
    url = reverse('recipe-detail', kwargs={'pk': 1})
    response = parametrize_client.delete(url)
    assert response.status_code == expected_status
