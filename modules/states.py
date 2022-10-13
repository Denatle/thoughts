from aiogram.fsm.state import StatesGroup, State


class Thoughts(StatesGroup):
    thought_new_message = State()
    fight_mode = State()
    by_id = State()
