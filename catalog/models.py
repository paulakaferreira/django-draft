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

    description = models.CharField(max_length=500, blank=True)
    supercategory = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subcategories')

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

class Review(models.Model):
    title = models.CharField(max_length=50, blank=False)
    comment = models.CharField(max_length=500, blank=False)
    notation = models.PositiveIntegerField(default=5)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(CustomerProfile, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer}'s review on {self.product}"
