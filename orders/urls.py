from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Other URL patterns
    path('choose_addresses/', views.choose_addresses, name='choose_addresses'),
    path('create_order/', views.create_order, name='create_order'),
    path('order_details/<int:order_id>/', views.order_details, name='order_details'),
]
