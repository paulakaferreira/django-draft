from django import forms
from . import models

class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        exclude = ['slug']
        widgets = {
            'supercategory': forms.Select(attrs={'required': False}),
        }
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        exclude = ['slug']
