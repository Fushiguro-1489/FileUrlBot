import datetime
import os
import asyncio
from aiogram import Router, types, F , Dispatcher
from aiogram.filters import Command
from aiogram.types import FSInputFile
from yt_dlp import YoutubeDL
from config import FREE_LINK_LIMIT
from keyboards.keyboards import main_menu_keyboard


router = Router()

DOWNLOAD_DIR = "downloads"
USER_LINK_COUNT = {}

@router.message(Command('start'))
async def start_command(message: types.Message):
    """
    Команда-обработчик для стартового сообщения.
    """
    await message.reply("Привет! Отправь мне ссылку на видео, и я помогу скачать его.",
                        reply_markup=main_menu_keyboard())

@router.message(Command('help'))
@router.message(F.text.lower() == "помощь")
async def help_command(message: types.Message):
    await message.reply("Этот бот создан для скачивания видео по ссылке.",
                        reply_markup=main_menu_keyboard())

@router.message(Command('add'))
@router.message(F.text.lower() == "введите ссылку")
async def add_command(message: types.Message):
    await message.reply("вставьте ссылку пожалуйста.",
                            reply_markup=main_menu_keyboard())

@router.message(Command('creator'))
@router.message(F.text.lower() == "создатель")
async def add_command(message: types.Message):
    await message.reply("Моё имя Степан,сделаем интернет чуть чуть анонимнее.",
                            reply_markup=main_menu_keyboard())

@router.message(Command('how_to_work'))
@router.message(F.text.lower() == "как работает бот")
async def how_to_work_command(message: types.Message):
    await message.reply("Работа,данного бота очень проста,вы отправляете ссылку видео,он отправляет вам готовый файл,что бы вы могли скачать его.",
                            reply_markup=main_menu_keyboard())

@router.message(Command('day_of_week'))
@router.message(F.text.lower() == "узнать день недели")
async def show_current_day_of_week(message: types.Message):
    await message.reply(f"Сегодня {days_of_week[current_day_of_week]}")
days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
current_day_of_week = datetime.datetime.now().weekday()


@router.message(Command('time'))
@router.message(F.text.lower() == "узнать время")
async def show_current_time(message: types.Message):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    await message.reply(f"Текущее время: {current_time}")


@router.message(F.text)
async def download_video_from_url(message: types.Message):
    """
    Обработчик для скачивания видео с Rutube
    """
    user_id = message.from_user.id
    url = message.text.strip()

    # Проверка, что ссылка правильная
    if not url:
        await message.reply("Пожалуйста, отправьте корректную ссылку на видео.")
        return

    # Проверка лимита ссылок для пользователя
    if user_id not in USER_LINK_COUNT:
        USER_LINK_COUNT[user_id] = 0
    if USER_LINK_COUNT[user_id] >= FREE_LINK_LIMIT:
        await message.reply("Вы достигли лимита скачиваний для бесплатных ссылок.")
        return

    try:
        # Скачиваем видео
        video_path = await download_video(url)

        # Отправляем файл пользователю
        video_file = FSInputFile(video_path)
        await message.reply_document(video_file)

        # Увеличиваем счетчик ссылок для пользователя
        USER_LINK_COUNT[user_id] += 1

        # Удаляем скачанный файл после отправки
        os.remove(video_path)
    except Exception as e:
        await message.reply(f"Произошла ошибка при скачивании видео: {e}")


async def download_video(url: str) -> str:
    """
    Функция для скачивания видео с любого сайта, поддерживаемого yt-dlp.
    """
    options = {
        'format': 'best',
        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
        'noplaylist': True,
        'force_generic_extractor': True,
        'socket-timeout': 30,  # Увеличение времени ожидания
    }

    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)


