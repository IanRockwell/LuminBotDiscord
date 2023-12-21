from bot import bot

import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

if __name__ == "__main__":
    print("Initialising Discord Bot...")

    bot = bot.LuminBotDiscord(
        token=DISCORD_TOKEN
    )

    bot.run_bot()
