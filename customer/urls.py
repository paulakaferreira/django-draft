from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('registration-success/', views.registration_success, name='registration_success'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('customerprofile-needed', views.customerprofile_needed, name='customerprofile-needed'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('edit-address/', views.edit_address, name='edit-address'),
    path('delete-address-confirmation/', views.delete_address_confirmation, name='delete-address-confirmation'),
    path('delete-address/<int:address_id>', views.delete_address, name='delete-address'),
    # path('login/', include('django.contrib.auth.urls'))
    # path('login/', views.login, name='login')
    # Other URL patterns for the "customer" app can be added here
]
