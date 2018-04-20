from django.shortcuts import render, redirect, get_object_or_404
from .models import Order,  OrderItem
from .forms import OrderCreateForm
from .tasks import order_created
from cart.cart import Cart
from shop.models import Product

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            order_created(order.id)
            # launch asynchronous task
            #order_created.delay(order.id)
            # add from online
            request.session['order_id'] = order.id
            return redirect('payment:process')
            # end add from online

            #return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart,
                                                        'form': form})

def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    orderitems = []
    allorderItems = OrderItem.objects.all()
    print(allorderItems)
    for item in allorderItems:
        #print(item.order)
        if item.order == order:
            orderitems.append(item)

    #print(orderitems)
    return render(request, 'orders/order/order_detail.html', {'order': order, 'orderitems': orderitems})
