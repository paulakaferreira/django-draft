from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Cart, Product
from customer.authorizations import is_customer
from django.contrib import messages

@login_required
@user_passes_test(is_customer, login_url='customer:customerprofile-needed', redirect_field_name=None)
def cart_view(request):
    customer = request.user.customerprofile
    cart_items = Cart.objects.filter(customer=customer)
    context = {
        'cart_items': cart_items,
        'select_quantity_iterator': range(9),
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
def change_quantity(request, product_id, item_number):

    user = request.user
    customer = user.customerprofile

    # check that product and cart_item for active customer exist, otherwise send a warning
    try:
        product = Product.objects.get(id=int(product_id))
        item = Cart.objects.get(product=product, customer=customer)

        # delete cart item if product is no longer available
        if item.product.stock == 0:
            messages.warning(request, f"Product {item.product} is not available at the moment")
            item.delete()

        else:
            # check that quantity is a valid positive integer
            try:
                item.number = int(item_number)
                # remove item if selected quantity is 0
                if item.number == 0:
                    item.delete()
                # set quantity to product stock if desired quantity is bigger
                elif item.number > item.product.stock:
                    item.number = item.product.stock
                    messages.warning(request, f"There are only {item.number} products in stock for {item.product}")
                    item.save()
                # if everything is OK, just save the item with the new quantity
                else:
                    item.save()
            except:
                messages.warning(request, f"Cannot resolve {item_number} to a valid quantity")
    except:
        messages.warning(request, "Cannot access desired item")
    return redirect('cart:cart_view')


@login_required
@user_passes_test(is_customer, login_url='customer:customerprofile-needed', redirect_field_name=None)
def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    customer = request.user.customerprofile
    cart_item = Cart.objects.get(product=product, customer=customer)
    cart_item.delete()
    return redirect('cart:cart_view')
