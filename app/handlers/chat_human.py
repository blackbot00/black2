import time
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from app.core.states import ChatChoice, HumanChat
from app.core import keyboards, messages
from app.database.mongo import get_db
from app.services.matcher import add_to_queue, remove_from_queue, find_match
from config import GROUP1_LOG_ID, GROUP2_LOG_ID

db = get_db()

MEDIA_DELAY = 120  # 2 minutes

# ---------- START HUMAN ----------
async def choose_human(call: types.CallbackQuery, state: FSMContext):
    user = db.users.find_one({"user_id": call.from_user.id})

    # daily limit
    if not user.get("is_premium"):
        count = user.get("human_count", 0)
        if count >= 11:
            await call.answer("🚫 Daily human chat limit reached (11)", show_alert=True)
            return
        db.users.update_one({"user_id": user["user_id"]}, {"$inc": {"human_count": 1}})

    await HumanChat.searching.set()
    add_to_queue(user)

    await call.message.edit_text(
        "🔎 <b>Searching for a partner...</b>\n\nPlease wait 💖",
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("🚪 Exit", callback_data="human_exit")
        )
    )

    match = find_match(user)
    if match:
        partner = db.users.find_one({"user_id": match["user_id"]})

        remove_from_queue(user["user_id"])
        remove_from_queue(partner["user_id"])

        chat_id = f"{user['user_id']}_{partner['user_id']}"

        db.active_chats.insert_one({
            "chat_id": chat_id,
            "type": "human",
            "user1": user["user_id"],
            "user2": partner["user_id"],
            "started_at": time.time()
        })

        info = f"🤝 <b>Partner Connected!</b>\n"

        if user.get("is_premium"):
            info += f"📍 {partner['state']}\n🚻 {partner['gender']}\n🎂 {partner['age']}\n"
        else:
            info += "🔒 Partner details only for Premium 💎\n"

        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("🚪 Exit Chat", callback_data="human_exit"))

        await call.bot.send_message(user["user_id"], info, reply_markup=kb)
        await call.bot.send_message(partner["user_id"], info, reply_markup=kb)

        await HumanChat.chatting.set()

# ---------- CHAT MESSAGE ----------
async def human_message(msg: types.Message, state: FSMContext):
    chat = db.active_chats.find_one({
        "$or": [
            {"user1": msg.from_user.id},
            {"user2": msg.from_user.id}
        ]
    })

    if not chat:
        return

    partner_id = chat["user2"] if chat["user1"] == msg.from_user.id else chat["user1"]

    # link block
    if "http" in msg.text or "www" in msg.text:
        await msg.answer("🔗 Links are not allowed 🙏")
        return

    # media delay
    if msg.content_type != "text":
        if time.time() - chat["started_at"] < MEDIA_DELAY:
            await msg.answer("⏳ Media allowed only after 2 minutes")
            return

    await msg.bot.send_message(partner_id, msg.text)

    # Group 2 log
    await msg.bot.send_message(
        GROUP2_LOG_ID,
        f"[{time.strftime('%I:%M %p')}] "
        f"{msg.from_user.first_name}({msg.from_user.id}) ➜ {partner_id}\n"
        f"💬 {msg.text}"
    )

# ---------- EXIT ----------
async def human_exit(call: types.CallbackQuery, state: FSMContext):
    chat = db.active_chats.find_one({
        "$or": [
            {"user1": call.from_user.id},
            {"user2": call.from_user.id}
        ]
    })

    if chat:
        partner_id = chat["user2"] if chat["user1"] == call.from_user.id else chat["user1"]
        db.active_chats.delete_one({"chat_id": chat["chat_id"]})

        await call.bot.send_message(
            partner_id,
            "⚠️ Partner exited the chat"
        )

    await state.finish()
    await ChatChoice.choosing.set()

    await call.message.edit_text(
        "💬 Chat ended.\n\nWho do you want to chat with again?",
        reply_markup=keyboards.chat_choice_kb()
    )

# ---------- REGISTER ----------
def register(dp: Dispatcher):
    dp.register_callback_query_handler(choose_human, lambda c: c.data == "chat:human", state=ChatChoice.choosing)
    dp.register_message_handler(human_message, state=HumanChat.chatting, content_types=types.ContentTypes.ANY)
    dp.register_callback_query_handler(human_exit, lambda c: c.data == "human_exit", state="*")
