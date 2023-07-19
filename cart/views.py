from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Cart, Product
from customer.authorizations import is_customer

@login_required
@user_passes_test(is_customer, login_url='customer:customerprofile-needed', redirect_field_name=None)
def cart_view(request):
    customer = request.user.customerprofile
    cart_items = Cart.objects.filter(customer=customer)
    context = {'cart_items': cart_items}
    return render(request, 'cart_view.html', context)


@login_required
@user_passes_test(is_customer, login_url='customer:customerprofile-needed', redirect_field_name=None)
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    customer = request.user.customerprofile
    cart_item, created = Cart.objects.get_or_create(product=product, customer=customer)
    if not created:
        cart_item.number += 1
        cart_item.save()
    return redirect('cart:cart_view')


@login_required
@user_passes_test(is_customer, login_url='customer:customerprofile-needed', redirect_field_name=None)
def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    customer = request.user.customerprofile
    cart_item = Cart.objects.get(product=product, customer=customer)
    if cart_item:
        cart_item.number -= 1
        cart_item.save()
    return redirect('cart:cart_view')