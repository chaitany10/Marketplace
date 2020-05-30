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
     path('logout/',views.logout_view,name="logout")
]