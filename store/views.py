from django.shortcuts import render
from .models import *


def store(request):
    products = Product.objects.all()
    return render(request,'store.html',{'products':products})

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete = False)
        itmes = order.orderitem_set.all()
    else:
        order = {'get_cart_total':0,'get_cart_items':0}
        itmes = []
    return render(request,'cart.html',{'items': itmes, 'order': order })

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete = False)
        itmes = order.orderitem_set.all()
    else:
        order = {'get_cart_total':0,'get_cart_items':0}
        itmes = []
    return render(request,'checkout.html',{'items': itmes, 'order': order })