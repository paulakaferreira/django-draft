from django.contrib import admin
from . import models


class OrderProductInline(admin.TabularInline):
    model = models.OrderProduct
    extra = 1

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'price', 'billing_address']
    inlines = [OrderProductInline]

@admin.register(models.Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'status', 'estimated_arrival_date', 'delivery_fee']
