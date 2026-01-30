from aiogram import Dispatcher, types
from config import ADMIN_IDS, AI_ENABLED
from app.database.mongo import get_db

db = get_db()

def admin_only(func):
    async def wrapper(msg: types.Message):
        if msg.from_user.id not in ADMIN_IDS:
            await msg.answer("🚫 This command is only for Admin")
            return
        await func(msg)
    return wrapper


@admin_only
async def ai_on(msg: types.Message):
    await msg.answer("🤖 AI chat enabled ✅")


@admin_only
async def ai_off(msg: types.Message):
    await msg.answer("🤖 AI chat disabled 🚫")


@admin_only
async def ban(msg: types.Message):
    try:
        uid = int(msg.get_args())
        db.users.update_one({"user_id": uid}, {"$set": {"banned": True}})
        await msg.answer(f"🚫 User {uid} banned")
    except:
        await msg.answer("Usage: /ban user_id")


@admin_only
async def unban(msg: types.Message):
    try:
        uid = int(msg.get_args())
        db.users.update_one({"user_id": uid}, {"$set": {"banned": False}})
        await msg.answer(f"✅ User {uid} unbanned")
    except:
        await msg.answer("Usage: /unban user_id")


@admin_only
async def warn(msg: types.Message):
    try:
        uid = int(msg.get_args())
        db.users.update_one({"user_id": uid}, {"$inc": {"warnings": 1}})
        await msg.answer(f"⚠️ Warning sent to {uid}")
    except:
        await msg.answer("Usage: /warn user_id")


def register(dp: Dispatcher):
    dp.register_message_handler(ai_on, commands=["ai_on"])
    dp.register_message_handler(ai_off, commands=["ai_off"])
    dp.register_message_handler(ban, commands=["ban"])
    dp.register_message_handler(unban, commands=["unban"])
    dp.register_message_handler(warn, commands=["warn"])
