from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import  views

router=DefaultRouter()
router.register(r'product',views.ProductView,basename='product')
router.register(r'profile',views.SellerView,basename='seller')
router.register(r'order',views.OrderView,basename='order')

urlpatterns=[
    path('',include(router.urls))
]