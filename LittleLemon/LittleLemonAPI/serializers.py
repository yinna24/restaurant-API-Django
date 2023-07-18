from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']
        
class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    menuitem = MenuItemSerializer
    class Meta:
        model = Cart
        read_only_fields = ['unit_price', 'price']
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price']
        
class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Order
        read_only_fields = ['delivery_crew', 'status', 'total']
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']
    
class OrderUpdateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Order
        read_only_fields = ['total', 'status', 'date']
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']
        
class DeliveryOrderUpdateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Order
        read_only_fields = ['delivery_crew', 'total', 'date']
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']
        