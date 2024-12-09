# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    # path('logout/', views.logout, name='logout'),
    path('order/', views.order, name='order'),
    path('flower/<int:pk>/', views.flower_detail, name='flower_detail'),
]