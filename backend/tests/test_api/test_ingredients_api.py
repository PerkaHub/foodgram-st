from http import HTTPStatus

from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_with_client_get_ingredients(client):
    """
    Тест для получения списка ингридиентов.
    """
    url = reverse('ingredient-list')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert len(response.data) > 0


@pytest.mark.parametrize(
        'id, name, expected_status',
        (
            (1, 'абрикосовое варенье', HTTPStatus.OK),
            (55, 'арбузная мякоть', HTTPStatus.OK),
            (3000, None, HTTPStatus.NOT_FOUND)
        )
)
@pytest.mark.django_db
def test_with_client_get_ingredient(client, id, name, expected_status):
    """
    Тест для получения одного ингридиента.
    """
    url = reverse('ingredient-detail', kwargs={'pk': id})
    response = client.get(url)

    assert response.status_code == expected_status

    if expected_status == HTTPStatus.OK:
        assert response.data['name'] == name
        assert 'id' in response.data
        assert 'measurement_unit' in response.data
