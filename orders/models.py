from django.db import models
from catalog.models import Product
from customer.models import CustomerProfile
from customer.models import Address


class Order(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through="OrderProduct")
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    billing_address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer}'s order on {self.date}"

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(default=1)
    subtotal = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.order} / {self.product}"

class Delivery(models.Model):
    estimated_arrival_date = models.DateField()
    delivery_date = models.DateField()
    status = models.CharField(max_length=50)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return f"Delivery to {self.shipping_address}"
