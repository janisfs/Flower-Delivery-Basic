# my_flower_delivery\my_flower_del\urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'my_flower_del'

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница с каталогом
    path('login/', views.login, name='login'),
    path('account/', views.account, name='account'),
    path('cart/', views.cart, name='cart'),
    path('logout/', views.logout_view, name='logout'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Исправлено
    path('register/', views.register, name='register'),
    path('create-order/', views.create_order, name='create_order'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('<int:product_id>/add_comment/', views.add_comment, name='add_comment'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)