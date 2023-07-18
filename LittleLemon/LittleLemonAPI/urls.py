from django.urls import path
from . import views

urlpatterns = [
    path('categories', views.CategoriesView.as_view()),
    path('menu-items', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('groups/manager/users', views.ManagerView.as_view()),
    path('groups/manager/users/<int:pk>', views.RemoveManagerView.as_view()),
    path('groups/delivery-crew/users', views.DeliveryCrewView.as_view()),
    path('groups/delivery-crew/users/<int:pk>', views.RemoveDeliveryCrewView.as_view()),
    path('cart/menu-items', views.CartView.as_view()),
    path('cart/menu-items/<int:pk>', views.RemoveCartView.as_view()),
    path('cart/orders', views.OrderView.as_view()),
    path('cart/orders/<int:pk>', views.UpdateDestroyOrderView.as_view()),
]