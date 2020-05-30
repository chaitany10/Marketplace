from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login
from django import forms
from django.contrib import auth
# from .models import Item
from django.conf import settings
import datetime
from datetime import datetime,timedelta,timezone
# Using Custom registration form

ROLE_CHOICES = [
    ('customer','Customer'),
    ('Seller','Seller')

]
class RegisterForm(forms.Form):
    username = forms.CharField(label='username', min_length=3,widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'please enter user name'}))
    password = forms.CharField(label='Password',min_length=8, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Password'}))
    password_again = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Same Password Again'}))
    address = forms.CharField(label = 'Address',widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'please enter your address'}))
    role = forms.CharField(label='Select Role', widget=forms.Select(choices=ROLE_CHOICES))
    # Checking for Same Password 
    def clean_password_again(self):
        password = self.cleaned_data.get('password')
        password_again = self.cleaned_data.get('password_again')
        if password and password_again and password != password_again:
            raise forms.ValidationError('Inconsistent password entered twice')
        return password_again



# Custom login Form
class LoginForm(forms.Form):
    username = forms.CharField(label='username', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'please enter user name'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Password'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('Username or password is incorrect')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data
