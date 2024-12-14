# my_flower_delivery\my_flower_del\urls.py
from django.urls import path
from . import views
from .views import catalog  # Эта строка экспортирует функцию catalog

urlpatterns = [
    path('', views.catalog, name='index'),  # Главная страница с каталогом
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('catalog/<slug:slug>/', views.product_detail, name='product_detail'),  # Детали товара
]
