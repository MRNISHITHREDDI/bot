import os
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook import WebhookRequestHandler
from aiogram.utils import executor
from aiohttp import web
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Webhook settings
WEBHOOK_HOST = 'https://your-app-url.com'  # Set to your server URL
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

async def on_start(update: Update):
    await update.message.reply("Bot started!")

dp.message.register(on_start)

# Register the webhook URL
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

# Cleanup the webhook on shutdown
async def on_shutdown(dp):
    await bot.delete_webhook()

async def handle_webhook(request):
    # Get the update from the webhook request
    json_str = await request.json()
    update = Update(**json_str)
    await dp.process_update(update)
    return web.Response(status=200)

if __name__ == "__main__":
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle_webhook)

    # Start the aiohttp web server to handle requests
    web.run_app(app, host='0.0.0.0', port=int(os.getenv('PORT', 8000)))
