from aiogram import Dispatcher, types
from app.database.mongo import get_db

db = get_db()

def premium_kb():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("💎 1 Week – ₹29", callback_data="buy:week"),
        types.InlineKeyboardButton("💎 1 Month – ₹79", callback_data="buy:month"),
        types.InlineKeyboardButton("💎 3 Months – ₹149", callback_data="buy:3month"),
    )
    return kb


async def premium(msg: types.Message):
    user = db.users.find_one({"user_id": msg.from_user.id})
    status = "Active ✅" if user.get("is_premium") else "Inactive ❌"

    await msg.answer(
        f"💎 <b>Premium Status:</b> {status}\n\n"
        "✨ Premium Benefits\n"
        "• Unlimited AI chats\n"
        "• 18+ AI Mode\n"
        "• Unlimited Human connects\n\n"
        "Choose a plan 👇",
        reply_markup=premium_kb()
    )


async def buy_plan(call: types.CallbackQuery):
    plan = call.data.split(":")[1]
    await call.message.edit_text(
        "💳 <b>Payment processing via Cashfree</b>\n\n"
        "⚠️ (Cashfree order creation hook here)"
    )


def register(dp: Dispatcher):
    dp.register_message_handler(premium, commands=["premium"])
    dp.register_callback_query_handler(buy_plan, lambda c: c.data.startswith("buy:"))
