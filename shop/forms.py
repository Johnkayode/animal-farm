from django import forms
from django.forms.widgets import PasswordInput, TextInput, EmailInput, FileInput, NumberInput, DateInput, Select
from .models import Product, Category

import string
import random


def slugify(word):
    letters = string.ascii_lowercase
    random_str = ''.join(random.choice(letters) for i in range(5)) 
    slug = word.lower().replace(" ", "-") + f"-{random_str}"
    return slug

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name','display_image', 'detail', 'price', 'age','minimum_order_amount') 
        widgets = {
        'name':TextInput(attrs={'class':'form-control', 'required':'required'}),
        'age' : TextInput(attrs={'class':'form-control', 'required':'required'}),
        'detail': TextInput(attrs={'class':'form-control', 'required':'required'}),
        'price' : NumberInput(attrs={'class':'form-control', 'required':'required'}),
        'minimum_order_amount' : NumberInput(attrs={'class':'form-control', 'required':'required'}),
        'display_image' : FileInput(attrs={'class':'form-control', 'required':'required'})
    }

    def save(self, commit=True):
        product = super().save(commit=False)
        slug = slugify(self.cleaned_data["name"])
        product.slug = slug
        if commit:
            product.save()
        return product
