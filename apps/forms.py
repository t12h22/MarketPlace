from django import forms
from .models import Product
from .models import CustomUser

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'image')

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')
