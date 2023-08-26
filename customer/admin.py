from django.contrib import admin
from . import models
from . import forms

# Register your models here.

@admin.register(models.CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    form = forms.CustomerProfileAdminForm


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["name", "customer", "__str__"]
    form = forms.AddressAdminForm
