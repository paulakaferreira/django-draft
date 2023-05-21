from django.contrib import admin
from . import models
from . import forms

# Register your models here.

@admin.register(models.CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    form = forms.CustomerProfileForm
