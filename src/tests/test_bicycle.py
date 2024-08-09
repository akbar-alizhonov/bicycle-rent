import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_get_list_of_bicycles(client, jwt_token, bicycle):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
    response = client.get(reverse('bicycle_list'))

    assert len(response.data) == 1


@pytest.mark.django_db
def test_create_rental(client, jwt_token, bicycle, bicycle_data):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
    response = client.post(reverse('create_rental'), data=bicycle_data)

    assert response.status_code == 201


@pytest.mark.django_db
def test_return_bicycle(client, jwt_token, bicycle, bicycle_data):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
    client.post(reverse('create_rental'), data=bicycle_data)

    response = client.post(reverse('return_bicycle'), data=bicycle_data)

    assert response.status_code == 200


@pytest.mark.django_db
def test_user_history(client, jwt_token, bicycle, bicycle_data):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)
    client.post(reverse('create_rental'), data=bicycle_data)
    client.post(reverse('return_bicycle'), data=bicycle_data)

    response = client.get(reverse('history'))

    assert response.status_code == 200
