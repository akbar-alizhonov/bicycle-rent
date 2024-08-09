import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_user_register(client, data):
    response = client.post(path=reverse('register_user'), data=data)
    response_data = response.data

    assert response_data['username'] == data['username']
    assert response_data['email'] == data['email']


@pytest.mark.django_db
def test_user_login(client, user, data):
    response = client.post(path=reverse('token_obtain_pair'), data=data)

    assert response.status_code == 200
