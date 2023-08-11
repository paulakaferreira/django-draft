from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('product/<slug:slug>/', views.product_view, name='product_view'),
    path('category/<slug:slug>/', views.category_view, name='category_view'),
    path('search/', views.search_results_view, name='search-results'),
    path('add_review/<slug:slug>/', views.add_review, name='add_review'),
    # Other URL patterns for the "catalog" app can be added here
]
