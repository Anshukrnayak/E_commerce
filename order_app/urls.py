from django.urls import path
from . import views

urlpatterns=[
    path('<int:pk>/',views.PlaceOrderView.as_view(),name='order'),
    path('cart/',views.CartView.as_view(),name='cart'),
    path('payment/',views.create_checkout_session,name='payment'),

]

