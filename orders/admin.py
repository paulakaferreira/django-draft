from django.contrib import admin
from . import models

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    ...

@admin.register(models.Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    ...

@admin.register(models.OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    ...