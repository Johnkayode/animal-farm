from django.db import models


from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .manager import CustomUserManager

import uuid

class CustomUser(AbstractUser):


    username = None
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), blank=False, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Vendor(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    business_name = models.CharField(_("business name"), max_length=250, blank=False, null=False)
    phone_number = models.CharField(_("phone number"), max_length=15)
    logo = models.ImageField(blank=True, null=True)
    address = models.CharField(_("address"), max_length=250)
    city = models.CharField(_("city"), max_length=250)

    def __str__(self):
        return self.business_name