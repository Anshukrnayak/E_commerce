from tkinter.font import names

from django.urls import path
from home import views

urlpatterns=[

    path('', views.IndexView.as_view(), name='home'),
    path('product-detail/<int:pk>/',views.ProductDetailView.as_view(),name='product_detail'),
    path('product-delete/<int:pk>/',views.ProductDeleteView.as_view(),name='delete_product'),
    path('product-add/',views.CreateProductView.as_view(),name='create_product'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('create-profile/',views.CreateProfileView.as_view(),name='create_profile'),


]

