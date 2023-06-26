from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomerProfileForm, AddressForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        profile_form = CustomerProfileForm(request.POST)
        address_form = AddressForm(request.POST)
        if form.is_valid() and profile_form.is_valid() and address_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            address = address_form.save(commit=False)
            address.customer = profile
            address.save()
            return redirect('registration_success')
    else:
        form = UserCreationForm()
        profile_form = CustomerProfileForm()
        address_form = AddressForm()
    return render(request, 'registration/register.html', {'form': form, 'profile_form': profile_form, 'address_form': address_form})


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
