from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, Product

@login_required(login_url='/customer/login')
def cart_view(request):
    customer = request.user.customerprofile
    cart_items = Cart.objects.filter(customer=customer)
    context = {'cart_items': cart_items}
    return render(request, 'cart_view.html', context)


@login_required(login_url='/customer/login')
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    customer = request.user.customerprofile
    cart_item, created = Cart.objects.get_or_create(product=product, customer=customer)
    if not created:
        cart_item.number += 1
        cart_item.save()
    return redirect('cart:cart_view')