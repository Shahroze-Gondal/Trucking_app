from django.urls import reverse
from rest_framework import status


def test_get_dispatch(user_factory, dispatch_factory, authed_token_client_generator):
    user = user_factory()
    dispatch = dispatch_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('dispatch-detail', kwargs={'pk': dispatch.dispatch_id}), format='json')
    assert response.json()['dispatch_id'] == dispatch.dispatch_id
    assert response.json()['title'] == dispatch.title
    assert response.status_code == status.HTTP_200_OK


def test_patch_dispatch(user_factory, dispatch_factory, authed_token_client_generator):
    user = user_factory()
    dispatch = dispatch_factory()
    data = {
        "status": "In Transit"
    }
    client = authed_token_client_generator(user)
    response = client.patch(reverse('dispatch-detail', kwargs={'pk': dispatch.dispatch_id}), data=data, format='json')
    assert response.json()['status'] == data['status']


def test_delete_dispatch(user_factory, dispatch_factory, authed_token_client_generator):
    user = user_factory()
    dispatch = dispatch_factory()
    client = authed_token_client_generator(user)
    response = client.delete(reverse('dispatch-detail', kwargs={'pk': dispatch.dispatch_id}), format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_get_dispatch_invalid_id(user_factory, dispatch_factory, authed_token_client_generator):
    user = user_factory()
    dispatch = dispatch_factory()
    client = authed_token_client_generator(user)
    response = client.get(reverse('dispatch-detail', kwargs={'pk': user.id}), format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_patch_dispatch_Invalid_status(user_factory, dispatch_factory, authed_token_client_generator):
    user = user_factory()
    dispatch = dispatch_factory()
    data = {
        "status": "Scheduled"
    }
    client = authed_token_client_generator(user)
    response = client.patch(reverse('dispatch-detail', kwargs={'pk': dispatch.dispatch_id}), data=data, format='json')
    assert response.status_code == status.HTTP_203_NON_AUTHORITATIVE_INFORMATION


def test_delete_dispatch_invalid_id(user_factory, dispatch_factory, authed_token_client_generator):
    user = user_factory()
    client = authed_token_client_generator(user)
    response = client.delete(reverse('dispatch-detail', kwargs={'pk': user.id}), format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_patch_dispatch_Invalid_data(user_factory, dispatch_factory, authed_token_client_generator):
    user = user_factory()
    dispatch = dispatch_factory()
    data = {
        "status": 344
    }
    client = authed_token_client_generator(user)
    response = client.patch(reverse('dispatch-detail', kwargs={'pk': dispatch.dispatch_id}), data=data, format='json')
    assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE


def test_patch_dispatch_Invalid_status_after_pod(user_factory, dispatch_factory, authed_token_client_generator):
    user = user_factory()
    dispatch = dispatch_factory()
    data = {
        "pod": "masfnas",
        "status": "safs"
    }
    client = authed_token_client_generator(user)
    response = client.patch(reverse('dispatch-detail', kwargs={'pk': dispatch.dispatch_id}), data=data, format='json')
    assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE
