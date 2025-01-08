from aiogram.fsm.state import StatesGroup, State


class AddLink(StatesGroup):
    choosing_url = State()
    choosing_name = State()