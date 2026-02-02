from django.contrib import admin
from .models import *

# Register your models here.

class AdminSetting(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone']
    
    
    
admin.site.register(Setting, AdminSetting)
admin.site.register(Cart)
admin.site.register(Order)