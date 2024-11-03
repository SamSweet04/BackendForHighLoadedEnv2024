from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)  # Индекс для цены
    stock = models.IntegerField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, db_index=True)  # Индекс для категории

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)  # Индекс для пользователя
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True, db_index=True)  # Индекс для даты заказа

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
