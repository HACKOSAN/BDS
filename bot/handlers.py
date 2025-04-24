from aiogram import types
from aiogram.dispatcher import Dispatcher
from core.manager import add_account, confirm_code, remove_account, get_client_count
from data.config import ADMINS
from core.manager import sessions_pending, active_clients


dp: Dispatcher = None  # Will be set from bot.py

def is_admin(user_id):
    return user_id in ADMINS

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    if not is_admin(message.from_user.id):
        return await message.reply("🚫 You’re not authorized.")
    await message.reply("✅ Bot online. Use /add, /remove, /start, /stop, /progress, /count.")

@dp.message_handler(commands=['count'])
async def cmd_count(message: types.Message):
    if not is_admin(message.from_user.id): return
    await message.reply(f"🧮 Total active accounts: {get_client_count()}")

@dp.message_handler(commands=['add'])
async def cmd_add(message: types.Message):
    if not is_admin(message.from_user.id): return
    try:
        phone = message.get_args().strip()
        if not phone:
            return await message.reply("⚠️ Usage: /add +123456789")
        await message.reply("📞 Sending code...")
        await add_account(phone)
        await message.reply("📲 Code sent. Now reply with it.")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

@dp.message_handler(commands=['remove'])
async def cmd_remove(message: types.Message):
    if not is_admin(message.from_user.id): return
    try:
        phone = message.get_args().strip()
        if not phone:
            return await message.reply("⚠️ Usage: /remove +123456789")
        await remove_account(phone)
        await message.reply(f"🗑 Removed {phone}")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

@dp.message_handler(commands=['progress'])
async def cmd_progress(message: types.Message):
    if not is_admin(message.from_user.id): return
    # Future: add tracking logic here
    await message.reply("📊 Progress tracking not implemented yet.")

@dp.message_handler(commands=['stop'])
async def cmd_stop(message: types.Message):
    if not is_admin(message.from_user.id): return
    # You can later pause automation here
    await message.reply("⏹ Automation paused (not implemented yet).")

@dp.message_handler(commands=['startauto'])
async def cmd_startauto(message: types.Message):
    if not is_admin(message.from_user.id): return
    # You can later resume automation here
    await message.reply("▶️ Automation resumed (not implemented yet).")

@dp.message_handler()
async def handle_code_input(message: types.Message):
    if not is_admin(message.from_user.id): return
    if message.text.startswith("+"):
        phone = message.text.strip()
        if phone in sessions_pending:
            await message.reply("⏳ Waiting for code...")
        else:
            await message.reply("ℹ️ Send /add <number> first.")
        return

    for phone in list(sessions_pending.keys()):
        try:
            await confirm_code(phone, message.text.strip())
            await message.reply(f"✅ {phone} logged in.")
            del sessions_pending[phone]
            return
        except Exception as e:
            await message.reply(f"❌ Error: {e}")
