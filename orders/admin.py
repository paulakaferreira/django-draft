from django.contrib import admin
from . import models

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'price', 'billing_address']

@admin.register(models.Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'status', 'estimated_arrival_date', 'delivery_fee']

@admin.register(models.OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'number', 'subtotal']