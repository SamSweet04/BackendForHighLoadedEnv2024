import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_order_creation():
    client = APIClient()
    response = client.post('/api/create-order/', {
        'orderId': '123',
        'userId': 1,
        'totalAmount': 150.00,
        'customerEmail': 'customer@example.com'
    })
    assert response.status_code == 200
    assert response.data['message'] == "Заказ #123 создан. Email отправлен на customer@example.com."