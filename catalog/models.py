from django.db import models
from django.utils.text import slugify

from customer.models import CustomerProfile


class SlugModel(models.Model):   
    name = models.CharField(max_length=200, unique=True, null=False, blank=False)
    slug = models.SlugField(max_length=200, unique=True, null=False, blank=True)

    class Meta:
        abstract = True

    # Override
    def save(self, *args, **kwargs):
        # Generate the slug from the name field
        self.slug = slugify(self.name)

        # Call the original save() method
        super().save(*args, **kwargs)

class Category(SlugModel):

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Product(SlugModel):
    categories = models.ManyToManyField(Category, related_name='products')
    description = models.TextField(blank=True)
    #image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    products = models.ManyToManyField(Product, through="CartProduct")
    customer = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE, related_name='cart')
    total = models.PositiveIntegerField(default=0)

    def __str__(self):
        # return "Panier de "+str(self.customer)
        return f"Panier de {self.customer}"

class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(default=1)
    subtotal = models.PositiveIntegerField(default=0)

    def __str__(self):
        # return str(self.product)+" / "+str(self.cart)
        return f"{self.product} / {self.cart}"
