from django.db import models
from catalog.models import Product
from customer.models import CustomerProfile
from customer.models import Address

from datetime import datetime, timedelta

class Order(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=50, default="Pending")
    date = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through="OrderProduct")
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    billing_address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer}'s order on {self.date}"

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    number = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.number * self.price

    def __str__(self):
        return f"{self.order} / {self.product}"

class Delivery(models.Model):
    estimated_arrival_date = models.DateField(default=datetime.now() + timedelta(days=5))
    delivery_date = models.DateField(default=datetime.now() + timedelta(days=2))
    status = models.CharField(max_length=50, default="Pending")
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=1.99)

    def __str__(self):
        return f"Delivery to {self.shipping_address}"
