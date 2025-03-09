from django.core.serializers import serialize
from rest_framework import  viewsets
from home.models import Product,Order,OrderItem,Profile,Payment,Category
from .serializers import ProductSerializer,ProfileSerializer,OrderSerializer



class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        profile=Profile.objects.get(user=self.request.user)
        return serializer.save(seller=profile)


class SellerView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        return serializer(user=self.request.user)


class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        profile=Profile.objects.get(user=self.request.user)
        return serializer.save(seller=profile)

