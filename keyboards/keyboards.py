import types

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# keyboards.py
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_menu_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=("узнать время"), callback_data="time")
    keyboard.button(text=("введите ссылку"), callback_data="add")
    keyboard.button(text=("помощь"), callback_data="help")
    keyboard.button(text=("создатель"), callback_data="creator")
    keyboard.button(text=("как работает бот"), callback_data="how_to_work")
    keyboard.button(text=("узнать день недели"), callback_data="day_of_week")
    

    return keyboard.as_markup()


