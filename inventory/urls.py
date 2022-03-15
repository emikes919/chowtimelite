from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.landingPage, name='landingpage'),
    path('home/', views.Home, name='home'),
    
    path('inventory/', views.InventoryList, name='inventorylist'),
    path('inventory-create/', views.InventoryCreate, name='inventorycreate'),
    path('inventory-update/<str:pk>/', views.InventoryUpdate, name='inventoryupdate'),
    path('inventory-delete/<str:pk>/', views.InventoryDelete, name='inventorydelete'),
    
    path('menus/', views.MenuList, name='menulist'),
    path('menu-create/', views.MenuCreate, name='menucreate'),
    path('menu/<str:pk>/', views.MenuView, name='menuview'),
    path('menu-update/<str:pk>/', views.MenuUpdate, name='menuupdate'),
    path('menu-delete/<str:pk>/', views.MenuDelete, name='menudelete'),
    
    path('menu/<str:pk>/item-create/', views.ItemCreate, name='itemcreate'),
    path('menu/<str:pk>/item-update/', views.ItemUpdate, name='itemupdate'),
    path('menu/<str:pk>/item-delete/', views.ItemDelete, name='itemdelete'),

    path('orders/', views.OrderList, name='orderlist'),
    path('order-create/', views.OrderCreate, name='ordercreate'),
    path('order-update/<str:pk>', views.OrderUpdate, name='orderupdate'),
    path('order-delete/<str:pk>/', views.OrderDelete, name='orderdelete'),

    path('pnl-view/', views.pnlView, name='pnlview')   
]