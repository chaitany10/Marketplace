from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from UserActions import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'UserActions'

urlpatterns =[
     path('login/', views.login_view, name='login'),
     path('register/',views.register_view, name='register'),
     path('logout/',views.logout_view,name="logout"),
     path('profile/',views.profile_view, name='profile'),
     path('itemList/',views.item_list_view, name = 'itemList'),
     path('search/',views.search, name='search'),
     path('item/<int:item_id>',views.single_item_view, name = 'singleItem'),
     path('addtocart/<int:item_id>',views.addToCart, name = 'addtocart'),
     path('cart/<int:item_id>',views.cart, name = 'cart')
     # path('search/',views.search, name='search'),
]