from django.urls import reverse
from rest_framework import status


def test_get_orders(user_factory, order_factory, authed_token_client_generator):
    user = user_factory()
    order = order_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('order-list'))
    assert response.status_code == status.HTTP_200_OK


def test_create_orders(user_factory, dispatch_factory, authed_token_client_generator):
    user = user_factory()
    dispatch = dispatch_factory()
    data = {
     "order_id": 2,
     "title": "order-pytest",
     "company": "liva",
     "dispatch_id": dispatch.dispatch_id
    }
    client = authed_token_client_generator(user)
    response = client.post(reverse('order-list'), data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['title'] == data['title']


def test_create_dispatch_without_dispatch_id(user_factory, dispatch_factory, authed_token_client_generator):
    user = user_factory()
    dispatch = dispatch_factory()
    data = {
     "order_id": 2,
     "title": 3421,
     "company": 534,
    }
    client = authed_token_client_generator(user)
    response = client.post(reverse('order-list'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
