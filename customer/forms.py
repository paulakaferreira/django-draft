from django import forms
from . import models

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = models.CustomerProfile
        exclude = ['created', 'last_updated']
