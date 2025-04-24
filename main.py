# main.py

import asyncio
from bot.bot import start_bot
from core.manager import start_manager

async def main():
    # Start both the bot interface and the Telegram account manager
    await asyncio.gather(
        start_bot(),
        start_manager()
    )

if __name__ == "__main__":
    asyncio.run(main())
