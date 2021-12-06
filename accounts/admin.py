from django.contrib import admin

from .models import Vendor, CustomUser


admin.site.register(Vendor)
admin.site.register(CustomUser)