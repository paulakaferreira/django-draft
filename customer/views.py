from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .forms import CustomerProfileForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import CustomerProfile

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        profile_form = CustomerProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('/customer/registration-success')
    else:
        form = SignUpForm()
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

# NOTE : for now, all users are able to access this page but this creates 
# a 404 if they don't have a customer profile (which is the case for staff members and admin)
# 
# we need to fix this and decide how the site should behave in such cases
@login_required
def profile_view(request):
    customer = get_object_or_404(CustomerProfile, user=request.user)
    return render(request, 'account_management/profile.html', {'customer': customer})

@login_required
def change_profile_view(request):
    user_change_form = UserChangeForm()
    password_change_form = PasswordChangeForm(request.user)
    customer = get_object_or_404(CustomerProfile, user=request.user)
    return render(request, 'account_management/change_profile.html', {'customer': customer, 
                                                                      'user_change_form': user_change_form,
                                                                      'password_change_form': password_change_form})