import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReactionTypeEmoji
from aiogram.fsm.storage.memory import MemoryStorage
from config.py import BOT_TOKENS, BOT_EMOJIS, IGNORED_MESSAGES  # Import tokens from config

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bots and dispatchers
bots = [Bot(token=t) for t in BOT_TOKENS]
dispatchers = [Dispatcher(storage=MemoryStorage()) for _ in BOT_TOKENS]

async def auto_react_to_channel_post(post: Message, bot_index: int):
    """Function to make each bot react to the post with its assigned emoji."""
    try:
        bot = bots[bot_index]
        emoji = BOT_EMOJIS[bot_index]

        await bot.set_message_reaction(
            chat_id=post.chat.id,
            message_id=post.message_id,
            reaction=[ReactionTypeEmoji(emoji=emoji)]
        )

        logger.info(f"✅ Bot {bot_index+1} reacted with {emoji} in {post.chat.title or post.chat.id}")
    except Exception as e:
        logger.error(f"❌ Error with Bot {bot_index+1}: {e}")

async def post_handler(post: Message):
    """Handles new channel posts and triggers bot reactions."""
    logger.info(f"📩 New post detected: {post.text}")

    if post.text is None:
        logger.warning("🚫 Received a message without text. Skipping processing.")
        return

    normalized_text = " ".join(post.text.lower().strip().split())

    if any(normalized_text in ignored.lower() for ignored in IGNORED_MESSAGES):
        logger.info("🚫 This message is ignored, no reactions will be sent.")
        return

    for i in range(len(bots)):
        await auto_react_to_channel_post(post, i)
        await asyncio.sleep(2)

async def main():
    """Main function to start all bots."""
    logger.info("🚀 Starting all bots...")

    for dp in dispatchers:
        dp.channel_post.register(post_handler)

    await asyncio.gather(*(dp.start_polling(bot) for dp, bot in zip(dispatchers, bots)))

    for bot in bots:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
