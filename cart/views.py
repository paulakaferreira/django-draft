from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Cart, Product
from customer.authorizations import is_customer

@login_required
@user_passes_test(is_customer, login_url='customer:customerprofile-needed', redirect_field_name=None)
def cart_view(request):
    customer = request.user.customerprofile
    cart_items = Cart.objects.filter(customer=customer)
    context = {
        'cart_items': cart_items,
        'select_quantity_iterator': range(10),
        }
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
def change_quantity(request, item_counter, item_number):
    user = request.user
    customer = user.customerprofile
    cart_items = Cart.objects.filter(customer=customer)
    item = cart_items[item_counter]
    item.number = item_number
    item.save()
    return redirect('cart:cart_view')


@login_required
@user_passes_test(is_customer, login_url='customer:customerprofile-needed', redirect_field_name=None)
def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    customer = request.user.customerprofile
    cart_item = Cart.objects.get(product=product, customer=customer)
    cart_item.delete()
    return redirect('cart:cart_view')