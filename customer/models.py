from django.db import models
from django.contrib.auth.models import User
from .validators import  valid_phone_number

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # profile_picture = models.ImageField(upload_to='profile_pictures/')
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, validators=[valid_phone_number])
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    products = models.ManyToManyField('catalog.Product', through='cart.Cart')

    def __str__(self):
        return self.user.username
    
class Address(models.Model):
    street_number = models.CharField(max_length=10, blank=True)
    street = models.CharField(max_length=100, blank=False)
    postal_code = models.CharField(max_length=10, blank=False)
    city = models.CharField(max_length=100, blank=False)
    country = models.CharField(max_length=100, blank=False)
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.street_number} {self.street}\n{self.postal_code} {self.city}\n{self.country}"
