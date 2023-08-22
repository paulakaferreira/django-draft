from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderProduct, Delivery
from .forms import OrderCreationForm
from django.contrib.auth.decorators import login_required
from customer.models import Address
from django.shortcuts import render, redirect
from cart.models import Cart
from django.http import HttpResponse


@login_required
def choose_addresses(request):
    customer = request.user.customerprofile

    customer_addresses = Address.objects.filter(customer=customer)

    context = {
        'customer_addresses': customer_addresses,
    }

    return render(request, 'choose_address.html', context)

@login_required
def create_order(request):
    customer = request.user.customerprofile
    customer_addresses = Address.objects.filter(customer=customer)
    if request.method == 'POST':
        order_form = OrderCreationForm(request.POST)
        if order_form.is_valid():

            billing_id = order_form.cleaned_data['billingAddress']
            delivery_address = order_form.cleaned_data['deliveryAddress']

            billing_address = Address.objects.get(id=billing_id)

            order = Order.objects.create(
                price=0,  # TODO: correct the price
                status='Pending',  
                customer=customer,
                billing_address=billing_address,
            )

            cart_items = Cart.objects.filter(customer=customer)

            for cart_item in cart_items:
                OrderProduct.objects.create(
                    order=order,
                    product=cart_item.product,
                    number=cart_item.number,
                    subtotal=cart_item.subtotal(),
                )

            return redirect('orders:order-details', order_id=order.id)
        else:
            return HttpResponse("Form is not valid.")
    else:
        order_form = OrderCreationForm(customer_addresses)

def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_products = OrderProduct.objects.filter(order=order)

    context = {
        'order': order,
        'order_products': order_products,
    }

    return render(request, 'order_details.html', context)