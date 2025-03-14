import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReactionTypeEmoji
from aiogram.fsm.storage.memory import MemoryStorage

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot tokens (Replace these with your actual tokens)
BOT_TOKENS = [
    "7969285298:AAHuohmfq7rVhJiIymW5x2B6TeF-b8VnxCM",
    "8075551315:AAHWTIU-ZOfzbm-LlFuawoEiSwWC72RU3EA",
    "7776558825:AAGBhnpwwGwaBXQ22YZxGLKshNE3_nqLfJ8",
    "7632399315:AAEwJU2PpSG-6pbbj4cKbrFwlmBP8FJYlww",
    "7880551516:AAGIN9b57Q18DL5936sd-3xpf79kZNFGc0U"
]

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


async def auto_react_to_channel_post(post: Message, bot_index: int):
    """Function to make each bot react to the post with its assigned emoji."""
    try:
        bot = bots[bot_index]
        emoji = BOT_EMOJIS[bot_index]  # Assign emoji based on bot index

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

    # Normalize message: remove extra spaces, lowercase, and strip newlines
    if post.text is None:
        logger.warning("🚫 Received a message without text. Skipping processing.")
        return

    normalized_text = " ".join(post.text.lower().strip().split())

    # Check if the message should be ignored
    if any(normalized_text in ignored.lower() for ignored in IGNORED_MESSAGES):
        logger.info("🚫 This message is ignored, no reactions will be sent.")
        return  # Stop execution for this message

    # Each bot reacts to the post with a delay
    for i in range(len(bots)):
        await auto_react_to_channel_post(post, i)
        await asyncio.sleep(2)  # Delay between each bot reaction


async def main():
    """Main function to start all bots."""
    logger.info("🚀 Starting all 5 bots...")

    # Register event handler for each bot
    for dp in dispatchers:
        dp.channel_post.register(post_handler)

    # Run bots concurrently
    await asyncio.gather(*(dp.start_polling(bot) for dp, bot in zip(dispatchers, bots)))

    # Properly close bot sessions after execution
    for bot in bots:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
