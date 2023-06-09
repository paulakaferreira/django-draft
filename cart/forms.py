from django import forms
from . import models


class CartForm(forms.ModelForm):
    class Meta:
        model = models.Cart
        exclude = ['total']

class CartProductForm(forms.ModelForm):
    class Meta:
        model = models.CartProduct
        exclude = ['subtotal']
