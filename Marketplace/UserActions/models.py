from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django import forms


# Create your models here.

class Pincodes(models.Model):
    pincode = models.IntegerField()

#Item Model
class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_price = models.FloatField()
    item_name = models.CharField(max_length = 100)
    item_description = models.CharField(max_length = 250, blank = True)
    image_url = models.FileField(upload_to='documents')
    pincode = models.ForeignKey(Pincodes,on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.item_name, self.highest_bid)


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    total_amount = models.FloatField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    
class UserAttribute(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length = 250, blank = True)
    address = models.CharField(max_length = 250, blank = True)
    money =  models.FloatField( blank = True)
    # cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
