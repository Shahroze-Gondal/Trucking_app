import pytz
from django.urls import reverse
from django.utils import timezone
from rest_framework import status


def test_get_dispatch(user_factory, dispatch_factory, authed_token_client_generator):
    user = user_factory()
    dispatch = dispatch_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('dispatch-list'))
    assert response.json()[0]['dispatch_id'] == dispatch.dispatch_id
    assert response.json()[0]['title'] == dispatch.title


def test_create_dispatch(user_factory, authed_token_client_generator):
    user = user_factory()
    data = {
     "dispatch_id": 2,
     "title": "dispatch_pytest",
     "status": "Scheduled",
    }
    client = authed_token_client_generator(user)
    response = client.post(reverse('dispatch-list'), data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['title'] == data['title']


def test_create_dispatch_invalid_status(user_factory, authed_token_client_generator):
    user = user_factory()
    data = {
     "dispatch_id": 2,
     "title": "dispatch_pytest",
     "status": "hello",
    }
    client = authed_token_client_generator(user)
    response = client.post(reverse('dispatch-list'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_dispatch_invalid_data(user_factory, authed_token_client_generator):
    user = user_factory()
    data = {
     "dispatch_id": 2,
     "title": 434,
     "status": "hello",
    }
    client = authed_token_client_generator(user)
    response = client.post(reverse('dispatch-list'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_dispatch_invalid_action(user_factory, authed_token_client_generator):
    user = user_factory()
    data = {
     "dispatch_id": 2,
     "title": "cool-dispatch",
     "action": "sfdds",
    }
    client = authed_token_client_generator(user)
    response = client.post(reverse('dispatch-list'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
