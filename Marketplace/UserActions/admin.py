from django.contrib import admin
from .models import UserAttribute,Item,Pincodes
# Register your models here.

@admin.register(UserAttribute)
class userattributeadmin(admin.ModelAdmin):
    list_display =('role','money','address','user')


@admin.register(Item)
class Itemadmin(admin.ModelAdmin):
    list_display =('item_id','item_price','item_name','item_description','image_url','pincode','seller_id')

@admin.register(Pincodes)
class Pincodeadmin(admin.ModelAdmin):
    list_display =  ['pincode']

