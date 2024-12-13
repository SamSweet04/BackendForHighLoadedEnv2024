import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_user_registration():
    client = APIClient()
    response = client.post('/api/auth/register/', {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'securepassword'
    })
    assert response.status_code == 201
    assert response.data['message'] == 'User testuser registered successfully.'

@pytest.mark.django_db
def test_user_login():
    client = APIClient()
    client.post('/api/auth/register/', {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'securepassword'
    })
    response = client.post('/api/auth/login/', {
        'username': 'testuser',
        'password': 'securepassword'
    })
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data