from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'shopper'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.login, {'template_name': 'shopper_login.html'}, name='login'),
    path('logout/', auth_views.logout, {'next_page': 'shopper:login'}, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('take_order/',views.take_order, name='take_order'),
    #path('dashboard/',views.dashboard, name='dashboard'),
]
