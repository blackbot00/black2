from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ---------- COMMON ----------
def back_btn():
    return InlineKeyboardButton("🔙 Back", callback_data="back")

# ---------- STATE ----------
INDIAN_STATES = [
    "Tamil Nadu", "Kerala", "Karnataka", "Andhra Pradesh",
    "Telangana", "Maharashtra", "Delhi", "West Bengal",
    "Punjab", "Rajasthan", "Uttar Pradesh", "Bihar"
]

def states_kb():
    kb = InlineKeyboardMarkup(row_width=3)
    for s in INDIAN_STATES:
        kb.insert(InlineKeyboardButton(s, callback_data=f"state:{s}"))
    return kb

# ---------- GENDER ----------
def gender_kb():
    kb = InlineKeyboardMarkup(row_width=3)
    kb.add(
        InlineKeyboardButton("♂ Male", callback_data="gender:male"),
        InlineKeyboardButton("♀ Female", callback_data="gender:female"),
        InlineKeyboardButton("⚧ Transgender", callback_data="gender:trans")
    )
    kb.add(back_btn())
    return kb

# ---------- AGE ----------
def age_kb():
    kb = InlineKeyboardMarkup(row_width=7)
    for age in range(18, 51):
        kb.insert(InlineKeyboardButton(str(age), callback_data=f"age:{age}"))
    kb.add(back_btn())
    return kb

# ---------- CHAT CHOICE ----------
def chat_choice_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("👤 Human", callback_data="chat:human"),
        InlineKeyboardButton("🤖 AI", callback_data="chat:ai")
    )
    return kb
