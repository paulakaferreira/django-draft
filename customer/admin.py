from django.contrib import admin
from . import models
from . import forms

# Register your models here.

@admin.register(models.CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    form = forms.CustomerProfileForm


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["pk", "customer", "__str__"]
    form = forms.AddressForm
