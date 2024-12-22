# my_flower_del/telegram_bot.py
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update
from django.conf import settings
import asyncio
import logging

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class TelegramBot:
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.chat_id = settings.TELEGRAM_CHAT_ID
        self.application = None

    async def start_bot(self):
        """Инициализация и запуск бота"""
        self.application = Application.builder().token(self.token).build()

        # Регистрация обработчиков команд
        self.application.add_handler(CommandHandler("start", self.start_command))

        # Запуск бота
        await self.application.initialize()
        await self.application.start()
        await self.application.run_polling()

    @staticmethod
    async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        chat_id = update.effective_chat.id
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Бот запущен. ID чата: {chat_id}\n"
                 f"Используйте этот ID в настройках Django."
        )

    async def send_message(self, text: str):
        """Отправка сообщения в заданный чат"""
        if not self.application:
            await self.start_bot()

        async with Application.builder().token(self.token).build() as app:
            await app.bot.send_message(chat_id=self.chat_id, text=text)


# Создаем экземпляр бота
telegram_bot = TelegramBot()


# Функция для отправки уведомления о новом заказе
async def send_order_notification(order):
    """Формирование и отправка уведомления о новом заказе"""
    message = (
        f"🆕 Новый заказ #{order.id}\n\n"
        f"👤 Заказчик: {order.user.get_full_name() or order.user.username}\n"
        f"📦 Товары:\n"
    )

    for item in order.items.all():
        message += f"- {item.product.name} x {item.quantity} шт.\n"

    message += f"\n💰 Общая сумма: {sum(item.price * item.quantity for item in order.items.all())} руб."

    if order.delivery_address:
        message += f"\n📍 Адрес доставки: {order.delivery_address}"

    await telegram_bot.send_message(message)