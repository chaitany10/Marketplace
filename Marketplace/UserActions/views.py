from django.shortcuts import render
from django.shortcuts import redirect, render
from django.http.response import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegisterForm
from django.contrib import auth, messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import UserAttribute
from datetime import datetime, timedelta, timezone
from itertools import chain
from django.db.models import Q

# Create your views here.

def register_view(request):
    #  checking for authentication
    if request.user.is_authenticated:
        return redirect('')
    else:
        #  Getting Form Info
        if request.method == "POST":
            form = RegisterForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')

                password = form.cleaned_data.get('password')
                address = form.cleaned_data.get('address')
                role = form.cleaned_data.get('role')
                if User.objects.filter(username=form.cleaned_data['username']).exists():
                    messages.error(request, 'Username exists')
                else:
                    user = User.objects.create_user(
                        username=username, password=password)  # Creating new User
                    # Authenticating New User
                    userattribute = UserAttribute()
                    userattribute.user = user
                    userattribute.address = address
                    userattribute.role = role
                    userattribute.money = 0
                    userattribute.save()
                    user1 = authenticate(username=username, password=password)
                    login(request, user1)  # Logging In
                    return redirect('UserActions:profile')
        else:
            form = RegisterForm()
        return render(request, 'signup.html', {'form': form})

def login_view(request):
    #  Authentication check. Users currently logged in cannot view this page.
    if request.user.is_authenticated:
        return redirect('')

    #  Standard Login through Forms
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(
                username=login_form.cleaned_data['username'],
                password=login_form.cleaned_data['password']
            )
            login(request, user)

            if user is not None:
                return HttpResponseRedirect('/profile/')
            else:
                messages.error(request, 'Username or Password not correct')

    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)
@login_required
def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect('')
