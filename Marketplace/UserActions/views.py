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
    return HttpResponseRedirect('home')



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


# def history_view(request):
#     # Check for Authentication
#     if not request.user.is_authenticated:
#         return redirect('userActions:login')
#     else:
#         # Get all the items that have been uploaded by the user
#         user_history_active_items = Item.objects.filter(username=request.user)
#         user_history_claimed_items = ClaimedItems.objects.filter(
#             upload_user=request.user)
#         context = {}
#         # Appending both list by using itertools library(implemented in C)
        
#         if len(user_history_active_items) == 0 and len(user_history_claimed_items) == 0:
#             context['empty'] = True

        

#         context['user_history_claimed_items'] =  user_history_claimed_items
#         context['user_history_active_items'] = user_history_active_items
        
#         return render(request, 'history.html', context)



# #  Views to view all items uploaded by other users
# # Requests: GET


# def item_list_view(request):
#     # Check for Authentication
#     if not request.user.is_authenticated:
#         return redirect('userActions:login')
#     else:
#         # Getting all Items
#         itemsList = Item.objects.all()
#         # Filtering out item that are uploaded by the current user
#         itemsListExcludingCurrentuser = itemsList.exclude(
#             username=request.user)
#         final_items = []
#         for item in itemsListExcludingCurrentuser:  # Excluding item that have long passed their deadline, a good implementation would be to create a new model for archived_items
#             if(time_difference(item.deadline_date) > 0):
#                 final_items.append(item)

#         context = {
#             'itemList': final_items,
#         }

#         return render(request, 'item_list.html', context)

# # A detailed view for Single Item
# # Requests: GET for gettting the item and POST for getting new bid


# def single_item_view(request, item_id):
#     # Check for Authentication
#     if not request.user.is_authenticated:

#         return redirect('userActions:login')

#     else:
#         context = {}
#         context['claimed_item'] = False
#         item = Item.objects.get(item_id=item_id)  # Get specified Object
#         if item is None:
#             return redirect('userActions:profile')
#         context['item'] = item
#         can_bid = False  # Whether the Item is Still available for bidding or not
#         # Checking whether the current time has crossed Deadline Date
#         if(time_difference(item.deadline_date) > 0):
#             can_bid = True
#         else:
#             can_bid = False
#         context['can_bid'] = can_bid

#         # Getting new Bid from User
#         if request.method == 'POST':
#             form = BidForm(request.POST)

#             if form.is_valid():
#                 success = False
#                 new_bid = form.cleaned_data.get('new_bid')

#                 # Checking whether the new bid is greater than the current highest bid
#                 if(new_bid > item.highest_bid):
#                     item.highest_bid = new_bid
#                     item.highest_bid_user = request.user
#                     item.save()  # Saving the object after updating highest bid

#                     # Saving details to bid object if the bid by user for that item already exists
#                     if Bid.objects.filter(username=request.user, item=item).exists():
#                         bid = Bid.objects.get(username=request.user, item=item)
#                         bid.bid_amount = new_bid
#                         bid.save()

#                     # Creating new bid if user is bidding for the first time for the selected item
#                     else:
#                         bid = Bid()
#                         bid.username = request.user
#                         bid.item = item
#                         bid.bid_amount = new_bid
#                         bid.save()

#                     context['success'] = True
#                     messages.success(request, 'Bid Successfull')

#                 else:
#                     messages.error(
#                         request, 'New Bid cant be less than current Highest Bid')
#                     context['success'] = False
#         else:
#             form = BidForm()
#         context['available'] = True
#         context['form'] = form
#         return render(request, 'single_item.html', context)

# # View for checking the items that the user has bidded on and is currently the hhighest bidder
# # Requests: GET


# # View for finally claiming the item after deadline has crossed
# # Requests: GET and POST for saving new info


# def checked_out(request, item_id):
#     if not request.user.is_authenticated:
#         return redirect('userActions:login')
#     else:
#         context = {}
#         item = Item.objects.get(item_id=item_id)
#         if(time_difference(item.deadline_date) < 0):  # Check whether deadline has crossed
#             context['item'] = item
#             save_to_claimed_item(item)
#             item.delete()
#             context['item'] = item
#             context['claimed_item'] = True
#             return render(request, 'single_item.html', context)
#         else:
#             return redirect('userActions:profile')