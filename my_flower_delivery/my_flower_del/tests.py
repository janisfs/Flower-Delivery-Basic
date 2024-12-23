from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Product, Order, OrderItem, Cart, CartItem
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from django.conf import settings


User = get_user_model()


class UserRegistrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('my_flower_del:register')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }

    def test_user_registration_success(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_user_registration_invalid_data(self):
        invalid_data = self.user_data.copy()
        invalid_data['password2'] = 'wrongpass'
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, 200)  # Stay on the same page
        self.assertFalse(User.objects.filter(username='testuser').exists())


class ProductCatalogTests(TestCase):
    def setUp(self):
        settings.MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'test_media')
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)

        self.client = Client()

        # Создаем тестовое изображение
        image_content = b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
        test_image = SimpleUploadedFile(
            'test_image.gif',
            image_content,
            content_type='image/gif'
        )

        self.product = Product.objects.create(
            name='Розы красные',
            slug='rozy-krasnye',
            price=Decimal('1000.00'),
            description='Букет из 11 роз',
            stock=10,
            available=True,
            image=test_image
        )

    def test_catalog_view(self):
        response = self.client.get(reverse('my_flower_del:catalog'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Розы красные')

    def test_product_detail(self):
        response = self.client.get(reverse('my_flower_del:product_detail', kwargs={'product_id': self.product.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertContains(response, '1000,00')


class CartTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.product = Product.objects.create(
            name='Тюльпаны',
            slug='tyulpany',
            price=Decimal('500.00'),
            stock=5,
            available=True
        )
        self.client.login(username='testuser', password='testpass123')

    def test_add_to_cart(self):
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=2
        )
        self.assertEqual(cart_item.get_total_price(), Decimal('1000.00'))


class OrderTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='customer',
            email='customer@example.com',
            password='customerpass123'
        )
        self.product = Product.objects.create(
            name='Тюльпаны',
            slug='tyulpany',
            price=Decimal('500.00'),
            stock=5,
            available=True
        )
        self.client.login(username='customer', password='customerpass123')
        self.order_url = reverse('my_flower_del:create_order')

    def test_create_order(self):
        self.client.login(username='customer', password='customerpass123')

        # Создаем корзину с товаром
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=1
        )

        response = self.client.post(reverse('my_flower_del:create_order'))
        self.assertEqual(response.status_code, 302)

        # Проверяем созданный заказ
        order = Order.objects.last()
        self.assertIsNotNone(order)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.total_amount, Decimal('500.00'))  # Цена из setUp

    def test_create_order_unauthorized(self):
        self.client.logout()
        response = self.client.get(reverse('my_flower_del:create_order'))
        # Проверяем редирект на страницу входа
        self.assertEqual(response.status_code, 302)


class TelegramBotTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='customer',
            email='customer@example.com',
            password='customerpass123'
        )
        self.product = Product.objects.create(
            name='Лилии',
            slug='lilii',
            price=Decimal('700.00'),
            stock=3,
            available=True
        )
        self.order = Order.objects.create(
            user=self.user,
            delivery_address='ул. Ленина, д. 5',
            recipient_name='Петр Петров',
            phone_number='+7999999999',
            total_amount=Decimal('700.00'),
            status='pending'
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            price=Decimal('700.00')
        )

    def test_order_confirmation_triggers_notification(self):
        # Проверяем, что при изменении статуса заказа на 'confirmed'
        # срабатывает сигнал для отправки уведомления
        self.order.status = 'confirmed'
        self.order.save()
        # В реальности здесь нужно проверить, что уведомление было отправлено
        # Это можно сделать через mock или проверку логов


