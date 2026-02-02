from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name = 'home'),
    path('about', about, name = 'about'),
    path('contact', contact, name = 'contact'),
    path('products',products,name='products'),
    path('productdetails/<int:product_id>',productDetails,name='productdetails'),
    path('addtocart/<int:product_id>', addtocart, name='addtocart'),
    path('carts', carts, name='carts'),
    path('delete-cart/<int:cart_id>', deleteCart, name='delete-cart'),
    path('order-item/<int:product_id>/<int:cart_id>', orderItem, name = 'order-item'),
    path('stripe-checkout', stripeCheckout, name = 'stripe-checkout'),
    path('create-checkout-session/<int:order_id>/<int:cart_id>',create_checkout_session, name = 'create-checkout-session'),
    path('success/',stripeSuccess, name = 'stripe-success'),
    path('all-orders',allOrders, name = 'all-orders')
]