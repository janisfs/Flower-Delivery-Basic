import asyncio
from telegram.ext import Application, CommandHandler
from telegram import Update
from telegram.ext import ContextTypes
import logging


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Привет! ID этого чата: {update.effective_chat.id}')


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Доступные команды:\n/start - начать работу\n/help - показать справку')


async def main():
    application = Application.builder().token('7840150552:AAGAzxoppLN7MrIBw4lzIWzLVvjXdEabW4Y').build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))  # Добавляем новый обработчик

    await application.initialize()
    await application.start()
    await application.run_polling()


if __name__ == '__main__':
    asyncio.run(main())
