from django.apps import apps
from asgiref.sync import async_to_sync, sync_to_async
from telegram.ext import Application
from django.conf import settings

def get_order():
    return apps.get_model('my_flower_del', 'Order')

@sync_to_async
def get_order_data(order):
    return {
        'order_id': order.id,
        'date': order.created_at.strftime("%Y-%m-%d %H:%M"),
        'client_name': f"{order.user.first_name} {order.user.last_name}",
        'phone': order.phone_number,
        'delivery_address': order.delivery_address,
        'bouquets': "\n".join([f"- {item.product.name} x{item.quantity}" for item in order.items.all()]),
        'total_amount': order.total_amount
    }

async def notify_about_order(order):
    order_data = await get_order_data(order)
    app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    await app.bot.send_message(
        chat_id=settings.TELEGRAM_CHAT_ID,
        text=f"""
Новый заказ #{order_data['order_id']}!
Дата: {order_data['date']}
Клиент: {order_data['client_name']}
Телефон: {order_data['phone']}
Адрес доставки: {order_data['delivery_address']}
Заказ:
{order_data['bouquets']}
Сумма: {order_data['total_amount']} руб.
        """
    )
