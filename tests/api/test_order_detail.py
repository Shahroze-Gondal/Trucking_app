import pytz
from django.urls import reverse
from django.utils import timezone
from rest_framework import status


def test_retrieve_order(user_factory, order_factory, authed_token_client_generator):
    user = user_factory()
    order = order_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('dispatch-detail', kwargs={'pk': order.order_id}), format='json')


def test_retrieve_order_invalid_id(user_factory, order_factory, authed_token_client_generator):
    user = user_factory()
    order = order_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('dispatch-detail', kwargs={'pk': user.id}), format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND
