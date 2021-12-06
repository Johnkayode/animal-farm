from django.db import models


from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .manager import CustomUserManager
from .utils import generate_code

import uuid

class CustomUser(AbstractUser):


    username = None
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), blank=False, unique=True)
    verified = models.BooleanField(default=False)
    verification_code = models.CharField(_("verification code"), max_length=6, default=generate_code)

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
    street = models.CharField(_("street"), max_length=250, null=True)
    city = models.CharField(_("city"), max_length=250, null=True)
    state = models.CharField(_("state"), max_length=250, null=True)

    def __str__(self):
        return self.business_name