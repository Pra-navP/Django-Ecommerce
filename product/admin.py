from django.contrib import admin
from .models import *

# Register your models here.

class AdminCategory(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name', ]
    list_filter = ['created_at',]

class AdminProduct(admin.ModelAdmin):
    list_display = ['title', 'stock', 'discounted_price', 'trending', 'created_at',]
    search_fields = ['title', 'category',]
    list_filter = ['created_at', 'actual_price', 'stock']

admin.site.register(Category, AdminCategory)
admin.site.register(Product, AdminProduct)
