from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Cart, Product
from customer.authorizations import is_customer
from django.contrib import messages

@login_required
@user_passes_test(is_customer, login_url='customer:customerprofile-needed', redirect_field_name=None)
def cart_view(request):
    """Renders a page with a list of items in customer's cart."""
    customer = request.user.customerprofile
    cart_items = Cart.objects.filter(customer=customer)
    context = {
        'cart_items': cart_items,
        'select_quantity_iterator': range(9),
        }
    return render(request, 'cart-view.html', context)


@login_required
@user_passes_test(is_customer, login_url='customer:customerprofile-needed', redirect_field_name=None)
def add_to_cart(request, product_id):
    """Adds a product (retrieved by its id) to authenticated customer's cart.
    Increases quantity by redirecting to change_quantity() if product already in cart.
    Otherwise, redirects to cart_view()"""
    product = Product.objects.get(id=product_id)
    customer = request.user.customerprofile
    cart_item, created = Cart.objects.get_or_create(product=product, customer=customer)
    if not created: # product is already in cart
        quantity = cart_item.number + 1
        return redirect('cart:change-quantity', product_id=product_id, item_number=quantity)
    else:
        return redirect('cart:cart-view')


@login_required
@user_passes_test(is_customer, login_url='customer:customerprofile-needed', redirect_field_name=None)
def change_quantity(request, product_id, item_number):
    """Takes in a product id and desired quantity as parameters. Retrieves authenticated customer
    and changes quantity of product in their cart.
    
    Throws exceptions and generate messages if :
    * product is no longer available (deletes cart item)
    * asked quantity outnumbers available stock (sets quantity to max availability)
    * requested quantity is not valid
    * product is no longer in cart
    
    Redirects to cart_view"""

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
    return redirect('cart:cart-view')


@login_required
@user_passes_test(is_customer, login_url='customer:customerprofile-needed', redirect_field_name=None)
def remove_from_cart(request, product_id):
    """Removes product from cart and redirects to cart_view"""
    product = Product.objects.get(id=product_id)
    customer = request.user.customerprofile
    cart_item = Cart.objects.get(product=product, customer=customer)
    cart_item.delete()
    return redirect('cart:cart-view')
