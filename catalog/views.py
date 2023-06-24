from django.shortcuts import get_object_or_404, render
from catalog.models import Product, Category

# Create your views here.

def product_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {'product': product}
    return render(request, 'product.html', context)

def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    context = {'category': category}
    return render(request, 'category.html', context)
