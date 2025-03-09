from home.models import Product,Order,OrderItem,Profile,Payment,Category
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['product_pic','seller','name','price','content','quantity','category']


class ProfileSerializer(serializers.ModelSerializer):
    products=ProductSerializer(read_only=True,many=True)

    class Meta:
        model=Profile
        fields=['user','profile_pic','location','contact','products']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields='__all__'


