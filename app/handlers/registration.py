from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from app.core.states import Registration, ChatChoice
from app.core import messages, keyboards
from app.database.mongo import get_db
from config import GROUP1_LOG_ID

db = get_db()

async def start_registration(msg: types.Message, state: FSMContext):
    await Registration.state.set()
    await msg.answer(messages.SELECT_STATE, reply_markup=keyboards.states_kb())

async def state_selected(call: types.CallbackQuery, state: FSMContext):
    state_name = call.data.split(":")[1]
    await state.update_data(state=state_name)

    await Registration.gender.set()
    await call.message.edit_text(
        messages.SELECT_GENDER,
        reply_markup=keyboards.gender_kb()
    )

async def gender_selected(call: types.CallbackQuery, state: FSMContext):
    gender = call.data.split(":")[1]
    await state.update_data(gender=gender)

    await Registration.age.set()
    await call.message.edit_text(
        messages.SELECT_AGE,
        reply_markup=keyboards.age_kb()
    )

async def age_selected(call: types.CallbackQuery, state: FSMContext):
    age = int(call.data.split(":")[1])
    data = await state.get_data()

    user = {
        "user_id": call.from_user.id,
        "name": call.from_user.first_name,
        "username": call.from_user.username,
        "state": data["state"],
        "gender": data["gender"],
        "age": age,
        "is_premium": False,
        "banned": False
    }

    db.users.insert_one(user)

    # Group 1 log
    await call.bot.send_message(
        GROUP1_LOG_ID,
        f"🆕 <b>Registration Completed</b>\n"
        f"👤 {user['name']} ({user['user_id']})"
    )

    await state.finish()
    await ChatChoice.choosing.set()

    await call.message.edit_text(
        messages.REG_DONE + "\n\n" + messages.CHOOSE_CHAT,
        reply_markup=keyboards.chat_choice_kb()
    )

def register(dp: Dispatcher):
    dp.register_message_handler(start_registration, commands=["start"], state="*")
    dp.register_callback_query_handler(state_selected, lambda c: c.data.startswith("state"), state=Registration.state)
    dp.register_callback_query_handler(gender_selected, lambda c: c.data.startswith("gender"), state=Registration.gender)
    dp.register_callback_query_handler(age_selected, lambda c: c.data.startswith("age"), state=Registration.age)
