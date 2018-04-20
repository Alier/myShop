from django.urls import path, re_path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    re_path(r'^order/(?P<order_id>[0-9]+)/$', views.order_detail, name='order_detail'),
]
