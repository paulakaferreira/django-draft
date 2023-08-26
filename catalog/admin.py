from django.contrib import admin
from . import models
from . import forms

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_number', 'supercategory']
    form = forms.CategoryForm

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock']
    form = forms.ProductForm
