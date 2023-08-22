from django import forms
from customer.models import Address

class OrderCreationForm(forms.Form):
    billingAddress = forms.IntegerField()
    deliveryAddress = forms.IntegerField()
