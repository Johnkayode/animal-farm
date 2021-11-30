from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

from .models import Vendor

def is_vendor(function):
  @wraps(function)
  def wrap(request, *args, **kwargs):
        user = request.user
        vendor = Vendor.objects.filter(user=user)
        if vendor is not None:
             return function(request, *args, **kwargs)
        else:
            messages.error(request, "You don't have necessary permissions")
            return redirect("shop:home")
  return wrap