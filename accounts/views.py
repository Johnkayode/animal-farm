from django.shortcuts import render, redirect

from accounts.models import Vendor
from .forms import UserRegistrationForm, VendorRegistrationForm, CustomAuthForm, UserForm, VendorForm
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from shop.models import Category

def register(request):
    user_form = UserRegistrationForm(request.POST or None)
    vendor_form = VendorRegistrationForm(request.POST or None)
    if request.method == "POST":
        if user_form.is_valid() and vendor_form.is_valid():
            user = user_form.save()
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            vendor.save()
            messages.success(request, 'Account succesfully created. You can now login')
            return redirect("account:login")
    categories = Category.objects.all()
    context = {"user_form":user_form, "vendor_form":vendor_form,"categories":categories}
    return render(request, "accounts/register.html", context)

def login_user(request):
    form = CustomAuthForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email = cd['email'], password=cd['password']) 
            if user is not None:
                login(request, user)
                messages.success(request, 'Login Successful')
                return redirect(request.GET.get('next','dashboard:home'))
            else:
                messages.error(request, 'Account does not exist')
    categories = Category.objects.all()
    context = {"form": form,"categories":categories}
    return render(request, "accounts/login.html", context)

@login_required
def logout_user(request):
    logout(request)
    return redirect("shop:home")


@login_required
def profile(request):
    user_form = UserForm(request.POST or None, instance=request.user)
    vendor_form = VendorForm(request.POST or None, instance=request.user.vendor)
    if request.method == 'POST':
        if user_form.is_valid() and vendor_form.is_valid():
            user_form.save()
            vendor_form.save()
            messages.success(request, 'Account successfully updated')
            return redirect('account:profile')
    return render(request, "dashboard/profile.html", context = {"user_form":user_form,"vendor_form":vendor_form})