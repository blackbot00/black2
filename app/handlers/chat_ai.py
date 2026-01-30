from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from app.core.states import ChatChoice, AIChat
from app.core import keyboards, messages
from app.database.mongo import get_db
from app.services.ai_engine import generate_ai_reply, is_restricted
from config import GROUP2_LOG_ID, AI_ENABLED

db = get_db()

# --------- START AI FLOW ----------
async def choose_ai(call: types.CallbackQuery, state: FSMContext):
    if not AI_ENABLED:
        await call.answer("🚫 AI chat is temporarily disabled", show_alert=True)
        return

    await AIChat.language.set()
    await call.message.edit_text(
        "🌐 <b>Select AI Language</b>",
        reply_markup=keyboards.ai_language_kb()
    )


async def ai_language_selected(call: types.CallbackQuery, state: FSMContext):
    lang = call.data.split(":")[1]
    await state.update_data(language=lang)

    user = db.users.find_one({"user_id": call.from_user.id})
    is_premium = user.get("is_premium", False)

    await AIChat.mode.set()
    await call.message.edit_text(
        "🎭 <b>Select AI Personality</b>",
        reply_markup=keyboards.ai_mode_kb(is_premium)
    )


async def ai_mode_selected(call: types.CallbackQuery, state: FSMContext):
    mode = call.data.split(":")[1]

    if mode == "locked":
        await call.answer("💎 Only for Premium users", show_alert=True)
        return

    await state.update_data(mode=mode)
    await AIChat.chatting.set()

    await call.message.edit_text(
        "💬 <b>AI Chat Started</b>\n\nType your message below 💖",
        reply_markup=keyboards.ai_chat_kb()
    )


# --------- AI CHAT MESSAGES ----------
async def ai_chat_message(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    user = db.users.find_one({"user_id": msg.from_user.id})

    # limit check
    if not user.get("is_premium"):
        today_count = user.get("ai_count", 0)
        if today_count >= 40:
            await msg.answer("🚫 Daily AI limit reached (40). Upgrade to Premium 💎")
            return
        db.users.update_one(
            {"user_id": msg.from_user.id},
            {"$inc": {"ai_count": 1}}
        )

    restricted = is_restricted(msg.text)
    if restricted:
        await msg.answer(restricted)
        return

    reply = generate_ai_reply(
        msg.text,
        gender=user["gender"],
        mode=data["mode"],
        language=data["language"]
    )

    await msg.answer(reply, reply_markup=keyboards.ai_chat_kb())

    # Group 2 log
    await msg.bot.send_message(
        GROUP2_LOG_ID,
        f"👤 {msg.from_user.first_name} ({msg.from_user.id}) ↔ 🤖 AI\n"
        f"💬 {msg.text}\n🤖 {reply}"
    )


# --------- EXIT ----------
async def ai_exit(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await ChatChoice.choosing.set()
    await call.message.edit_text(
        messages.CHOOSE_CHAT,
        reply_markup=keyboards.chat_choice_kb()
    )


def register(dp: Dispatcher):
    dp.register_callback_query_handler(choose_ai, lambda c: c.data == "chat:ai", state=ChatChoice.choosing)
    dp.register_callback_query_handler(ai_language_selected, lambda c: c.data.startswith("ai_lang"), state=AIChat.language)
    dp.register_callback_query_handler(ai_mode_selected, lambda c: c.data.startswith("ai_mode"), state=AIChat.mode)
    dp.register_message_handler(ai_chat_message, state=AIChat.chatting)
    dp.register_callback_query_handler(ai_exit, lambda c: c.data == "ai_exit", state=AIChat.chatting)
