from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from app.database.mongo import get_db
from config import GROUP1_LOG_ID

db = get_db()

def report_kb():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("🚩 Scam", callback_data="report:scam"),
        types.InlineKeyboardButton("😡 Abuse", callback_data="report:abuse"),
        types.InlineKeyboardButton("🔞 Adult", callback_data="report:adult"),
        types.InlineKeyboardButton("📛 Spam", callback_data="report:spam"),
    )
    return kb


async def ask_report(msg: types.Message):
    await msg.answer(
        "🚨 <b>Do you want to report the previous chat?</b>",
        reply_markup=report_kb()
    )


async def handle_report(call: types.CallbackQuery):
    reason = call.data.split(":")[1]

    db.reports.insert_one({
        "reporter": call.from_user.id,
        "reason": reason
    })

    await call.bot.send_message(
        GROUP1_LOG_ID,
        f"🚩 <b>New Report</b>\n"
        f"👤 Reporter: {call.from_user.first_name} ({call.from_user.id})\n"
        f"📌 Reason: {reason}"
    )

    await call.message.edit_text("✅ Report submitted. Thank you for keeping the community safe 🛡️")


def register(dp: Dispatcher):
    dp.register_callback_query_handler(handle_report, lambda c: c.data.startswith("report:"))
