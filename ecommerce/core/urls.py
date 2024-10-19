
from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.home_page,name='home'),
    path('about/',views.about_page,name='about'),
    path('detail<int:pk>',views.product_detail,name='detail'),
    path('category/<int:pk>',views.product_category,name='category'),
    path('search/',views.search_page,name='search'),
    path('product/',views.add_product,name='product'),
    path('edit/<int:pk>',views.product_edit,name='edit'),
    path('delete/<int:pk>',views.delete_product,name='delete'),
    

]
