
from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    
    path('vendor/<int:pk>',views.vendor_detail,name='vendor'),
    path('login/',views.Login_page,name='login'),
    path('logout/',views.logout_page,name='logout'),
    path('signup/',views.signup_page,name='signup'),
    path('account/',views.myaccount_page,name='account'),
    



]
