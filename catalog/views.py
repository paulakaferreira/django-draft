from django.shortcuts import get_object_or_404, render, redirect
from catalog.models import Product, Category
from .forms import ReviewForm

# Create your views here.

def product_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    review_form = ReviewForm()
    context = {
        'product': product,
        'review_form': review_form,
        }
    return render(request, 'product.html', context)

def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    context = {'category': category}
    return render(request, 'category.html', context)

def add_review(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.customer = request.user.customerprofile
            review.product = product
            review.save()
    return redirect('catalog:product_view', slug=slug)
