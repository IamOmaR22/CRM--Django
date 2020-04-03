from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('customer/<str:pk>/', views.customer, name='customer'),
    path('create_order/<str:pk>/', views.createOrder, name='createOrder'),
    path('update_order/<str:pk>/', views.updateOrder, name='updateOrder'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
]
