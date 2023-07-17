from django.shortcuts import render, redirect
from .forms import CustomerProfileForm, AddressForm, SignUpForm, EditUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import CustomerProfile, Address

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

@login_required
def profile(request):
    customer_profile = CustomerProfile.objects.get(user=request.user)

    customer_addresses = Address.objects.filter(customer=customer_profile)

    context = {
        'profile': customer_profile,
        'addresses': customer_addresses,
    }
    
    return render(request, 'account_management/profile.html', context)


@login_required
def edit_profile(request):
    user = request.user
    profile = user.customerprofile

    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=user)
        profile_form = CustomerProfileForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('customer:profile')
        
    else:
        user_form = EditUserForm(instance=user)
        profile_form = CustomerProfileForm(instance=profile)
        
    context = {
        'user_form' : user_form,
        'profile_form': profile_form,
    }

    return render(request, 'account_management/edit_profile.html', context)



@login_required
def edit_address(request):
    user = request.user
    profile = user.customerprofile

    addresses = Address.objects.filter(customer=profile)
    current_tab = request.GET.get('current_tab')  # Retrieve the current_tab value from the form data
    try:
        address = addresses[int(current_tab)]
    except Exception:
        address = None

    if request.method == 'POST':
        address_form = AddressForm(request.POST, instance=address)
    
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.customer = profile
            address.save()
            return redirect('customer:profile')
    else:
        address_form = AddressForm(instance=address)

    context = {
        'address_form': address_form,
        'current_tab': current_tab,  # Pass the current_tab value to the template context
    }

    return render(request, 'account_management/edit_address.html', context)
