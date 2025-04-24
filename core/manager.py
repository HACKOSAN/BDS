import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import ParseMode
from aiogram.utils import executor
from data.config import API_ID, API_HASH

accounts_dir = "accounts"
sessions_pending = {}  # phone_number: Bot
active_clients = {}

# Util to get session path
def get_session_path(phone):
    return os.path.join(accounts_dir, f"{phone}.session")

# Initialize bot instance
bot = Bot(token=API_HASH)  # replace API_HASH with bot token
dp = Dispatcher(bot)

# Util to add an account
async def add_account(phone):
    session_path = get_session_path(phone)
    bot_instance = Bot(token=API_HASH)
    
    try:
        await bot_instance.send_message(phone, "Please verify your phone number.")
        sessions_pending[phone] = bot_instance
    except Exception as e:
        raise e

# Handle code confirmation
async def confirm_code(phone, code):
    if phone not in sessions_pending:
        raise Exception("Session not found")

    bot_instance = sessions_pending[phone]
    
    try:
        await bot_instance.send_message(phone, f"Code confirmed: {code}")
        active_clients[phone] = bot_instance
        del sessions_pending[phone]
    except Exception as e:
        del sessions_pending[phone]
        raise e

# Remove an account
async def remove_account(phone):
    if phone in active_clients:
        bot_instance = active_clients[phone]
        await bot_instance.close()  # Closes the bot instance
        
        del active_clients[phone]

    session_path = get_session_path(phone)
    if os.path.exists(session_path):
        os.remove(session_path)

# Stop all accounts
async def stop_all():
    for bot_instance in active_clients.values():
        await bot_instance.close()
    active_clients.clear()

# Start all accounts
async def start_all():
    for filename in os.listdir(accounts_dir):
        if filename.endswith(".session"):
            phone = filename.replace(".session", "")
            if phone in active_clients:
                continue

            bot_instance = Bot(token=API_HASH)
            await bot_instance.set_webhook()  # Setup webhook for the bot
            
            active_clients[phone] = bot_instance
            await start_farmbot(bot_instance)

# Start farmbot
async def start_farmbot(bot_instance):
    try:
        await bot_instance.send_message("@farmstarstgbot", "/start")
    except Exception as e:
        print(f"[ERROR] {e}")

# Get client count
def get_client_count():
    return len(active_clients)

# Placeholder for uncollected count
def get_uncollected_count():
    return 0

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
