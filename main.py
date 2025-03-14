import os
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.fsm.storage.memory import MemoryStorage
from aiohttp import web
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Webhook settings
WEBHOOK_HOST = 'https://your-app-url.com'  # Replace with your actual domain
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# Define a handler function for the incoming updates
async def on_start(update: Update):
    await update.message.reply("Bot started!")

dp.message.register(on_start)

# Register the webhook URL
async def on_startup(dp):
    # Set the webhook for your bot
    await bot.set_webhook(WEBHOOK_URL)

# Clean up the webhook on shutdown
async def on_shutdown(dp):
    # Delete the webhook when shutting down the bot
    await bot.delete_webhook()

async def handle_webhook(request):
    # Retrieve the incoming update from the request
    json_str = await request.json()
    update = Update(**json_str)
    # Process the update using the dispatcher
    await dp.process_update(update)
    return web.Response(status=200)

if __name__ == "__main__":
    app = web.Application()
    # Add the route to handle webhook requests
    app.router.add_post(WEBHOOK_PATH, handle_webhook)

    # Start the aiohttp web server to listen for webhook requests
    web.run_app(app, host='0.0.0.0', port=int(os.getenv('PORT', 8000)))
