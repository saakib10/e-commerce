from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserSignupForm
from django.contrib.auth import login, authenticate, logout


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        itmes = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0,'shipping':False}
        itmes = []
        cartItems = ['get_cart_items']
    products = Product.objects.all()
    return render(request, 'store.html', {'products': products,'cartItems': cartItems})


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        itmes = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0,'shipping':False}
        itmes = []
        cartItems = ['get_cart_items']
    return render(request, 'cart.html', {'items': itmes, 'order': order,'cartItems':cartItems})


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        itmes = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0,'shipping':False}
        itmes = []
        cartItems = ['get_cart_items']
    return render(request, 'checkout.html', {'items': itmes, 'order': order,'cartItems': cartItems})


def update_item(request):
    data = json.loads(request.body)
    productId = int(data['productId'])
    action = data['action']
    print('productId:', productId)
    print('action:', action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item is added', safe=False)


def sign_in(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            form = UserSignupForm()
    else:
        form = UserSignupForm()
    return render(request, 'signin.html', {'form': form})


def log_in(request):
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            upass = form.cleaned_data['password']

            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                form = AuthenticationForm()
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})
