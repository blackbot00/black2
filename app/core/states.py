from aiogram.dispatcher.filters.state import State, StatesGroup

class Registration(StatesGroup):
    state = State()
    gender = State()
    age = State()

class ChatChoice(StatesGroup):
    choosing = State()

class AIChat(StatesGroup):
    language = State()
    mode = State()
    chatting = State()

class HumanChat(StatesGroup):
    searching = State()
    chatting = State()
