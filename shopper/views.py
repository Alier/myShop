# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied

from shopper.forms import SignUpForm
from orders.models import Order, OrderItem
from .models import Profile

# clear cache
from django.core.cache import cache
from django.db import connections, transaction

def clearcache():
    # This works as advertised on the memcached cache:
    cache.clear()
    # This manually purges the SQLite cache:
    #print(settings.DATABASES)
    cursor = connections['cache_database'].cursor()
    cursor.execute('DELETE FROM cache_table')
    transaction.commit_unless_managed(using='cache_database')

# clear cache end

def start(request):
    return render(request, 'start.html')

@login_required
def home(request):
    return render(request, 'shopper_home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.zipcode = form.cleaned_data.get('zipcode')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('shopper:dashboard')
    else:
        form = SignUpForm()
    return render(request, 'shopper_signup.html', {'form': form})

@login_required
def dashboard(request):
    clearcache()
    shopper = request.user
    shoppername = shopper.username
    shopperzip = shopper.profile.zipcode
    allorders = Order.objects.filter(postal_code = shopperzip)
    print(type(allorders))
    allorderItems = OrderItem.objects.all()
    orders = [] # [[order1, [orderitem1, orderitem2]], [order2, [orderItem1, orderItem3]],[order3, []]]
    for order in allorders:
        if order.shopper is None:
            orderItems = []
            for orderitem in allorderItems:
                if orderitem.order == order:
                    orderItems.append(orderitem)
            orders.append([order, orderItems])

    return render(request, 'shopper_dashboard.html', {'shopper': shopper, 'orders': orders})

def take_order(request):
    if request.method == 'POST':
        order_id = request.POST.get("order_id")
        shopper_id = request.POST.get("shopper_id")

        order = Order.objects.get(pk=order_id)
        shopper = User.objects.get(pk=shopper_id)
        if order.shopper is None and shopper:
            order.shopper = shopper
            order.save()
            return render(request, 'take_order_success.html', {'order_id': order_id, 'shopper_id': shopper_id})
        else:
            return render(request, 'take_order_failed.html')
    else:
        raise PermissionDenied
