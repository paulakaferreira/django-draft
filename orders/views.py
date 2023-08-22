from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderProduct, Delivery
from .forms import OrderCreationForm
from django.contrib.auth.decorators import login_required
from customer.models import Address
from django.shortcuts import render, redirect
from cart.models import Cart
from django.http import HttpResponse
from datetime import datetime, timedelta


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
            delivery_id = order_form.cleaned_data['deliveryAddress']

            billing_address = Address.objects.get(id=billing_id)
            delivery_address = Address.objects.get(id=delivery_id)

            order, created = Order.objects.get_or_create(
                customer=customer,
                billing_address=billing_address,
            )

            cart_items = Cart.objects.filter(customer=customer)

            order.price = 0

            for cart_item in cart_items:
                OrderProduct.objects.get_or_create(
                    order=order,
                    product=cart_item.product,
                    number=cart_item.number,
                )
                order.price += cart_item.subtotal

            order.save()

            delivery, created = Delivery.objects.get_or_create(
                order=order,
                shipping_address=delivery_address,
            )

            if created is False and delivery.status == "Pending":

                delivery.estimated_arrival_date = datetime.today().date() + timedelta(days=5)
                delivery.delivery_date = datetime.today().date() + timedelta(days=2)
                delivery.save()

            return redirect('orders:order-details', order_id=order.id)
        else:
            return HttpResponse("Form is not valid.")
    else:
        order_form = OrderCreationForm(customer_addresses)

@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    delivery = get_object_or_404(Delivery, order=order)
    order_products = OrderProduct.objects.filter(order=order)

    context = {
        'order': order,
        'delivery': delivery,
        'order_products': order_products,
    }

    return render(request, 'order_details.html', context)