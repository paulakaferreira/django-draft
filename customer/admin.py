from django.contrib import admin
from . import models
from . import forms

# Register your models here.

@admin.register(models.CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "date_of_birth", "phone_number", "gender", "created", "last_updated"]
    form = forms.CustomerProfileAdminForm


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["name", "customer", "__str__"]
    form = forms.AddressAdminForm
