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
