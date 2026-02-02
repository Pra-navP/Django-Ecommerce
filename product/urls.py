from django.urls import path
from .views import *

urlpatterns = [


    path('add-category', addCategory, name='add-category'),
    path('all-category', allCategory, name='all-category'),
    path('delete-category/<int:category_id>', deleteCategory, name='delete-category'),
    path('update-category/<int:category_id>', updateCategory, name='update-category'),


    path('add-product', addProduct, name='add-product'),
    path('all-products', allProducts, name='all-products'),
    path('delete-product/<int:product_id>', deleteProduct, name='delete-product'),
    path('update-product/<int:product_id>', updateProduct, name='update-product'),

    
]
