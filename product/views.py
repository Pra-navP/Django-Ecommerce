from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib import messages

# Create your views here.

    
def addCategory(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Category Added')
            return redirect('all-category')
        else:
            messages.error(request, 'Invalid Input')
            return render(request, 'vendor/addcategory.html', {'form': form})
        
    context = {
        'form': CategoryForm    
    }
    return render(request, 'vendor/addcategory.html', context)


def allCategory(request):
    context = {
        'categories': Category.objects.all()
    }
    return render(request, 'vendor/allcategory.html', context)
    

def deleteCategory(request, category_id):
    category = Category.objects.get(id = category_id)
    category.delete()
    messages.success(request, 'Item Deleted Successfully.')
    return redirect('all-category')

def updateCategory(request, category_id):
    category = Category.objects.get(id = category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category Updated Successfully.')
            return redirect('all-category')

    context = {
        'form': CategoryForm(instance=category)
    }
    return render(request,'vendor/updatecategory.html', context)


#==================================================================================================================
def addProduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POS, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product Added Successfully.')
            return redirect('all-products')
        else:
            messages.error(request, 'Product Added Failed.')
            return render(request, 'vendor/addProduct.html', {'form':form})
        
    context = {
        'form': ProductForm    
    }
    return render(request, 'vendor/addProduct.html', context)


def allProducts(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'vendor/allproducts.html', context)
    

def deleteProduct(request, category_id):
    product = Product.objects.get(id = category_id)
    product.delete()
    messages.success(request, 'Item Deleted Successfully.')
    return redirect('all-products')

def updateProduct(request, product_id):
    product  = Product.objects.get(id = product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES,instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product Updated Successfully.')
            return redirect('all-products')

    context = {
        'form': ProductForm(instance=product)
    }
    return render(request,'vendor/updateproduct.html', context)