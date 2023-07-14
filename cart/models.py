from django.db import models
from catalog.models import Product
from customer.models import CustomerProfile


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.number * self.product.price

    def __str__(self):
        return f"{self.product} / {self.customer}"
