import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv  # Import dotenv

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get bot tokens from environment variables
BOT_TOKENS = [
    os.getenv("BOT_TOKEN_1"),
    os.getenv("BOT_TOKEN_2"),
    os.getenv("BOT_TOKEN_3"),
    os.getenv("BOT_TOKEN_4"),
    os.getenv("BOT_TOKEN_5"),
]

# Remove any `None` values (in case some env variables are missing)
BOT_TOKENS = [token for token in BOT_TOKENS if token]

# Assign unique emojis to each bot
BOT_EMOJIS = ["🤩", "🤩", "🔥", "🏆", "❤️", "👍"]

# Messages that should NOT trigger reactions
IGNORED_MESSAGES = [
    "⚠️ chart not stable 🥹 wait for 2 minutes 🤩",
    "⚠️ chart not stable 🥹 wait 2 minutes 🤩"
]

# Initialize bots and dispatchers
bots = [Bot(token=t) for t in BOT_TOKENS]
dispatchers = [Dispatcher(storage=MemoryStorage()) for _ in BOT_TOKENS]

# Define a message handler to respond to messages
async def on_message(message: Message):
    if message.text not in IGNORED_MESSAGES:
        await message.answer(f"Hello from bot {message.from_user.first_name}!")
    else:
        logger.info(f"Ignored message: {message.text}")

# Function to set up the dispatcher for each bot
async def setup(dp: Dispatcher):
    dp.message.register(on_message)  # Correct way to register handlers in aiogram 3.x

async def main():
    """Main function to start all bots."""
    logger.info("🚀 Starting all bots...")

    # Register handlers for each dispatcher
    for dp in dispatchers:
        await setup(dp)

    # Run bots concurrently
    await asyncio.gather(*(dp.start_polling(bot) for dp, bot in zip(dispatchers, bots)))

    # Properly close bot sessions after execution
    for bot in bots:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
