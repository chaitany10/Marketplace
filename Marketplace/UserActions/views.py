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
from .models import UserAttribute,Item,Cart,Slottings
from datetime import datetime, timedelta, timezone
from itertools import chain
from django.db.models import Q

# Create your views here.

def register_view(request):
    #  checking for authentication
    if request.user.is_authenticated:
        return redirect('UserActions:profile')
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
        return redirect('UserActions:profile')

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
    return HttpResponseRedirect(reverse('home'))



def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('UserActions:login')
    else:
        user = request.user
        userattribute = UserAttribute.objects.get(user=user)
        context = {
            'userattribute' : userattribute
        }

        return render(request, 'profile.html',context)


def history_view(request):
    # Check for Authentication
    if not request.user.is_authenticated:
        return redirect('userActions:login')
    else:
        # Get all the items that have been uploaded by the user
        orders = Item.objects.filter(username=request.user)
        user_history_claimed_items = ClaimedItems.objects.filter(
            upload_user=request.user)
        context = {}
        # Appending both list by using itertools library(implemented in C)
        
        if len(user_history_active_items) == 0 and len(user_history_claimed_items) == 0:
            context['empty'] = True

        

        context['user_history_claimed_items'] =  user_history_claimed_items
        context['user_history_active_items'] = user_history_active_items
        
        return render(request, 'history.html', context)



# #  Views to view all items uploaded by other users
# # Requests: GET


def item_list_view(request):
    # Check for Authentication
    if not request.user.is_authenticated:
        return redirect('UserActions:login')
    else:
        # Getting all Items
        itemsList = Item.objects.all()
        # Filtering out item that are uploaded by the current user
        
        
        context = {
            'itemList': itemsList
        }

        return render(request, 'item_list.html', context)

def search(request):
    if request.method == 'GET':
        query = request.GET.get('search')

        if query is not None:
            context = {}
            results = Item.objects.filter(item_name__contains=query)
            # Filtering out item that are uploaded by the current user
            
            context['results'] = results
            context['search'] = True
            if len(results) == 0:
                context['empty'] = True
            return render(request, 'item_list.html', context)

        else:
            return render(request, 'item_list.html')

    else:
        return render(request, 'item_list.html')


# # A detailed view for Single Item
# # Requests: GET for gettting the item and POST for getting new bid


def single_item_view(request, item_id):
    # Check for Authentication
    if not request.user.is_authenticated:

        return redirect('UserActions:login')

    else:
        available = False
        cart = Cart.objects.filter(cart_id = request.user,item_id = item_id).exists()
        print(cart)
        if(cart != False):
            available = False
            print(available)
        else:
            available = True
        item = Item.objects.get(item_id=item_id)  # Get specified Object
        
        context={
            'item' : item,
            'cart' : available
        }
        return render(request, 'single_item.html', context)

def cart(request):
    if not request.user.is_authenticated:
        return redirect('UserActions:login')
    else:
        cart_items = Cart.objects.filter(cart_id = request.user)
        total_amount = Cart.objects.filter(cart_id = request.user).last().total_amount
        
        context={
            'list' : cart_items,
            'total_amount' : total_amount
        }
        return render(request, 'cart.html', context)


def addToCart(request,item_id):
    if not request.user.is_authenticated:
        return redirect('UserActions:login')
    else:
        cart = Cart.objects.filter(cart_id = request.user).exists()

        if cart == False:
            item = Item.objects.get(item_id = item_id)
            cart = Cart()
            cart.cart_id = request.user
            cart.item = item
            cart.total_amount = item.item_price
            cart.save()
            cart = False
        else:
            last_cart = Cart.objects.filter(cart_id = request.user).last()
            cart=Cart()
            item = Item.objects.get(item_id = item_id)
            cart.cart_id = request.user
            cart.item = item
            cart.total_amount = last_cart.total_amount + item.item_price
            cart.save()
            cart = False
            
        return HttpResponseRedirect('/item/'+str(item.item_id))
# # View for checking the items that the user has bidded on and is currently the hhighest bidder
# # Requests: GET


# # View for finally claiming the item after deadline has crossed
# # Requests: GET and POST for saving new info


def checked_out(request):
    if not request.user.is_authenticated:
        return redirect('UserActions:login')
    else:
        
        cart_items = Cart.objects.filter(cart_id = request.user)
        total_amount = Cart.objects.filter(cart_id = request.user).last().total_amount
        user = UserAttribute.objects.get(user = request.user)
        
        
        slots = Slottings.objects.all()

        if(total_amount>user.money):
             messages.error(request, 'Insufficient balance')
        else:
            user.money -= total_amount
            user.save()
        context = {
            'user' : user,
            'itemList':cart_items,
            'total_amount' : total_amount,
            'slots':slots,
            
        }
        return render(request,'checkout.html',context)
        

def time_difference(deadline_date):
    current_time = datetime.now(timezone.utc)  # Getting current time UTC
    difference_time = deadline_date - current_time
    #  Using total_seconds() function to calulate time difference in seconds, subtracting 19800(5 hours 30 minutes for time correction)
    return (difference_time.total_seconds() - 19800)
