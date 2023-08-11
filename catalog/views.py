from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from catalog.models import Product, Category
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
    else:
        reviewed = bool(product.reviews.filter(customer=request.user.customerprofile))

    context = {
        'product': product,
        'review_form': review_form,
        'reviewed': reviewed
        }
    
    return render(request, 'product.html', context)

def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    context = {'category': category}
    return render(request, 'category.html', context)

def search_results_view(request):
    """Returns products that match submitted query"""

    query = request.GET.get('query') # retrieve query
    if not query:
        query = ''

    sort = request.GET.get('sort') # retrieve sort option if there is one
    if sort == 'top-rated': # not implemented yet : have to deal with non-existent rating field
        sort_attribute = 'name'
    elif sort == 'l-exp':
        sort_attribute = 'price'
    elif sort == 'm-exp':
        sort_attribute = '-price'
    else:
        sort_attribute = '-created'

    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    ).order_by(sort_attribute) # get all products whose name OR description contains query

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
    return redirect('catalog:product_view', slug=slug)
