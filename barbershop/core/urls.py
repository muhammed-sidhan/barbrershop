from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('register/barber/',barber_register,name='barber_register'),
    path('register/customer/',customer_register,name='customer_register'),
    path('login/',auth_views.LoginView.as_view(template_name='registration/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('customer/dashboard/',customer_dashboard,name='customer_dashboard'),
    path('customer/barbers/',customer_barber_list,name='customer_barber_list'),
    path('customer/join_queue/<int:barber_id>/',join_queue,name='join_queue'),
    path('customer/leave_queue/<int:entry_id>/',leave_queue,name='leave_queue'),
    path('barber/dashboard/',barber_dashboard,name='barber_dashboard'),
    path('barber/queue/',barber_queue,name='barber_queue'),
    path('barber/mark_served/<int:entry_id>/',mark_served,name='mark_served'),
    path('home/',role_based_home,name='role_based_home'),
    path('', index, name='index'),
    path('barber/block_customer/<int:customer_id>/',block_customer,name='block_customer'),
    path('barber/unblock_customer/<int:customer_id>/',unblock_customer,name='unblock_customer'),
    path('barber/blocked_customers/',blocked_customers,name='blocked_customers'),
  
]
