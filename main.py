import os
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.utils.executor import start_webhook
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Webhook settings
WEBHOOK_HOST = 'https://your-app-url.com'
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

async def on_start(update: Update):
    await update.message.reply("Bot started!")

dp.register_message_handler(on_start)

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    await bot.delete_webhook()

if __name__ == "__main__":
    from aiohttp import web
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, dp)

    # Start the webhook
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host="0.0.0.0",
        port=int(os.getenv('PORT', 8000))
    )
