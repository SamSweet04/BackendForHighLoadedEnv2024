from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Product, Category, Order
from django.contrib.auth.models import User
from celery import Celery
from decimal import Decimal

# ----------- ЮНИТ-ТЕСТЫ  -----------

class ProductModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics", description="All kinds of electronics")
        self.product = Product.objects.create(
            name="Smartphone",
            description="Latest model",
            price=999.99,
            stock=50,
            category=self.category
        )

    def test_product_creation(self):
        product = Product.objects.get(name="Smartphone")
        self.assertEqual(product.price, Decimal('999.99'))
        self.assertEqual(product.category.name, "Electronics")

class CategoryModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Home Appliances", description="Appliances for home use")

    def test_category_creation(self):
        category = Category.objects.get(name="Home Appliances")
        self.assertEqual(category.description, "Appliances for home use")

class OrderModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.category = Category.objects.create(name="Books", description="All kinds of books")
        self.product = Product.objects.create(
            name="Fiction Book",
            description="A best-selling novel",
            price=19.99,
            stock=100,
            category=self.category
        )
        self.order = Order.objects.create(user=self.user, product=self.product, quantity=2, total_price=39.98)

    def test_order_creation(self):
        order = Order.objects.get(id=self.order.id)
        self.assertEqual(order.total_price, Decimal('39.98'))
        self.assertEqual(order.product.name, "Fiction Book")
        self.assertEqual(order.user.username, "testuser")

# ----------- ИНТЕГРАЦИОННЫЕ ТЕСТЫ  -----------

class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics", description="All kinds of electronics")
        self.product_url = reverse('product-list')
        self.product_data = {
            "name": "Laptop",
            "description": "A high-end laptop",
            "price": 1500.99,
            "stock": 10,
            "category": self.category.id
        }

    def test_get_products(self):
        response = self.client.get(self.product_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        response = self.client.post(self.product_url, self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Laptop")

class OrderAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.category = Category.objects.create(name="Books", description="All kinds of books")
        self.product = Product.objects.create(
            name="Fiction Book",
            description="A best-selling novel",
            price=19.99,
            stock=100,
            category=self.category
        )
        self.order_url = reverse('order-list')
        self.order_data = {
            "user": self.user.id,
            "product": self.product.id,
            "quantity": 3,
            "total_price": 59.97
        }

    def test_get_orders(self):
        response = self.client.get(self.order_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.order_url, self.order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_price'], "59.97")
