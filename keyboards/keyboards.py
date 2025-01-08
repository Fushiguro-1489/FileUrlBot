
# keyboards.py
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_menu_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=("Добавить ссылку"),callback_data='add')
    keyboard.button(text=("О боте и справка"),callback_data='help')
    return keyboard.as_markup()
