# my_flower_del/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .telegram_bot import send_order_notification
import asyncio

@receiver(post_save, sender=Order)
def order_created_notification(sender, instance, created, **kwargs):
    """Отправка уведомления при создании нового заказа"""
    if created:
        # Запускаем асинхронную отправку в синхронном контексте
        asyncio.run(send_order_notification(instance))

# my_flower_del/apps.py
from django.apps import AppConfig

class MyFlowerDelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_flower_del'

    def ready(self):
        import my_flower_del.signals  # Импортируем сигналы