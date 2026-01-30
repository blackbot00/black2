from aiogram import Dispatcher, types

async def edit_profile(msg: types.Message):
    await msg.answer("💎 Edit profile feature coming soon")

def register(dp: Dispatcher):
    dp.register_message_handler(edit_profile, commands=["edit_profile"])
