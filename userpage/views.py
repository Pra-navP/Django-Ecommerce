from django.shortcuts import render, redirect
from product.models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from .forms import *
from django.urls import reverse
import stripe
from django.conf import settings

# Create your views here.


def index(request):
    # print("This is a test(First Django Project)")
    # return HttpResponse("Hello!")
    context = {
        'products': Product.objects.filter(trending=True).order_by('-id')[:4]      
        # 'products': Product.objects.filter(trending = True)
    }
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


def products(request):
    category_id = request.GET.get('category')
    categories = Category.objects.all()
    search_query = request.GET.get('search')

    products = Product.objects.all().order_by('-id')

    if category_id:
        products = products.filter(category_id=category_id)

    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) |
            Q(l_description__icontains=search_query)
        )

    context = {
        'products': products,
        'categories': categories,
        'selected_categories': int(category_id) if category_id else None,
        'search_query': search_query
    }

    return render(request, 'products.html', context)


def productDetails(request,product_id):
    product = Product.objects.get(id=product_id)
    context = {
        'item': product
    }
    return render(request,'product_details.html',context)


@login_required
def addtocart(request, product_id):
    product = Product.objects.get(id = product_id)
    user = request.user

    existingItem = Cart.objects.filter(user=user, product=product)
    if existingItem:
        messages.error(request, "Item Already Exists. ")
        return redirect('productdetails', product_id)
    
    else:
        cart = Cart.objects.create(user=user, product=product)
        messages.success(request, 'Item added to the cart.')
        return redirect('home') 

@login_required
def carts(request):
    user = request.user
    context = {
        'cart' : Cart.objects.filter(user=user)
    }
    return render(request,'cartpage.html', context)
    
@login_required
def deleteCart(request, cart_id):
    cartitem = Cart.objects.get(id=cart_id)
    cartitem.delete()
    messages.success(request,'Item deleted Successfully')
    return redirect('carts')
    
@login_required
def orderItem(request, product_id, cart_id):
    product = Product.objects.get(id=product_id )
    cart = Cart.objects.get(id=cart_id)
    user = request.user
    if request.method =='POST':
        # storing data requesting from te form in variables
        form = OrderForm(request.POST)
        if form.is_valid():
            quantity = request.POST.get('quantity')
            price = product.discounted_price
            total_price = int(price) * int(quantity) 
            # total_price = int(product.discounted_price) * int(quantity)
            address = request.POST.get('address')
            phone = request.POST.get('phone')
            payment_method = request.POST.get('payment_method')
            # payment_status = request.POST.get('payment_status')

                # storing requested data in database table of Order model.
            order = Order.objects.create(
                user = user,
                product = product,
                quantity = quantity,
                total_price = total_price,
                address = address,
                # status = status,
                phone = phone,
                payment_method = payment_method,
                payment_status = False
            )

            if order.payment_method == 'Cash':
                cart = Cart.objects.get(id=cart_id)
                cart.delete()
                messages.success(request,'Order Placed Successfully.')
                return redirect('/')
            elif order.payment_method == 'Esewa':
                pass

            elif order.payment_method == 'Stripe':
                return redirect(reverse('stripe-checkout')+'?o_id='+str(order.id)+'&c_id='+str(cart.id))
                
            else:
                messages.error(request, 'Order Failed.')
                return redirect('carts')

    context = {
        'orderform': OrderForm
    }
    return render(request, 'order_form.html', context)

@login_required
def allOrders(request):
    user = request.user
    context = {
        'orders' : Order.objects.filter(user=user)
    }
    return render(request, 'allorders.html',context)

@login_required
def stripeCheckout(request):
    cart_id =request.GET.get('c_id')
    order_id =request.GET.get('o_id')
    cart =Cart.objects.get(id = cart_id)
    order =Order.objects.get(id = order_id)

    context = {
        'cart': cart,
        'order': order
    }
    return render(request,'checkout.html', context)

import stripe
# This is your test secret API key.
stripe.api_key = settings.STRIPE_SECRET_KEY
YOUR_DOMAIN = 'http://127.0.0.1:8000'

@login_required
def create_checkout_session(request, order_id, cart_id):
    order= Order.objects.get(id = order_id)
    cart = Cart.objects.get(id = cart_id)
    checkout_session = stripe.checkout.Session.create(
        payment_method_types= ['card'],
        line_items=[
            {
                # Provide the exact Price ID (for example, price_1234) of the product you want to sell
                'price_data':{
                    'currency': 'npr',
                    'product_data':{
                        'name': f"{order.product.title}"
                    },
                    'unit_amount': int(order.product.discounted_price)*100
                },
                'quantity': order.quantity,
            },
        ],
        mode='payment',

        metadata={
            'order_id' : str(order.id),
            'cart_id' : str(cart.id),
        },
        success_url= YOUR_DOMAIN + f'/success/?session_id={{CHECKOUT_SESSION_ID}}&order_id={order.id}&cart_id={cart.id}',
        cancel_url= YOUR_DOMAIN + '/cart',
    )
    return redirect(checkout_session.url, code=303)


@login_required
def stripeSuccess(request):
    session_id = request.GET.get('session_id')
    order_id = request.GET.get('order_id')
    cart_id = request.GET.get('cart_id')

    if session_id:
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status =='paid':
            order = Order.objects.get(id = order_id)
            cart = Cart.objects.get(id = cart_id)
            order.payment_status = True
            order.save()
            cart.delete()
            
            messages.success(request,'Payment Done! Please check your order status.')
            return redirect('/')
        else:
            messages.error(request,'Payment Failed')
            return redirect('cart')
    else:
        messages.error(request,'Invalid Session')
        return redirect('cart')
    