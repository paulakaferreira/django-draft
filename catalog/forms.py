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


class ReviewForm(forms.ModelForm):
    notation = forms.TypedChoiceField(coerce=int, choices=((1,'1/5'),(2,'2/5'),(3,'3/5'),(4,'4/5'),(5,'5/5')), initial=5)
    comment = forms.CharField(widget=forms.Textarea, max_length=models.Review._meta.get_field('comment').max_length)
    class Meta:
        model = models.Review
        exclude = ['created', 'last_updated', 'customer', 'product']
