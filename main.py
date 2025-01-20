# main.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from config import TOKEN
from database.db import init_db
from handlers import handlers

logging.basicConfig(level=logging.INFO)

bot = Bot(TOKEN)
dp = Dispatcher()

async def set_bot_commands(bot: Bot):
    """
    Устанавливает команды для бота.

    :param bot: Экземпляр бота.
    """
    commands = [
        BotCommand(command="start", description="Начать работу с ботом"),
        BotCommand(command="help", description="помощь"),
        BotCommand(command="time", description="узнать время"),
        BotCommand(command="add", description="введите ссылку"),
        BotCommand(command="day_of_week", description="узнать день недели"),
        BotCommand(command="creator", description="создатель"),
    ]
    await bot.set_my_commands(commands)


def main():
    # Регистрируем обработчики команд
    dp.include_router(handlers.router)

    init_db()

    # Запускаем бота
    asyncio.run(start_bot())


async def start_bot():
    """
    Главная функция
    """
    await bot.delete_webhook(drop_pending_updates=True)

    await set_bot_commands(bot)
    try:
        await dp.start_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        await dp.stop_polling()

if __name__ == "__main__":
    main()
