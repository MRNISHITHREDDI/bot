import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

BOT_TOKENS = os.getenv("BOT_TOKENS").split(",")  # Read tokens from .env
BOT_EMOJIS = ["🤩", "🤩", "🔥", "🏆", "❤️", "👍"]

IGNORED_MESSAGES = [
    "⚠️ chart not stable 🥹 wait for 2 minutes 🤩",
    "⚠️ chart not stable 🥹 wait 2 minutes 🤩"
]
