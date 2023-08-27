from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from catalog.models import Product, Category
from orders.models import Order
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required, user_passes_test
from customer.authorizations import is_customer

# Create your views here.

def product_view(request, slug):

    product = get_object_or_404(Product, slug=slug)
    review_form = ReviewForm()

    # reviewed is True if logged in customer already reviewed the product
    # in that case, template won't display the review form
    if not request.user.is_authenticated or not is_customer(request.user):
        reviewed = False
        bought = False
    else:
        reviewed = bool(product.reviews.filter(customer=request.user.customerprofile))
        bought = False
        orders = Order.objects.filter(customer=request.user.customerprofile, status='Complete')
        for order in orders:
            if product in order.products.all():
                bought = True

    context = {
        'product': product,
        'review_form': review_form,
        'reviewed': reviewed,
        'bought': bought,
        }
    
    return render(request, 'product.html', context)

def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    subcategories = Category.objects.filter(supercategory=category)
    context = {
        'category': category,
        'subcategories': subcategories,
    }
    return render(request, 'category.html', context)

def search_results_view(request):
    """Returns products that match submitted query"""

    query = request.GET.get('query') # retrieve query
    if not query:
        query = ''

    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    ) # get all products whose name OR description contains query

    sort = request.GET.get('sort') # retrieve sort option if there is one
    if sort == 'top-rated':
        average_ratings = dict()
        for product in products: # dictionary of avg ratings ; replace None rating by 0 to support sorting
            average_ratings[product] = (product.get_average_rating() or 0)
        products = sorted(products, key=lambda l: average_ratings[l], reverse=True) # sort products by rating
    elif sort == 'l-exp':
        products = products.order_by('price')
    elif sort == 'm-exp':
        products = products.order_by('-price')
    else:
        products = products.order_by('-created')

    context = {
        'products': products,
        'query': query
    }
    
    return render(request, 'search-results.html', context)

@login_required
@user_passes_test(is_customer, login_url='customer:customerprofile-needed', redirect_field_name=None)
def add_review(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.customer = request.user.customerprofile
            review.product = product
            review.save()
    return redirect('catalog:product-view', slug=slug)

def catalog_view(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'catalog.html', context)