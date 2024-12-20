# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django import forms



class User(AbstractUser):  # Наследуем встроенную модель AbstractUser
    email = models.EmailField(unique=True)  # Поле email становится уникальным




class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(unique=True)
    stock = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True, verbose_name="Изображение")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    class Meta:
        ordering = ['name']
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name




# Затем определяем Order и связанные модели
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'В обработке'),
        ('paid', 'Оплачен'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Order {self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f'{self.quantity}x {self.product.name}'


class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f'Shipping for {self.order.id}'


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('card', 'Банковская карта'),
        ('cash', 'Наличные при получении'),
        ('bank_transfer', 'Банковский перевод'),
    )

    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Ожидает оплаты'),
        ('processing', 'Обрабатывается'),
        ('completed', 'Выполнен'),
        ('failed', 'Ошибка'),
        ('refunded', 'Возвращен')
    )

    order = models.ForeignKey(Order, related_name='payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    payment_details = models.JSONField(null=True, blank=True)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Payment {self.id} for Order {self.order.id}'


class Comment(models.Model):
    author = models.CharField('Автор', max_length=100)
    text = models.TextField('Текст комментария')
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Продукт'
    )
    created_at = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True
    )

    def __str__(self):
        return f'Комментарий от {self.author} к продукту {self.product.name}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']  # Добавим сортировку


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in cart"


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1, label="Количество")
