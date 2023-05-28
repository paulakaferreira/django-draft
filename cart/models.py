from django.db import models

from customer.models import CustomerProfile
from catalog.models import Product


class Cart(models.Model):
    products = models.ManyToManyField(Product, through="CartProduct")
    customer = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE, related_name='cart')
    total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Panier de {self.customer}"

class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(default=1)
    subtotal = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product} / {self.cart}"
