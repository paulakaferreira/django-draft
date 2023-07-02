from django.shortcuts import get_object_or_404, render
from cart.models import Cart
from customer.models import CustomerProfile
from django.contrib.auth.decorators import login_required

@login_required(login_url='/customer/login')
def cart_view(request):
    return render(request, 'cart.html')
