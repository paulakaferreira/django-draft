from django.contrib import admin
from . import models
from . import forms

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    form = forms.CategoryForm

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    form = forms.ProductForm
