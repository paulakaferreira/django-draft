from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models

class SignUpForm(UserCreationForm):
    """Customized sign-up form based on Django's built-in UserCreationForm (also includes first_name, 
    last_name & email fields)"""
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class CustomerProfileForm(forms.ModelForm):
    """Sign-up form relative to customer information"""
    class Meta:
        model = models.CustomerProfile
        exclude = ['created', 'last_updated', 'user', 'products']

class CustomerProfileAdminForm(forms.ModelForm):
    """Customer form specific to admin app: add User field"""
    class Meta:
        model = models.CustomerProfile
        exclude = ['created', 'last_updated', 'products']
        widgets = {
            'user': forms.Select(attrs={'required': False}),
        }

class AddressForm(forms.ModelForm):
    """Add an address form"""
    class Meta:
        model = models.Address
        exclude = ['created', 'last_updated', 'customer']

class AddressAdminForm(forms.ModelForm):
    """Address form for admin app: add customer field"""
    class Meta:
        model = models.Address
        exclude = ['created', 'last_updated']
        widgets = {
            'customer': forms.Select(attrs={'required': False}),
        }

class EditUserForm(forms.ModelForm):
    """The same as SignUpForm, without the password field"""
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
