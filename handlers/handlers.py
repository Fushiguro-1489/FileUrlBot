from aiogram import Router, types
from aiogram.filters import Command

from keyboards.keyboards import main_menu_keyboard

router = Router()

@router.message(Command('start'))
async def start_command(message: types.Message):
    """
    Команда-обработчик для просмотра стартовой информации.

    :param message:
    :return:
    """
    await message.reply('Добро пожаловать в бот для загрузки файлов по URL!', reply_markup=main_menu_keyboard())

@router.message(Command('help'))
async def help_command(message: types.Message):
    """
    Команда-обработчик для просмотра справочной информации.

    :param message:
    :return:
    """
    await message.reply('Бот позволяет: TODO')
