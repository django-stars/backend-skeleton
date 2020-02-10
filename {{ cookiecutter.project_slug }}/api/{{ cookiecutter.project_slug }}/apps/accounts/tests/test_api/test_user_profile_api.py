from django.urls import reverse

from rest_framework import status

import pytest


@pytest.mark.django_db
def test_user_profile_api_get_success(user_account, api_client):
    email = "john@example.com"
    first_name = "John"
    last_name = "Doe"
    user = user_account(email=email, first_name=first_name, last_name=last_name)
    client = api_client(auth_user=user)

    response = client.get(reverse("api-v1-accounts:user-profile"))

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"email": email, "first_name": first_name, "last_name": last_name}


@pytest.mark.django_db
def test_user_profile_api_update_success(user_account, api_client):
    email = "john@example.com"
    old_first_name = "John"
    old_last_name = "Doe"
    new_first_name = "Jane"
    user = user_account(email=email, first_name=old_first_name, last_name=old_last_name)
    client = api_client(auth_user=user)

    response = client.put(reverse("api-v1-accounts:user-profile"), {"first_name": new_first_name})

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"email": email, "first_name": new_first_name, "last_name": old_last_name}
    user.refresh_from_db()
    assert user.email == email
    assert user.first_name == new_first_name
    assert user.last_name == old_last_name
