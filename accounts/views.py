from django.shortcuts import render, redirect
from django.template.loader import get_template, render_to_string

from accounts.models import CustomUser, Vendor

from .forms import UserRegistrationForm, VendorRegistrationForm, CustomAuthForm, UserForm, VendorForm
from .tasks import send_mail_task


from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from shop.models import Category

import os, requests


def register(request):
    user_form = UserRegistrationForm(request.POST or None)
    vendor_form = VendorRegistrationForm(request.POST or None)
    if request.method == "POST":
        if user_form.is_valid() and vendor_form.is_valid():
            user = user_form.save()
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            vendor.save()
            message = "One more step to start selling your poultry birds"
            verification_code = user.verification_code
            html_message = f"Hi {vendor.business_name},\n\nYou're almost done setting up your account.\n\nYour verification code: {verification_code}"
            """
            send_mail_task.delay( 
               email=user.email
               html_message=html_message
            )
            """
            requests.post("https://api.mailgun.net/v3/animalfarm.ng/messages", auth=("api", os.environ.get("MAILGUN_API_KEY")), data={"from": "Animal Farm NG <hello@animalfarm.ng>", "to": [user.email],  "subject": "Verify Your Account", "text": html_message})
            
            messages.success(request, 'Account successfully created. Verify your Account')
            return redirect("account:verify")
        else:
            print(user_form.errors, vendor_form.errors)

    categories = Category.objects.all()
    context = {"user_form":user_form, "vendor_form":vendor_form,"categories":categories}
    return render(request, "accounts/register.html", context)


def verify(request):
    if request.method == "POST":
        code = request.POST.get("verification_code")
        user = CustomUser.objects.filter(verification_code=code).first()
        if not user.verified:
            print(user.verified)
            user.verified = True
            user.save()
            messages.success(request, 'Account successfully verified. You can now log in.')
            return redirect("account:login")
        else:
            messages.success(request, 'Account has been verified already.')
            return redirect("account:login")
    return render(request, "accounts/verify.html")
    

def login_user(request):
    form = CustomAuthForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email = cd['email'], password=cd['password']) 

            if user is not None:
                if not user.verified:
                    messages.error(request, 'Account has not been verified')
                    return redirect("account:verify")
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
    vendor_form = VendorForm(request.POST or None, request.FILES or None, instance=request.user.vendor)
    if request.method == 'POST':
        if user_form.is_valid() and vendor_form.is_valid():
            user_form.save()
            vendor_form.save()
            messages.success(request, 'Account successfully updated')
            return redirect('account:profile')
    return render(request, "dashboard/profile.html", context = {"user_form":user_form,"vendor_form":vendor_form})