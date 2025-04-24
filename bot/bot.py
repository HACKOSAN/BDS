# bot/bot.py

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from data.config import BOT_TOKEN
from bot.handlers import router

# Aiogram 3.x setup
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)

async def start_bot():
    await bot.delete_web_
