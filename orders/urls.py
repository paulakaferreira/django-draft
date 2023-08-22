from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Other URL patterns
    path('choose-address/', views.choose_addresses, name='choose-address'),
    path('create-order/', views.create_order, name='create-order'),
    path('order-details/<int:order_id>/', views.order_details, name='order-details'),
]
