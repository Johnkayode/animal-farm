from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import Vendor

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self) :
        return self.name

class Product(models.Model):
    name = models.CharField(_("name"), max_length=250)
    slug = models.CharField(max_length=100, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="products")
    category = models.ManyToManyField(Category, related_name="products")
    age = models.CharField(_("age"), max_length=100, null=True)
    display_image = models.ImageField()
    price  = models.DecimalField(decimal_places=2, max_digits=10)
    minimum_order_amount = models.IntegerField(default=1)

    def __str__(self) :
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField()

    def __str__(self) :
        return self.id