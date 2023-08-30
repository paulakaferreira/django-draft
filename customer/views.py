from django.shortcuts import render, redirect

from orders.models import Order
from .forms import CustomerProfileForm, AddressForm, SignUpForm, EditUserForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomerProfile, Address
from .authorizations import is_customer
from django.contrib.auth.models import Group

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        profile_form = CustomerProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            customer_group, created = Group.objects.get_or_create(name='Customers')
            user.groups.add(customer_group) # add new user to Customers
            user.save()
            profile.user = user
            profile.save()
            return redirect('/customer/registration-success')
    else:
        form = SignUpForm()
        profile_form = CustomerProfileForm()
    return render(request, 'registration/register.html', {'form': form, 'profile_form': profile_form})


def registration_success(request):
    return render(request, 'registration/registration-success.html')


def login(request):
    """Generates an empty login form in response to a GET request. Logs customer in in response to a 
    POST request. Redirects to home"""
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
    """Logs user out and redirects to home"""
    logout(request)
    return redirect('home')


@login_required
def customerprofile_needed(request):
    """Renders a basic page requesting authentication as customer"""
    return render(request, 'registration/customerprofile-needed.html')


@login_required
@user_passes_test(is_customer, login_url='customer:customerprofile-needed', redirect_field_name=None)
def profile(request):
    """Renders profile page with profile, address and orders data."""
    customer_profile = CustomerProfile.objects.get(user=request.user)

    customer_addresses = Address.objects.filter(customer=customer_profile)

    customer_orders = Order.objects.filter(customer=customer_profile)

    context = {
        'profile': customer_profile,
        'addresses': customer_addresses,
        'orders': customer_orders,
    }
    
    return render(request, 'account-management/profile.html', context)


@login_required
@user_passes_test(is_customer, login_url='customer:customerprofile-needed', redirect_field_name=None)
def edit_profile(request):
    """Registers EditUserForm and CustomerProfileForm information. Redirects to profile after
    form validation."""
    user = request.user
    profile = user.customerprofile

    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=user) # custom user form
        profile_form = CustomerProfileForm(request.POST, instance=profile) # customerprofile form
        
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

    return render(request, 'account-management/edit-profile.html', context)



@login_required
@user_passes_test(is_customer, login_url='customer:customerprofile-needed', redirect_field_name=None)
def edit_address(request):
    """Register address information. If no GET data is retrieved, creates a new address. Otherwise if 
    GET has current_tab parameter, changes data from matching address.
    Redirects user to previous page or customer profile by default after form validation."""
    user = request.user
    profile = user.customerprofile

    addresses = Address.objects.filter(customer=profile)
    current_tab = request.GET.get('current_tab')  # Retrieve the current_tab value from the form data
    try:
        address = addresses[int(current_tab)] # Retrieve matching address
    except Exception:
        address = None

    if request.method == 'POST':
        address_form = AddressForm(request.POST, instance=address)
    
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.customer = profile
            address.save()
            # redirect to whatever page led the user to edit-address (useful when add address during order)
            if(request.POST.get('next')):
                return redirect(request.POST['next'])
            else:
                return redirect('customer:profile')
    else:
        address_form = AddressForm(instance=address)

    context = {
        'address': address,
        'address_form': address_form,
    }

    return render(request, 'account-management/edit-address.html', context)


@login_required
@user_passes_test(is_customer, login_url='customer:customerprofile-needed', redirect_field_name=None)
def delete_address_confirmation(request):
    """User confirms they want to delete given address"""
    user = request.user
    profile = user.customerprofile

    addresses = Address.objects.filter(customer=profile)
    current_tab = request.GET.get('current_tab')  # Retrieve the current_tab value from the form data

    try:
        address = addresses[int(current_tab)]
    except Exception:
        address = None

    context = {
        'address': address,
    }

    return render(request, 'account-management/delete-address.html', context)


@login_required
@user_passes_test(is_customer, login_url='customer:customerprofile-needed', redirect_field_name=None)
def delete_address(request, address_id):
    """Unlink address from customer after validation. We do not want to delete the address
    so that we can still track where past orders where billed and sent to."""
    address = Address.objects.get(id=address_id)
    address.customer = None
    address.save()

    return redirect('customer:profile')


@login_required
@user_passes_test(is_customer, login_url='customer:customerprofile-needed', redirect_field_name=None)
def change_password(request):
    """Allow customers to change their password"""
    user = request.user
    if request.method == 'POST':
        password_form = PasswordChangeForm(user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user) # prevent password change to log the user out
            return redirect('customer:profile')
    else:
        password_form = PasswordChangeForm(user=user)
    context = {
        'password_form': password_form,
    }
    return render(request, 'account-management/change-password.html', context)
