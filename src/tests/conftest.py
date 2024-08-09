import pytest
from django.urls import reverse

from rest_framework.test import APIClient

from bicycle.models import Bicycle


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def data():
    data = {
        'username': 'test_username',
        'email': 'test@test.com',
        'password': 'test_password',
    }

    return data


@pytest.fixture
def user(client, data):
    response = client.post(reverse('register_user'), data=data)

    return response


@pytest.fixture
def jwt_token(client, user, data):
    response = client.post(path=reverse('token_obtain_pair'), data=data)

    return response.data['access']


@pytest.fixture
def bicycle():
    return Bicycle.objects.create(
        name='test bicycle',
        price=100
    )


@pytest.fixture
def bicycle_data():
    return {
        'user': 1,
        'bicycle': 1,
    }
