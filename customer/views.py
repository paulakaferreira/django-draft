from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomerProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomerProfileForm, AddressForm
from .models import Address


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        profile_form = CustomerProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('/customer/registration-success')
    else:
        form = UserCreationForm()
        profile_form = CustomerProfileForm()
    return render(request, 'registration/register.html', {'form': form, 'profile_form': profile_form})


def registration_success(request):
    return render(request, 'registration/registration_success.html')


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def edit_profile(request):
    user = request.user
    profile = user.customerprofile

    if request.method == 'POST':
        profile_form = CustomerProfileForm(request.POST, instance=profile)
        address_form = AddressForm(request.POST, instance=profile.address)

        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
        if address_form.is_valid():
            address_form.save()
            return redirect('profile')

    else:
        profile_form = CustomerProfileForm(instance=profile)
        address, _ = Address.objects.get_or_create(customer=profile)
        address_form = AddressForm(instance=address)

    context = {
        'profile_form': profile_form,
        'address_form': address_form,
    }

    return render(request, 'account_management/edit_profile.html', context)
