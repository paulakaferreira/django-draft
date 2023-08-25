from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderProduct, Delivery, Payment
from django.contrib.auth.decorators import login_required, user_passes_test
from customer.models import Address
from django.shortcuts import render, redirect
from cart.models import Cart
from django.contrib import messages
from customer.authorizations import is_customer


@login_required
@user_passes_test(is_customer, login_url='customer:customerprofile-needed', redirect_field_name=None)
def choose_addresses(request):
    customer = request.user.customerprofile

    customer_addresses = Address.objects.filter(customer=customer)

    context = {
        'customer_addresses': customer_addresses,
    }

    return render(request, 'choose_address.html', context)

@login_required
@user_passes_test(is_customer, login_url='customer:customerprofile-needed', redirect_field_name=None)
def create_order(request):

    customer = request.user.customerprofile

    if request.method == 'POST':

        # delete pending orders (and associated deliveries) if any
        pending_orders = Order.objects.filter(customer=customer, status='Pending')
        if pending_orders:
            pending_orders.delete()

        # retrieve post data
        billing_id = request.POST['billingAddress']
        delivery_id = request.POST['deliveryAddress']

        # retrieve addresses
        billing_address = Address.objects.get(id=billing_id)
        delivery_address = Address.objects.get(id=delivery_id)

        # create Order object
        order = Order.objects.create(
            customer=customer,
            billing_address=billing_address
        )

        # create OrderProduct and increment order price
        cart_items = Cart.objects.filter(customer=customer)
        for cart_item in cart_items:
            OrderProduct.objects.create(
                order=order,
                product=cart_item.product,
                number=cart_item.number,
                price=cart_item.product.price,
            )
            order.price += cart_item.subtotal

        order.save()

        # create associated delivery
        Delivery.objects.create(
            order=order,
            shipping_address=delivery_address,
        )

        # redirect to order_details view
        return redirect('orders:order-details', order_id=order.id)
    
    # redirect to cart if request method is not POST
    else:
        return redirect('cart:cart_view')


@login_required
@user_passes_test(is_customer, login_url='customer:customerprofile-needed', redirect_field_name=None)
def order_details(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    # check if requested order belongs to authenticated customer
    if order.customer != request.user.customerprofile:
        messages.error(request, "You cannot view this order's details")
        return redirect('home')

    delivery = get_object_or_404(Delivery, order=order)
    order_products = OrderProduct.objects.filter(order=order)

    context = {
        'order': order,
        'delivery': delivery,
        'total': order.price + delivery.delivery_fee,
        'order_products': order_products,
    }

    return render(request, 'order_details.html', context)


@login_required
@user_passes_test(is_customer, login_url='customer:customerprofile-needed', redirect_field_name=None)
def payment(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    if order.customer != request.user.customerprofile:
        messages.error(request, "You cannot view this payment")
        return redirect('home')

    context = {
        'order': order,
    }

    return render(request, 'confirm_payment.html', context)


@login_required
@user_passes_test(is_customer, login_url='customer:customerprofile-needed', redirect_field_name=None)
def payment_success(request, order_id):
    
    order = get_object_or_404(Order, id=order_id)

    if order.customer != request.user.customerprofile:
        messages.error(request, "You cannot view this payment")
        return redirect('home')
    
    payment, created = Payment.objects.get_or_create(
        order = order
    )

    context = {
        'order': order,
        'payment': payment,
    }
    
    if created:
        order.status = 'Complete'
        order.save()

        return render(request, 'payment_success.html', context)
    else:
        # TODO: change redirect page in case of payment error
        return redirect('cart:cart_view')

