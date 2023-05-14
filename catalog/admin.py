from django.contrib import admin
from . import models

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    ...

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    ...
