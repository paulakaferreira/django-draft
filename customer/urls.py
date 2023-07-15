from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('registration-success/', views.registration_success, name='registration_success'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('change-profile/', views.change_profile_view, name='change_profile')
    # path('login/', include('django.contrib.auth.urls'))
    # path('login/', views.login, name='login')
    # Other URL patterns for the "customer" app can be added here
]
