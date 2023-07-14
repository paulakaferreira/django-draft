from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/customer/login')
def cart_view(request):
    return render(request, 'cart.html')
