from django.contrib import admin
from .models import UserAttribute
# Register your models here.

@admin.register(UserAttribute)
class userattributeadmin(admin.ModelAdmin):
    list_display =('role','money','address','user')
