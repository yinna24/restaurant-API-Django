from django.shortcuts import render
from .models import Category, MenuItem, Cart, Order, OrderItem
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import CategorySerializer, MenuItemSerializer, UserSerializer, CartSerializer, OrderSerializer, OrderUpdateSerializer, DeliveryOrderUpdateSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import User, Group
# from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.shortcuts import get_object_or_404



# User group management section

class ManagerView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name="manager")
    serializer_class = UserSerializer
    
    def get_permissions(self):
        permission_classes = []
        if(self.request.user.groups.filter(name='manager').exists()):
            return [permission() for permission in permission_classes]
        else:
            res = ValidationError({'message':'Access Denied'})
            res.status_code = 403
            raise res
        
    def create(self, request, *args, **kwargs):
        if(self.request.user.groups.filter(name='manager').exists()):
            username = self.request.data['username']
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name="manager")
            managers.user_set.add(user)
            return Response({"message": "User added to manager group"}, status=201)
    
class RemoveManagerView(generics.RetrieveDestroyAPIView):
    queryset = User.objects.filter(groups__name="manager")
    serializer_class = UserSerializer
    
    def get_permissions(self):
        permission_classes = []
        if(self.request.user.groups.filter(name='manager').exists()):
            return [permission() for permission in permission_classes]
        else:
            res = ValidationError({'message':'Access Denied'})
            res.status_code = 403
            raise res
        
    def destroy(self, request, *args, **kwargs):
        if(self.request.user.groups.filter(name='manager').exists()):
            username = self.request.data['username']
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name="manager")
            managers.user_set.remove(user)
            return Response({"message": "Success"}, status=200)
    
class DeliveryCrewView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name="delivery_crew")
    serializer_class = UserSerializer
    
    def get_permissions(self):
        permission_classes = []
        if(self.request.user.groups.filter(name='manager').exists()):
            return [permission() for permission in permission_classes]
        else:
            res = ValidationError({'message':'Access Denied'})
            res.status_code = 403
            raise res
        
    def create(self, request, *args, **kwargs):
        username = self.request.data['username']
        user = get_object_or_404(User, username=username)
        crew = Group.objects.get(name="delivery_crew")
        crew.user_set.add(user)
        return Response({"message": "User added to delivery crew group"}, status=201)
    
class RemoveDeliveryCrewView(generics.RetrieveDestroyAPIView):
    queryset = User.objects.filter(groups__name="delivery crew")
    serializer_class = UserSerializer
    
    def get_permissions(self):
        permission_classes = []
        if(self.request.user.groups.filter(name='manager').exists()):
            return [permission() for permission in permission_classes]
        else:
            res = ValidationError({'message':'Access Denied'})
            res.status_code = 403
            raise res
        
    def destroy(self, request, *args, **kwargs):
        if(self.request.user.groups.filter(name='manager').exists()):
            username = self.request.data['username']
            user = get_object_or_404(User, username=username)
            crew = Group.objects.get(name="delivery_crew")
            crew.user_set.remove(user)
            return Response({"message": "Success"}, status=200)



# Menu items section

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class MenuItemsView(generics.ListCreateAPIView):
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price']
    filterset_fields = ['price']
    search_fields = ['title']
    
    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            if(self.request.user.groups.filter(name='manager').exists()):
                return [permission() for permission in permission_classes]
            else:
                res = ValidationError({'message':'Access Denied'})
                res.status_code = 403
                raise res
        return [permission() for permission in permission_classes]
    
class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            if(self.request.user.groups.filter(name='manager').exists()):
                return [permission() for permission in permission_classes]
            else:
                res = ValidationError({'message':'Access Denied'})
                res.status_code = 403
                raise res
        return [permission() for permission in permission_classes]
 


# Cart and Order section

class CartView(generics.ListCreateAPIView):
    # queryset = Cart.objects.all()
    # serializer_class = CartSerializer
    
    def get_serializer_class(self):
        if(self.request.user.is_authenticated):
            return CartSerializer
        else:
            res = ValidationError({'message':'You don\'t have any items in cart'})
            res.status_code = 401
            raise res
        
    def get_queryset(self):
        if(self.request.user.is_authenticated):
            return Cart.objects.all()
        else:
            res = ValidationError({'message':'Authentication failed'})
            res.status_code = 401
            raise res
  
    def perform_create(self, serializer):
        if(self.request.user.is_authenticated):
            user = self.request.user.id
            menuitem = self.request.data['menuitem']
            quantity = self.request.data['quantity']
            
            data = MenuItem.objects.filter(id=menuitem).values()
            unit_price = data.values('price').get()['price']

            item_price_total = float(quantity) * float(unit_price)
            cart = Cart(user_id=user, menuitem_id=menuitem, quantity=quantity, unit_price=unit_price, price=item_price_total)
            cart.save()
   
class RemoveCartView(generics.RetrieveDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    
    def perform_destroy(self, instance):
        if(self.request.user.is_authenticated):
            user = self.request.user.id
            Cart.objects.all().filter(user=user).delete()
            return Response({"message": "Success"}, status=200)
    
class OrderView(generics.ListCreateAPIView):
    # serializer_class = OrderSerializer
    ordering_fields = ['date']
    filterset_fields = ['status']
    search_fields = ['user']
    
    def get_serializer_class(self):
        if(self.request.user.groups.filter(name='manager').exists()):
            return OrderUpdateSerializer
        elif(self.request.user.groups.filter(name='delivery_crew').exists()):
            return DeliveryOrderUpdateSerializer
        else:
            return OrderSerializer
    
    def get_queryset(self):
        if(self.request.user.groups.filter(name='manager').exists()):
            return Order.objects.all()
        elif(self.request.user.groups.filter(name='delivery_crew').exists()):
            user = self.request.user.id
            return Order.objects.filter(delivery_crew=user)
        elif(self.request.user.is_authenticated):
            user = self.request.user.id
            return Order.objects.filter(user=user)
        else:
            res = ValidationError({'message':'Authentication failed'})
            res.status_code = 401
            raise res
    
    def perform_create(self, serializer):
        if(self.request.user.is_authenticated):
            user = self.request.user.id
            if(Cart.objects.filter(user=user).exists()):
                date = self.request.data['date']
                data = Cart.objects.filter(user=user).values_list('price', flat=True)
                total = sum(data)
                order = Order(user_id=user, total=total, date=date)
                order.save()
                
                userOrder = self.request.user
                menuitem_id = Cart.objects.filter(user=user).values('menuitem')
                for items in menuitem_id:    
                    query = Cart.objects.filter(user=user).filter(menuitem=items['menuitem']).values('quantity', 'unit_price', 'price')
                    menu = MenuItem.objects.get(pk=items['menuitem'])
                    order_item = OrderItem(order=userOrder, menuitem=menu, quantity=query[0]['quantity'], unit_price=query[0]['unit_price'], price=query[0]['price'])
                    order_item.save()
                
                Cart.objects.all().filter(user=user).delete()
                res = ValidationError({'message':'Order created'})
                res.status_code = 201
                raise res

            else:
                res = ValidationError({'message':'You don\'t have any items in cart'})
                res.status_code = 400
                raise res
    
class UpdateDestroyOrderView(generics.RetrieveUpdateDestroyAPIView):
    # serializer_class = OrderUpdateSerializer
    
    def get_serializer_class(self):
        if(self.request.user.groups.filter(name='manager').exists()):
            return OrderUpdateSerializer
        elif(self.request.user.groups.filter(name='delivery_crew').exists()):
            return DeliveryOrderUpdateSerializer
        else:
            return OrderSerializer
    
    def get_queryset(self):
        if(self.request.user.groups.filter(name='manager').exists()):
            return Order.objects.all()
        elif(self.request.user.groups.filter(name='delivery_crew').exists()):
            user = self.request.user.id
            return Order.objects.filter(delivery_crew=user)
        elif(self.request.user.is_authenticated):
            user = self.request.user.id
            return Order.objects.filter(user=user)
        else:
            res = ValidationError({'message':'Authentication failed'})
            res.status_code = 401
            raise res
    
    def perform_update(self, serializer):
        if(self.request.user.groups.filter(name='manager').exists()):
            pk = self.kwargs['pk']
            delivery_crew = self.request.data['delivery_crew']
            # status = self.request.data['status']
            Order.objects.filter(pk=pk).update(delivery_crew=delivery_crew) #status=status)    
            res = ValidationError({'message':'Order updated'})
            res.status_code = 201
            raise res
        elif(self.request.user.groups.filter(name='delivery_crew').exists()):
            pk = self.kwargs['pk']
            status = self.request.data['status']
            Order.objects.filter(pk=pk).update(status=status)
            res = ValidationError({'message':'Order updated'})
            res.status_code = 201
            raise res
        else:
            res = ValidationError({'message':'Access Denied'})
            res.status_code = 403
            raise res
    
    def perform_destroy(self, instance):
        if(self.request.user.groups.filter(name='manager').exists()):
            pk = self.kwargs['pk']
            Order.objects.filter(pk=pk).delete()
            res = ValidationError({'message':'Order deleted'})
            res.status_code = 200
            raise res
        else:
            res = ValidationError({'message':'Access Denied'})
            res.status_code = 403
            raise res
  