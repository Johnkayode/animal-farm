from django import forms
from django.forms.widgets import PasswordInput, TextInput, EmailInput, FileInput, NumberInput, DateInput, Select
from .models import CustomUser, Vendor





class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=PasswordInput(attrs={'class':'form-control', 'required':'required', "placeholder":"Password"}))
    confirm_password = forms.CharField(widget=PasswordInput(attrs={'class':'form-control', 'required':'required', "placeholder":"Confirm Password", "aria-describedby":"validationPasswordFeedback"}))
    
    
    class Meta:
        model = CustomUser
        fields = ('email',) 
        widgets = {
        'email': EmailInput(attrs={'class':'form-control', 'required':'required',"placeholder":"Email"})
    }


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class VendorRegistrationForm(forms.ModelForm):

    class Meta:
        model = Vendor
        fields = ('business_name',"phone_number","logo","street","city","state") 
        widgets = {
        'business_name': TextInput(attrs={'class':'form-control', 'required':'required',"placeholder":"Business Name"}),
        'phone_number': TextInput(attrs={'class':'form-control', 'required':'required', "placeholder":"WhatsApp Number (+234**********)"}),
        'street': TextInput(attrs={'class':'form-control', 'required':'required', "placeholder":"Street"}),
        'city': TextInput(attrs={'class':'form-control', 'required':'required', "placeholder":"City"}),
        'state': TextInput(attrs={'class':'form-control', 'required':'required', "placeholder":"State"}),
    }

class CustomAuthForm(forms.Form): 
    email = forms.CharField(widget=EmailInput(attrs={'class':'form-control', 'placeholder':'ex. name@gmail.com', 'required':'required'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class':'form-control','placeholder':'*******', 'required':'required'}))



class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email',) 
        widgets = {
        'email': EmailInput(attrs={'class':'form-control', 'required':'required'}),
    }

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ('business_name','phone_number', 'logo', 'street',"city","state") 
        widgets = {
        'business_name': TextInput(attrs={'class':'form-control', 'required':'required'}),
        'phone_number': TextInput(attrs={'class':'form-control', 'required':'required'}),
        'street': TextInput(attrs={'class':'form-control', 'required':'required'}),
        'city': TextInput(attrs={'class':'form-control', 'required':'required'}),
        'state': TextInput(attrs={'class':'form-control', 'required':'required'}),
    }