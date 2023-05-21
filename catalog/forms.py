from django import forms
from . import models

class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        exclude = ['slug']

class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        exclude = ['slug']

class CartForm(forms.ModelForm):
    class Meta:
        model = models.Cart
        exclude = ['total']

class CartProductForm(forms.ModelForm):
    class Meta:
        model = models.CartProduct
        exclude = ['subtotal']
