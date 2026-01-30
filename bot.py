import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN
from app.database.mongo import init_db
from app.handlers import start, common, registration, chat_ai, chat_human, premium, profile
from app.admin import commands

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

# register handlers
start.register(dp)
registration.register(dp)
chat_ai.register(dp)
chat_human.register(dp)
premium.register(dp)
profile.register(dp)
common.register(dp)
commands.register(dp)

async def start_bot():
    await init_db()
    await dp.start_polling()
